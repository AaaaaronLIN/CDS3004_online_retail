# CDS3004 Group F — Speaker Cue Cards
**Group F · CRN 234 · 19 November 2026 · total 9:35**
One page per slide. Upper block = what the audience sees; lower block = what you say.

<div style="page-break-after: always;"></div>
## Slide 1 — Title and hook
**0:00–0:35 (35 s)** · **Speaker:** Member E

**On screen**
- From transactions to a customer operating system
- What should we do on Monday morning, for which customers, with what offer?
- CDS3004 Data Mining · Group F · 19 November 2026
- Public repository: `github.com/GITHUB-USERNAME/cds3004-online-retail` (QR code bottom-right)

**Visual:** clean title card; no data figure. Team name, course, one-line promise.

**Say (verbatim from the plan):**

> Good morning. Every retailer records every transaction, yet most still cannot answer a simple operational question: of my thousands of customers, who is about to leave, what should I offer them, and who should my team call first on Monday? Over the next ten minutes we show how we turned twelve months of raw retail transactions into a customer operating system — one joined-up analysis that ends not in a chart, but in a ranked, budget-bounded action list.

**Do:** look up at the audience here; do not read the slide.

<div style="page-break-after: always;"></div>
## Slide 2 — Agenda
**0:35–1:00 (25 s)** · **Speaker:** Member E

**On screen**
- Data and quality → features → segmentation
- Churn prediction and validation → association rules → similarity
- One integrated decision framework, with honest limits
- Agent-assisted workflow and contributions

**Visual:** three-column agenda strip (Data / Models / Decisions); progress indicator at the bottom of every subsequent slide.

**Say (verbatim from the plan):**

> We follow the project's logic rather than the syllabus order. First, the data and the cleaning decisions that shape everything else. Second, the models: segmentation, churn, rules and similarity. Third, the decision layer that combines them and the limitations we want you to challenge. Each section is owned by a different team member, so you will hear from most of us.

**Do:** look up at the audience here; do not read the slide.

<div style="page-break-after: always;"></div>
## Slide 3 — The question and the framing
**1:00–1:50 (50 s)** · **Speaker:** Member E

**On screen**
- Business question: who are our customers, who will leave, what to offer, whom to call?
- Stakeholders: CRM, e-commerce, finance, data team
- Alternatives considered: RFM-only; CLV regression; basket-only
- Why integrated: one decision needs risk × value × action × capacity

**Visual:** simple four-question diagram converging into one "priority target list" box; optional mini table of the three rejected framings.

**Say (verbatim from the plan):**

> We deliberately did not start from a technique. We started from four decisions the business actually makes. Segmentation answers who they are, churn answers who is leaving, rules answer what to offer, similarity helps where segments are sparse. Any one of these alone produces a report; together they produce a decision. We considered an RFM-only study and a spend-prediction model, and rejected both as standalone framings — the first is static, the second cannot be validated without campaign data. The integration is the contribution.

**Do:** look up at the audience here; do not read the slide.

<div style="page-break-after: always;"></div>
## Slide 4 — Data and data quality
**1:50–2:40 (50 s)** · **Speaker:** Member A

**On screen**
- UCI Online Retail: 541,909 lines, 8 fields, Dec 2010–Dec 2011
- Missing `CustomerID`: 24.9267% of lines
- Returns, cancellations, admin codes, duplicates → logged decisions
- Two temporal snapshots, not one random split
- Bias caveat: anonymous lines = 13.572% of revenue

**Visual:** `f01_data_quality_overview` (data-quality overview) with the audit table `t02_data_quality_issues` and cleaning log `t03_cleaning_decisions` cropped to five rows on the right.

**Say (verbatim from the plan):**

> The data is one year of real line items from a UK online retailer — 541,909 rows, with all the mess that implies. About 24.9267% of lines have no customer ID, so they cannot enter a customer snapshot at all. Returns and cancellations are real behaviour, not errors, so we keep them as a feature but remove them from spend. Every decision is counted in the audit log. And we flag the bias up front: the anonymous lines we drop carry 13.572% of revenue, so our customer-level conclusions describe identified customers only.

**Do:** look up at the audience here; do not read the slide.

<div style="page-break-after: always;"></div>
## Slide 5 — Pipeline design
**2:40–3:25 (45 s)** · **Speaker:** Member E

**On screen**
- Ten notebook sections (S0 setup + S1–S9), each writing a reproducible artifact
- T1 (2011-05-31) trains and evaluates churn; T2 (2011-08-31) is the out-of-time decision cohort
- 90-day churn label; features strictly before the as-of date
- Transforms and selection are refit inside each training fold — no leakage
- Decision layer joins segment × risk × action under a capacity limit

**Visual:** horizontal S0–S9 pipeline diagram, colour-coded data / models / decision; or Table 5 from the report rendered as a slide.

**Say (verbatim from the plan):**

> This is the whole system on one line. S0 is setup and S1 is the data-quality funnel; S2 builds the temporal snapshots; S3 compares distance metrics; S4 engineers and selects features. S5 to S7 are the modelling components: segmentation, churn and association rules. S8 is the decision framework that joins them, and S9 writes the metrics, artifact index and reproducibility checks. The critical design choice is the temporal split: T1 develops and tests the model, T2 is locked away until the end and opened exactly once.

**Do:** look up at the audience here; do not read the slide.

<div style="page-break-after: always;"></div>
## Slide 6 — Feature engineering and leakage control
**3:25–4:10 (45 s)** · **Speaker:** Member B

**On screen**
- Nine families: RFM, monetary structure, basket, breadth, engagement, rhythm, momentum, behaviour, context
- Heavy tails → log1p; continuous features z-scored; transforms live inside sklearn pipelines
- Selection: correlation filter (|r| > 0.9) → mutual information → RFE
- 10 of 16 features retained; validation PR-AUC improves
- Leakage guard: transforms refit on every training fold; T2 never used

**Visual:** `f08_feature_importance` (permutation importance) beside `f02_feature_distributions` (cropped), with the selection-funnel numbers from `t05_feature_selection` as caption.

**Say (verbatim from the plan):**

> RFM features are only the starting point. We add basket size, breadth, rhythm, momentum and returns so that a loyal low-spend customer is distinguishable from a lapsing high-spend one. Spend is heavy-tailed, so we log-transform and scale inside scikit-learn pipelines, which means every fold refits its own transforms. Selection is a documented three-stage funnel from 16 to 10 features. The important honest note: permutation importance is led by basket size, return rate and momentum, and recency_days was dropped by RFE — a caveat we state in the report.

**Do:** look up at the audience here; do not read the slide.

<div style="page-break-after: always;"></div>
## Slide 7 — Customer segmentation
**4:10–5:05 (55 s)** · **Speaker:** Member B

**On screen**
- K-means on the T2 decision cohort — descriptive, in-sample, not predictive
- K chosen from 4–6 by elbow + silhouette + bootstrap ARI + a minimum-segment-size rule
- K = 5, silhouette 0.3279, ARI 0.9699
- Five named segments: Champions, Loyal, Potential, At-risk, Hibernating
- Silhouette is highest at smaller K; K = 5 is chosen for stability and actionable size

**Visual:** `f04_elbow_silhouette` (K diagnostics) and `f05_segment_profiles` (profile heatmap) side by side.

**Say (verbatim from the plan):**

> We cluster the T2 decision cohort — the customers we would act on — and we are explicit that this is descriptive, in-sample, not a predictive model. K is chosen from 4 to 6 using inertia, silhouette, bootstrap stability and a rule that every segment must exceed 10% of the base. K equals 5, with ARI 0.9699 and silhouette 0.3279. Honesty point: silhouette is actually highest at smaller K, but K = 2 is too coarse for a five-tier action framework and K = 4 is far less stable under resampling. We chose K = 5 for stability, meaningful size and business interpretability.

**Do:** look up at the audience here; do not read the slide.

<div style="page-break-after: always;"></div>
## Slide 8 — Churn prediction: CV, held-out and out-of-time
**5:05–6:15 (70 s)** · **Speaker:** Member C

**On screen**
- Three models: logistic regression, decision tree, random forest; selected on validation PR-AUC
- 5-fold CV → 70/15/15 T1 train/val/test → out-of-time T2 (opened once)
- Selected model: logistic regression; out-of-time ROC-AUC 0.7392
- Top-decile lift 1.6916×; RF is the non-linear benchmark and importance source
- Two thresholds: F1-optimal and top-10% capacity; pilot list capped at 200

**Visual:** `f07_cv_model_comparison` (cross-validated comparison) and `f08_roc_test_oot` (held-out and out-of-time ROC) together, with the top-decile lift from `f09_lift_curve` as a callout; highlight the selected model and the out-of-time number.

**Say (verbatim from the plan):**

> This is the slide that must be honest. We compare three models and report three levels of evidence: cross-validation, a held-out slice of T1, and the out-of-time cohort T2. Model selection uses validation PR-AUC only, never the test set — and the winner is logistic regression, not the more glamorous forest. Its out-of-time ROC-AUC is 0.7392, and at the top decile it captures 1.6916 times the churners of random contact. The random forest is kept as a non-linear benchmark and as the source of permutation importance. The pilot campaign then contacts only the top 200 priority customers.

**Do:** look up at the audience here; do not read the slide.

<div style="page-break-after: always;"></div>
## Slide 9 — Association rules: what to offer
**6:15–6:55 (40 s)** · **Speaker:** Member D

**On screen**
- FP-Growth mined on Dec 2010–Jul 2011 invoices; validated on Aug–Dec 2011 holdout
- 5441 rules retained; 5402 evaluated out of time
- Median holdout lift 12.174; 99.8% keep lift > 1 and 99.4% keep lift > 2
- Business filter (support ≥ 1%, lift ≥ 2): 593 rules; top pair REGENCY TEACUP, lift 16.4
- Caveat: top-by-lift rules are rare colour/size variants, so lift overstates incremental cross-sell

**Visual:** `f10_association_rules` (support vs lift, size = confidence, colour = holdout lift) plus the business-filtered rules from `t10b_business_rules`.

**Say (verbatim from the plan):**

> Association rules answer the 'what should we offer' question, but only if they are validated. We mine with FP-Growth on invoices from December to July, then re-test every rule on a later holdout period the miner never saw — August to December. Of 5441 retained rules, 5402 were evaluated out of time: median holdout lift 12.174, and 99.8% keep lift above one. We do not headline the mean lift because rare colour-variant pairs inflate it. Instead we apply a business filter — support at least 1%, lift at least 2 — leaving 593 actionable rules such as GREEN REGENCY TEACUP to ROSES REGENCY TEACUP.

**Do:** look up at the audience here; do not read the slide.

<div style="page-break-after: always;"></div>
## Slide 10 — Similarity and lookalikes
**6:55–7:30 (35 s)** · **Speaker:** Member D

**On screen**
- Compare Euclidean, cosine and Manhattan on silhouette and kNN label agreement
- Selected metric: `cosine` (highest silhouette, near-tied agreement)
- Lookalikes for seed expansion and cold-start scoring
- Similar products for long-tail cross-sell and bundles
- Similar ≠ responsive: similarity is a description, not a cause

**Visual:** `t04_lookalikes` and `t05_similar_products` as cropped example tables, with the metric comparison from `t03_distance_metrics`.

**Say (verbatim from the plan):**

> Similarity does two jobs. For customers, nearest neighbours expand a seed group of Champions and give a provisional segment to brand-new customers before enough history exists for the churn model. For products, similarity covers long-tail items that association rules cannot reach because they lack co-occurrence support. We compared Euclidean, cosine and Manhattan on two pieces of evidence — silhouette and kNN label agreement — and selected cosine, which has the highest silhouette while agreement is near-tied. The honest caveat: a lookalike customer is not automatically a responsive one.

**Do:** look up at the audience here; do not read the slide.

<div style="page-break-after: always;"></div>
## Slide 11 — Integrated decision framework and business impact
**7:30–8:30 (60 s)** · **Speaker:** Member E

**On screen**
- Segment × risk matrix = where value and risk coincide
- Priority = predicted churn probability × monetary value
- Pilot: top 200 customers (7.12% of T2)
- Conservative validated ROI: net GBP 14802.58 (ROI 925.16%); model-precision GBP 33799.89 is an optimistic bound
- Random-200 baseline nets GBP 1925.76; model value is the GBP 31874.13 uplift — a scenario, not measured uplift

**Visual:** `f12_segment_risk_matrix` (bubble chart) beside the action table `t13_action_table`, the three-scenario comparison `t16_targeting_comparison`, and `f13_roi_sensitivity`.

**Say (verbatim from the plan):**

> This is the payoff. Each customer sits in a segment and a risk tier, and the action table says what to do: VIP call, loyalty upgrade, nurture, win-back, or low-cost reactivation. Priority is predicted churn probability times monetary value. The pilot contacts the top 200 customers, the top 7.12% of the cohort. Lead with the conservative number: using the churn rate actually observed in the priority list, net expected value is GBP 14802.58, ROI 925.16%. The model-precision figure GBP 33799.89 is an optimistic bound. Random-200 nets just GBP 1925.76, so the value is the GBP 31874.13 uplift. ROI is a scenario analysis, not measured uplift; the dataset contains no campaign history.

**Do:** look up at the audience here; do not read the slide.

<div style="page-break-after: always;"></div>
## Slide 12 — Limitations and what we would do next
**8:30–9:00 (30 s)** · **Speaker:** Member A

**On screen**
- Anonymous-customer bias: 13.572% of revenue excluded
- 90-day churn label is a proxy; T2 season differs from T1; clustering is descriptive
- Rule lift inflated by rare colour/size variants; recency_days dropped by RFE
- No campaign data: ROI is a scenario (validated net GBP 14802.58; optimistic GBP 33799.89)
- Next: survival analysis, uplift testing, longer history

**Visual:** text slide with five short limitation cards; no chart (deliberate pause before closing).

**Say (verbatim from the plan):**

> We want to be judged on what we can defend. The customer-level view misses 13.572% of revenue, so every rate describes identified customers. The 90-day label is a proxy, our out-of-time cohort covers a different season, and the segmentation is descriptive rather than predictive. Some top association rules pair colour variants of the same product, so their lift overstates cross-sell, and recency_days was dropped by RFE. Most importantly, we predict inactivity, not response: the ROI is a scenario with a conservative validated figure, not measured uplift.

**Do:** look up at the audience here; do not read the slide.

<div style="page-break-after: always;"></div>
## Slide 13 — Contributions and agent-assisted workflow
**9:00–9:20 (20 s)** · **Speaker:** Member E

**On screen**
- Five roles, each owning rubric items and commits (Member A–E)
- Human–agent loop: define → propose → review → implement → verify
- Every agent output verified by re-run, recomputation and code review
- Per-person trajectories in `agent-logs/`

**Visual:** contribution table (5 rows: role, rubric items, key artifacts); small loop diagram of the human–agent workflow.

**Say (verbatim from the plan):**

> Five members, five clear ownership areas, visible in the commit history and in our individual agent trajectories. We used agents throughout, but every output passed a human gate: the notebook was re-run from a clean kernel, headline numbers were recomputed independently, and agent diffs were reviewed before merge. The logs record what the agent proposed and what we changed — including the proposals we rejected. That workflow is documented in the repository and in the report.

**Do:** look up at the audience here; do not read the slide.

<div style="page-break-after: always;"></div>
## Slide 14 — Closing and Q&A
**9:20–9:35 (15 s)** · **Speaker:** Member E

**On screen**
- One joined-up system: segment, predict, recommend, prioritise
- From 541,909 transactions to a defensible action list
- Public repository and full report in the QR code
- Questions welcome

**Visual:** single takeaway sentence, repository QR code, team names and contact.

**Say (verbatim from the plan):**

> So: from 541,909 raw transactions to a ranked, budget-bounded action list, with every model validated on a future cohort and every assumption written down. The value is not any single chart — it is the integration, and the honesty about what the data cannot tell us. All code, figures and our agent-use logs are in the public repository. Thank you — we are happy to take your questions.

**Do:** look up at the audience here; do not read the slide.
