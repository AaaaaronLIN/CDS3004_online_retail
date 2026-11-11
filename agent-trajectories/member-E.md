# Agent-use trajectory — Member E (name TBD)

**Group:** F · **CRN:** 234 · **Course:** CDS3004 Data Mining, Lingnan University, 2026/27 Term 1
**Role:** Association rules, decision layer, repository (S7–S8)
**Module:** FP-Growth rules, holdout validation, segment x risk decision, ROI, repo management
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

### Task 1: Re-derive the rules headline

**Do:** Confirm 5,441 rules retained, 5,402 evaluated on the later holdout, median holdout lift 12.174, 99.8% keep lift > 1, 593 business rules (support>=1%, lift>=2). Explain why the mean holdout lift (28.1957) must not be headlined.

**Evidence to paste:** Paste the numbers plus your two-sentence explanation.

### Task 2: Rebuild the ROI scenarios

**Do:** Confirm base net GBP 33,799.89 (optimistic bound), validated net GBP 14,802.58, random-200 GBP 1,925.76, uplift GBP 31,874.13, break-even save rate 0.452% targeted vs 4.538% random. Then redo the calculation with contact cost GBP 12 and save rate 5%.

**Evidence to paste:** Paste your recomputation and say whether the campaign still pays.

### Task 3: Own the repository and the submission checklist

**Do:** Create the public repo, push the scaffold, confirm it opens in an incognito window, then walk submission/SUBMISSION-CHECKLIST.md and list what is still missing.

**Evidence to paste:** Record the repo URL, the incognito check result, and the gap list.


## What "good" looks like

- You can explain the number without reading it off the screen.
- You have at least one entry where you **rejected or changed** the agent's suggestion.
- Every claim points to an artifact: a table row, a figure, a commit hash, or a command output.
- No invented entries. If you did not do a task, delete it rather than fake it.
