# Agent-use trajectory — Member B (name TBD)

**Group:** F · **CRN:** 234 · **Course:** CDS3004 Data Mining, Lingnan University, 2026/27 Term 1
**Role:** Data engineering (S1–S2)
**Module:** Data-quality audit, cleaning, snapshots, churn labels
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

### Task 1: Recompute the data-quality funnel yourself

**Do:** Run the S1 cells and compare to the audit: 24.93% missing CustomerID (135,080 rows), 13.57% of gross revenue anonymous, 5,268 duplicate rows flagged / 5,187 removed, 9,288 cancellations / 8,905 removed, 2,916 non-product lines / 1,547 removed. Explain why audit counts exceed funnel removals (one line can violate several rules).

**Evidence to paste:** Paste the two numbers side by side and your explanation.

### Task 2: Test one cleaning decision

**Do:** Change one rule (e.g. keep zero-price lines, or drop returns instead of using them as a feature), re-run S1 and report what changes in row count and in the churn cohort sizes.

**Evidence to paste:** Record the numbers before/after and whether you would keep the rule.

### Task 3: Verify the temporal snapshots are leakage-free

**Do:** In S2, confirm features use only dates <= as_of and the label only dates in (as_of, as_of+90d]. Check T1 (as_of 2011-05-31) and T2 (as_of 2011-08-31) and the label windows.

**Evidence to paste:** Quote the two code lines that enforce it, plus cohort sizes 2,716 / 2,809.


## What "good" looks like

- You can explain the number without reading it off the screen.
- You have at least one entry where you **rejected or changed** the agent's suggestion.
- Every claim points to an artifact: a table row, a figure, a commit hash, or a command output.
- No invented entries. If you did not do a task, delete it rather than fake it.
