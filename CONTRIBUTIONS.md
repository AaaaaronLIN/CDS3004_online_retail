# Contributions — Who Owns What

**Project:** From Transactions to a Customer Operating System (CDS3004 Data Mining group project)
**Team:** Group F — LIN Xiaotong (4589755), Patten Lai (4001777), Weng Zhi Chao (4589896), Lim Man Tung Marcus (4592996), Huang Hao Lin (4455930)
**Purpose of this file:** record each member's role, the rubric items they own, the code and report areas they are responsible for, the slides they present and the commit areas the workload evidence should show. It also lists the per-member evidence the course expects: **meaningful GitHub commits plus a personal agent-use trajectory**.

**Status:** names and student IDs are filled in. Add each member's GitHub username and contact once the accounts are confirmed (only LIN Xiaotong's is known: `AaaaaronLIN`). The course assesses workload roughly from GitHub commits and agent trajectories, so the repository commits must be authored by the real members.

## 1. Member labels, names and accounts

| Label | Full name | Student ID | GitHub username | Preferred contact |
|---|---|---|---|---|
| A | Patten Lai | 4001777 | — | — |
| B | Weng Zhi Chao | 4589896 | — | — |
| C | Lim Man Tung Marcus | 4592996 | — | — |
| D | Huang Hao Lin | 4455930 | — | — |
| E (Host) | LIN Xiaotong | 4589755 | AaaaaronLIN | — |

## 2. Ownership table

| Member | Role | Rubric items owned (22% rubric) | Code / notebook / artifact areas | Slides | Expected commit areas |
|---|---|---|---|---|---|
| **Patten Lai (4001777)** | Data and quality lead | Collect and load datasets, assign feature characteristics, handle missing and noisy data (LO5); data visualisation (data part) | Notebook S1–S2 (data-quality audit, cleaning funnel, returns ledger, T1/T2 snapshots); `results/tables/t02_data_quality_issues.csv`, `t03_cleaning_decisions.csv`, `t02_cohort_summary.csv`; `results/figures/f01_data_quality_overview.png`; report §2 | 4–6, 18 (limitations) | `data/README.md`, notebook S1–S2 cells, `results/tables/t02*`, `t03*`, report §2 |
| **Weng Zhi Chao (4589896)** | Feature engineering and segmentation lead | Apply data-mining techniques to select features (LO5); advanced feature transformations (LO5); data visualisation (feature/segment part) | Notebook S3 (distance comparison support) and S4–S5 (16 features, correlation/MI/RFE, K-means, profiles); `t03_distance_metrics.csv`, `t04_feature_dictionary.csv`, `t05_feature_selection.csv`, `t05b_feature_evidence.csv`, `t06_cluster_metrics.csv`, `t07_segment_profiles.csv`; figures `f02`–`f08`; report §4–§5 | 6–7 | Notebook S4–S5 cells, `results/tables/t04*`–`t07*`, feature/segmentation figures, report §4–§5 |
| **Lim Man Tung Marcus (4592996)** | Churn modelling and evaluation lead | Use data-mining techniques to learn models (LO4); use the right techniques to evaluate learnt models (LO6) | Notebook S6 (three classifiers, 70/15/15 split, 5-fold CV, validation PR-AUC selection, thresholds, held-out and out-of-time evaluation, lift); `t08_model_metrics.csv`, `t09_lift_deciles.csv`, `s06_threshold_analysis.csv`; figures `f07`–`f09`; report §6 | 8 | Notebook S6 cells, `results/tables/t08*`, `t09_lift_deciles.csv`, model figures, report §6 |
| **Huang Hao Lin (4455930)** | Association rules and similarity lead | Apply different data-mining techniques for various data (LO3) | Notebook S3 and S7 (distance metrics, lookalikes, similar products, FP-Growth mining, holdout validation); `t03_distance_metrics.csv`, `t04_lookalikes.csv`, `t05_similar_products.csv`, `t09_top_rules.csv`, `t10_association_rules.csv`; figures `f10`, `f11`; report §7–§8 | 9–10 | Notebook S3/S7 cells, `results/tables/t03*`, `t04_lookalikes.csv`, `t05_similar_products.csv`, `t09_top_rules.csv`, `t10_association_rules.csv`, `f10*`, `f11*`, report §7–§8 |
| **LIN Xiaotong (4589755)** | Integration, decision framework and repository lead | Problem definition (with team); solution design (with team); interpret results correctly and critically (LO7); deliver learnt models for decision making (LO7); presentation and repository compliance | Notebook S8–S9 (T2 scoring, segment × risk matrix, priority list, ROI scenarios, metrics/ARTIFACTS generation), README, CONTRIBUTIONS, submission checklist, agent-log templates; `t10_decision_table.csv`, `t11_top200_targets.csv`, `t12_segment_risk_matrix.csv`, `t13_action_table.csv`, `t14_roi_assumptions.csv`, `t15_priority_list_summary.csv`; figures `f12`, `f13`; report §1, §3, §9–§10, §13 | 1–3, 7, 16–17, 19–20 | `README.md`, `CONTRIBUTIONS.md`, notebook S8–S9 cells, `results/tables/t10*`–`t15*`, `f12*`, `f13*`, report §1/§3/§9–§13, `agent-logs/README.md`, `submission/*` |

Rubric items 1 (problem definition) and 2 (solution design) are team-owned: LIN Xiaotong drafts, but all five review and sign off. Rubric item 6 (data visualisation) is distributed across the five members as shown; the presentation and report make the distribution explicit.

## 3. Commit and trajectory evidence (course requirement)

The course estimates each student's workload roughly from **GitHub commits** and **agent trajectories**, and the project rubric rewards a documented human–agent workflow. Each member must therefore produce both.

**Commit requirements (per member)**

- At least **three meaningful commits spread across at least two weeks** — not one large commit at the end.
- Commit messages identify the section and artifact, e.g. `S5: K-means stability check and segment profiling` or `report: §6 threshold and lift revisions`.
- Commits touch the areas listed in §2. For shared files (notebook, report), make small section-scoped commits so the history shows individual work.
- No bulk "final submission" commit from one account containing everyone's work; those undermine the workload estimate.
- Before submission, capture `git shortlog -sne` and per-author `git log --oneline --author="<name>"` output as evidence.

**Trajectory requirements (per member)**

- One `agent-logs/MemberX_agent-trajectory.md` with at least three dated entries: prompt, agent proposal, human review/decision (accepted/rejected/changed and why), implementation (files + commit hash), verification (how checked) and artifact/evidence.
- At least one entry where the member **rejected or changed** the agent's proposal.
- At least one entry where an agent output was **verified independently** (fresh-kernel re-run, hand recomputation, code review, cross-artifact check).
- Public share links (if used) collected in `agent-logs/LINKS.md` and tested in an incognito window; a local transcript fallback in `agent-logs/raw/`.

## 4. Presentation roles

| Role | Owner | Notes |
|---|---|---|
| Opening, executive summary, question, pipeline, decision framework, process, closing | LIN Xiaotong | Slides 1–3, 7, 16–17, 19–20; keeps the 20-minute timing |
| Data, cleaning, temporal design, limitations | Patten Lai | Slides 4–6, 18 |
| Feature engineering, segmentation, profiles | Weng Zhi Chao | Slides 8–10 |
| Churn modelling, evaluation, error analysis | Lim Man Tung Marcus | Slides 11–13 |
| Association rules and similarity | Huang Hao Lin | Slides 14–15 |
| Timekeeper / slide operator | Patten Lai (backup Huang Hao Lin) | Holds the timer; signals at 30 s before each slide budget |
| Backup presenter for any slide | every member | Each member knows the whole deck in case of illness |

## 5. Cross-checks before submission

| Check | Owner |
|---|---|
| Every member has ≥3 meaningful commits spread over ≥2 weeks | LIN Xiaotong |
| Every member has a complete trajectory file and (if used) a working public link | Member D (collects), each member (writes) |
| Names and student IDs appear in the report, this file, and the PDF | Member E |
| Report/slides/README numbers match `results/metrics.json` after the fill step | Member C |
| Notebook runs from a fresh kernel and regenerates every artifact | Member C |
| ZIP built, checked and uploaded | Member E (second check by any member) |
| Everyone reads the final PDF and slides and confirms their own contribution line | all members |

## 6. Sign-off

By signing, each member confirms that the contribution descriptions above are accurate and that they have reviewed the final report, slides and repository.

| Member | Signature / confirmation (name) | Date |
|---|---|---|
| Member A | | |
| Member B | | |
| Member C | | |
| Member D | | |
| Member E | | |
