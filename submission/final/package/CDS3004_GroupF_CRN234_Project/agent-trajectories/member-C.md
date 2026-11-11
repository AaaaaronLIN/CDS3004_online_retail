# Agent-use trajectory — Member C (name TBD)

**Group:** F · **CRN:** 234 · **Course:** CDS3004 Data Mining, Lingnan University, 2026/27 Term 1
**Role:** Clustering, similarity, visualisation (S3, S5)
**Module:** K-means segmentation, distance metrics, figures
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

### Task 1: Re-run the K sweep and defend K=5

**Do:** Read results/tables/t06_cluster_metrics.csv. Note silhouette is highest at K=2 (0.4223) and K=4 (0.347), while K=5 has ARI 0.9699 and every segment >=10% of the base. Write two sentences explaining why K=5 is still the defensible choice.

**Evidence to paste:** Paste the K table rows you used and your two-sentence justification.

### Task 2: Compare distance metrics

**Do:** Reproduce the metric comparison: cosine silhouette 0.3283 vs manhattan 0.2183 vs euclidean 0.1844, plus kNN label agreement. Argue why cosine is used for lookalikes.

**Evidence to paste:** Record the three numbers and one sentence on the business meaning of a lookalike.

### Task 3: Audit the figures

**Do:** Open results/figures/f04, f05, f06, f11, f12. For each: axis labels, units, legend, and whether the caption matches. Fix at least one cosmetic issue and re-run the notebook.

**Evidence to paste:** List figure → issue → fix, and the commit hash.


## What "good" looks like

- You can explain the number without reading it off the screen.
- You have at least one entry where you **rejected or changed** the agent's suggestion.
- Every claim points to an artifact: a table row, a figure, a commit hash, or a command output.
- No invented entries. If you did not do a task, delete it rather than fake it.
