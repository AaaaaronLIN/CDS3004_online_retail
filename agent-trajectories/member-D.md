# Agent-use trajectory — Member D (name TBD)

**Group:** F · **CRN:** 234 · **Course:** CDS3004 Data Mining, Lingnan University, 2026/27 Term 1
**Role:** Feature engineering, churn models, evaluation (S4, S6)
**Module:** Feature selection/transformation, classification, held-out and out-of-time evaluation
**Harness / model:** DeepSeek Harness (deepseek-flash) · plus any other harness you personally used (ChatGPT, Claude Code, Copilot, Codex)

> This file is **evidence, not a diary**. For each task record: what you asked, what the agent gave,
> what **you** accepted / rejected / changed, and **how you verified** it. Aim for 4–6 entries by 6 Dec.
> The course estimates individual workload from commits **and** these trajectories (deck p.9).
> Only record work you actually did — do not paste a group conversation and call it yours.

## Session log

| # | Date | Task / goal | Prompt used (short) | Agent proposal (2–5 sentences) | Human decision (accepted / rejected / changed + why) | Verification (command, number, comparison) | Artifact / commit |
|---|---|---|---|---|---|---|---|
| 0 | 2026-11-11 | Group scaffold: build a reproducible analysis pipeline + report + slide deck | "Design and implement a complete data-mining pipeline for UCI Online Retail covering cleaning, snapshots, similarity, clustering, churn, rules, decision layer; verify it runs top-to-bottom" | Agent produced the pipeline notebook, 23 figures, 29 tables, metrics JSON, report draft and 14-slide deck | **Group decision:** accepted as a scaffold, not as final work; each member must independently verify their module (see tasks below) | Notebook re-executed from a clean kernel twice: 0 errors, identical `metrics.json` (only `runtime_sec` differs) | scaffold commit |
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |

## Your three verification tasks (do them, then fill the table)

### Task 1: Verify the feature-selection claim

**Do:** Read t05b_feature_evidence.csv: all features PR-AUC 0.6966, correlation filter 0.6973, MI top-12 0.7032, RFE top-10 0.7036. Explain why this is evidence (and why the gain is small).

**Evidence to paste:** Paste the four numbers and your interpretation.

### Task 2: Reproduce one model comparison and one threshold

**Do:** Confirm CV ROC-AUC logreg 0.7593 / DT 0.7397 / RF 0.7505; T1 test logreg AUC 0.7227, PR-AUC 0.6744; T2 out-of-time AUC 0.7392, PR-AUC 0.5947, lift@10% 1.6916. Then change the capacity from top-10% to top-20% and report precision/recall.

**Evidence to paste:** Record both threshold results and whether the decision changes.

### Task 3: Test the selected model against the benchmark

**Do:** Swap logreg for random forest as the deployment model (S8 scoring) and compare the resulting priority list and net campaign value. Say whether you would keep logreg.

**Evidence to paste:** Record the two net values and your recommendation.


## What "good" looks like

- You can explain the number without reading it off the screen.
- You have at least one entry where you **rejected or changed** the agent's suggestion.
- Every claim points to an artifact: a table row, a figure, a commit hash, or a command output.
- No invented entries. If you did not do a task, delete it rather than fake it.
