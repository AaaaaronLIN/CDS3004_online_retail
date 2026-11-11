# Q&A Drill — 20 likely examiner questions (Group F, CRN 234)

Use this for rehearsal. Each answer is 2–4 sentences; the numbers are the ones in `results/metrics.json`.
If you cannot answer a question in your own words, that is the section to re-read in the report.

---

## A. Problem and design

### 1. Why did you integrate four techniques instead of doing one well?
Because the business decision needs four different questions: *who are they* (segmentation), *who is leaving*
(churn), *what to offer* (association rules), *who looks like our best customers* (similarity). Any one alone
produces a report; together they produce a ranked, budget-bounded action list. We also compared RFM-only,
CLV-regression and basket-only framings in §1.3 and explained why each was insufficient alone.

### 2. Why this dataset?
It is a real, messy, transaction-level extract (541,909 lines, 2010-12 to 2011-12) with genuine quality
problems (24.93% missing CustomerID, cancellations, zero prices, service codes, duplicates). Transaction-level
data is required for market-basket rules and for behaviour features; a clean summary table would not support
the analysis. It is public and citable, so the work is reproducible.

### 3. Why is 90 days the churn horizon?
It matches the retailer's buying cycle (many customers buy every 1–3 months) and it balances label noise
against signal: shorter horizons label too many loyal customers as churned, longer horizons censor more of the
label window. We label "no purchase in the 90 days after the as-of date" and say explicitly that this is a
**lapsing proxy**, not contractual cancellation.

### 4. Why did you segment the T2 cohort rather than T1?
T2 is the decision cohort — the customers we would actually act on today. Segmentation is descriptive, so it
should describe the population being targeted. We state that this is **in-sample and descriptive**, not a
predictive claim; the churn model is what is validated out of time.

## B. Method choices

### 5. Silhouette is highest at K=2 — why did you choose K=5 anyway?
Because silhouette alone is a poor decision rule here. At K=2 the two clusters are nearly "high value vs the
rest" — useless for five different CRM actions. We used a **pre-registered rule**: among K=4–6, require every
segment ≥10% of the base and silhouette ≥0.30, then pick the most stable solution (bootstrap ARI). K=5 gives
ARI **0.9699** with silhouette **0.3279** and five actionable tiers; K=4 is less stable, K=2 is too coarse.
This trade-off is stated openly in the report — we did **not** claim silhouette was maximised.

### 6. Why logistic regression and not the random forest?
Model selection used **validation PR-AUC only**: logreg 0.7079 vs RF 0.6683. On the held-out T1 test the two
are close (AUC 0.7227 vs 0.7216) and out of time logreg is slightly better (0.7392 vs 0.7323). Given equal
performance, we prefer the interpretable, cheaper, more stable model — and we keep the RF as a non-linear
benchmark and as the source of **permutation importance** (basket size, return rate, revenue momentum).

### 7. How do you know there is no label leakage?
Features use only transactions up to the as-of date; the label uses only the 90 days after it. All transforms,
scaling and feature selection are fitted **inside a scikit-learn pipeline on the training folds only**. T2 is
touched exactly once, for out-of-time evaluation, after the model is frozen. We can point to the two code
lines that enforce the temporal cut in the notebook (S2).

### 8. Why cosine distance for similarity?
It won on cluster separation with z-scored log features: silhouette **0.3283** vs manhattan 0.2183 and
euclidean 0.1844, with near-tied kNN label agreement. Cosine is also the natural choice for sparse,
high-dimensional behaviour vectors. We use it for lookalike customers and item–item product similarity.

### 9. Why was recency dropped by RFE — isn't recency the most important churn signal?
In **this feature set** recency is largely redundant with `distinct_months` and `avg_gap_days`; RFE with
logistic regression removed it while validation PR-AUC slightly improved (0.6966 → 0.7036). That is a
modelling decision, not a claim that recency is unimportant. We flag it as a known trade-off in the report.

## C. Evaluation

### 10. Why PR-AUC instead of accuracy or ROC-AUC alone?
Churn is the minority class and the business action is "contact the top K", so ranking quality at the top
matters. Accuracy would be misleading: predicting "nobody churns" would score ~50% on T1. We report PR-AUC
with ROC-AUC, plus **top-decile precision/recall/lift** and Brier score.

### 11. What does "lift@10% = 1.69" mean, in business terms?
If we contact the 200 highest-risk customers (7.1% of T2) instead of 200 random customers, we capture **1.69×**
as many future churners. At a fixed contact budget, that is the value the model adds.

### 12. T1 churn is 50.4% and T2 is 39.6% — doesn't that invalidate the out-of-time test?
No — it makes it a fair test. It reflects a real distribution shift (T2's label window runs Sep–Nov, before the
Christmas peak) and the model still achieves AUC 0.7392 / PR-AUC 0.5947 out of time. We report both cohorts and
treat the out-of-time result as the deployment estimate, not the cross-validated one.

### 13. Is 2,716 / 2,809 customers enough data?
For customer-level models, yes: 5-fold CV AUC standard deviations are ~0.02, so differences larger than that
are meaningful. We avoid over-fitting by shallow trees, regularised logreg, and selection on a validation split.
We also state that a single out-of-time period cannot tell us how much AUC varies across future quarters.

## D. Rules and decision

### 14. Many high-lift rules are just colour variants — isn't that cheating?
Correct, and we say so. The mean holdout lift (28.2) is inflated by rare product-variant pairs with tiny
support, so we do **not** headline it. We report the **median holdout lift 12.174**, the replication rate
(99.8% of rules keep lift > 1), and a business-filtered set of **593 rules** with support ≥1% and lift ≥2
(e.g. GREEN REGENCY TEACUP → ROSES REGENCY TEACUP, support 3.4%, holdout lift 21.6).

### 15. The ROI looks too high — how do you defend it?
We do not defend it as a forecast; we label it a **scenario analysis** and lead with the conservative,
validated variant: **GBP 14,802.58 net** (using the realised 0.31 churn rate in the priority list), versus the
optimistic model-precision bound of GBP 33,799.89. The break-even save rate is only **0.452%**, so the decision
is robust to the assumption; the report states the dataset has no campaign history, so these are not measured
uplift.

### 16. Why is targeting better than contacting everyone?
At the same budget and assumptions, random-200 nets **GBP 1,925.76** while the model's top-200 nets
**GBP 14,802.58–33,799.89**; the net uplift is **GBP 31,874.13** at the base scenario. The point is prioritisation
under a fixed contact capacity, not that everyone should be contacted.

### 17. What would the business actually do on Monday morning?
Run the 200-customer list by priority (churn probability × monetary value), give each segment its mapped action
(VIP retention call, win-back voucher, cross-sell bundle, low-cost reactivation), and attach the relevant
market-basket rule to the contact. The action table (t13/t15) is the deliverable; the model is the ranking.

## E. Process and honesty

### 18. How did you use AI agents, and what did you verify?
We used a harness (DeepSeek Harness / the harnesses listed on p.17) as an accelerator, following the course's
human–agent loop: human defines → agent proposes → human reviews → agent implements → human verifies. Every
module owner independently re-ran their section, checked the numbers against `metrics.json`, and in several
cases changed or rejected agent output (the K=5 justification, the ROI framing, the labelless customer count).
The per-person trajectories record prompts, decisions and verification. The report's §12 documents this.

### 19. What are the biggest limitations?
(1) Anonymous guests — 24.93% of lines / 13.57% of revenue — are excluded, so conclusions describe identified
customers; (2) churn is a no-purchase proxy, not a cancellation; (3) no campaign/response data, so ROI is a
scenario analysis; (4) single retailer, single market — no generalisation claim; (5) associations show
co-purchase, not causation; (6) T2's label window precedes the Christmas peak.

### 20. If you had three more months, what would you do?
Get campaign/response data and run an uplift (incremental-value) model or a randomised holdout; add customer
lifetime value and survival analysis; add product embeddings for cold-start; deploy as a scheduled scoring job
with drift monitoring; validate on a second retailer.

---

## Backup answers (if the room is quiet)

- **What surprised you most?** The model value comes from prioritisation, not prediction accuracy: AUC ~0.74 is
  modest, but the top decile still captures 1.69× the churners, which is what changes the campaign economics.
- **Which single chart matters most?** The ROC/PR + lift chart (f08/f09), because it is the honest evidence that
  the ranking works out of time.
- **What did you deliberately not do?** No deep learning, no SHAP, no oversampling tricks — they would add
  complexity without improving a 2.7k-row tabular problem, and would make the model harder to justify.
