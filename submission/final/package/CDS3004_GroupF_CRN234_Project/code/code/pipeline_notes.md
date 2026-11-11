# Pipeline notes — CDS3004 Online Retail

Runtime: 29.0 s end-to-end (single machine, pandas 3.1.1, scikit-learn 1.9.1); budget was <10 min, so grids are deliberately small.
Data decisions: drop missing CustomerID (24.9% of lines = 13.6% of gross revenue), cancelled invoices, Quantity<=0, UnitPrice<=0, non-product/service StockCodes and exact duplicates; keep a separate returns ledger so return_rate exists as a feature (funnel removals are smaller than audit counts because one line can violate several rules).
Bias to disclose: the clean base is purchase-only and identified-customer-only, so it describes registered customers, not the whole business; guest revenue is outside the model.
Snapshots: T1 as_of 2011-05-31 (features 2010-12-01..2011-05-31, churn = no purchase Jun-Aug 2011) and T2 as_of 2011-08-31 (features Mar-Aug 2011, churn = no purchase Sep-Nov 2011). Only customers with >=1 purchase in the feature window get a row.
Churn definition is a 3-month no-purchase rule; it captures lapsing, not contractual cancellation.
Gap statistic gotcha: in pandas 3, groupby.apply returning a Series yields a stacked Series; we unstack it, so avg_gap_days/std_gap_days are aligned correctly. Single-visit customers get 0 gaps.
revenue_last90_ratio is smoothed ((last90+1)/(prev90+1), capped at 10) because ~65% of customers have no previous-90-day revenue; it therefore partly flags new/returning customers.
Distance choice: cosine wins on silhouette (0.33 vs 0.18 euclidean, 0.22 manhattan) with near-tied kNN label agreement, so lookalikes/products use cosine on log1p+z-scored features.
Feature selection is fitted on the T1 train split only (correlation filter -> MI top-12 -> RFE top-10); all transforms live inside sklearn Pipelines so CV has no leakage.
Segmentation: K=5 chosen from K=4-6 by bootstrap stability (ARI 0.97) with silhouette near its local peak and every segment >=10% of the base; segments named by RFM rank.
Model selection uses validation PR-AUC only; logreg was selected and also leads on T1 test and T2 out-of-time AUC, while random forest is close but does not beat it.
Association rules: FP-Growth min_support=0.005, max_len=3, confidence>=0.2, lift>=1.2; validated on a later period (median holdout lift 12.2, 99.8% keep lift>1); the mean is inflated by rare product-variant pairs, so business rules (support>=1%) are reported separately.
Caution: many high-lift rules are variants of the same product (colour/size), so lift overstates incremental cross-sell; holdout lift is reported to keep this honest.
Decision framework: priority = predicted churn probability x monetary; ROI is churn-conditional (p_churn_targeted=0.669, base save rate 10%, cost GBP 8.00, margin 35%) and is compared with random targeting under the same scenarios. It remains a scenario analysis, not measured uplift - the realised churn rate inside the value-weighted list is lower (0.31), giving a validated net of GBP 14,803.
Clustering is descriptive and fitted on the T2 decision cohort, so segment labels are in-sample; no predictive claim is made about them.
Reproducibility: random_state=42 everywhere, relative paths, mlxtend installed project-locally (Colab fallback %pip install), notebook executed in place via nbconvert.
