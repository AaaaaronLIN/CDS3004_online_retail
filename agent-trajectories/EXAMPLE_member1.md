# Agent-Use Trajectory — Member A (WORKED EXAMPLE)

> **THIS IS AN EXAMPLE, NOT A REAL LOG.** It shows the expected format and level of detail for a filled trajectory, using realistic tasks from this project. The prompt wording, decisions and commit hashes are illustrative; no numerical result in this file is a project result. Before submission, replace every entry with your own real trajectory (or annotate clearly which parts are examples), and replace `[commit]` with the real hash. Keep the structure: prompt → agent proposal → human decision → implementation → verification → artifact.

## Header

| Field | Value |
|---|---|
| Member label | Member A |
| Name and student ID | [Member A full name] / [student ID] |
| Role in the project | Data and quality lead — audit, cleaning funnel, temporal snapshots |
| Tools, harnesses and models used | DeepSeek Harness + `deepseek-flash` (main); ChatGPT + GPT-5 (one brainstorming session) |
| Repository | `https://github.com/<org>/<repo>` |
| Date range covered | 2026-10-20 to 2026-11-10 |
| Commits covered | `[commit]` … `[commit]` |
| Public link(s) | [DeepSeek Harness session export in `agent-logs/raw/MemberA_2026-10-27.md`] |

## Trajectory summary

| # | Date | Task | Tool / model | Commit | Verified? |
|---|---|---|---|---|---|
| 1 | 2026-10-20 | Problem scoping and analysis-plan options | DeepSeek Harness / deepseek-flash | — | Yes — team review |
| 2 | 2026-10-27 | Data-quality audit and cleaning funnel | DeepSeek Harness / deepseek-flash | `[commit]` | Yes — independent recompute |
| 3 | 2026-11-03 | T1/T2 snapshot construction and gap features | DeepSeek Harness / deepseek-flash | `[commit]` | Yes — hand-checked one customer |
| 4 | 2026-11-10 | Draft data-quality section of the report | DeepSeek Harness / deepseek-flash | `[commit]` | Yes — every count checked against metrics |

---

## Entry 1 — Problem scoping and analysis-plan options

**Date and time:** 2026-10-20, 14:10 · **Tool / model:** DeepSeek Harness + `deepseek-flash` · **Commit(s):** none (planning task)

**Task / goal.** Choose a defensible framing before writing any code, and make sure the plan covers the course rubric's problem-definition and solution-design criteria.

**Prompt used.**
> We have the UCI Online Retail dataset (541,909 transaction lines, Dec 2010–Dec 2011) and a five-person team project on customer analytics. Before writing any code: inspect the dataset description, identify the main data-quality issues we will face, and propose 2–3 analysis approaches that fit a "customer retention" question. For each approach, explain why it fits, what assumptions we would need to check, and what it would not be able to answer. Do not modify any data yet.

**Agent proposal.** The agent proposed three framings: (a) descriptive RFM/K-means segmentation, (b) supervised churn or spend prediction with a random forest, and (c) market-basket recommendation. It recommended (b) alone and suggested starting with a classifier on a random split.

**Human review and decision.** We rejected the random-split design because it would leak future behaviour into the features, and we rejected framing (b) alone because it would produce a risk score with no action attached. We adopted an integrated framing — segmentation + churn + rules + similarity — with **temporal snapshots** (features before an as-of date, labels after it) and an explicit decision layer. This became the project's problem definition and solution design.

**Implementation.** No code changes; the decision was documented in the team plan and in the report's §1 and §3.

**Verification.** The whole team reviewed the framing against the rubric's problem-definition, solution-design and interpretation criteria before accepting it. We specifically checked that alternatives were considered and that the plan named the constraints (no campaign data, anonymous transactions).

**Artifact / evidence.** Report §1 (alternative framings), §3 (pipeline design).

---

## Entry 2 — Data-quality audit and cleaning funnel

**Date and time:** 2026-10-27, 10:30 · **Tool / model:** DeepSeek Harness + `deepseek-flash` · **Commit(s):** `[commit]`

**Task / goal.** Implement the audit of data-quality issues and a reproducible cleaning funnel that keeps the raw file untouched.

**Prompt used.**
> Implement a data-quality audit for the raw Online Retail table: missingness, duplicates, cancellations, negative quantities, non-positive prices, non-product stock codes. Then write a cleaning funnel that produces the customer-level purchase base. Report the row count and the revenue retained after each step. The raw file must not be modified. Flag every decision explicitly rather than silently dropping rows.

**Agent proposal.** The agent wrote a correct audit, but its first cleaning implementation simply dropped rows with missing `CustomerID`, cancelled invoices, non-positive quantities and non-product codes in one step, reporting a single total. It described the result as "removed all invalid transactions".

**Human review and decision.** **Changed.** Two problems. First, the audit counts and the funnel removals are not the same thing — a line can violate several rules, so summing audit counts overstates what the funnel removes. We required a sequential funnel with rows remaining after each step and a separate audit table. Second, dropping anonymous rows silently would hide a bias, so we required the anonymous revenue share to be measured and reported, the raw file preserved, and returns kept in a separate ledger so `return_rate` could still be built.

**Implementation.** Notebook section S1; outputs `results/tables/t02_data_quality_issues.csv`, `t03_cleaning_decisions.csv`, `f01_data_quality_overview.png`. Commit `[commit]`.

**Verification.** I recomputed the funnel in a short, separately written pandas script — starting from the raw row count, applying each rule in order and printing rows remaining — and compared every step with the notebook's log. I also recomputed the anonymous revenue share from the raw `Quantity × UnitPrice` before and after removing anonymous lines. Both checks matched the notebook to the displayed precision.

**Artifact / evidence.** `t02_data_quality_issues.csv`, `t03_cleaning_decisions.csv`, report §2.3–§2.4.

---

## Entry 3 — Snapshot construction and gap features

**Date and time:** 2026-11-03, 16:00 · **Tool / model:** DeepSeek Harness + `deepseek-flash` · **Commit(s):** `[commit]`

**Task / goal.** Build the T1/T2 customer snapshots (features before the as-of date, churn label in the 90 days after) and the inter-purchase gap features, then sanity-check them.

**Prompt used.**
> Build a snapshot function: given the cleaned purchase table and an as-of date, produce one row per customer with RFM, return-rate and gap features using only transactions before the as-of date. Add a churn label based only on the 90 days after the as-of date. For customers with fewer than two purchase days, define the gap features sensibly. Add assertions that no feature date is on or after the as-of date. Do not touch the T2 cohort for any modelling choice.

**Agent proposal.** The agent implemented the snapshots and label correctly, with leakage assertions. However, its gap implementation used `groupby.apply` returning a Series, which in the installed pandas version produced a stacked result; for single-visit customers the gap features were misaligned or NaN instead of zero.

**Human review and decision.** **Changed.** We required the stacked result to be unstacked and explicit zeros for single-visit customers, plus a spot-check that a customer with one purchase day has zero gaps. We also required tenure to be computed from the customer's first purchase in the data (not the file's first date), and documented the left-truncation by the data start.

**Implementation.** Notebook section S2; commit `[commit]`. The bug and fix were also recorded in `code/pipeline_notes.md` so the next person would not reintroduce it.

**Verification.** I picked one real customer, filtered their raw rows by hand, and computed recency, frequency, monetary value, tenure and gaps on paper; the snapshot row matched. I also checked that the number of snapshot rows equals the number of customers with at least one purchase in the feature window, and that the churn label rate was plausible against a hand count for a sample of ten customers.

**Artifact / evidence.** `t02_cohort_summary.csv`, report §4.1.

---

## Entry 4 — Drafting the data-quality section of the report

**Date and time:** 2026-11-10, 09:45 · **Tool / model:** DeepSeek Harness + `deepseek-flash` · **Commit(s):** `[commit]`

**Task / goal.** Turn the audit, cleaning log and metrics into a submission-quality report section without overclaiming or hand-typing numbers.

**Prompt used.**
> Draft the data-quality and cleaning section of our report from `results/metrics_summary.md`, `results/tables/t02_data_quality_issues.csv` and `t03_cleaning_decisions.csv`. Use only numbers that appear in those files, keep every number in a placeholder token if our fill step expects one, and make the anonymous-customer bias explicit. Do not describe the cleaning as "removing bad data"; describe the decisions and their rationale.

**Agent proposal.** The agent produced a well-structured draft, but it wrote "we removed all guest customers to keep the data clean", described the audit counts as if they were the sequential funnel removals, and added a sentence claiming the cleaned base represented "the whole business".

**Human review and decision.** **Changed.** We rewrote the claim to "anonymous lines are excluded from customer analytics, the raw file is preserved, and the excluded revenue share is reported as a bias"; used the sequential funnel table for removals and the audit table for issue counts; and deleted the "whole business" claim. We also added the limitation that identified customers only are described.

**Implementation.** Report §2; commit `[commit]`.

**Verification.** I checked every number in the section against `results/metrics.json` and the two CSVs, confirmed that no result was hand-typed, and searched the section for authoring language and leftover placeholder tokens. A second team member read it against the rubric's data criterion.

**Artifact / evidence.** Report §2; `t02_data_quality_issues.csv`, `t03_cleaning_decisions.csv`.

---

## Self-check

- [x] Four dated entries, each with prompt, proposal, human decision, implementation and verification.
- [x] Entry 2 and Entry 3 record proposals that were **changed**, with the reason.
- [x] Every implementation links to a commit token (replace tokens with real hashes).
- [x] Entries 2, 3 and 4 show independent verification, not just "it looked right".
- [x] No secrets, tokens, private contact details or unrelated conversations.
- [x] Public link placeholder replaced by a local transcript fallback note before submission.
