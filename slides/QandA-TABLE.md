# Q&A Table — CDS3004 Group F (20-minute talk, Q&A after)

> Use this for rehearsal. Each answer is 20–40 seconds. The "Owner" column decides who speaks first; others can add one sentence.
> Rule: if nobody knows, the Host says *"We did not test that; we will follow up after the session"* — never improvise a number.

## A. Data (owner: Patten Lai)

| # | Likely question | Answer points | Evidence |
|---|---|---|---|
| A1 | Why did you drop 24.9% of lines with no customer ID? Isn't that throwing away data? | Can't link anonymous lines across visits, so no customer feature/label/segment can be defined. We audited them and quantified the cost: 13.57% of gross revenue. Conclusions describe identified customers only. | t02_data_quality_issues, report §2 |
| A2 | Why not build a separate model for guest buyers? | Guest rows have no identity and no repeat-purchase label — a model would be aggregate demand forecasting, a different project. We list it as future work. | report §2.5, §10 |
| A3 | How do you know cleaning did not bias the results? | Every rule is counted and applied identically to T1 and T2; no rule uses the churn label. We report retained rows/revenue (72.2%/81.9%) and state the anonymity bias. | t03_cleaning_decisions |
| A4 | Why is 90 days the churn horizon? | Matches a 1–3 month buying cycle; shorter over-labels loyal customers, longer censors more of the label window. It is a lapsing proxy, not cancellation. | report §4.1 |
| A5 | Is 2,716 / 2,809 customers enough? | For customer-level tabular models, yes: CV AUC standard deviations are ~0.02, so larger differences are meaningful. We also report one out-of-time period and say it cannot estimate quarter-to-quarter variance. | metrics_extra models_cv |
| A6 | What is the single biggest weakness of the data? | No campaign-response history, so we cannot measure uplift, only rank risk; and the anonymity share means the customer view under-represents guest demand. | report §10 |

## B. Features and segmentation (owner: Weng Zhi Chao)

| # | Likely question | Answer points | Evidence |
|---|---|---|---|
| B1 | Why K=5 when silhouette is highest at K=2? | Pre-registered rule: among K=4–6 require every segment ≥10% and silhouette ≥0.30, then maximise bootstrap stability. K=5: ARI 0.9699, five actionable tiers; K=2 too coarse, K=4 less stable. We never claimed silhouette was maximised. | t06_cluster_metrics |
| B2 | Are the segments stable if the data refreshes? | Bootstrap ARI 0.9699 at K=5; segment names are assigned by RFM rank in code, so they reproduce. | t06, notebook S5 |
| B3 | Why log1p and scaling? | Spend is heavy-tailed; distance-based methods would be dominated by a few large customers. log1p compresses, z-scoring equalises units. | report §4.3 |
| B4 | The feature-selection gain is tiny (0.6966 → 0.7036). Why bother? | Because it is measured, not assumed: the smaller set is cheaper to maintain and slightly better on validation. We report the honest number rather than exaggerating. | t05b_feature_evidence |
| B5 | Why was recency dropped by RFE? | It is largely redundant with distinct_months and avg_gap_days in this feature set; RFE with logistic regression removed it while validation PR-AUC improved. | report §4.4 |
| B6 | Why cosine for clustering? | Silhouette 0.3283 vs 0.2183 Manhattan and 0.1844 Euclidean, with near-tied kNN agreement. Cosine suits sparse, high-dimensional behaviour vectors. | t11_similarity_metric_comparison |

## C. Churn model and evaluation (owner: Lim Man Tung Marcus)

| # | Likely question | Answer points | Evidence |
|---|---|---|---|
| C1 | Why logistic regression and not random forest? | Selection used validation PR-AUC only: 0.7079 vs 0.6683. Test and out-of-time performance are near-tied (0.7227/0.7216; 0.7392/0.7323). With tied accuracy we choose the explainable model. | t08_model_metrics |
| C2 | AUC 0.74 — is that good? | Moderate but useful for tabular churn; the business metric is ranking, and top-decile lift is 1.69×. We do not oversell the absolute AUC. | t09_lift_deciles |
| C3 | Why PR-AUC instead of accuracy? | Churn is the minority class and the action is top-K contact; accuracy would be ~50% by predicting "nobody churns". PR-AUC and lift reflect ranking quality. | report §6 |
| C4 | Why two thresholds? | F1-optimal (0.267) and campaign-capacity / top-10% (0.738) answer different questions; the campaign team budgets contacts, not probabilities. | f09, report §6.5 |
| C5 | How do you know there is no leakage? | Features use only data before the as-of date; labels only the next 90 days; all transforms and selection are fitted inside pipelines on training folds; T2 is opened once. | notebook S2, report §4.5 |
| C6 | What does out-of-time change? | It removes the optimism of same-period CV: T2 churn base rate differs (39.6% vs 50.4%) and AUC still holds at 0.739 — the number we quote to a sponsor. | report §6.4 |
| C7 | What about false negatives? | At the F1 threshold the model trades missed churners against wasted contacts; the threshold is a budget decision, and we show the trade-off curve. | f09 |

## D. Association rules and similarity (owner: Huang Hao Lin)

| # | Likely question | Answer points | Evidence |
|---|---|---|---|
| D1 | Many high-lift rules are colour variants — isn't that trivial? | Yes, and we do not headline the mean lift (28.2). We report median holdout lift 12.17, replication 99.8%, and a business filter of 593 rules with support ≥1% and lift ≥2. | t10, t10b |
| D2 | Are the rules validated out of sample? | Mined on Dec 2010–Jul 2011, re-tested on Aug–Dec 2011 that the miner never saw; 5,402 of 5,441 were evaluable, rest excluded and counted. | t10_association_rules |
| D3 | Do rules imply causation? | No — co-purchase, not "recommending A causes B". We present them as candidate cross-sell bundles to be A/B tested. | report §7.4 |
| D4 | Why cosine for similarity? | Best cluster separation (0.3283) and natural for sparse behaviour vectors; used for lookalike customers and item–item similarity. | t11 |
| D5 | What is similarity actually used for? | Cold-start and sparse customers (nearest established customers' segment/offer as a prior) and substitution/bundle candidates for products. | t04_lookalikes, t05_similar_products |

## E. Decision layer, ROI and business value (owner: LIN Xiaotong)

| # | Likely question | Answer points | Evidence |
|---|---|---|---|
| E1 | Why contact only 200 customers? | It is a pilot capacity, 7.1% of T2; the threshold is capacity-bounded, and the framework works for any contact budget (we show the sensitivity). | t13_action_table |
| E2 | The ROI looks very high — defend it. | We lead with the conservative validated net GBP 14,802.58 using the realised 0.31 churn rate in the list, label GBP 33,799.89 as an optimistic bound, and show the random baseline GBP 1,925.76. Break-even save rate is 0.452% vs 4.538%. It is a scenario, not measured uplift. | t16_targeting_comparison |
| E3 | How sensitive is the decision to assumptions? | We ran pessimistic/base/optimistic scenarios and a break-even calculation; the decision survives because break-even is far below plausible save rates. | t16, f13 |
| E4 | What is the model's value over random targeting? | GBP 31,874.13 uplift at base assumptions; the model's contribution is prioritisation, not prediction accuracy. | metrics_extra decision |
| E5 | What would you actually do on Monday? | Send the 200-customer priority list to CRM with segment actions and matched cross-sell rules; run a randomised holdout to measure uplift. | t13, report §9 |
| E6 | Why is ROI a scenario, not measured? | The dataset has no campaign/response history. We state the assumption set explicitly and give a sensitivity curve. | report §9.4, §10 |

## F. Method, alternatives and process (owner: host + all)

| # | Likely question | Answer points | Evidence |
|---|---|---|---|
| F1 | Why integrate four techniques instead of doing one well? | Each answers a different decision question; the integration ends in an action list. We compared RFM-only, CLV regression and basket-only framings and rejected each as standalone. | report §1.3 |
| F2 | Why not deep learning / why no SHAP? | 2.7k-row tabular data at AUC ~0.74: complexity would not add measurable value and would hurt explainability. Permutation importance already gives model-agnostic drivers. | report §3.3, §4.4 |
| F3 | Would this generalise to another retailer? | Method yes (temporal snapshots, dual cohort, capacity thresholds); numbers no — single retailer, single year. We propose a second dataset. | report §10 |
| F4 | How is the work divided, and who did what? | Five module owners (data, features/segmentation, churn/evaluation, rules/similarity, decision/repo), each with commits and a personal agent trajectory. | CONTRIBUTIONS.md, agent-trajectories/ |
| F5 | How did you use AI? | DeepSeek Harness as an accelerator under the course's human–agent loop; each member re-ran and verified their module, rejected or rewrote several agent suggestions, and recorded a trajectory. | report §12 |

## G. Hostile / curveball questions (owner: decide on the spot)

| # | Question | Safe answer |
|---|---|---|
| G1 | "What is the single most important number in this talk?" | The out-of-time top-decile lift, 1.69× — it is the only number that combines honest validation with a business action. |
| G2 | "If the model is wrong, what breaks first?" | The high-value At-risk segment: few customers, large spend, high churn. That is why the priority list surfaces them first. |
| G3 | "Did you tune on the test set?" | No. Hyper-parameters and the model were chosen on validation PR-AUC; the test set and T2 were used once, for reporting. |
| G4 | "Can you show the code?" | Yes — notebook section referenced by each slide's source line; the repository is public. |
| G5 | "What would you do with one more week?" | Run a randomised pilot with campaign-response capture, add calibration and drift monitoring, and validate on a second retailer. |

## Per-person must-rehearse (top 3)

| Member | Must-be-able-to-answer |
|---|---|
| Patten Lai | A1, A3, A4 |
| Weng Zhi Chao | B1, B4, B5 |
| Lim Man Tung Marcus | C1, C2, C5 |
| Huang Hao Lin | D1, D2, D3 |
| LIN Xiaotong (Host) | E2, E4, F1, F3 — plus all of A–D at summary level |
