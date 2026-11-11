# Agent-use trajectory — Member A (name TBD)

**Group:** F · **CRN:** 234 · **Course:** CDS3004 Data Mining, Lingnan University, 2026/27 Term 1
**Role:** Lead / problem definition / report editor / main speaker
**Module:** Problem definition, solution design, report consistency, rehearsal
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

### Task 1: Cross-check every number in the report against results/metrics.json

**Do:** Open report/REPORT.md and results/metrics.json; verify at least 10 filled values (abstract, §6.3, §6.4, §9). Expected: 2,716 / 0.5044 / 2,809 / 0.3955 / 0.7227 / 0.7392 / 0.5947 / 1.6916 / 5,441 / 12.174.

**Evidence to paste:** Paste the comparison table (report sentence → JSON key → value) into this log.

### Task 2: Challenge one claim and change it

**Do:** Pick one statement you disagree with (e.g. the K=5 justification or the ROI framing), change the wording in REPORT.md, and say why.

**Evidence to paste:** Record the before/after sentence + your reasoning.

### Task 3: Own the rubric map and the run-through

**Do:** Walk project-management/RUBRIC-MATRIX.md line by line with the report PDF; confirm each of the 11 project items and 7 presentation items has evidence. Then time a full rehearsal.

**Evidence to paste:** Record which evidence you could not find, and the rehearsal times per speaker.


## What "good" looks like

- You can explain the number without reading it off the screen.
- You have at least one entry where you **rejected or changed** the agent's suggestion.
- Every claim points to an artifact: a table row, a figure, a commit hash, or a command output.
- No invented entries. If you did not do a task, delete it rather than fake it.
