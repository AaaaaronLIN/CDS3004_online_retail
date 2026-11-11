# Internal fill notes — placeholders, values and manual fields

**Do not include this file in the submitted PDF report or the ZIP report folder.** It is an internal working note for the final number-fill step. The public deliverables are `report/REPORT.md`, `slides/SLIDES.md`, `README.md`, `CONTRIBUTIONS.md`, `submission/SUBMISSION-CHECKLIST.md` and `agent-logs/*`.

## 1. What the fill step must do

1. Read `results/metrics.json`, `results/metrics_extra.json` and `results/metrics_summary.md`.
2. Replace every `METRIC` token with the exact value at that JSON path; replace every `EXTRA` token from `metrics_extra.json`. Format percentages as 0–100, rates/margins as 0–1, currency as GBP, and keep the units used in the surrounding sentence.
3. Replace every figure marker with the corresponding PNG from `results/figures/` and every table marker with the markdown rendering of the CSV from `results/tables/` (canonical names below).
4. Fill the manual fields in §5 (group ID, member names/IDs, repository URL).
5. Re-read the report for contradictions, then verify: `grep -R "{{" report/ slides/ README.md` returns nothing; no `[GROUP-ID]`/`<repository>` remains in the exported PDF; every number matches `metrics.json`.

## 2. Verification performed now (reconciliation pass)

- Placeholder tokens found in the three documents: **64 unique keys** across REPORT.md, SLIDES.md and README.md.
- Tokens whose path does not resolve in the current JSON files: **0**
- Every token below was resolved against the actual `results/metrics.json` / `results/metrics_extra.json` at the time of writing, so the fill step should be mechanical.

## 3. METRIC tokens — `results/metrics.json`

| Key | Format | Meaning | Used in | Current value (sanity check) |
|---|---|---|---|---|
| `association_rules.max_lift` | multiplier | Max training lift | report/REPORT.md | 128.4608 |
| `association_rules.mean_holdout_lift` | multiplier | Mean holdout lift | report/REPORT.md, slides/SLIDES.md | 28.1957 |
| `association_rules.n_rules` | integer | Rules retained after pruning | report/REPORT.md, slides/SLIDES.md | 5441 |
| `association_rules.n_rules_holdout_evaluated` | integer | Rules evaluated on holdout | report/REPORT.md, slides/SLIDES.md | 5402 |
| `association_rules.top_rule` | string | Top rule, "A -> B" | report/REPORT.md | 23285 -> 23286 |
| `best_model` | string | Selected model (logreg / decision_tree / random_forest) | report/REPORT.md | logreg |
| `clustering.ari_stability` | metric 0-1 | Bootstrap stability ARI at chosen K | README.md, report/REPORT.md, slides/SLIDES.md | 0.9699 |
| `clustering.k` | integer | Chosen number of segments | README.md, report/REPORT.md, slides/SLIDES.md | 5 |
| `clustering.silhouette` | metric 0-1 | Mean silhouette at chosen K | README.md, report/REPORT.md, slides/SLIDES.md | 0.3279 |
| `cohorts.T1.churn_rate` | fraction 0-1 | T1 churn rate | report/REPORT.md | 0.5044 |
| `cohorts.T1.n` | integer | T1 cohort customers | report/REPORT.md | 2716 |
| `cohorts.T2.churn_rate` | fraction 0-1 | T2 out-of-time churn rate | report/REPORT.md | 0.3955 |
| `cohorts.T2.n` | integer | T2 cohort customers | report/REPORT.md | 2809 |
| `data_quality.missing_customerid_pct` | percent 0-100 | Share of raw lines without CustomerID | report/REPORT.md, slides/SLIDES.md | 24.9267 |
| `data_quality.revenue_retained_pct` | percent 0-100 | Share of raw revenue retained | report/REPORT.md | 81.9114 |
| `data_quality.rows_retained_pct` | percent 0-100 | Share of raw lines retained | report/REPORT.md | 72.18 |
| `decision.assumed_cost_per_contact` | GBP | Assumed contact cost | report/REPORT.md | 8.0 |
| `decision.n_targets` | integer | Pilot campaign capacity / target list size | README.md, report/REPORT.md, slides/SLIDES.md | 200 |
| `decision.net_expected_value` | GBP | Pilot campaign net expected value | README.md, report/REPORT.md, slides/SLIDES.md | 33799.89 |
| `feature_selection.n_features_all` | integer | Engineered features before selection | report/REPORT.md, slides/SLIDES.md | 16 |
| `feature_selection.n_features_selected` | integer | Features after selection | slides/SLIDES.md | 10 |
| `feature_selection.val_pr_auc_all` | metric 0-1 | Validation PR-AUC, all features | report/REPORT.md | 0.6966 |
| `feature_selection.val_pr_auc_selected` | metric 0-1 | Validation PR-AUC, selected features | report/REPORT.md | 0.7036 |
| `meta.date_max` | YYYY-MM-DD | Last invoice date | report/REPORT.md | 2011-12-09 |
| `meta.date_min` | YYYY-MM-DD | First invoice date | report/REPORT.md | 2010-12-01 |
| `meta.n_customers` | integer | Identified customers in the clean base | README.md, report/REPORT.md | 4334 |
| `meta.n_rows_clean` | integer | Cleaned line-item count | README.md, report/REPORT.md | 391150 |
| `meta.runtime_sec` | seconds | Notebook end-to-end runtime | README.md, report/REPORT.md | 27.5 |
| `models.T1_test.logreg.auc` | metric 0-1 | ROC-AUC, logistic regression, T1 held-out test | report/REPORT.md | 0.7227 |
| `models.T1_test.logreg.lift10` | multiplier | top-decile lift, logistic regression, T1 held-out test | report/REPORT.md | 1.3526 |
| `models.T1_test.logreg.pr_auc` | metric 0-1 | PR-AUC, logistic regression, T1 held-out test | report/REPORT.md | 0.6744 |
| `models.T1_test.logreg.top10_precision` | metric 0-1 | top-decile precision, logistic regression, T1 held-out test | report/REPORT.md | 0.6829 |
| `models.T1_test.logreg.top10_recall` | metric 0-1 | top-decile recall, logistic regression, T1 held-out test | report/REPORT.md | 0.1359 |
| `models.T2_oot.logreg.auc` | metric 0-1 | ROC-AUC, logistic regression, T2 out-of-time | README.md, report/REPORT.md, slides/SLIDES.md | 0.7392 |
| `models.T2_oot.logreg.lift10` | multiplier | top-decile lift, logistic regression, T2 out-of-time | README.md, report/REPORT.md, slides/SLIDES.md | 1.6916 |
| `models.T2_oot.logreg.pr_auc` | metric 0-1 | PR-AUC, logistic regression, T2 out-of-time | report/REPORT.md | 0.5947 |
| `models.T2_oot.logreg.top10_precision` | metric 0-1 | top-decile precision, logistic regression, T2 out-of-time | report/REPORT.md | 0.669 |
| `models.T2_oot.logreg.top10_recall` | metric 0-1 | top-decile recall, logistic regression, T2 out-of-time | report/REPORT.md | 0.1692 |
| `models.T2_oot.random_forest.auc` | metric 0-1 | ROC-AUC, random forest, T2 out-of-time | report/REPORT.md | 0.7323 |
| `similarity.best_metric` | string | Selected distance metric | report/REPORT.md, slides/SLIDES.md | cosine |
| `similarity.silhouette_cosine` | metric 0-1 | Silhouette, cosine | report/REPORT.md | 0.3283 |
| `similarity.silhouette_euclidean` | metric 0-1 | Silhouette, Euclidean | report/REPORT.md | 0.1844 |
| `similarity.silhouette_manhattan` | metric 0-1 | Silhouette, Manhattan | report/REPORT.md | 0.2183 |

## 4. EXTRA tokens — `results/metrics_extra.json`

| Key | Format | Meaning | Used in | Current value (sanity check) |
|---|---|---|---|---|
| `association_rules.n_excluded_no_antecedent` | integer | Rules excluded: antecedent absent from holdout | report/REPORT.md | 27 |
| `association_rules.n_excluded_no_consequent` | integer | Rules excluded: consequent absent from holdout | report/REPORT.md | 12 |
| `clustering.pca_variance_pc1` | proportion 0-1 | PCA variance, PC1 | report/REPORT.md | 0.3647 |
| `clustering.pca_variance_pc2` | proportion 0-1 | PCA variance, PC2 | report/REPORT.md | 0.1506 |
| `data.anonymous_revenue_share_pct` | percent 0-100 | Anonymous line revenue share | README.md, report/REPORT.md, slides/SLIDES.md | 13.572 |
| `decision.campaign_capacity_pct` | percent 0-100 | Target list as share of T2 | report/REPORT.md, slides/SLIDES.md | 7.12 |
| `decision.cost_total` | GBP | Pilot campaign total cost | report/REPORT.md | 1600.0 |
| `decision.roi_pct` | percent 0-100 | Pilot campaign ROI | report/REPORT.md | 2112.5 |
| `decision.segment_expected_value_total` | GBP | Whole-base campaign expected value | report/REPORT.md | 36834.23 |
| `decision.segment_net_total` | GBP | Whole-base campaign net expected value | report/REPORT.md, slides/SLIDES.md | 14362.23 |
| `feature_selection.n_after_corr` | integer | Features after correlation filter | report/REPORT.md | 15 |
| `feature_selection.n_after_mi` | integer | Features after mutual information | report/REPORT.md | 12 |
| `feature_selection.n_after_rfe` | integer | Features after RFE | report/REPORT.md | 10 |
| `models_cv.decision_tree.auc_mean` | metric 0-1 | CV mean ROC-AUC, decision tree | report/REPORT.md | 0.7397 |
| `models_cv.decision_tree.auc_std` | metric 0-1 | CV std ROC-AUC, decision tree | report/REPORT.md | 0.0179 |
| `models_cv.logreg.auc_mean` | metric 0-1 | CV mean ROC-AUC, logreg | report/REPORT.md | 0.7593 |
| `models_cv.logreg.auc_std` | metric 0-1 | CV std ROC-AUC, logreg | report/REPORT.md | 0.0217 |
| `models_cv.random_forest.auc_mean` | metric 0-1 | CV mean ROC-AUC, random forest | report/REPORT.md | 0.7505 |
| `models_cv.random_forest.auc_std` | metric 0-1 | CV std ROC-AUC, random forest | report/REPORT.md | 0.022 |
| `thresholds.capacity_threshold_test` | probability 0-1 | Top-10% capacity threshold (T1 test scores) | report/REPORT.md | 0.7382 |
| `thresholds.f1_optimal_threshold` | probability 0-1 | Validation F1-optimal threshold | report/REPORT.md | 0.2665 |

## 5. Manual fields (not in the pipeline)

- `[GROUP-ID]` and member names/student IDs: title page and Table 20 of REPORT.md; CONTRIBUTIONS.md; agent-logs files; slides.
- Public repository URL: REPORT.md title page and README.md (`https://github.com/AaaaaronLIN/CDS3004_online_retail`).
- Presentation duration and PPT deadline: confirm with the course announcement/TA (assumed 10 min + Q&A and 2026-11-19).
- Agent trajectory links: `agent-logs/LINKS.md` and each `agent-logs/MemberX_agent-trajectory.md`; replace `[commit]` tokens in EXAMPLE_member1.md with real hashes.

## 6. Canonical artifact markers used in the documents

Figures: f01_data_quality_overview, f02_feature_distributions, f04_elbow_silhouette, f05_segment_profiles, f06_cluster_pca, f07_cv_model_comparison, f08_feature_importance, f08_roc_test_oot, f09_lift_curve, f10_association_rules, f11_similarity_lookalikes, f12_segment_risk_matrix, f13_roi_sensitivity

Tables: t01_dataset_schema, t02_cohort_summary, t02_data_quality_issues, t03_cleaning_decisions, t03_distance_metrics, t04_feature_dictionary, t05_feature_selection, t06_cluster_metrics, t07_segment_profiles, t08_model_metrics, t09_lift_deciles, t09_top_rules, t11_top200_targets, t12_segment_risk_matrix, t13_action_table, t14_roi_assumptions

Rule: use the canonical (non-alias) file names from `results/ARTIFACTS.md`. Alias files exist for convenience but should not be introduced into new text.

## 7. Post-fill acceptance checks

- [ ] Zero `{{` characters remain in report, slides and README.
- [ ] Every inserted figure renders at a sensible size; captions still match the content (for example the segment × risk matrix is a bubble chart, not a heatmap).
- [ ] Every inserted table keeps its caption and column meaning; the top-rules table is `t09_top_rules` (top 10), not the full `t10_association_rules`.
- [ ] No authoring-only text (draft notes, placeholder indexes, "replace before export") remains in the PDF.
- [ ] Numbers in the abstract, report, slides and README agree with each other and with `results/metrics.json`.

## 8. Fill status — COMPLETE

- Date of fill: 2026-11-11 (final pipeline run, nbconvert exit 0).
- All `METRIC` and `EXTRA` tokens in `report/REPORT.md`, `slides/SLIDES.md` and `README.md` were resolved from `results/metrics.json` (with the `report` block taking precedence) and `results/metrics_extra.json`. Remaining unresolved tokens: **0**.
- Artifact markers (`FIGURE` / `TABLE`) in REPORT.md are intentionally left for the PDF/PPT export step, which embeds the PNGs and renders the CSVs. Canonical filenames are listed in §6.
- The fill was verified mechanically: every token resolves, every inserted value matches the JSON exactly (no rounding or hand entry), and no pre-fill placeholder remains in the three public documents.
- Note: the conservative validated ROI variant (net GBP 14,802.58, ROI 925.16%) leads the report and slides; the model-precision figure (GBP 33,799.89 / 2,112.5%) is labelled an optimistic bound; random-200 baseline GBP 1,925.76 and uplift GBP 31,874.13 are reported alongside. Association rules lead with median holdout lift 12.17 (not the inflated mean 28.20).
