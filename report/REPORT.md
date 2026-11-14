# From Transactions to a Customer Operating System

## An Agent-Assisted Data Mining Study of Online Retail Customer Behaviour

**Course:** CDS3004 Data Mining — Group Project (22%) and Group Presentation (8%)
**Institution:** Lingnan University, School of Data Science, 2026/27 Term 1
**Instructor:** Prof. Daoyuan Wu
**Team:** Group F — LIN Xiaotong (4589755), Patten Lai (4001777), Weng Zhi Chao (4589896), Lim Man Tung Marcus (4592996), Huang Hao Lin (4455930)
**Submission date:** 6 December 2026
**Repository:** `https://github.com/AaaaaronLIN/CDS3004_online_retail` (public)

---

## Abstract

This report asks how an online retailer can turn twelve months of raw transaction records into a *customer operating system*: one integrated set of models that describes who customers are, predicts who is about to leave, recommends what to offer, and ranks retention actions under a fixed campaign budget. Using 541,909 transaction lines from the UCI Online Retail dataset (December 2010 to December 2011), we build temporal customer snapshots, engineer and select behavioural features, and combine four data-mining techniques: K-means segmentation into 5 descriptive segments with bootstrap stability, churn classification (logistic regression, decision tree, random forest) trained on a T1 cohort and validated by 5-fold cross-validation, a held-out split and a T2 out-of-time cohort, FP-Growth association rules validated on a later holdout period, and similarity-based lookalike analysis. The selected logistic-regression model reaches an out-of-time ROC-AUC of 0.7392 and top-decile lift of 1.6916×; the random forest, used for feature importance, reaches 0.7323. The T2 cohort is then segmented, scored and mapped into a segment-by-risk matrix with a transparent, churn-conditional ROI scenario: a conservative validated net expected value of GBP 14802.58 for the pilot campaign, against an optimistic model-precision bound of GBP 33799.89. Limitations, including anonymous-customer bias and the absence of campaign data, are stated explicitly.

**Keywords:** customer segmentation, churn prediction, association rules, similarity, decision support, online retail, agent-assisted data mining.

---

## 1. Problem Definition

### 1.1 Business question

An online retailer sits on a year of line-item transactions but has no operational view of its customers. The commercial question is not "can we train a model?" but "what should the business do on Monday morning, for which customers, with what offer, and with what expected return?" We frame the problem as building a *customer operating system* with four linked questions and one decision output:

1. **Who are our customers?** — a stable, interpretable segmentation of the current customer base.
2. **Who is about to leave?** — a ranked 90-day churn risk for every customer.
3. **What should we offer them?** — cross-sell rules from real baskets, plus lookalike similarities for sparse and cold-start customers.
4. **What is the single prioritised action list?** — a capacity-bounded target list whose expected value and assumptions are explicit.

The unit of analysis is the customer at a fixed as-of date; the horizon is 90 days; the actions are retention contact and cross-sell recommendation.

### 1.2 Stakeholders and constraints

Four stakeholders need different things. CRM and marketing need a ranked contact list within campaign capacity. E-commerce operations need an interpretable picture of which segments drive revenue and which are decaying. Finance needs the assumptions behind any expected-value claim so it can challenge them. The data team needs reproducible, leakage-free code that re-runs on new data. The constraints shape every later choice: one 12-month transaction extract with no demographics, consent or campaign-response data, and a substantial share of anonymous transactions; a single retailer in a single market; a CPU-only environment expected to run the notebook in well under ten minutes; and English-language, fully reproducible deliverables. The presentation is 20 minutes excluding Q&A, confirmed with the course.

### 1.3 Alternative framings considered

**Table 1.** Alternative problem framings and the reason for the final choice.

| Framing | What it would deliver | Why it was not sufficient alone | Verdict |
|---|---|---|---|
| A. Descriptive RFM segmentation | Segment profiles and revenue shares | Static; no forward-looking signal; cannot rank customers or justify a campaign | Retained as a *component* |
| B. Supervised lifetime-value regression | Predicted 90-day spend | No campaign or response data to validate the target; noisy and right-censored | Rejected; future work (§10.4) |
| C. Market-basket recommendation only | Cross-sell rules and product similarities | No customer state or retention signal; cannot allocate a contact budget | Retained as the *offer layer* |
| **D. Integrated customer operating system** | Segmentation + churn + rules + similarity + one decision list | More engineering; four techniques must agree on one cohort definition | **Chosen** |

The integrated framing wins because it is the only one that ends in an actionable decision, and because the four techniques answer different questions rather than competing. It also gives the rubric direct evidence for problem definition, solution design, learning, evaluation, interpretation and delivery, rather than a single technique applied once.

### 1.4 Success criteria

We judged the project successful if: (i) the chosen number of segments is stable under bootstrap resampling (mean adjusted Rand index in §5.2); (ii) the churn models beat a no-skill baseline on held-out and out-of-time cohorts and concentrate churners in the top decile (lift > 1); (iii) association rules retain support and lift on a later holdout period; (iv) the decision layer produces a capacity-bounded list with every ROI assumption stated and a sensitivity analysis; and (v) every figure, table and number is regenerated by running one notebook on the raw data.

---

## 2. Data

### 2.1 Source and schema

The analysis uses the UCI Machine Learning Repository *Online Retail* dataset (Chen, Sain and Guo, 2012): 541,909 line items from a UK-based registered non-store online retailer, covering December 2010 to December 2011. Each row is one product line on one invoice. Table 2 shows the schema.

**Table 2.** Dataset schema: column, type, non-null count, example value and role.

{{TABLE:t01_dataset_schema}}

The dataset is distributed by UCI for research and teaching use; the download source, schema notes and usage note are reproduced in `data/README.md`, and we report only aggregate, segment-level findings. The raw workbook stays unmodified in `data/`; all cleaning is code, so every decision is auditable and reversible.

### 2.2 Collection and preparation process

We did not collect the data; our preparation work is the reconstruction of *customer states* from raw line items. First, a cleaned line-item table is produced by the audit-and-cleaning step. Second, the line items are aggregated into two **temporal customer snapshots**: a training cohort **T1** with an as-of date of 31 May 2011, and a decision cohort **T2** with an as-of date of 31 August 2011. For each snapshot, features use only transactions strictly before the as-of date, and the churn label uses only transactions in the 90 days after it. Third, T1 is split 70/15/15 into train, validation and test sets for churn model development and evaluation, while T2 is held back entirely during development, opened once for out-of-time evaluation, and then used as the cohort on which the operating system produces its decisions. This construction — not any single cleaning rule — is what makes the evaluation honest.

T2 was chosen to leave a buffer before the dataset ends: with 31 August 2011 as the snapshot, the 90-day label window closes in late November 2011, inside the observation period, so T2 labels are fully observed rather than truncated by the end of the file. The exact observation dates are in the pipeline output (2010-12-01 to 2011-12-09).

### 2.3 Data-quality issues

The raw extract is realistic rather than clean. Table 3 lists the issue classes with their raw size and the action taken; Figure 1 summarises them. The audit counts overlap — one line can violate several rules — so the cleaning funnel in Table 4 removes fewer lines than the sum of the audit counts; both views are reported so that neither is mistaken for the other.

**Table 3.** Data-quality audit: issue, affected rows or share, and treatment.

{{TABLE:t02_data_quality_issues}}

{{FIGURE:f01_data_quality_overview}}

*Figure 1.* Data-quality overview: missing customer identifiers, cancellation and administrative lines, duplicates and date coverage across the 12-month window.

Four issues matter enough to discuss. Missing customer identifiers are the most consequential: 24.9267% of raw lines have no `CustomerID`, so they can be described in revenue terms but cannot be attached to a customer snapshot. Returns and cancellations (negative quantities and `C`-prefixed invoices) are legitimate events, not errors; we exclude them from monetary aggregates but retain them in a separate returns ledger so that return behaviour becomes a *feature*. Price anomalies and non-product stock codes (postage, manuals, bank charges, discounts, test SKUs) are administrative artefacts that would distort product similarity and association rules, so they leave product-level analysis while remaining visible in the audit. Duplicate rows and inconsistent description strings are removed or normalised; missing descriptions are filled with an `UNKNOWN` label that affects product labels only.

### 2.4 Cleaning decisions and rationale

Three principles guided the decisions: *never silently drop information* (every removal is counted and reported); *separate description from prediction* (rows that cannot be attributed to a customer leave the modelling population but stay in the audit); and *avoid target leakage during cleaning* (rules depend only on transaction fields and are applied identically to T1 and T2). Table 4 gives the sequential cleaning funnel with the rows remaining after each step and the reason for the step.

**Table 4.** Cleaning decisions: sequential funnel, rows affected, rows remaining and rationale.

{{TABLE:t03_cleaning_decisions}}

After cleaning, 72.18% of lines and 81.9114% of revenue are retained for the customer-level analysis, across 391150 lines and 4334 identified customers. The revenue figure matters: it shows how much of the business the customer-level view still describes.

### 2.5 Analysis population and bias caveat

The customer-level analysis population is the set of customers with at least one valid purchase and a known identifier: 2716 customers in T1 and 2809 in T2. Anonymous transactions are **not** part of it, because they cannot be linked across visits, so no feature, label or segment can be defined for them.

This creates a bias we state rather than hide. Anonymous lines represent 13.572% of gross revenue, so the customer-level view under-represents guest purchasing, and the dropped population may differ systematically (one-off buyers, other markets, customers who later register). Every segment share, churn rate and ROI claim below therefore describes *identified customers only*, and the revenue share is the scale of the blind spot.

---

## 3. Solution Design

### 3.1 End-to-end pipeline

The solution is one reproducible notebook organised into ten sections, S0–S9 (Table 5). Each section writes an artifact that later sections consume, which makes the analysis reproducible and the agent-assisted development verifiable.

**Table 5.** Notebook sections S0–S9: what each does and which artifacts it produces.

| Section | What it does | Method | Output |
|---|---|---|---|
| S0 Setup | Load the raw workbook; configure paths, seed and helper functions | pandas, scikit-learn pipelines | Clean environment; schema audit |
| S1 Data quality and cleaning | Audit issues, build the returns ledger, clean the purchase base | Rule-based sequential cleaning funnel | `t02_data_quality_issues`, `t03_cleaning_decisions`, `f01_data_quality_overview` |
| S2 Snapshots and churn labels | Build T1/T2 as-of customer tables and 90-day churn labels | Temporal aggregation; disjoint feature and label windows | `t02_cohort_summary`, `t04_feature_dictionary` |
| S3 Similarity and distance | Compare three distance metrics; lookalike customers; similar products | Silhouette and kNN label agreement; cosine kNN and item-item cosine | `t03_distance_metrics`, `t04_lookalikes`, `t05_similar_products`, `f11_similarity_lookalikes` |
| S4 Feature engineering and selection | Build 16 behavioural features; correlation/MI/RFE selection | Mutual information; RFE with logistic regression; log1p and scaling inside pipelines | `t05_feature_selection`, `t05b_feature_evidence`, `f02_feature_distributions`, `f08_feature_importance` |
| S5 Segmentation | Segment the T2 decision cohort | K-means with elbow, silhouette, bootstrap ARI and a business-size rule | `t06_cluster_metrics`, `t07_segment_profiles`, `f04`–`f06` |
| S6 Churn models | Train and evaluate three classifiers; thresholds and lift | Stratified 70/15/15 split; 5-fold CV; validation PR-AUC selection; T1 test and T2 out-of-time | `t08_model_metrics`, `t09_lift_deciles`, `f07`–`f09` |
| S7 Association rules | Mine and validate cross-sell rules | FP-Growth on training-period baskets; holdout validation on a later period | `t09_top_rules`, `t10_association_rules`, `f10_association_rules` |
| S8 Integrated decision framework | Score T2, build segment × risk matrix, priority list and ROI scenarios | Priority = churn probability × monetary value; explicit ROI assumptions | `t12_segment_risk_matrix`, `t13_action_table`, `t11_top200_targets`, `t15_priority_list_summary`, `f12`, `f13` |
| S9 Summary and reproducibility | Write metrics, artifact index and notes; run integrity checks | — | `metrics.json`, `metrics_extra.json`, `metrics_summary.md`, `ARTIFACTS.md` |

### 3.2 Why the components are integrated rather than run separately

Four separate analyses would satisfy the letter of "apply several techniques" but not the business question, because the decisions are entangled. Segmentation alone says *who* a customer is but not *whether to act now*. Churn alone says *when* to act but not *what to say* or *how much the customer is worth*. Association rules say *what to offer* but not *to whom*. Similarity supports targeting when a segment is too sparse to estimate churn reliably. The decision layer is the integration point: a customer is prioritised because of a *risk* (churn probability), a *context* (segment and its value), an *offer* (rule or lookalike) and a *capacity constraint* (contacts the team can make). Each technique contributes one factor to the same score, and the matrix in §9.1 is where the factors meet.

Integration also improves evaluation. The churn model is trained on T1 and applied unchanged to T2, so the risk scores that drive the decision layer are genuinely out-of-time. Segmentation is unsupervised and fitted in-sample on T2, so it adds no label information. The result is a decision matrix whose every cell is produced under the same temporal discipline.

### 3.3 Why each method fits the question

**Table 6.** Method choice and justification, with alternatives rejected.

| Question | Chosen method | Why it fits | Alternatives rejected |
|---|---|---|---|
| Who are our customers? | K-means on scaled RFM and behavioural features | Compact centroids; fast assignment; matched to continuous, standardised features | GMM (soft assignments hard to operationalise), hierarchical (no need for a dendrogram), DBSCAN (density varies across customers) |
| Who will churn? | Supervised classification with imbalance handling | 90-day label is directly actionable; probabilities rank customers for a fixed budget | Survival analysis (needs longer history), anomaly detection (no calibrated risk) |
| What to offer? | FP-Growth frequent itemsets | No candidate generation, scales to half a million lines; readable support/confidence/lift | Apriori (same result, slower), sequential rules (no meaningful session sequence) |
| Who resembles our best customers? | Cosine, Jaccard and Euclidean similarity | Scale-free for sparse baskets; supports cold-start and lookalike expansion | Clustering alone (too coarse), matrix factorisation (needs more interaction data) |
| What should we do on Monday? | Priority score plus explicit ROI | One capacity-bounded action list whose assumptions finance can audit | Dashboards (informative but not decisive) |

The design is deliberately not the most complex possible: it uses only methods introduced in CDS3004 and justified by the question, and reserves complexity for the out-of-time validation, the holdout-validated rules and the decision layer's explicit assumptions.

---

## 4. Feature Engineering

### 4.1 Temporal snapshots and label definition

Features are computed from transactions strictly **before** the snapshot date, and the churn label from transactions **after** it; no feature observes the label window. For snapshot date *t*: features aggregate all valid transactions with `InvoiceDate < t`; `churn = 1` if the customer has no valid purchase in `[t, t + 90 days]`, else `0`. **T1** (*t* = 31 May 2011, feature window December 2010 to May 2011) is the training cohort used for feature selection, model selection and threshold choice; **T2** (*t* = 31 August 2011, feature window March to August 2011) is the out-of-time evaluation cohort and the cohort the operating system acts on. The 90-day window is a business choice matching a quarterly retention cycle: long enough that a quiet month is not churn, short enough that features and labels do not overlap.

Only customers with at least one purchase inside the feature window receive a snapshot row; otherwise recency, frequency and monetary value would be undefined. The empirical churn rate is 0.5044 in T1 and 0.3955 in T2, expressed as the proportion of the cohort with no purchase in its label window. The rates differ because the cohorts cover different calendar periods — important when reading the out-of-time results. Table 7 summarises the cohorts.

**Table 7.** Cohort summary: as-of date, feature and label windows, size and churn rate.

{{TABLE:t02_cohort_summary}}

### 4.2 Feature families

Sixteen behavioural features are built per customer from the snapshot (Table 8). They fall into nine families: **RFM** (recency, frequency, monetary), **monetary structure** (average basket, average unit price, largest invoice), **basket size** (items per invoice), **breadth** (distinct products), **engagement** (distinct months, tenure), **rhythm** (mean and standard deviation of inter-purchase gaps), **momentum** (last-90-day revenue ratio), **behaviour** (weekend share, return rate) and **context** (UK indicator). The design follows RFM but does not stop there, because RFM cannot distinguish a loyal low-spend customer from a lapsing high-spend one.

Two engineered features deserve a note. The revenue-momentum ratio is smoothed as `(last90+1)/(prev90+1)` and capped, because roughly two-thirds of customers have no prior-90-day revenue; it therefore partly flags new or returning customers rather than pure acceleration. The return rate comes from the separate returns ledger built in S1, so cancellations are not lost. The feature dictionary (Table 8) gives every definition and family.

**Table 8.** Feature dictionary: definition and family for each of the sixteen engineered features.

{{TABLE:t04_feature_dictionary}}

### 4.3 Transformation rationale

Raw retail features are heavy-tailed: a few customers and orders account for a disproportionate share of spend, and monetary and quantity distributions are strongly right-skewed (Figure 2). Untransformed, these variables would dominate distance-based methods and destabilise logistic-regression coefficients. We therefore apply **log1p** to monetary, quantity and interval features (compressing the long tail, defined at zero, order-preserving, so centroids remain interpretable after exponentiation); **standardisation (z-scores)** before K-means and regularised logistic regression; a **binary UK indicator** for the only static market flag (no one-hot expansion of `StockCode` or `Country`); and **no target encoding** of customer aggregates, because it would leak label information across snapshots.

{{FIGURE:f02_feature_distributions}}

*Figure 2.* Heavy-tailed raw features and the same features after log1p transformation; transformed columns are then standardised before distance-based modelling.

All transformations live inside a scikit-learn `Pipeline`, so scalers and selectors are refit on each training fold during cross-validation rather than once on the full data. The pipeline asserts that no transformed column contains infinite values and drops all-zero-variance columns before modelling.

### 4.4 Feature selection and evidence

Selection proceeds in three stages, fitted inside the training folds only. **Correlation filter:** among any pair with absolute Pearson correlation above 0.9, drop the member with the lower mutual information with churn — in practice this removes `avg_basket`. **Mutual information:** a non-linear, model-free relevance ranking keeps the top 12 features. **Recursive feature elimination:** a logistic regression with step-wise elimination keeps the top 10. The funnel runs from 16 engineered features to 15 after the correlation filter, 12 after mutual information and 10 after RFE. Table 9 records the validation evidence, and the per-feature file `t05b_feature_evidence.csv` records the stage outcomes for every variable.

**Table 9.** Feature-selection funnel and validation PR-AUC at each stage.

{{TABLE:t05_feature_selection}}

Selection is validated, not assumed. On the T1 validation split the selected set reaches PR-AUC 0.7036 versus 0.6966 for the full set, so the reduction removes redundancy without discarding signal; when two stages were within 0.005 validation PR-AUC, the smaller set was preferred. Figure 3 shows the permutation importance of the final features, computed with the random forest on the held-out test set. It is led by basket size (items per invoice), return rate and revenue momentum, with frequency and gap regularity next. Notably, `recency_days` was dropped by RFE even though recency is univariately strong; it is partly captured by `distinct_months` and `avg_gap_days`. That is a documented modelling caveat, not evidence that recency is unimportant. The final 10-feature set is used by the three churn models; the K-means segmentation in §5 uses all 15 behavioural features (the same list without the static `is_uk` flag) because it is descriptive.

{{FIGURE:f08_feature_importance}}

*Figure 3.* Random-forest permutation importance of the final feature set on the held-out T1 test set.

### 4.5 Leakage control

Leakage is the most common failure mode here, so controls are explicit. **Temporal discipline:** snapshot features never reference transactions at or after the as-of date, and the label window is disjoint from the feature window; the notebook asserts this. **Transforms fitted on training data only:** inside cross-validation, scalers and selectors are refit on each training fold; for the final deployment model they are fitted on the T1 training split and applied unchanged to the T1 test set and to T2. **No cross-snapshot label information:** T2 features use only transactions before 31 August 2011, and T2 labels are used only for evaluation, never for fitting or choosing anything. **Threshold selected on T1 only:** the contact thresholds are chosen on T1 validation scores, then applied to T1 test and T2. **Single decision point:** the out-of-time cohort is opened once, after features, model and thresholds are frozen; the agent logs record this as a deliberate human gate. The K-means segmentation is fitted on T2 features but is unsupervised, so it uses no labels and cannot leak them.

---

## 5. Customer Segmentation

### 5.1 Method and setup

K-means is fitted on the **T2 decision cohort** (customers as of 31 August 2011) across the 15 behavioural features — every engineered feature except the static `is_uk` market flag — after log1p transformation and z-scoring. This segmentation is **descriptive**: customers are clustered in-sample on the decision cohort, so the labels describe the current base rather than predict future behaviour, and no predictive claim is made about them. T1 is not used for segmentation; it exists to train and evaluate the churn model, which is then refit on T1 train+validation and applied to T2 (§6). For a production refresh, the same procedure re-segments the latest snapshot and re-scores it with the current model.

### 5.2 Choosing K

Three diagnostics are used together, because no single one is trustworthy alone: the **elbow** in within-cluster inertia, the **silhouette coefficient** under the winning distance metric (higher is better), and **bootstrap stability** measured by the adjusted Rand index (ARI) between ten resampled (80%) segmentations and the full-data solution (Hubert and Arabie, 1985). A fourth, business-level criterion is applied: every segment must be large enough to target (at least 10% of the base) and map to a distinct RFM story.

We considered K = 4–6. K = 2–3 gives only a coarse tiering, and K ≥ 7 produces very small segments (at K = 6–8 one segment falls below 3% of customers). Within the candidate range, **K = 5** has the highest bootstrap stability (mean ARI 0.9699) and keeps every segment above 10% of the base. It is important to be precise about the evidence: **K = 5 is not the silhouette maximum**. Silhouette is highest at smaller K, but K = 2 is too coarse for the five-tier action framework and K = 4 is substantially less stable under resampling. We chose K = 5 on the balance of stability, meaningful segment size and business interpretability, with a mean silhouette of 0.3279 — adequate rather than maximal. The diagnostics are in Figure 4 and Table 10; presenting the choice as a silhouette optimum would overstate the evidence.

{{FIGURE:f04_elbow_silhouette}}

*Figure 4.* K-selection diagnostics: elbow curve (inertia), silhouette coefficient and bootstrap stability (mean ARI) across candidate values of K.

**Table 10.** K-means diagnostics for candidate numbers of segments, including the selected K.

{{TABLE:t06_cluster_metrics}}

### 5.3 Segment profiles and naming

The solution yields five segments — **Champions, Loyal, Potential, At-risk and Hibernating** — named after their RFM signature rather than a number, so the business can use the names in campaign briefs. Table 11 profiles each segment: size, share of customers, recency, frequency, monetary value, basket structure, momentum, return behaviour, UK share and actual churn rate. Naming and profiling are applied by code, not by hand, so they reproduce when the data refreshes.

**Table 11.** Segment profiles: size, revenue share, RFM means, behaviour and actual churn rate.

{{TABLE:t07_segment_profiles}}

{{FIGURE:f05_segment_profiles}}

*Figure 5.* Segment profile heatmap: standardised feature means per segment, annotated with segment size and revenue share.

### 5.4 Visualising the segments

Because the models live in a high-dimensional space, we visualise the segmentation through a two-dimensional principal-component projection (Figure 6); the first two components explain 0.3647 and 0.1506 of the variance respectively (as proportions). The projection is used only for communication, never for modelling. The clusters separate chiefly along the value and frequency axes and, to a lesser extent, along recency, which the profile table also shows.

{{FIGURE:f06_cluster_pca}}

*Figure 6.* PCA projection of the T2 customer base coloured by segment; the projection is for visualisation only.

### 5.5 Interpretation

The segmentation is commercially meaningful in three ways. First, segments differ by *orders of magnitude* in monetary value, so a small number of customers carries a large share of revenue — visible in the revenue-share column of Table 11 and the reason the decision layer weights customers by value. Second, segments differ in actual churn rate: Champions churn least, while At-risk and Hibernating churn most, which is the bridge to §6 and makes the segment × risk matrix in §9.1 more informative than either dimension alone. Third, the smallest segments are not necessarily the least important: the At-risk segment is modest in size but combines high value with high risk, which is exactly where retention spending earns the most. Segment names and profiles must be read together, not as a ranking of size.

---

## 6. Churn Prediction and Evaluation

### 6.1 Cohorts and split strategy

The churn target is defined in §4.1. **T1** (as-of 31 May 2011, label window June–August 2011) is split 70/15/15 into train, validation and test sets, stratified on the label so the churn base rate is preserved in every split. The validation split selects features, hyperparameters, the model and the operating thresholds; the held-out test set is used once for an unseen estimate. **T2** (as-of 31 August 2011, label window September–November 2011) is never touched during development and serves as the out-of-time test; after the model is frozen, the selected model is refit on T1 train+validation and applied to T2 to produce the risk scores used by the decision layer. This gives three levels of evidence — cross-validation, held-out and out-of-time — that the rubric explicitly requires. No modelling decision used the held-out test set or T2.

### 6.2 Models and training protocol

Three families are compared, spanning the interpretability–accuracy trade-off. **Logistic regression** with L2 regularisation and class-balanced weights is the transparent baseline; its regularisation strength is tuned on validation (C = 0.01 in the selected configuration). **Decision tree** with a depth constraint tuned on validation (maximum depth 3) produces rules a non-technical stakeholder can follow. **Random forest** with 400 trees and class-balanced subsampling captures non-linearities and interactions at the cost of transparency, which is why permutation importance is reported instead of coefficients. All models use the same frozen 10-feature set. A stratified 5-fold cross-validation on the training split reports mean ± standard deviation for ROC-AUC and PR-AUC; hyperparameters and model choice use the validation split, and the test and out-of-time cohorts are never used for tuning. Class imbalance is handled with balanced weights and evaluated with threshold-free ranking metrics (ROC-AUC, PR-AUC, Brier score) rather than accuracy, which would mislead at the observed churn rate.

### 6.3 Cross-validation results

Figure 7 shows the cross-validated model comparison. The cross-validated mean ROC-AUC is 0.7593 ± 0.0217 for logistic regression, 0.7397 ± 0.0179 for the decision tree and 0.7505 ± 0.022 for the random forest. The model selected on **validation PR-AUC only** is `logreg`; its held-out and out-of-time results are reported as-is in Table 12, including wherever a more flexible model would have looked better in-sample.

{{FIGURE:f07_cv_model_comparison}}

*Figure 7.* Five-fold cross-validated model comparison on the T1 training split (mean ± standard deviation ROC-AUC and PR-AUC).

**Table 12.** Model performance on held-out T1 and out-of-time T2 (AUC, PR-AUC, precision, recall and top-decile metrics).

{{TABLE:t08_model_metrics}}

The cross-validated ranking is only the first filter. We carry all three models to the held-out and out-of-time tests rather than selecting one on cross-validation alone: a model that wins inside T1 but degrades out of time is not deployable, and the three families serve different stakeholder needs (interpretability, communicability, ranking accuracy).

### 6.4 Held-out and out-of-time results

The selected logistic regression achieves ROC-AUC 0.7227 on the held-out T1 test set and 0.7392 out of time on T2, with PR-AUC 0.5947 against 0.6744 on T1. The random forest is retained as a non-linear benchmark and as the source of permutation importance, but it is not the selected decision model; its out-of-time ROC-AUC is 0.7323. Figure 8 shows the held-out and out-of-time ROC curves for all three models, and Table 12 gives the complete per-model results including precision and recall at the operating threshold. The out-of-time number is the one to quote to a business sponsor, because the cross-validated estimate is optimistic when the same period produced the features, the labels and the model choices.

{{FIGURE:f08_roc_test_oot}}

*Figure 8.* Held-out T1 and out-of-time T2 ROC curves for the three models.

Two points matter for honest interpretation. First, the T2 base rate differs from T1 (0.3955 versus 0.5044), so the two ROC curves answer slightly different questions; Table 12 therefore reports both AUC and PR-AUC, and no claim rests on PR-AUC alone. Second, the out-of-time result is a single period, not a distribution: one holdout cannot tell us how much the AUC would vary across future quarters.

### 6.5 Threshold choice and top-decile lift

A probability is not a decision, and there are two operating points worth reporting. The **F1-optimal threshold** (0.2665), chosen on the T1 validation split, maximises the balance between precision and recall; it is the threshold used in the confusion matrix and is useful when the cost of a missed churner and a wasted contact are comparable. The **capacity threshold** (0.7382) selects the top 10% of scored customers by predicted risk; it is the operating point for a campaign of that size. The two trade recall for precision: the F1-optimal threshold catches most churners but also contacts many customers who would have stayed, while the capacity threshold contacts a tenth of the base and is much more precise as a share of contacts. The pilot campaign itself is tighter still: the priority list is capped at 200 contacts, which is the top 7.12% of the T2 cohort.

At the top-decile operating point the selected model achieves lift of 1.6916× over random contact on T2, with precision 0.669 and recall 0.1692; the corresponding T1 test values are 1.3526× lift, precision 0.6829 and recall 0.1359. Figure 9 shows the lift curve and Table 13 the decile breakdown. Lift is the metric that connects the model to the campaign: it says how many churners the business reaches per hundred contacts compared with random contact.

{{FIGURE:f09_lift_curve}}

*Figure 9.* Cumulative lift curve for top-K targeting for the selected model, with the top-decile operating point marked.

**Table 13.** Decile lift table: contact decile, captured churners, precision, capture rate and lift.

{{TABLE:t09_lift_deciles}}

### 6.6 Error analysis and caveats

Errors were examined in four ways. First, the confusion matrix at the F1-optimal threshold shows the trade-off the campaign accepts: false negatives are customers who leave without contact, false positives are contacts spent on customers who would have stayed. Second, the threshold sweep shows how precision and recall move as the contact budget changes, so the campaign owner can see the cost of cutting or expanding capacity; both panels are in `f09_confusion_and_threshold`. Third, permutation importance (Figure 3) is led by basket size, return rate and revenue momentum, while `recency_days` was dropped by RFE and is only partly captured by `distinct_months` and `avg_gap_days`; that is a documented caveat, not evidence that recency is unimportant. Fourth, we checked error composition by segment, because a model that is accurate on average but systematically wrong for a small high-value segment is dangerous.

The label is a proxy: a customer with no purchase in 90 days may be on a long holiday rather than lost. The out-of-time cohort covers a different season, so its base rate and feature distributions differ from T1. The model has no marketing-contact information, so it predicts *who will be inactive*, not *who would respond to a campaign* — a distinction treated again in §9.5 and §10.2.

---

## 7. Association Rules

### 7.1 Mining setup

Rules are mined on baskets defined as distinct invoices in the cleaned line-item table. Cancellations and administrative stock codes are excluded because they would create spurious co-purchases. FP-Growth is used rather than Apriori because it avoids candidate generation and scales to half a million lines. The mining period is the training window 1 December 2010 to 31 July 2011; the later period 1 August to 9 December 2011 is held out for validation. Rules are mined with minimum support 0.005, maximum itemset length 3, minimum confidence 0.20 and a lift floor of 1.2.

### 7.2 Pruning and ranking

Raw rule sets are dominated by near-duplicates (a rule and all its supersets). We keep rules above the confidence and lift floors, rank them by lift with confidence and support as tie-breakers, and report two views. Table 14 shows the ten highest-lift rules as mined; this is the view that exposes the overstatement problem, because the top rules turn out to be near-identical colour or size variants of one product. Table 15 instead applies a business filter: support of at least 1%, lift of at least 2, one direction per product pair, ranked by frequency. The business-filtered set is what a campaign planner should read; the full rule set is in `t10_association_rules.csv`.

**Table 14.** Top association rules by training lift: antecedent, consequent, support, confidence, lift and holdout lift (the top rules are mostly product variants).

{{TABLE:t09_top_rules}}

**Table 15.** Business-filtered association rules (support ≥ 1%, lift ≥ 2, one direction per pair, ranked by frequency).

{{TABLE:t10b_business_rules}}

{{FIGURE:f10_association_rules}}

*Figure 10.* Association-rule scatter: support versus lift, with bubble size showing confidence and colour showing holdout lift; product descriptions are annotated and the low-support variant pairs behind the highest lift are flagged.

### 7.3 Holdout validation

Rules mined on one period can be seasonal artefacts, so we validate them on a **later holdout period** that was not used for mining. Of 5441 rules retained after pruning and filtering, 5402 were evaluated out of time; 27 were excluded because the antecedent never appears in the holdout and 12 because the consequent vanished — their quality is unknown, not zero. The headline evidence is the **median** holdout lift of 12.174 at a median holdout support of 0.00588 (0.59% of invoices); 99.8% of evaluated rules keep lift above 1 and 99.4% keep lift above 2. We deliberately do not headline the mean holdout lift (28.1957) or the maximum training lift (128.4608): both are inflated by rare product-variant pairs with support around 0.5%, so they describe statistical rarity rather than commercial usefulness.

That is also the main caveat: many high-lift rules pair colour or size variants of the same item — the highest-lift rule, "23285 -> 23286", is a pair of beaker variants. For such near-duplicate items, lift is high because the baseline support of the consequent is tiny, not because the pair is a genuine cross-sell insight. Holdout lift is reported precisely to expose this, but it still overstates incremental cross-sell for variant pairs. The honest reading is that the raw rule set provides *candidate* cross-sell content; the business-filtered set behind Table 15, which contains 593 rules and whose top rule is GREEN REGENCY TEACUP AND SAUCER → ROSES REGENCY TEACUP AND SAUCER (support 3.4%, confidence 0.79, training lift 16.4, holdout lift 21.6), is the more defensible starting point.

### 7.4 From rules to cross-sell actions

Each retained rule becomes an operational action: when a customer in a prioritised segment buys the antecedent, the engine suggests the consequent. Two safeguards apply. Rules are filtered to those whose consequent is not already in the customer's history — recommending what someone owns wastes attention. And rules are matched to segments: a high-value frequent segment uses premium-basket rules, an occasional segment uses broadly supported rules. The recommendation is attached to the contact in the decision layer (§9), so the customer receives one coordinated action rather than a retention message and a separate product email. The limitation is causal: a rule shows that products are bought together, not that recommending one causes the other to be bought.

---

## 8. Similarity and Distance

### 8.1 Metric comparison

Distance-based methods are only as good as the metric and transform pair, so the distance is treated as a modelling decision with evidence. For **customers**, candidates are (a) the scaled continuous RFM and behavioural vector with Euclidean or Manhattan distance and (b) the binary purchase vector with cosine similarity. For **products**, the product-by-customer incidence matrix is compared with cosine and Jaccard. Table 16 compares the metrics on two pieces of evidence computed on the same K = 5 solution: the **silhouette** (cluster separation under each metric) and **kNN label agreement** (whether a 5-nearest-neighbour classifier trained on 70% of customers reproduces the K-means labels on the held-out 30%).

**Table 16.** Similarity-metric comparison: silhouette and kNN label agreement for each distance.

{{TABLE:t03_distance_metrics}}

{{FIGURE:f11_similarity_lookalikes}}

*Figure 11.* Similarity analysis: cosine-similarity heatmap for high-value customers with their lookalikes, and similar products under the selected metric.

The cosine representation has the highest silhouette (0.3283, against 0.1844 for Euclidean and 0.2183 for Manhattan), while label agreement is near-tied across the three metrics. We therefore adopt `cosine` — the separation advantage decides it, and the comparison is not cosmetic: Euclidean distance on untransformed monetary values is dominated by a few large spenders (hence log1p and scaling in §4.3), and cosine on binary vectors measures *what* a customer bought rather than how much, which is the right notion for lookalike audiences. Jaccard is stricter about set overlap and penalises large baskets, which is useful for products where co-occurrence counts are dominated by popular items.

### 8.2 Lookalike customers

For each customer we retrieve the nearest neighbours (excluding itself) under the selected representation. The file `t04_lookalikes.csv` lists the top five lookalikes for three high-value customers, including each neighbour's segment and similarity score, so the business can see what "looking alike" means in practice. Three uses follow. **Seed expansion:** given a seed set of high-value Champions, their lookalikes are acquisition or upsell candidates. **Cold-start scoring:** a new or sparse customer with one purchase gets a provisional segment from its neighbours before enough history exists for churn scoring. **Segment enrichment:** the share of a segment's neighbours that are Champions is a second signal of latent value, used when two customers have similar risk scores. The caveat is the curse of dimensionality: in a sparse high-dimensional purchase space every customer begins to look similar. We mitigate this by restricting the representation to selected features and binary purchase vectors, using a popularity-aware comparison, and validating that neighbour lists are not simply the most frequent buyers.

### 8.3 Similar products

For each stock code we retrieve the most similar products under the selected metric; `t05_similar_products.csv` lists the top five similar products for five popular items. These complement the association rules: rules require co-occurrence support and cannot say anything about long-tail products, whereas similarity still produces neighbours for a slow-moving item. The outputs support "complete the basket" suggestions, substitute discovery when a product is out of stock, and bundle construction for the retention offer. The methods are used together, not interchangeably: rules capture *validated co-purchase*, similarity captures *structural resemblance*.

### 8.4 What similarity does not tell us

A similar customer is not necessarily a responsive one, and a similar product is not necessarily a profitable bundle. Similarity describes the observed behaviour space; it becomes useful only when combined with the risk and value signals in the decision layer — which is why it is an enabler of the integrated framework rather than an end in itself.

---

## 9. Integrated Decision Framework

### 9.1 Segment × risk matrix and action table

The integration point is a matrix whose rows are the five T2 segments from §5, summarised with the average predicted churn probability from the T1-trained model applied to T2 (§6) and grouped into risk tiers (low, medium, high) at 0.30 and 0.50. Figure 12 shows the matrix as a bubble chart — average predicted churn probability against average monetary value (log scale), with bubble size equal to segment size — and Tables 17 and 18 give the underlying cells and the recommended actions. The matrix is the single view that answers the business question: it shows *where in the customer base* risk and value coincide.

{{FIGURE:f12_segment_risk_matrix}}

*Figure 12.* Segment × churn-risk matrix: average predicted churn probability against average monetary value (log y-axis), bubble size = segment size.

**Table 17.** Segment × risk matrix: size, average monetary value, average churn probability and risk tier.

{{TABLE:t12_segment_risk_matrix}}

**Table 18.** Action table: segment, recommended action, target count, expected churners and saves, gross benefit, campaign cost and net expected value.

{{TABLE:t13_action_table}}

### 9.2 Priority scoring

Within the matrix, customers are ranked by a transparent score:

> **priority = predicted churn probability × monetary value**,

where monetary value is the customer's spend in the feature window. Multiplying by value ensures that a slightly riskier low-value customer does not jump ahead of an at-risk high-value customer, so the ranking reflects *expected value at risk* rather than risk alone. The score is sorted and cut to campaign capacity. The multiplication is a deliberate simplification: it is readable, auditable and easy to challenge, which matters more for a decision-support tool than a black-box optimiser. The action assigned to each customer comes from the segment-level action table (Table 18); the priority score decides *whom* to contact first, the segment decides *what to say*.

### 9.3 The target list

The output is not a chart but a list: one row per customer with rank, segment, recency, frequency, monetary value, predicted churn probability, priority score, recommended action and expected net value. Table 19 is the capacity-bounded top-200 target list, the top 7.12% of the T2 cohort; the full list is regenerated by the notebook, and `t15_priority_list_summary.csv` gives the decile summary for the whole T2 cohort. The list never contains more customers than the campaign can contact, because an unconstrained list is a ranking, not a plan.

**Table 19.** Capacity-bounded priority target list: rank, segment, behaviour, predicted churn probability, priority score, action and expected net value.

{{TABLE:t11_top200_targets}}

### 9.4 ROI assumptions and expected value

The ROI model is deliberately explicit and modest, and it is **churn-conditional**: contacts are the highest-risk customers, so expected saves start from the predicted churn probability of the targeted group rather than the cohort base rate. The calculation is:

> expected churners = contacts × mean predicted churn probability of the targeted list;
> expected saves = expected churners × assumed save rate;
> expected gross benefit = expected saves × average monetary value × assumed margin;
> net expected value = expected gross benefit − contacts × contact cost.

The headline in this report is the **conservative validated variant**, which replaces the model's optimistic mean churn probability with the churn rate actually observed inside the value-weighted 200-customer priority list (0.31). On that basis the pilot is expected to save 6.2 customers, with a net expected value of GBP 14802.58 and an ROI of 925.16% (Table 20). The model-precision version — using the top-decile precision of 0.669 as the expected churn rate — gives a net expected value of GBP 33799.89 and an ROI of 2112.5; we report it as an **optimistic bound**, not as the headline. A random 200-customer campaign in the same base scenario gives a net expected value of only GBP 1925.76 (ROI 120.4%), so the model's value is the **net uplift of GBP 31874.13**, not the absolute ROI.

The three scenarios in Table 20 span save rate 5–15%, contact cost GBP 5–12 and margin 30–35%. Under the pessimistic scenario the targeted campaign still nets GBP 12771.38 (ROI 532.1%), while random targeting is negative; under the optimistic scenario it nets GBP 52099.83 (ROI 5210.0%). The targeted campaign breaks even at a save rate of 0.452%, compared with 4.538% for random targeting; the full targeted-versus-random comparison for all three scenarios is in `t16_targeting_comparison.csv`. **ROI is a scenario analysis, not measured uplift; the dataset contains no campaign history.** Every assumption is stated in Table 20 so that a finance reviewer can replace it, and Figure 13 shows how the conclusion moves across save rates and contact costs.

**Table 20.** ROI assumptions, values and rationale (base scenario, with the three-scenario comparison in `t16_targeting_comparison.csv`).

{{TABLE:t14_roi_assumptions}}

{{FIGURE:f13_roi_sensitivity}}

*Figure 13.* ROI sensitivity: net expected value across save rates and contact costs for the targeted top-200 campaign versus random targeting.

### 9.5 What the ROI number is not

The ROI is a **scenario**, not a forecast. It assumes the response rate is caused by the intervention; without a controlled experiment we cannot separate selection effects (we contact high-risk customers, who might have behaved differently anyway) from treatment effects. It uses segment-level expected value rather than individual lifetime value, ignores cannibalisation and offer-cost variation, and assumes out-of-time model performance transfers to the campaign period. Every assumption is stated in Table 20 so no reader mistakes the calculation for a measured return. The correct claim: the conservative validated figure is the defensible planning number, the 0.669-precision figure is an optimistic bound, and the next step is a randomised A/B test to estimate the save rate.

---

## 10. Interpretation, Limitations, Ethics and Future Work

### 10.1 What the results support

The evidence supports four careful claims. (i) The customer base is *segmentable*: a small number of behavioural groups explains a large share of revenue variation, and the solution is stable under resampling. (ii) Churn is *predictable at cohort level*: the models rank future churners well enough that the top decile contains far more churners than a random decile. (iii) Some co-purchase relationships are *stable across periods*, not only within the mining window. (iv) Combining these signals produces a *capacity-bounded, auditable action list*. None of these claims requires a causal interpretation, and none should be read as one.

### 10.2 Limitations

- **Anonymous-customer bias.** Identified customers cover only part of the revenue (13.572% of gross revenue is anonymous), and the excluded population may differ systematically. All customer-level rates describe identified customers only.
- **Label-window and seasonality effects.** The 90-day label is a business proxy, not observed attrition. T1 and T2 cover different seasons and therefore different base rates; T2's label window precedes the Christmas peak, so its churn rate is period-specific. A snapshot placed later than August 2011 would have a truncated label window before the data ends.
- **Single retailer, single market, one year.** Churn rates, rules and segment names do not transfer without refitting; the method transfers, the numbers do not.
- **No campaign or response data.** We predict inactivity, not treatment effect. The ROI is a churn-conditional scenario analysis: the conservative headline uses the realised churn rate of the priority list, the model-precision version is an optimistic bound, random targeting is only marginally positive and negative in the pessimistic scenario, and no measured uplift exists without an A/B test.
- **Descriptive clustering and in-sample labels.** Segments are fitted on T2 and assigned in-sample; they describe the decision cohort rather than predict future segment membership.
- **Association-rule lift is inflated by product variants.** Many high-lift rules pair colour or size variants of the same item, so lift overstates incremental cross-sell for those pairs.
- **Proxy features and a dropped recency variable.** RFM-style features proxy value and engagement rather than true lifetime value; `recency_days` was dropped by RFE and is only partly recovered by `distinct_months` and `avg_gap_days`.
- **Similarity and rule generalisation.** Rules depend on support thresholds and product mix; similarity suffers from sparsity and popularity bias. Both are descriptive, not causal.

### 10.3 Ethical and privacy considerations

The data contains no names, addresses or payment details, and `CustomerID` is a retailer-internal pseudonymous identifier. Even so, customer-level predictions are personal data in spirit: reporting is at segment and matrix level, small cells are not described individually, the priority list is an internal campaign tool, and no re-identification is attempted. The analysis uses no protected attributes, but country and purchasing behaviour can act as proxies, so campaigns should be reviewed for discriminatory targeting and customers should retain a clear opt-out. Where the retailer serves EU customers, GDPR principles of purpose limitation and data minimisation apply; in Hong Kong, the Personal Data (Privacy) Ordinance governs personal data. A production deployment would need a lawful basis, retention limits and human review before any contact.

### 10.4 What we would do with more data

(i) **Longer history and survival analysis** would model time-to-churn with censoring instead of a fixed 90-day label, giving a warning lead time. (ii) **Campaign data and uplift modelling** would replace the assumed response rate with an estimated incremental effect, turning the ROI scenario into a forecast. (iii) **Richer features** — product hierarchy, promotions, delivery experience, service contacts — would separate "left because of price" from "left because of a bad experience". (iv) **Graph or embedding representations** of customer–product interactions would improve cold-start similarity. With a longer horizon we would monitor drift, retrain on a rolling window, and test the priority list in a randomised holdout.

---

## 11. Contribution Statement

Five members delivered the project with clearly separated ownership. Table 21 maps each member to rubric items, code and report areas, and slides. The fuller statement, including commit areas and the requirement of meaningful commits and a personal agent trajectory, is in `CONTRIBUTIONS.md`.

**Table 21.** Individual contributions and rubric ownership. Names and student IDs are listed in the table below.

| Member | Primary role | Rubric items owned (22% rubric) | Code and artifact areas | Report sections | Slides |
|---|---|---|---|---|---|
| Patten Lai (4001777) | Data and quality lead | Collect/load data, handle missing and noisy data (LO5); visualisation | Data audit, cleaning funnel, snapshots; `t02_data_quality_issues`, `t03_cleaning_decisions`, `f01_data_quality_overview` | §2, Appendix A | 4–6, 18 |
| Weng Zhi Chao (4589896) | Feature engineering and segmentation lead | Feature selection (LO5); feature transformation (LO5); visualisation | 16 features, selection funnel, K-means; `t04_feature_dictionary`, `t05_feature_selection`, `t06_cluster_metrics`, `t07_segment_profiles`, `f02`–`f08` | §4–§5 | 8–10 |
| Lim Man Tung Marcus (4592996) | Churn modelling and evaluation lead | Learn models (LO4); evaluate performance (LO6) | Three classifiers, CV, held-out and out-of-time evaluation, thresholds, lift; `t08_model_metrics`, `t09_lift_deciles`, `f07`–`f09` | §6 | 11–13 |
| Huang Hao Lin (4455930) | Association rules and similarity lead | Apply different data-mining techniques (LO3) | FP-Growth and holdout validation, metric comparison, lookalikes, similar products; `t03_distance_metrics`, `t04_lookalikes`, `t05_similar_products`, `t09_top_rules`, `t10_association_rules`, `f10`, `f11` | §7–§8 | 14–15 |
| LIN Xiaotong (4589755) | Integration, decision framework and repository lead | Problem definition; solution design; interpretation (LO7); deliver models; presentation and repository compliance | Segment × risk matrix, priority list, ROI, README, agent-trajectory templates; `t12`, `t13`, `t11`, `t15`, `f12`, `f13` | §1, §3, §9–§10, §13 | 1–3, 7, 16–17, 19–20 |

Each member also writes and verifies their own sections, commits to their own files or branch so the GitHub history reflects the workload, and maintains a personal trajectory under `agent-trajectories/` (§12). Workload is assessed from commits and trajectories, and ownership is structured so every member has substantive, visible work in both.

---

## 12. Agent Usage and Verification

### 12.1 How the project was built

AI agents were accelerators, not authors. Every interaction followed the workflow recommended in the course and documented in our logs: **human defines the problem → agent proposes a plan → human reviews the plan → agent implements or analyses → human verifies the output → revise and repeat**. The gate that matters is the fourth arrow: no agent output entered the report, notebook or slides without a named human review.

| Activity | Human-led | Agent-assisted | Human verification |
|---|---|---|---|
| Problem framing, method choice | All members | Drafting alternatives | Team review against the rubric |
| Data audit and cleaning rules | Patten Lai | Profiling code, candidate rules | Rule-by-rule review; counts re-derived |
| Feature definitions and transforms | Weng Zhi Chao | Implementation, plots, checks | Distribution and leakage assertions inspected |
| Model training and evaluation | Lim Man Tung Marcus | Scaffolding, CV harness, plots | Independent re-run; metrics recomputed |
| Rules and similarity | Huang Hao Lin | Mining, holdout and neighbour code | Holdout numbers cross-checked against the rule table |
| Decision layer and ROI | LIN Xiaotong | Scenario table and sensitivity code | Assumption audit; arithmetic checked independently |
| Writing and editing | All members | Drafting and consistency checks | Every number checked against `metrics.json` |

### 12.2 How agent outputs were verified

Six checks were applied, with evidence in the per-member trajectories:

1. **Independent re-execution.** The notebook is run from a fresh kernel (`Restart & Run All`, or `jupyter nbconvert --execute`) and its outputs compared with committed figures and tables. A result that reproduces only in the agent's session is not accepted.
2. **Independent recomputation.** For each headline number, a member recomputed the quantity with a short, separately written check — for example, recomputing a churn rate from the cleaned line items for one snapshot, or the row count after cleaning — and compared it with the pipeline value.
3. **Code review of agent diffs.** Every agent-authored diff is read before merge, checking for hard-coded numbers, silent exception handling, accidental use of future transactions, and transforms fitted on full data.
4. **Cross-artifact consistency.** Figures are checked against the tables they illustrate (axes, category order, counts) and tables against `metrics.json`; a discrepancy means a defect, not a rounding difference.
5. **Adversarial review.** Each member prompted an agent to attack the evaluation ("how could this lift be optimistic?"), and the objections were fixed or written into the limitations — the product-variant caveat on rule lift is one result of this review.
6. **Reproducibility check.** Seeds are fixed, splits deterministic, environment pinned in `requirements.txt`; a second machine reproduces the same metrics.

### 12.3 Kept and rejected outputs

The logs record rejected proposals, because that is what demonstrates human judgement. Typical rejections included over-engineered models the data could not support, metrics that would have overstated performance (accuracy on an imbalanced label; lift computed on the test set rather than held out), and cleaning rules that silently dropped most of the data without reporting it. Agent-generated text was edited for accuracy; agent-generated code was retained only after review and a successful re-run. `agent-trajectories/` contains a README explaining the evidence standard, a per-person template and a filled example; each member keeps `agent-logs/MemberX_agent-trajectory.md`.

---

## 13. Reproducibility

The project runs on Python 3 with the libraries in `requirements.txt` (pandas, numpy, scipy, scikit-learn, mlxtend, matplotlib, seaborn, openpyxl and Jupyter). A single global seed (42) controls train/validation/test splits, cross-validation folds, K-means initialisation, bootstrap resamples and tree ensembles; the notebook sets `numpy` and `random` seeds at start-up and records library versions. The data file is not modified: `data/Online_Retail.xlsx` is the raw UCI download and all cleaning is code. The executed notebook runs in 27.5 seconds on the development machine, well inside the ten-minute target.

To reproduce: (1) run `python data/download_data.py` or download the UCI Online Retail `.xlsx` to `data/Online_Retail.xlsx`; (2) `pip install -r requirements.txt`; (3) `jupyter nbconvert --to notebook --execute --inplace notebooks/CDS3004_Project.ipynb` (equivalent to Restart & Run All); (4) the run regenerates every figure and table in `results/` plus `results/metrics.json`, `results/metrics_extra.json`, `results/metrics_summary.md` and `results/ARTIFACTS.md`. In Google Colab the notebook installs `mlxtend` automatically if it is missing.

```text
cds3004-project/
├── README.md, CONTRIBUTIONS.md
├── data/{Online_Retail.xlsx, README.md, download_data.py}
├── notebooks/CDS3004_Project.ipynb      # sections S0-S9, executed in place
├── code/{make_notebook.py, pipeline_notes.md}
├── results/{figures/, tables/, metrics.json, metrics_extra.json, metrics_summary.md, ARTIFACTS.md}
├── report/REPORT.md
├── slides/SLIDES.md
├── submission/SUBMISSION-CHECKLIST.md
└── agent-logs/
```

Results are deterministic given the seed and library versions, with two exceptions: floating-point differences can move a metric in the last decimal place across operating systems, and tree-ensemble results can differ slightly across scikit-learn versions. The committed `metrics.json` is the reference for every number reported here.

---

## References

Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5–32.

Chen, D., Sain, S. L., & Guo, K. (2012). Data mining for the online retail industry: A case study of RFM model-based customer segmentation using data mining. *Journal of Database Marketing & Customer Strategy Management*, 19(3), 197–208.

Han, J., Kamber, M., & Pei, J. (2011). *Data Mining: Concepts and Techniques* (3rd ed.). Morgan Kaufmann.

Hubert, L., & Arabie, P. (1985). Comparing partitions. *Journal of Classification*, 2(1), 193–218.

Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics*, 20, 53–65.

UCI Machine Learning Repository. *Online Retail Data Set*. https://archive.ics.uci.edu/dataset/352/online+retail

---

## Appendix A. Rubric Coverage

The 22% project rubric has eleven items worth roughly 2% each; the presentation rubric (8%) is mapped slide-by-slide in `slides/SLIDES.md`.

| # | Rubric item (22%) | Where addressed | Artifact / evidence |
|---|---|---|---|
| 1 | Problem definition: clear problem, constraints, alternative solutions | §1.1–§1.3; Table 1 | Business question, four framings, success criteria |
| 2 | Solution design: related to problem, explained approaches, innovative integration | §3.1–§3.3; Tables 5–6 | Ten-section pipeline S0–S9, integration rationale, method-fit table |
| 3 | Collect/load datasets, feature characteristics, handle missing and noisy data (LO5) | §2.1–§2.5; Tables 2–4; Figure 1 | Schema, audit, sequential cleaning funnel, bias caveat |
| 4 | Apply data-mining techniques to select relevant features (LO5) | §4.4; Table 9; Figure 3 | Correlation filter, mutual information, RFE, validation PR-AUC, permutation importance |
| 5 | Advanced feature transformations (LO5) | §4.2–§4.3; Table 8; Figure 2 | Feature families, log1p, scaling, momentum and return features, leakage control |
| 6 | Data visualisation (LO5) | §5.3–§5.4, §6.3–§6.6, §7.2, §8.1, §9.1; Figures 1–13 | Diagnostics, profiles, ROC/lift, rules, similarity, matrix, sensitivity |
| 7 | Apply different data-mining techniques for various data (LO3) | §5–§9 | Clustering, classification, association rules, similarity, decision layer |
| 8 | Use data-mining techniques to learn models from data (LO4) | §5.1, §6.2, §7.1 | K-means, three classifiers, FP-Growth setups |
| 9 | Evaluate model performance with cross-validation, nested validation and separations (LO6) | §4.5, §6.1–§6.5; Tables 12–13; Figures 7–9 | 5-fold CV, 70/15/15 split, held-out T1, out-of-time T2, thresholds, lift |
| 10 | Interpret results correctly and critically (LO7) | §5.5, §6.6, §7.3, §9.5, §10.1–§10.2 | Interpretation, error analysis, product-variant and recency caveats, limitations |
| 11 | Deliver learnt models for decision making, with sound decisions (LO7) | §9.1–§9.5; Tables 17–20; Figures 12–13 | Segment × risk matrix, priority list, ROI assumptions and sensitivity |

## Appendix B. Artifact Inventory

All artifacts are regenerated by the notebook; `results/ARTIFACTS.md` is the authoritative file index. The figures and tables below are the ones embedded in the text; the remaining files are supporting evidence.

| Artifact | File | Used in |
|---|---|---|
| Table 2 | `t01_dataset_schema` | §2.1 |
| Table 3 | `t02_data_quality_issues` | §2.3 |
| Table 4 | `t03_cleaning_decisions` | §2.4 |
| Table 7 | `t02_cohort_summary` | §4.1 |
| Table 8 | `t04_feature_dictionary` | §4.2 |
| Table 9 | `t05_feature_selection` | §4.4 |
| Table 10 | `t06_cluster_metrics` | §5.2 |
| Table 11 | `t07_segment_profiles` | §5.3 |
| Table 12 | `t08_model_metrics` | §6.3–§6.4 |
| Table 13 | `t09_lift_deciles` | §6.5 |
| Table 14 | `t09_top_rules` | §7.2 |
| Table 15 | `t10b_business_rules` | §7.2–§7.3 |
| Table 16 | `t03_distance_metrics` | §8.1 |
| Table 17 | `t12_segment_risk_matrix` | §9.1 |
| Table 18 | `t13_action_table` | §9.1 |
| Table 19 | `t11_top200_targets` | §9.3 |
| Table 20 | `t14_roi_assumptions` | §9.4 |
| Figure 1 | `f01_data_quality_overview` | §2.3 |
| Figure 2 | `f02_feature_distributions` | §4.3 |
| Figure 3 | `f08_feature_importance` | §4.4, §6.6 |
| Figure 4 | `f04_elbow_silhouette` | §5.2 |
| Figure 5 | `f05_segment_profiles` | §5.3 |
| Figure 6 | `f06_cluster_pca` | §5.4 |
| Figure 7 | `f07_cv_model_comparison` | §6.3 |
| Figure 8 | `f08_roc_test_oot` | §6.4 |
| Figure 9 | `f09_lift_curve` | §6.5 |
| Figure 10 | `f10_association_rules` | §7.2 |
| Figure 11 | `f11_similarity_lookalikes` | §8.1 |
| Figure 12 | `f12_segment_risk_matrix` | §9.1 |
| Figure 13 | `f13_roi_sensitivity` | §9.4 |
| Supporting only | `f02_correlation_heatmap`, `f07_pr_and_lift_curve`, `f09_confusion_and_threshold`, `t05b_feature_evidence`, `t04_lookalikes`, `t05_similar_products`, `t10_association_rules`, `t10_decision_table`, `t15_priority_list_summary`, `t16_targeting_comparison`, `s06_permutation_importance`, `s06_threshold_analysis` | §4.4, §6.5–§6.6, §7.2, §8.2–§8.3, §9.4 |

Several alias files also exist for convenience, but the report and slides use only the canonical names above.
