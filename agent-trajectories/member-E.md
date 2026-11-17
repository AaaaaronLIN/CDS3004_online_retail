# Agent-use trajectory — Member E  — LIN Xiaotong (4589755)

**Group:** F · **CRN:** 234 · **Course:** CDS3004 Data Mining, Lingnan University, 2026/27 Term 1
**Role:** Integration, decision framework and repository lead
**Module:** 决策层（segment×risk、优先级、ROI）、指标汇总、仓库与提交合规（notebook S8–S9）
**Presents:** 1–3（开场/问题/框架）、5（pipeline 总览）、11（决策与 ROI）、13–14（贡献/结尾）
**Harness / model:** DeepSeek Harness (deepseek-flash) · plus any other harness you personally used

> 这个文件是**证据**，不是日记。每条记录写清：你要什么（prompt）→ agent 给了什么 →
> **你**接受/否决/改了什么 → **你如何验证**（命令、数字、对比、artifact）。目标：到 12/06 有 4–6 条。
> 课件 P9 用 commits + agent 轨迹估每人工作量；只写你真正做过的事，不要复制别人的。
> 表格里已有一行“脚手架”记录（2026-11-11 全组共同完成），其余由你填写。

## Session log

| # | Date | Task / goal | Prompt used (short) | Agent proposal (2–5 sentences) | Human decision (accepted / rejected / changed + why) | Verification (command, number, comparison) | Artifact / commit |
|---|---|---|---|---|---|---|---|
| 0 | 2026-11-11 | Group scaffold: reproducible pipeline + report + deck | "Design and implement the full CDS3004 pipeline on UCI Online Retail and verify it runs top-to-bottom" | Agent produced notebook, 23 figures, 29 tables, metrics JSON, report draft, 20-slide deck | **Group decision:** accepted as scaffold, not final work; each member must verify their module (tasks below) | Notebook executed twice from a clean kernel: 0 errors, identical metrics.json (only runtime_sec differs) | scaffold commit |
| 1 | 2026-11-14 | Reproduce the pipeline end-to-end; ROI-assumption sensitivity experiment | "Run the notebook; change base to save_rate 5%, contact cost GBP 12, margin 30%; re-run S8 and report the change" | Agent explained where to edit and what to expect | Accepted as a controlled experiment, repository restored afterwards | PIPELINE COMPLETE in 28.1s; T2 OOT AUC 0.7392; net GBP 33,799.89 -> 12,771.38 (ROI 532.1%); `git restore notebooks results` | commit |
| 2 | 2026-11-14 | Controlled model-swap experiment: random forest vs the selected logistic regression in the decision layer | "Force BEST_MODEL='random_forest' in S8.1, re-run the decision layer, and compare the priority list and net campaign value with the logreg baseline" | Agent showed the one-line override and predicted lower top-decile precision | Accepted as a controlled experiment; change removed afterwards | logreg: p_churn_targeted 0.669, value/saved GBP 2,645.58, net GBP 33,799.89. RF: 0.6263, GBP 1,910.75, net GBP 22,335.40 - precision and targeted value both fall, confirming the logreg choice; restored with `git restore notebooks results code/pipeline_notes.md` | commit |
| 3 | 2026-11-17 | Run the submission-compliance audit for the final ZIP | "Check the repo and ZIP against the P15 checklist: public URL, PDF-only report, five agent trajectories, code folder; report any gaps" | Agent inspected the repo, presentation assets, report and ZIP, and listed the remaining gaps (Member A commits, sign-offs) | Accepted the checklist; fixed the report placement and the ZIP report folder, and added the alternate-account note | Repo public; `git status` clean; ZIP has README with URL, code/, report PDF only and five trajectories; deck 24 pages | `0a86d9f` |


## Verification summary

| Suggested task | Covered by | Key evidence |
|---|---|---|
| Recompute the ROI scenarios and break-even | Row 1 | base net GBP 33,799.89; pessimistic GBP 12,771.38; break-even 0.452% vs 4.538% |
| Check the model choice in the decision layer | Row 2 | random forest top-decile precision 0.6263 and net GBP 22,335.40 vs logreg 0.669 / GBP 33,799.89; logreg retained |
| Run the submission-compliance audit | Row 3 | repo public, report PDF only, five trajectories present, ZIP structure checked |

All suggested tasks are covered by rows 1–3 above.
