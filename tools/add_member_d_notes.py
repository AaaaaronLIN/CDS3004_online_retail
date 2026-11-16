"""One-off: insert Member D's verification notes into the project notebook.

Inserted as new markdown cells (the notebook is hand-maintained after
code/make_notebook.py generates the scaffold, same as Member B's notes):
  * "### S3.5 Similarity verification notes (Member D)"  after S3.4 (cell 18)
  * "### S7.4 Verification of the rule and holdout numbers (Member D)" after S7.3
Run:  PYTHONPATH=.deps python tools/add_member_d_notes.py
"""
from pathlib import Path

import nbformat as nbf

NB = Path(__file__).resolve().parent.parent / "notebooks" / "CDS3004_Project.ipynb"

S3_NOTE = """### S3.5 Similarity verification notes (Member D)

- **Reproduced, not re-read.** `code/verify_member_d.py` rebuilds the T2 snapshot from
  `data/Online_Retail.xlsx` (2,809 customers, churn 39.55%) and re-runs the K=5 reference
  solution with the same seed. Silhouette is 0.3283 for cosine, 0.2183 for Manhattan and
  0.1844 for Euclidean, while kNN label agreement is 0.9359 / 0.9442 / 0.9419: the metrics
  are within 0.008 on agreement but 0.14 on separation, so cluster coherence decides the
  metric, not neighbour agreement.
- **Lookalike customers are exact.** All 15 neighbour IDs and scores re-derive to the same
  values (14646→14156 0.9877, 18102→17450 0.9833, 12415→17511 0.9640), so the cosine
  customer space is stable under an independent rebuild.
- **Similar products are exact too.** The five neighbourhoods match in order and score
  (85123A→21733 0.3943, 22423→22699 0.3637, 85099B→22386 0.4625, 47566→23298 0.3298,
  84879→21136 0.3665). 22423's neighbours are the same Regency family that dominates the
  top business rule in S7 — the structural-resemblance view of the same commercial fact.
- **What each view is for.** Customer lookalikes serve seed expansion and cold-start
  scoring (a sparse customer inherits its neighbours' segment); product lookalikes serve
  substitute discovery when a SKU is out of stock and bundle construction for the retention
  offer. Neither is a churn predictor on its own.
- **Evidence.** `results/tables/s07_similarity_check.csv` (recomputed vs committed scores),
  `results/tables/s07_rule_headline.csv` (the 44-check log)."""

S7_NOTE = """### S7.4 Verification of the rule and holdout numbers (Member D)

- **Reproduced from the raw workbook.** `code/verify_member_d.py` re-runs S1.4 and
  S7.1–S7.3 and recovers 3,792 frequent itemsets, 8,884 raw rules, **5,441** rules kept and
  **5,402** evaluated out of time (27 excluded for a missing antecedent, 12 for a missing
  consequent), median holdout lift **12.174** at median holdout support 0.00588, 99.78% of
  rules above lift 1 and **593** business rules.
- **Why the headline is the median, not the mean.** 282 rules (5.2%) exceed a holdout lift
  of 100; they are all symmetric variant pairs listed in both directions (top: 22860↔22858,
  lift 4,163.5 at support 0.55%) and they carry 38.5% of the summed lift. Removing them
  moves the mean from 28.1957 to 18.31, and the 10%-trimmed and support-weighted means
  (15.46, 19.18) bracket the median 12.17. The mean describes a handful of near-duplicate
  SKUs, not the rule set.
- **Hand check of the top business rule.** For 22697→22699, 261 holdout baskets contain the
  antecedent, 200 contain both items, 296 contain the consequent, and N_HOLD = 8,327, so
  P(con|ant) = 200/261 = 0.7663 and P(con) = 296/8,327 = 0.03555, giving 21.5569 — identical
  to the exported table.
- **Evidence.** `results/tables/s07_holdout_lift_quantiles.csv`, `s07_mean_lift_tail.csv`,
  `s07_variant_duplicates.csv`, `s07_hand_lift_22697_22699.csv`, `s07_rule_headline.csv`."""


def main() -> None:
    nb = nbf.read(NB, as_version=4)
    if any("Similarity verification notes (Member D)" in "".join(c.get("source", "")) for c in nb.cells):
        raise SystemExit("Member D notes already present; nothing to do")

    def index_of(marker: str) -> int:
        for i, cell in enumerate(nb.cells):
            if marker in "".join(cell.get("source", "")):
                return i
        raise SystemExit(f"marker not found: {marker}")

    # insert from the bottom up so earlier indices stay valid
    s7_after = index_of("# S7.3  Rule tables + support/lift figure")
    nb.cells.insert(s7_after + 1, nbf.v4.new_markdown_cell(S7_NOTE))
    s3_after = index_of("# S3.4  Similar products: item-item cosine similarity")
    nb.cells.insert(s3_after + 1, nbf.v4.new_markdown_cell(S3_NOTE))

    nbf.write(nb, NB)
    print(f"inserted 2 markdown cells; notebook now has {len(nb.cells)} cells")


if __name__ == "__main__":
    main()
