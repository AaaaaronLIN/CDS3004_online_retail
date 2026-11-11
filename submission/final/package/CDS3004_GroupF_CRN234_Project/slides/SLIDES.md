# CDS3004 Group Presentation — Slide-by-Slide Plan

**Project:** From Transactions to a Customer Operating System — An Agent-Assisted Data Mining Study of Online Retail Customer Behaviour
**Course:** CDS3004 Data Mining, Lingnan University, 2026/27 Term 1 — Group Presentation (8%)
**Team:** Group F — Member A, Member B, Member C, Member D, Member E
**Presentation date:** Thursday 19 November 2026 (confirm room, time and order with the course announcement)
**Duration:** 10 minutes + Q&A. **This duration is an assumption and must be confirmed with the TA or the course announcement before rehearsing the final timings.**

**Total planned speaking time: 9:35, leaving 25 seconds of buffer inside the 10:00 limit.** Times are cumulative, measured from the moment the speaker starts slide 1. Rehearse with a timer; if the talk must be shortened, cut slide 9 (rules detail) first, then slide 10.

**Speakers:** Member E opens and closes (slides 1–3, 5, 11–14); Member A presents data (slide 4); Member B presents features and segmentation (slides 6–7); Member C presents churn (slide 8); Member D presents rules and similarity (slides 9–10); all five participate in Q&A. Each speaker should stand, use the clicker, and hand over with a one-sentence bridge.

---

## Slide 1 — Title and hook

**Cumulative timing:** 0:00–0:35 (35 s) · **Speaker:** Member E

**On-slide bullets**
- From transactions to a customer operating system
- What should we do on Monday morning, for which customers, with what offer?
- CDS3004 Data Mining · Group F · 19 November 2026
- Public repository: `github.com/GITHUB-USERNAME/cds3004-online-retail` (QR code bottom-right)

**Visual:** clean title card; no data figure. Team name, course, one-line promise.

**Speaker notes (≈78 words):** "Good morning. Every retailer records every transaction, yet most still cannot answer a simple operational question: of my thousands of customers, who is about to leave, what should I offer them, and who should my team call first on Monday? Over the next ten minutes we show how we turned twelve months of raw retail transactions into a customer operating system — one joined-up analysis that ends not in a chart, but in a ranked, budget-bounded action list."

**Presentation rubric focus:** gains/holds attention (opening question); clarity of speech.

---

## Slide 2 — Agenda

**Cumulative timing:** 0:35–1:00 (25 s) · **Speaker:** Member E

**On-slide bullets**
- Data and quality → features → segmentation
- Churn prediction and validation → association rules → similarity
- One integrated decision framework, with honest limits
- Agent-assisted workflow and contributions

**Visual:** three-column agenda strip (Data / Models / Decisions); progress indicator at the bottom of every subsequent slide.

**Speaker notes (≈60 words):** "We follow the project's logic rather than the syllabus order. First, the data and the cleaning decisions that shape everything else. Second, the models: segmentation, churn, rules and similarity. Third, the decision layer that combines them and the limitations we want you to challenge. Each section is owned by a different team member, so you will hear from most of us."

**Presentation rubric focus:** clear, logically organised content (agenda sets the structure explicitly).

---

## Slide 3 — The question and the framing

**Cumulative timing:** 1:00–1:50 (50 s) · **Speaker:** Member E

**On-slide bullets**
- Business question: who are our customers, who will leave, what to offer, whom to call?
- Stakeholders: CRM, e-commerce, finance, data team
- Alternatives considered: RFM-only; CLV regression; basket-only
- Why integrated: one decision needs risk × value × action × capacity

**Visual:** simple four-question diagram converging into one "priority target list" box; optional mini table of the three rejected framings.

**Speaker notes (≈84 words):** "We deliberately did not start from a technique. We started from four decisions the business actually makes. Segmentation answers who they are, churn answers who is leaving, rules answer what to offer, similarity helps where segments are sparse. Any one of these alone produces a report; together they produce a decision. We considered an RFM-only study and a spend-prediction model, and rejected both as standalone framings — the first is static, the second cannot be validated without campaign data. The integration is the contribution."

**Presentation rubric focus:** clear, logically organised content; relevance to the problem.

---

## Slide 4 — Data and data quality

**Cumulative timing:** 1:50–2:40 (50 s) · **Speaker:** Member A

**On-slide bullets**
- UCI Online Retail: 541,909 lines, 8 fields, Dec 2010–Dec 2011
- Missing `CustomerID`: 24.9267% of lines
- Returns, cancellations, admin codes, duplicates → logged decisions
- Two temporal snapshots, not one random split
- Bias caveat: anonymous lines = 13.572% of revenue

**Visual:** `f01_data_quality_overview` (data-quality overview) with the audit table `t02_data_quality_issues` and cleaning log `t03_cleaning_decisions` cropped to five rows on the right.

**Speaker notes (≈86 words):** "The data is one year of real line items from a UK online retailer — 541,909 rows, with all the mess that implies. About 24.9267% of lines have no customer ID, so they cannot enter a customer snapshot at all. Returns and cancellations are real behaviour, not errors, so we keep them as a feature but remove them from spend. Every decision is counted in the audit log. And we flag the bias up front: the anonymous lines we drop carry 13.572% of revenue, so our customer-level conclusions describe identified customers only."

**Presentation rubric focus:** effective use of tools (clean, legible figure); clarity; body language and eye contact with audience.

---

## Slide 5 — Pipeline design

**Cumulative timing:** 2:40–3:25 (45 s) · **Speaker:** Member E

**On-slide bullets**
- Ten notebook sections (S0 setup + S1–S9), each writing a reproducible artifact
- T1 (2011-05-31) trains and evaluates churn; T2 (2011-08-31) is the out-of-time decision cohort
- 90-day churn label; features strictly before the as-of date
- Transforms and selection are refit inside each training fold — no leakage
- Decision layer joins segment × risk × action under a capacity limit

**Visual:** horizontal S0–S9 pipeline diagram, colour-coded data / models / decision; or Table 5 from the report rendered as a slide.

**Speaker notes (≈84 words):** "This is the whole system on one line. S0 is setup and S1 is the data-quality funnel; S2 builds the temporal snapshots; S3 compares distance metrics; S4 engineers and selects features. S5 to S7 are the modelling components: segmentation, churn and association rules. S8 is the decision framework that joins them, and S9 writes the metrics, artifact index and reproducibility checks. The critical design choice is the temporal split: T1 develops and tests the model, T2 is locked away until the end and opened exactly once."

**Presentation rubric focus:** solution design clarity; logical flow; use of a single organising visual.

---

## Slide 6 — Feature engineering and leakage control

**Cumulative timing:** 3:25–4:10 (45 s) · **Speaker:** Member B

**On-slide bullets**
- Nine families: RFM, monetary structure, basket, breadth, engagement, rhythm, momentum, behaviour, context
- Heavy tails → log1p; continuous features z-scored; transforms live inside sklearn pipelines
- Selection: correlation filter (|r| > 0.9) → mutual information → RFE
- 10 of 16 features retained; validation PR-AUC improves
- Leakage guard: transforms refit on every training fold; T2 never used

**Visual:** `f08_feature_importance` (permutation importance) beside `f02_feature_distributions` (cropped), with the selection-funnel numbers from `t05_feature_selection` as caption.

**Speaker notes (≈86 words):** "RFM features are only the starting point. We add basket size, breadth, rhythm, momentum and returns so that a loyal low-spend customer is distinguishable from a lapsing high-spend one. Spend is heavy-tailed, so we log-transform and scale inside scikit-learn pipelines, which means every fold refits its own transforms. Selection is a documented three-stage funnel from 16 to 10 features. The important honest note: permutation importance is led by basket size, return rate and momentum, and recency_days was dropped by RFE — a caveat we state in the report."

**Presentation rubric focus:** clear, logically organised content; appropriate use of charts.

---

## Slide 7 — Customer segmentation

**Cumulative timing:** 4:10–5:05 (55 s) · **Speaker:** Member B

**On-slide bullets**
- K-means on the T2 decision cohort — descriptive, in-sample, not predictive
- K chosen from 4–6 by elbow + silhouette + bootstrap ARI + a minimum-segment-size rule
- K = 5, silhouette 0.3279, ARI 0.9699
- Five named segments: Champions, Loyal, Potential, At-risk, Hibernating
- Silhouette is highest at smaller K; K = 5 is chosen for stability and actionable size

**Visual:** `f04_elbow_silhouette` (K diagnostics) and `f05_segment_profiles` (profile heatmap) side by side.

**Speaker notes (≈90 words):** "We cluster the T2 decision cohort — the customers we would act on — and we are explicit that this is descriptive, in-sample, not a predictive model. K is chosen from 4 to 6 using inertia, silhouette, bootstrap stability and a rule that every segment must exceed 10% of the base. K equals 5, with ARI 0.9699 and silhouette 0.3279. Honesty point: silhouette is actually highest at smaller K, but K = 2 is too coarse for a five-tier action framework and K = 4 is far less stable under resampling. We chose K = 5 for stability, meaningful size and business interpretability."

**Presentation rubric focus:** gains/holds attention (counter-intuitive point about small segments); clarity.

---

## Slide 8 — Churn prediction: CV, held-out and out-of-time

**Cumulative timing:** 5:05–6:15 (70 s) · **Speaker:** Member C

**On-slide bullets**
- Three models: logistic regression, decision tree, random forest; selected on validation PR-AUC
- 5-fold CV → 70/15/15 T1 train/val/test → out-of-time T2 (opened once)
- Selected model: logistic regression; out-of-time ROC-AUC 0.7392
- Top-decile lift 1.6916×; RF is the non-linear benchmark and importance source
- Two thresholds: F1-optimal and top-10% capacity; pilot list capped at 200

**Visual:** `f07_cv_model_comparison` (cross-validated comparison) and `f08_roc_test_oot` (held-out and out-of-time ROC) together, with the top-decile lift from `f09_lift_curve` as a callout; highlight the selected model and the out-of-time number.

**Speaker notes (≈92 words):** "This is the slide that must be honest. We compare three models and report three levels of evidence: cross-validation, a held-out slice of T1, and the out-of-time cohort T2. Model selection uses validation PR-AUC only, never the test set — and the winner is logistic regression, not the more glamorous forest. Its out-of-time ROC-AUC is 0.7392, and at the top decile it captures 1.6916 times the churners of random contact. The random forest is kept as a non-linear benchmark and as the source of permutation importance. The pilot campaign then contacts only the top 200 priority customers."

**Presentation rubric focus:** clear content; effective use of tools (two complementary charts, not four); pace — this is the densest slide, so speak slowly.

---

## Slide 9 — Association rules: what to offer

**Cumulative timing:** 6:15–6:55 (40 s) · **Speaker:** Member D

**On-slide bullets**
- FP-Growth mined on Dec 2010–Jul 2011 invoices; validated on Aug–Dec 2011 holdout
- 5441 rules retained; 5402 evaluated out of time
- Median holdout lift 12.174; 99.8% keep lift > 1 and 99.4% keep lift > 2
- Business filter (support ≥ 1%, lift ≥ 2): 593 rules; top pair REGENCY TEACUP, lift 16.4
- Caveat: top-by-lift rules are rare colour/size variants, so lift overstates incremental cross-sell

**Visual:** `f10_association_rules` (support vs lift, size = confidence, colour = holdout lift) plus the business-filtered rules from `t10b_business_rules`.

**Speaker notes (≈92 words):** "Association rules answer the 'what should we offer' question, but only if they are validated. We mine with FP-Growth on invoices from December to July, then re-test every rule on a later holdout period the miner never saw — August to December. Of 5441 retained rules, 5402 were evaluated out of time: median holdout lift 12.174, and 99.8% keep lift above one. We do not headline the mean lift because rare colour-variant pairs inflate it. Instead we apply a business filter — support at least 1%, lift at least 2 — leaving 593 actionable rules such as GREEN REGENCY TEACUP to ROSES REGENCY TEACUP."

**Presentation rubric focus:** clarity; logical content; pace (short slide, do not overrun).

---

## Slide 10 — Similarity and lookalikes

**Cumulative timing:** 6:55–7:30 (35 s) · **Speaker:** Member D

**On-slide bullets**
- Compare Euclidean, cosine and Manhattan on silhouette and kNN label agreement
- Selected metric: `cosine` (highest silhouette, near-tied agreement)
- Lookalikes for seed expansion and cold-start scoring
- Similar products for long-tail cross-sell and bundles
- Similar ≠ responsive: similarity is a description, not a cause

**Visual:** `t04_lookalikes` and `t05_similar_products` as cropped example tables, with the metric comparison from `t03_distance_metrics`.

**Speaker notes (≈80 words):** "Similarity does two jobs. For customers, nearest neighbours expand a seed group of Champions and give a provisional segment to brand-new customers before enough history exists for the churn model. For products, similarity covers long-tail items that association rules cannot reach because they lack co-occurrence support. We compared Euclidean, cosine and Manhattan on two pieces of evidence — silhouette and kNN label agreement — and selected cosine, which has the highest silhouette while agreement is near-tied. The honest caveat: a lookalike customer is not automatically a responsive one."

**Presentation rubric focus:** clarity; content relevance; maintaining momentum into the decision section.

---

## Slide 11 — Integrated decision framework and business impact

**Cumulative timing:** 7:30–8:30 (60 s) · **Speaker:** Member E

**On-slide bullets**
- Segment × risk matrix = where value and risk coincide
- Priority = predicted churn probability × monetary value
- Pilot: top 200 customers (7.12% of T2)
- Conservative validated ROI: net GBP 14802.58 (ROI 925.16%); model-precision GBP 33799.89 is an optimistic bound
- Random-200 baseline nets GBP 1925.76; model value is the GBP 31874.13 uplift — a scenario, not measured uplift

**Visual:** `f12_segment_risk_matrix` (bubble chart) beside the action table `t13_action_table`, the three-scenario comparison `t16_targeting_comparison`, and `f13_roi_sensitivity`.

**Speaker notes (≈94 words):** "This is the payoff. Each customer sits in a segment and a risk tier, and the action table says what to do: VIP call, loyalty upgrade, nurture, win-back, or low-cost reactivation. Priority is predicted churn probability times monetary value. The pilot contacts the top 200 customers, the top 7.12% of the cohort. Lead with the conservative number: using the churn rate actually observed in the priority list, net expected value is GBP 14802.58, ROI 925.16%. The model-precision figure GBP 33799.89 is an optimistic bound. Random-200 nets just GBP 1925.76, so the value is the GBP 31874.13 uplift. ROI is a scenario analysis, not measured uplift; the dataset contains no campaign history."

**Presentation rubric focus:** gains/holds attention (the business punchline); clarity; appropriate use of tools.

---

## Slide 12 — Limitations and what we would do next

**Cumulative timing:** 8:30–9:00 (30 s) · **Speaker:** Member A

**On-slide bullets**
- Anonymous-customer bias: 13.572% of revenue excluded
- 90-day churn label is a proxy; T2 season differs from T1; clustering is descriptive
- Rule lift inflated by rare colour/size variants; recency_days dropped by RFE
- No campaign data: ROI is a scenario (validated net GBP 14802.58; optimistic GBP 33799.89)
- Next: survival analysis, uplift testing, longer history

**Visual:** text slide with five short limitation cards; no chart (deliberate pause before closing).

**Speaker notes (≈86 words):** "We want to be judged on what we can defend. The customer-level view misses 13.572% of revenue, so every rate describes identified customers. The 90-day label is a proxy, our out-of-time cohort covers a different season, and the segmentation is descriptive rather than predictive. Some top association rules pair colour variants of the same product, so their lift overstates cross-sell, and recency_days was dropped by RFE. Most importantly, we predict inactivity, not response: the ROI is a scenario with a conservative validated figure, not measured uplift."

**Presentation rubric focus:** clear content; critical interpretation; body language and tone (confident, not defensive).

---

## Slide 13 — Contributions and agent-assisted workflow

**Cumulative timing:** 9:00–9:20 (20 s) · **Speaker:** Member E

**On-slide bullets**
- Five roles, each owning rubric items and commits (Member A–E)
- Human–agent loop: define → propose → review → implement → verify
- Every agent output verified by re-run, recomputation and code review
- Per-person trajectories in `agent-logs/`

**Visual:** contribution table (5 rows: role, rubric items, key artifacts); small loop diagram of the human–agent workflow.

**Speaker notes (≈70 words):** "Five members, five clear ownership areas, visible in the commit history and in our individual agent trajectories. We used agents throughout, but every output passed a human gate: the notebook was re-run from a clean kernel, headline numbers were recomputed independently, and agent diffs were reviewed before merge. The logs record what the agent proposed and what we changed — including the proposals we rejected. That workflow is documented in the repository and in the report."

**Presentation rubric focus:** instructor-defined role and appropriate dress (all members visible and introduced); clarity.

---

## Slide 14 — Closing and Q&A

**Cumulative timing:** 9:20–9:35 (15 s) · **Speaker:** Member E

**On-slide bullets**
- One joined-up system: segment, predict, recommend, prioritise
- From 541,909 transactions to a defensible action list
- Public repository and full report in the QR code
- Questions welcome

**Visual:** single takeaway sentence, repository QR code, team names and contact.

**Speaker notes (≈62 words):** "So: from 541,909 raw transactions to a ranked, budget-bounded action list, with every model validated on a future cohort and every assumption written down. The value is not any single chart — it is the integration, and the honesty about what the data cannot tell us. All code, figures and our agent-use logs are in the public repository. Thank you — we are happy to take your questions."

**Presentation rubric focus:** appropriate time allocation (finish on time); clarity; gains/holds attention to the end.

---

## Timing summary

| # | Slide | Speaker | Duration | Cumulative |
|---|---|---|---|---|
| 1 | Title and hook | Member E | 0:35 | 0:35 |
| 2 | Agenda | Member E | 0:25 | 1:00 |
| 3 | Question and framing | Member E | 0:50 | 1:50 |
| 4 | Data and data quality | Member A | 0:50 | 2:40 |
| 5 | Pipeline design | Member E | 0:45 | 3:25 |
| 6 | Feature engineering | Member B | 0:45 | 4:10 |
| 7 | Segmentation | Member B | 0:55 | 5:05 |
| 8 | Churn results | Member C | 1:10 | 6:15 |
| 9 | Association rules | Member D | 0:40 | 6:55 |
| 10 | Similarity and lookalikes | Member D | 0:35 | 7:30 |
| 11 | Decision framework and impact | Member E | 1:00 | 8:30 |
| 12 | Limitations | Member A | 0:30 | 9:00 |
| 13 | Contributions and agent workflow | Member E | 0:20 | 9:20 |
| 14 | Closing and Q&A | Member E | 0:15 | **9:35** |

**Speaking total 9:35; 25 s buffer before the 10:00 limit.** If the confirmed duration is shorter (for example 8 minutes), cut slide 10 and trim slide 9, then reduce slides 2 and 13 to a single sentence. If the confirmed duration is longer, restore the backup slides B2 and B4.

---

## Mapping to the 8% presentation rubric

| Rubric item (weight) | How this plan satisfies it | Slides |
|---|---|---|
| Appropriate time allocation and pace (1%) | Fixed per-slide budget summing to 9:35, 25 s buffer, one timer and one timekeeper; dense slide 8 speaks slowly | All; summary table above |
| Clear, logically organised and relevant content (2%) | Explicit agenda; data → methods → decision → limits arc; each slide answers one question; leads with the business question, not the algorithm | 2–12 |
| Effective use of presentation tools (1%) | One primary visual per slide, no chart walls; two-up only where comparison is the point; consistent theme, large fonts, slide numbers and progress indicator | 4–11 |
| Good body language, eye contact, appropriate voice tone (1%) | One standing speaker per section; hand-over at slide boundaries so the speaker can face the audience; notes are prompts, not a script to read | All |
| Gains/holds attention (1%) | Opening operational question; the "small segment, large value" counter-intuition; the ROI scenario framing; the honesty moment on limitations | 1, 7, 11, 12 |
| Instructor-defined role and appropriate dress (1%) | All five introduced on slides 1/13; formal/smart attire; presenter roles match the contribution table | 1, 13 |
| Clarity of speech and accuracy of grammar/pronunciation (1%) | English-only script; short sentences; terminology defined on first use (lift, silhouette, ARI, FP-Growth); rehearsal with a non-specialist listener | All |

---

## Backup slides (not presented; available for Q&A)

1. **B1 — Data-quality audit and cleaning log.** Full `t02_data_quality_issues` and `t03_cleaning_decisions` tables with every issue class, count and treatment; answers "how exactly did you clean?"
2. **B2 — Full model metrics.** `t08_model_metrics` for all three models on T1 test and T2 out-of-time, with the selected model shaded; answers "show me the numbers".
3. **B3 — Threshold and error analysis.** `f09_confusion_and_threshold` plus `s06_threshold_analysis.csv`: confusion matrix at the F1-optimal threshold, precision/recall versus contact volume, and both the F1-optimal and top-10% capacity thresholds; answers "how did you choose the cut-off?".
4. **B4 — Association-rule holdout detail.** `t10b_business_rules` (business-filtered top rules) and `t10_association_rules` in full, including per-rule holdout support and lift, plus the pruning rules; answers "which rules survived and why".
5. **B5 — Similarity metric comparison.** `t03_distance_metrics` and `t04_lookalikes` in full, including silhouette and kNN label agreement that justify the selected metric; answers "why this metric?".
6. **B6 — ROI assumptions and sensitivity.** `t14_roi_assumptions`, `t16_targeting_comparison` and `f13_roi_sensitivity` for the targeted versus random campaign across pessimistic, base and optimistic scenarios; answers "how fragile is the business case?".

---

## Likely Q&A and concise answers

**Q1. Why 90 days for churn, and what if it were 60 or 180?**
A: The 90-day window matches a quarterly retention cycle and gives enough time to distinguish a quiet month from real attrition. It is a business definition, not a statistical constant; a shorter window labels more customers as churned and a longer window fewer. The pipeline is parameterised, so the window can be changed and the models refitted without touching the code structure.

**Q2. Why K-means rather than GMM, DBSCAN or hierarchical clustering?**
A: The segmentation must be stable and easy to explain to a CRM team. K-means on standardised, selected features gives compact centroids, fast assignment of new customers and a clean story. GMM adds soft assignments we cannot use operationally; DBSCAN's density assumption does not hold across a customer base with very different engagement levels; hierarchical clustering offers no advantage at this scale and is less stable to report. We also check stability with bootstrap ARI, which is the property that matters for deployment.

**Q3. Is the ROI real, or did you just make up assumptions?**
A: The ROI is explicitly a scenario. Every input is a stated planning assumption — cost per contact, retention rate, margin — and all are in the report's table. We do not claim a measured return, because the data has no campaign-response history; estimating incremental uplift requires an A/B test. The value of the calculation is that it makes the business case auditable and shows what would have to be true for the campaign to pay off.

**Q4. You dropped anonymous customers — doesn't that invalidate the analysis?**
A: It limits the scope, and we say so: anonymous lines are 13.572% of revenue, so every customer-level statement is about identified customers. Dropping them is unavoidable for customer-level modelling because there is no key to link their visits. The honest framing is that this is a study of identified customers, and a production system would either incentivise identification or model the anonymous population separately.

**Q5. Why not use deep learning or gradient boosting for churn?**
A: With roughly a few thousand customers and a 90-day proxy label, a complex model would add variance and opaque behaviour without a trustworthy gain. We deliberately compare three families that span interpretability versus accuracy, report out-of-time performance, and use feature importance to explain the forest. The rubric rewards justified model choice, not the deepest model; our evidence supports the simpler ensemble.

**Q6. How do we know the agent-assisted analysis is not fabricated?**
A: Three independent checks. The notebook is re-run from a fresh kernel and its outputs compared with every committed figure and table; headline numbers are recomputed with short, separately written checks; and every agent diff is reviewed before merge for hard-coded numbers or leakage. The per-member trajectories in `agent-logs/` record the prompt, the agent proposal, what the human changed or rejected, and how the result was verified.

**Q7. Can we reproduce your results?**
A: Yes. The public repository contains the raw-data instructions, `requirements.txt`, the executed notebook and all figures and tables. Running the notebook regenerates every number from the UCI download; seeds and library versions are documented, and the report's reproducibility section lists the exact command. The only manual step is downloading the UCI file into `data/`.

---

## Slide-production notes

- Use 16:9, dark-on-light theme, minimum 20 pt body text; show the course code and slide number on every slide.
- Put one visual per slide; crop tables to five rows and move the full table to backup. Label axes and units on every figure.
- The churn slide (8) is the densest: one chart pair, three numbers maximum, and speaker notes are timed to 70 seconds.
- Keep the title and closing slides free of data so the audience knows when the talk starts and ends.
- Rehearse twice with a timer and once with a non-specialist listener; bring a PDF copy of the slides on a USB stick as backup.
