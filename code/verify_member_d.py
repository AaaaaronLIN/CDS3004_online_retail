#!/usr/bin/env python
"""Independent reproduction of Member D's S3 / S7 headline numbers.

Member D owns the association-rule module (notebook S7) and the similarity
module (notebook S3).  This script is deliberately *separate* from the
notebook: it re-derives the cleaning, the baskets, the rules, the holdout
evaluation and the two similarity views from the raw UCI workbook, then
compares its own numbers with the committed artefacts in ``results/``.

Run from the repository root::

    PYTHONPATH=.deps python code/verify_member_d.py

Outputs (committed, listed as "Supplementary" in results/ARTIFACTS.md):
    results/tables/s07_rule_headline.csv
    results/tables/s07_holdout_lift_quantiles.csv
    results/tables/s07_hand_lift_22697_22699.csv
    results/tables/s07_variant_duplicates.csv
    results/tables/s07_similarity_check.csv
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import association_rules, fpgrowth
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances, silhouette_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "Online_Retail.xlsx"
TABLES = ROOT / "results" / "tables"

RANDOM_STATE = 42
SERVICE_CODES = {
    "POST", "D", "M", "C2", "DOT", "PADS", "BANK CHARGES", "CRUK", "S",
    "AMAZONFEE", "B", "ADJUST", "ADJUST2", "TEST001", "TEST002",
}
SNAP_FEATURES = [
    "recency_days", "frequency", "monetary", "avg_basket", "avg_items_per_invoice",
    "distinct_products", "distinct_months", "tenure_days", "avg_gap_days", "std_gap_days",
    "revenue_last90_ratio", "weekend_share", "avg_unit_price", "max_invoice_value", "return_rate",
]

# same thresholds as notebook S7.1
MIN_SUPPORT, MIN_CONFIDENCE, MIN_LIFT, MAX_LEN = 0.005, 0.2, 1.2, 3

CHECKS: list[dict] = []


def check(item: str, expected, got, tol: float = 5e-4) -> None:
    """Record one notebook-vs-recomputed comparison."""
    if isinstance(expected, (int, float)) and isinstance(got, (int, float)):
        ok = abs(float(expected) - float(got)) <= tol
    else:
        ok = expected == got
    CHECKS.append({"item": item, "notebook_value": expected,
                   "recomputed_value": got, "match": bool(ok)})
    flag = "OK  " if ok else "DIFF"
    print(f"  [{flag}] {item:52s} notebook={expected!s:>14}  recomputed={got!s:>14}")


def banner(text: str) -> None:
    print()
    print("=" * 78)
    print(text)
    print("=" * 78)


# =====================================================================
# A. Clean the transaction log exactly as notebook S1.4 does
# =====================================================================
banner("A. S1.4 cleaning (reproduced from raw workbook)")

raw = pd.read_excel(DATA_PATH)
raw["InvoiceNo"] = raw["InvoiceNo"].astype(str).str.strip()
raw["StockCode"] = raw["StockCode"].astype(str).str.strip()
raw["InvoiceDate"] = pd.to_datetime(raw["InvoiceDate"])

funnel = []
df = raw.copy()
funnel.append(("raw", len(df)))
df = df[df["CustomerID"].notna()].copy()
df["CustomerID"] = df["CustomerID"].astype(int)
funnel.append(("no missing CustomerID", len(df)))
df = df[~df["InvoiceNo"].str.upper().str.startswith("C")].copy()
funnel.append(("no cancellations", len(df)))
df = df[df["Quantity"] > 0].copy()
funnel.append(("Quantity > 0", len(df)))
df = df[df["UnitPrice"] > 0].copy()
funnel.append(("UnitPrice > 0", len(df)))
df = df[~df["StockCode"].str.upper().isin(SERVICE_CODES)].copy()
funnel.append(("no service StockCodes", len(df)))
df = df.drop_duplicates().copy()
funnel.append(("no duplicate rows", len(df)))

clean = df.reset_index(drop=True)
clean["Revenue"] = clean["Quantity"] * clean["UnitPrice"]
clean["date"] = clean["InvoiceDate"].dt.normalize()
clean["Description"] = clean["Description"].fillna("UNKNOWN")
print("  funnel:", " -> ".join(f"{name}:{n:,}" for name, n in funnel))

committed_funnel = pd.read_csv(TABLES / "t03_cleaning_decisions.csv")
committed_dq = json.loads((ROOT / "results" / "metrics.json").read_text(encoding="utf-8"))["data_quality"]
pos = (raw["Quantity"] > 0) & (raw["UnitPrice"] > 0)
raw_gross = float((raw.loc[pos, "Quantity"] * raw.loc[pos, "UnitPrice"]).sum())
check("clean rows (t03 last step)", int(committed_funnel["rows_remaining"].iloc[-1]), len(clean), 0)
check("rows retained (%)", committed_dq["rows_retained_pct"], round(len(clean) / len(raw) * 100, 2), 0.01)
check("revenue retained (%)", committed_dq["revenue_retained_pct"],
      round(float(clean["Revenue"].sum()) / raw_gross * 100, 4), 0.001)
check("raw duplicate rows", committed_dq["duplicates_removed"], int(raw.duplicated().sum()), 0)
print(f"  clean customers / invoices : {clean['CustomerID'].nunique():,} / {clean['InvoiceNo'].nunique():,}")

returns = raw[
    raw["InvoiceNo"].str.upper().str.startswith("C")
    & (raw["Quantity"] < 0)
    & raw["CustomerID"].notna()
].copy()
returns["CustomerID"] = returns["CustomerID"].astype(int)
returns["date"] = returns["InvoiceDate"].dt.normalize()


# =====================================================================
# B. S7.1 baskets + FP-Growth + pruning
# =====================================================================
banner("B. S7.1 baskets, FP-Growth, rule pruning")


def basket_matrix(d: pd.DataFrame) -> pd.DataFrame:
    inv = d["InvoiceNo"].unique()
    prods = np.sort(d["StockCode"].unique())
    arr = np.zeros((len(inv), len(prods)), dtype=bool)
    arr[pd.Categorical(d["InvoiceNo"], categories=inv).codes,
        pd.Categorical(d["StockCode"], categories=prods).codes] = True
    return pd.DataFrame(arr, index=inv, columns=prods)


train_df = clean[(clean["date"] >= "2010-12-01") & (clean["date"] <= "2011-07-31")]
hold_df = clean[(clean["date"] >= "2011-08-01") & (clean["date"] <= "2011-12-09")]
B_train = basket_matrix(train_df)
B_hold = basket_matrix(hold_df)
print(f"  mining baskets : {B_train.shape[0]:,} invoices x {B_train.shape[1]:,} products")
print(f"  holdout baskets: {B_hold.shape[0]:,} invoices x {B_hold.shape[1]:,} products")

freq_items = fpgrowth(B_train, min_support=MIN_SUPPORT, use_colnames=True, max_len=MAX_LEN)
raw_rules = association_rules(freq_items, metric="confidence", min_threshold=0.0)
qualified = raw_rules[raw_rules["confidence"] >= MIN_CONFIDENCE]
final_rules = qualified[qualified["lift"] >= MIN_LIFT].reset_index(drop=True)
print(f"  frequent itemsets: {len(freq_items):,}")
print(f"  rules raw / conf>=0.2 / final: {len(raw_rules):,} / {len(qualified):,} / {len(final_rules):,}")

committed_extra = json.loads((ROOT / "results" / "metrics_extra.json").read_text(encoding="utf-8"))
committed_ar = committed_extra["association_rules"]
committed_metrics = json.loads((ROOT / "results" / "metrics.json").read_text(encoding="utf-8"))

check("frequent itemsets", committed_ar["n_frequent_itemsets"], int(len(freq_items)), 0)
check("raw rules", committed_ar["n_rules_raw"], int(len(raw_rules)), 0)
check("pruned rules kept", committed_ar["n_rules_pruned"], int(len(final_rules)), 0)
check("max training lift", round(float(committed_metrics["association_rules"]["max_lift"]), 4),
      round(float(final_rules["lift"].max()), 4))


# =====================================================================
# C. S7.2 holdout evaluation of every rule
# =====================================================================
banner("C. S7.2 holdout validation (2011-08 .. 2011-12)")

hold_col = {code: i for i, code in enumerate(B_hold.columns)}
H = B_hold.values
N_HOLD = len(H)


def basket_count(items) -> int:
    idx = [hold_col[x] for x in items if x in hold_col]
    if len(idx) != len(items):
        return 0
    return int(H[:, idx].all(axis=1).sum())


hold_support, hold_conf, hold_lift = [], [], []
hold_baseline, hold_status = [], []
n_excl_ant = n_excl_con = 0
for row in final_rules.itertuples():
    ant, con = tuple(row.antecedents), tuple(row.consequents)
    n_ant = basket_count(ant)
    if n_ant == 0:
        n_excl_ant += 1
        hold_support.append(np.nan); hold_conf.append(np.nan)
        hold_lift.append(np.nan); hold_baseline.append(np.nan)
        hold_status.append("excluded: antecedent not in holdout")
        continue
    n_both = basket_count(ant + con)
    n_con = basket_count(con)
    if n_con == 0:
        n_excl_con += 1
        hold_support.append(n_both / N_HOLD); hold_conf.append(np.nan)
        hold_lift.append(np.nan); hold_baseline.append(np.nan)
        hold_status.append("excluded: consequent not in holdout")
        continue
    conf = n_both / n_ant
    baseline = n_con / N_HOLD
    hold_support.append(n_both / N_HOLD)
    hold_conf.append(conf)
    hold_baseline.append(baseline)
    hold_lift.append(conf / baseline)
    hold_status.append("evaluated")

final_rules["holdout_support"] = hold_support
final_rules["holdout_confidence"] = hold_conf
final_rules["holdout_consequent_support"] = hold_baseline
final_rules["holdout_lift"] = hold_lift
final_rules["holdout_status"] = hold_status

evaluated_mask = pd.Series(hold_lift).notna()
lift_s = pd.Series(hold_lift)[evaluated_mask]
support_s = pd.Series(hold_support)[evaluated_mask]
N_EVAL = int(lift_s.size)
MEAN = float(lift_s.mean())
MEDIAN = float(lift_s.median())
SHARE_GT1 = float((lift_s > 1).mean())
SHARE_GT2 = float((lift_s > 2).mean())
MED_SUP = float(support_s.median())

print(f"  holdout baskets N_HOLD = {N_HOLD:,}")
print(f"  evaluated rules        = {N_EVAL:,} (excluded: {n_excl_ant} antecedent, {n_excl_con} consequent)")
print(f"  mean / median holdout lift = {MEAN:.4f} / {MEDIAN:.4f}")

check("rules evaluated on holdout", committed_metrics["association_rules"]["n_rules_holdout_evaluated"], N_EVAL, 0)
check("excluded: antecedent absent", committed_ar["n_excluded_no_antecedent"], n_excl_ant, 0)
check("excluded: consequent absent", committed_ar["n_excluded_no_consequent"], n_excl_con, 0)
check("mean holdout lift", committed_ar["mean_holdout_lift"], round(MEAN, 4))
check("median holdout lift", committed_ar["median_holdout_lift"], round(MEDIAN, 4))
check("share holdout lift > 1", committed_ar["share_holdout_lift_gt1"], round(SHARE_GT1, 4))
check("share holdout lift > 2", committed_ar["share_holdout_lift_gt2"], round(SHARE_GT2, 4))
check("median holdout support", committed_ar["median_holdout_support"], round(MED_SUP, 5))

# business subset: support >= 1% AND lift >= 2, one direction per unordered pair
def items_to_str(itemset) -> str:
    return ", ".join(sorted(itemset))


rule_export = pd.DataFrame({
    "antecedent": final_rules["antecedents"].apply(items_to_str),
    "consequent": final_rules["consequents"].apply(items_to_str),
    "support": final_rules["support"].round(5),
    "confidence": final_rules["confidence"].round(4),
    "lift": final_rules["lift"].round(4),
    "holdout_support": final_rules["holdout_support"].round(5),
    "holdout_confidence": final_rules["holdout_confidence"].round(4),
    "holdout_consequent_support": final_rules["holdout_consequent_support"].round(5),
    "holdout_lift": final_rules["holdout_lift"].round(4),
    "holdout_status": final_rules["holdout_status"],
}).sort_values(["lift", "confidence", "support"], ascending=False, kind="mergesort")

business = rule_export[(rule_export["support"] >= 0.01) & (rule_export["lift"] >= 2.0)].copy()
business["pair_key"] = business.apply(
    lambda r: "||".join(sorted([str(r["antecedent"]), str(r["consequent"])])), axis=1)
business = business.sort_values(["support", "lift"], ascending=False, kind="mergesort")
business = business.drop_duplicates("pair_key")
print(f"  business rules (support>=1%, lift>=2, one direction per pair): {len(business):,}")
check("business rules", committed_ar["n_business_rules"], int(len(business)), 0)
check("top business rule antecedent", committed_ar["top_business_rules"][0]["antecedent"],
      str(business.iloc[0]["antecedent"]))
check("top business rule consequent", committed_ar["top_business_rules"][0]["consequent"],
      str(business.iloc[0]["consequent"]))
check("top business rule holdout lift", committed_ar["top_business_rules"][0]["holdout_lift"],
      round(float(business.iloc[0]["holdout_lift"]), 4))


# =====================================================================
# D. Task 2 - hand recompute of one rule's holdout lift
# =====================================================================
banner("D. Task 2 - hand recompute: 22697 -> 22699 (GREEN -> ROSES REGENCY TEACUP)")

ANT, CON = "22697", "22699"
n_ant = basket_count((ANT,))
n_con = basket_count((CON,))
n_both = basket_count((ANT, CON))
conf = n_both / n_ant
baseline = n_con / N_HOLD
lift = conf / baseline
rule_row = rule_export[(rule_export["antecedent"] == ANT) & (rule_export["consequent"] == CON)].iloc[0]

print(f"  a = baskets with antecedent {ANT}            : {n_ant:,}")
print(f"  b = baskets with antecedent AND consequent   : {n_both:,}")
print(f"  c = baskets with consequent {CON}            : {n_con:,}")
print(f"  N_HOLD                                       : {N_HOLD:,}")
print(f"  P(con|ant) = b/a = {n_both}/{n_ant} = {conf:.4f}")
print(f"  P(con)     = c/N = {n_con}/{N_HOLD} = {baseline:.5f}")
print(f"  holdout lift = {conf:.4f} / {baseline:.5f} = {lift:.4f}")

check("t10 holdout_confidence for 22697->22699", float(rule_row["holdout_confidence"]), round(conf, 4))
check("t10 holdout_consequent_support", float(rule_row["holdout_consequent_support"]), round(baseline, 5))
check("t10 holdout_lift", float(rule_row["holdout_lift"]), round(lift, 4))
check("t10 training support", float(rule_row["support"]), 0.03385)
check("t10 training confidence", float(rule_row["confidence"]), 0.793)
check("t10 training lift", float(rule_row["lift"]), 16.406)

hand_rows = [
    ("holdout invoices (N_HOLD)", N_HOLD),
    ("a: baskets containing 22697", n_ant),
    ("b: baskets containing 22697 and 22699", n_both),
    ("c: baskets containing 22699", n_con),
    ("P(22699 | 22697) = b/a", round(conf, 4)),
    ("P(22699) = c/N_HOLD", round(baseline, 5)),
    ("holdout lift = P(con|ant)/P(con)", round(lift, 4)),
    ("t10 holdout_lift (committed table)", float(rule_row["holdout_lift"])),
    ("absolute difference", round(abs(lift - float(rule_row["holdout_lift"])), 6)),
]
pd.DataFrame(hand_rows, columns=["quantity", "value"]).to_csv(
    TABLES / "s07_hand_lift_22697_22699.csv", index=False)


# =====================================================================
# E. Task 1 - why the mean is not the headline
# =====================================================================
banner("E. Task 1 - mean vs median: concentration in rare same-product variants")

quantiles = [0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
q_rows = [{"scope": "all evaluated rules", "statistic": "mean", "value": round(MEAN, 4)},
          {"scope": "all evaluated rules", "statistic": "median", "value": round(MEDIAN, 4)}]
for q in quantiles:
    q_rows.append({"scope": "all evaluated rules", "statistic": f"p{int(q * 100)}",
                   "value": round(float(lift_s.quantile(q)), 4)})
q_rows.append({"scope": "all evaluated rules", "statistic": "max", "value": round(float(lift_s.max()), 4)})
# robustness: trimmed means and support-weighted mean
for k in (0.01, 0.05, 0.10):
    cut = lift_s.quantile(1 - k)
    q_rows.append({"scope": f"trimmed mean (drop top {int(k * 100)}%)", "statistic": "mean",
                   "value": round(float(lift_s[lift_s <= cut].mean()), 4)})
q_rows.append({"scope": "support-weighted mean", "statistic": "mean",
               "value": round(float(np.average(lift_s, weights=support_s)), 4)})
# one direction per unordered rule (the rule table lists A->B and B->A separately)
pair_key = rule_export.apply(lambda r: "||".join(sorted([r["antecedent"], r["consequent"]])), axis=1)
dedup = rule_export.assign(pair=pair_key).drop_duplicates("pair")["holdout_lift"].dropna()
q_rows.append({"scope": "one direction per pair", "statistic": "n", "value": int(dedup.size)})
q_rows.append({"scope": "one direction per pair", "statistic": "mean", "value": round(float(dedup.mean()), 4)})
q_rows.append({"scope": "one direction per pair", "statistic": "median", "value": round(float(dedup.median()), 4)})
df_q = pd.DataFrame(q_rows)
df_q.to_csv(TABLES / "s07_holdout_lift_quantiles.csv", index=False)
print(df_q.to_string(index=False))

# --- symmetric duplicates: the same product pair reported in both directions ---
pair_counts = rule_export.assign(
    pair=rule_export.apply(lambda r: frozenset([r["antecedent"], r["consequent"]]), axis=1)
)["pair"].value_counts()
symmetric = pair_counts[pair_counts > 1]
print(f"\n  unordered rule pairs: {pair_counts.size:,}; pairs reported both ways: {symmetric.size:,}")

# --- same-product-family variants, detected from the description text --------
COLOURS = {
    "RED", "BLUE", "GREEN", "PINK", "WHITE", "BLACK", "PURPLE", "YELLOW", "ORANGE",
    "SILVER", "GOLD", "BROWN", "GREY", "GRAY", "CREAM", "IVORY", "TURQUOISE",
    "ASSORTED", "MIXED", "MULTI", "VINTAGE", "RETROSPOT", "POLKADOT", "SPOT",
}
STOP = {"SET", "OF", "THE", "AND", "WITH", "IN", "ON", "A", "TO", "FOR", "BAG", "SMALL", "LARGE", "MINI"}


def stem(text: str) -> set[str]:
    tokens = "".join(ch if ch.isalpha() else " " for ch in str(text).upper()).split()
    return {t for t in tokens if t not in COLOURS and t not in STOP and len(t) > 2}


desc_map = (
    clean[clean["Description"] != "UNKNOWN"]
    .groupby("StockCode")["Description"]
    .agg(lambda s: s.value_counts().index[0])
)


def family(two_items: frozenset) -> bool:
    toks = [stem(desc_map.get(code.strip(), code.strip())) for code in two_items]
    if len(toks) < 2 or not toks[0] or not toks[1]:
        return False
    inter = len(toks[0] & toks[1])
    union = len(toks[0] | toks[1])
    return inter / union >= 0.5


is_family = rule_export.apply(lambda r: family(frozenset([r["antecedent"], r["consequent"]])), axis=1)
rare = rule_export["support"] < 0.01
print(f"  same-product-family rules: {int(is_family.sum()):,} ({is_family.mean():.1%} of rules)")
print(f"  rules with support < 1%  : {int(rare.sum()):,} ({rare.mean():.1%} of rules)")

groups = {
    "all evaluated rules": rule_export["holdout_lift"].dropna(),
    "same-product family": rule_export.loc[is_family, "holdout_lift"].dropna(),
    "different products": rule_export.loc[~is_family, "holdout_lift"].dropna(),
    "support < 1% (rare)": rule_export.loc[rare, "holdout_lift"].dropna(),
    "support >= 1%": rule_export.loc[~rare, "holdout_lift"].dropna(),
    "same family AND rare": rule_export.loc[is_family & rare, "holdout_lift"].dropna(),
}
variant_rows = []
for name, s in groups.items():
    variant_rows.append({
        "group": name,
        "n_rules": int(s.size),
        "share_of_evaluated": round(s.size / N_EVAL, 4),
        "mean_holdout_lift": round(float(s.mean()), 4),
        "median_holdout_lift": round(float(s.median()), 4),
        "share_lift_gt2": round(float((s > 2).mean()), 4),
    })
df_variant = pd.DataFrame(variant_rows)
df_variant.to_csv(TABLES / "s07_variant_duplicates.csv", index=False)
print(df_variant.to_string(index=False))

top10 = rule_export.nlargest(10, "holdout_lift")[["antecedent", "consequent", "support", "lift", "holdout_lift"]]
print("\n  top-10 rules by holdout lift (all rare, all variant pairs):")
print(top10.to_string(index=False))

# the extreme tail: how much of the mean comes from a handful of rules?
extreme = rule_export[rule_export["holdout_lift"] > 100].copy()
extreme["pair"] = extreme.apply(lambda r: "||".join(sorted([r["antecedent"], r["consequent"]])), axis=1)
both_directions = set(extreme["pair"][extreme["pair"].duplicated()])
extreme_summary = pd.DataFrame([
    {"quantity": "rules with holdout lift > 100", "value": int(len(extreme))},
    {"quantity": "share of all evaluated rules", "value": round(len(extreme) / N_EVAL, 4)},
    {"quantity": "median support of those rules", "value": round(float(extreme["support"].median()), 5)},
    {"quantity": "share whose pair also appears in the other direction",
     "value": round(len(extreme[extreme["pair"].isin(both_directions)]) / max(len(extreme), 1), 4)},
    {"quantity": "share of the mean explained by those rules",
     "value": round(float(extreme["holdout_lift"].sum() / lift_s.sum()), 4)},
    {"quantity": "mean holdout lift of the remaining rules",
     "value": round(float(rule_export.loc[~rule_export.index.isin(extreme.index), "holdout_lift"].dropna().mean()), 4)},
])
print("\n  extreme-tail diagnostics:")
print(extreme_summary.to_string(index=False))
extreme_summary.to_csv(TABLES / "s07_mean_lift_tail.csv", index=False)


# =====================================================================
# F. Task 3 - reproduce the two similarity views from notebook S3
# =====================================================================
banner("F. Task 3 - similarity: metric comparison, customer lookalikes, item-item cosine")


def log_scale(df_in: pd.DataFrame, feats: list[str]) -> np.ndarray:
    X = df_in[feats].astype(float).copy()
    X = np.log1p(X.clip(lower=0))
    return StandardScaler().fit_transform(X)


def build_snapshot(df_clean: pd.DataFrame, returns_df: pd.DataFrame, as_of, window_months=6,
                   label_months=3) -> pd.DataFrame:
    as_of = pd.Timestamp(as_of)
    start = as_of - pd.DateOffset(months=window_months) + pd.Timedelta(days=1)
    fw = df_clean[(df_clean["date"] >= start) & (df_clean["date"] <= as_of)]
    g = fw.groupby("CustomerID")

    snap = pd.DataFrame(index=g.size().index)
    snap.index.name = "CustomerID"
    inv = snap.index

    snap["recency_days"] = (as_of - g["date"].max()).dt.days
    snap["frequency"] = g["InvoiceNo"].nunique()
    snap["monetary"] = g["Revenue"].sum()

    basket = fw.groupby(["CustomerID", "InvoiceNo"])["Revenue"].sum().groupby("CustomerID")
    snap["avg_basket"] = basket.mean()
    snap["avg_items_per_invoice"] = (
        fw.groupby(["CustomerID", "InvoiceNo"]).size().groupby("CustomerID").mean()
    )
    snap["max_invoice_value"] = basket.max()
    snap["avg_unit_price"] = g["UnitPrice"].mean()

    snap["distinct_products"] = g["StockCode"].nunique()
    snap["distinct_months"] = g["date"].apply(lambda s: s.dt.to_period("M").nunique())

    first_ever = df_clean[df_clean["date"] <= as_of].groupby("CustomerID")["date"].min()
    snap["tenure_days"] = (as_of - first_ever.reindex(inv)).dt.days

    day_pairs = fw[["CustomerID", "date"]].drop_duplicates().sort_values(["CustomerID", "date"])
    day_pairs["gap"] = day_pairs.groupby("CustomerID")["date"].diff().dt.days
    gaps = day_pairs.groupby("CustomerID")["gap"]
    snap["avg_gap_days"] = gaps.mean().fillna(0.0)
    snap["std_gap_days"] = gaps.apply(lambda s: s.std(ddof=0) if s.notna().any() else 0.0).fillna(0.0)

    last90 = fw[fw["date"] > as_of - pd.Timedelta(days=90)].groupby("CustomerID")["Revenue"].sum()
    prev90 = fw[
        (fw["date"] <= as_of - pd.Timedelta(days=90))
        & (fw["date"] > as_of - pd.Timedelta(days=180))
    ].groupby("CustomerID")["Revenue"].sum()
    momentum = (last90.reindex(inv).fillna(0) + 1) / (prev90.reindex(inv).fillna(0) + 1)
    snap["revenue_last90_ratio"] = momentum.clip(upper=10)

    snap["weekend_share"] = fw.assign(w=fw["date"].dt.dayofweek >= 5).groupby("CustomerID")["w"].mean()
    snap["is_uk"] = (fw.groupby("CustomerID")["Country"].first() == "United Kingdom").astype(int)

    ret_in_window = (
        returns_df[(returns_df["date"] >= start) & (returns_df["date"] <= as_of)]
        .groupby("CustomerID").size().reindex(inv).fillna(0)
    )
    snap["return_rate"] = ret_in_window / (ret_in_window + g.size())

    label_end = as_of + pd.DateOffset(months=label_months)
    future_buyers = set(
        df_clean[(df_clean["date"] > as_of) & (df_clean["date"] <= label_end)]["CustomerID"].unique()
    )
    snap["churn"] = (~snap.index.isin(future_buyers)).astype(int)
    return snap.reset_index()


T2 = build_snapshot(clean, returns, "2011-08-31")
cohort = pd.read_csv(TABLES / "t02_cohort_summary.csv").set_index("cohort")
check("T2 cohort size", int(cohort.loc["T2", "n_customers"]), len(T2), 0)
check("T2 churn rate", float(cohort.loc["T2", "churn_rate"]), round(float(T2.churn.mean()), 4))

X_T2 = log_scale(T2, SNAP_FEATURES)
km_ref = KMeans(n_clusters=5, n_init=10, random_state=RANDOM_STATE).fit(X_T2)
ref_labels = km_ref.labels_

rng = np.random.RandomState(RANDOM_STATE)
idx = np.arange(len(X_T2))
rng.shuffle(idx)
split = int(0.7 * len(idx))
train_idx, test_idx = idx[:split], idx[split:]

metric_rows = []
for metric in ["euclidean", "cosine", "manhattan"]:
    sil = silhouette_score(X_T2, ref_labels, metric=metric)
    D = pairwise_distances(X_T2, metric=metric)
    knn = KNeighborsClassifier(n_neighbors=5, metric="precomputed").fit(
        D[np.ix_(train_idx, train_idx)], ref_labels[train_idx])
    pred = knn.predict(D[np.ix_(test_idx, train_idx)])
    metric_rows.append({"metric": metric, "silhouette_k5": round(float(sil), 4),
                        "knn_label_agreement": round(float((pred == ref_labels[test_idx]).mean()), 4)})
df_metric = pd.DataFrame(metric_rows).sort_values("silhouette_k5", ascending=False).reset_index(drop=True)
print(df_metric.to_string(index=False))

committed_metric = pd.read_csv(TABLES / "t03_distance_metrics.csv").set_index("metric")
for _, r in df_metric.iterrows():
    check(f"silhouette ({r['metric']})", float(committed_metric.loc[r["metric"], "silhouette_k5"]),
          round(float(r["silhouette_k5"]), 4))
    check(f"kNN agreement ({r['metric']})", float(committed_metric.loc[r["metric"], "knn_label_agreement"]),
          round(float(r["knn_label_agreement"]), 4))
check("selected metric", "cosine", str(df_metric.loc[0, "metric"]))

# --- customer lookalikes (cosine) ---
SIM_T2 = 1.0 - pairwise_distances(X_T2, metric="cosine")
np.fill_diagonal(SIM_T2, -1.0)
example_positions = np.argsort(-T2["monetary"].to_numpy())[:3]
lookalike_rows = []
for p in example_positions:
    ex = T2.iloc[p]
    for rank, q in enumerate(np.argsort(-SIM_T2[p])[:5], start=1):
        lookalike_rows.append({
            "example_customer_id": int(ex.CustomerID),
            "rank": rank,
            "lookalike_customer_id": int(T2.iloc[q].CustomerID),
            "cosine_similarity": round(float(SIM_T2[p, q]), 4),
        })
df_look = pd.DataFrame(lookalike_rows)
committed_look = pd.read_csv(TABLES / "t04_lookalikes.csv")
print("\n  recomputed lookalikes:")
print(df_look.to_string(index=False))
check("lookalike example IDs (3)",
      sorted(committed_look["example_customer_id"].unique().tolist()),
      sorted(df_look["example_customer_id"].unique().tolist()))
check("lookalike customer IDs (all 15)",
      committed_look["lookalike_customer_id"].tolist(), df_look["lookalike_customer_id"].tolist())
check("lookalike max |sim| difference",
      0.0, round(float((committed_look["cosine_similarity"].to_numpy()
                        - df_look["cosine_similarity"].to_numpy()).__abs__().max()), 4))

# --- item-item cosine (identical construction to notebook S3.4) ---
invoices = clean["InvoiceNo"].unique()
products = np.sort(clean["StockCode"].unique())
M_bin = np.zeros((len(invoices), len(products)), dtype=bool)
M_bin[pd.Categorical(clean["InvoiceNo"], categories=invoices).codes,
      pd.Categorical(clean["StockCode"], categories=products).codes] = True
invoice_count = M_bin.sum(axis=0).astype(float)
col_norm = np.sqrt(invoice_count)
col_norm[col_norm == 0] = 1.0
M_norm = M_bin / col_norm

committed_sim = pd.read_csv(TABLES / "t05_similar_products.csv", dtype={"base_stockcode": str,
                                                                      "similar_stockcode": str})
sim_rows, diffs = [], []
for base, grp in committed_sim.groupby("base_stockcode", sort=False):
    j = int(np.where(products == base)[0][0])
    sims = (M_norm[:, j] @ M_norm).astype(float)
    sims[j] = -1.0
    top = np.argsort(-sims)[:5]
    codes = [str(products[i]) for i in top]
    check(f"similar products for {base} (top-5 order)", grp["similar_stockcode"].tolist(), codes)
    for (_, row), code, s_idx in zip(grp.iterrows(), codes, top):
        diffs.append(abs(float(row["cosine_similarity"]) - round(float(sims[s_idx]), 4)))
        sim_rows.append({
            "base_stockcode": base,
            "rank": int(row["rank"]),
            "similar_stockcode": code,
            "committed_cosine": float(row["cosine_similarity"]),
            "recomputed_cosine": round(float(sims[s_idx]), 4),
            "co_occurrence_invoices": int((M_bin[:, j] & M_bin[:, s_idx]).sum()),
        })
check("similar products max |cosine| difference", 0.0, round(max(diffs), 4))

pd.DataFrame(sim_rows).to_csv(TABLES / "s07_similarity_check.csv", index=False)


# =====================================================================
# G. Write the headline check table and summarise
# =====================================================================
banner("G. Summary")
df_checks = pd.DataFrame(CHECKS)
df_checks.to_csv(TABLES / "s07_rule_headline.csv", index=False)

headline = pd.DataFrame([
    {"metric": "rules kept after pruning", "committed": committed_ar["n_rules_pruned"],
     "recomputed": int(len(final_rules))},
    {"metric": "rules evaluated on holdout", "committed": committed_metrics["association_rules"]["n_rules_holdout_evaluated"],
     "recomputed": N_EVAL},
    {"metric": "median holdout lift", "committed": committed_ar["median_holdout_lift"], "recomputed": round(MEDIAN, 4)},
    {"metric": "share holdout lift > 1", "committed": committed_ar["share_holdout_lift_gt1"],
     "recomputed": round(SHARE_GT1, 4)},
    {"metric": "business rules (support>=1%, lift>=2)", "committed": committed_ar["n_business_rules"],
     "recomputed": int(len(business))},
    {"metric": "mean holdout lift (NOT the headline)", "committed": committed_ar["mean_holdout_lift"],
     "recomputed": round(MEAN, 4)},
])
headline["match"] = headline.apply(
    lambda r: abs(float(r["committed"]) - float(r["recomputed"])) < 5e-4, axis=1)
print(headline.to_string(index=False))

n_fail = int((~df_checks["match"]).sum())
print(f"\n  checks run: {len(df_checks)}   mismatches: {n_fail}")
print(f"  outputs   : {', '.join(sorted(p.name for p in TABLES.glob('s07_*.csv')))}")
if n_fail:
    print("\n  MISMATCHES:")
    print(df_checks[~df_checks["match"]].to_string(index=False))
    raise SystemExit(1)
print("\n  all notebook figures reproduced within rounding tolerance")
