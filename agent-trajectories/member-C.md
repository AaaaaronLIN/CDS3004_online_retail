# Agent-use trajectory — Member C  — Lim Man Tung Marcus (4592996)

**Group:** F · **CRN:** 234 · **Course:** CDS3004 Data Mining, Lingnan University, 2026/27 Term 1
**Role:** Churn modelling and evaluation lead
**Module:** 三分类器、CV、留出集、时间外验证、阈值与 lift（notebook S6）
**Presents:** 8（流失预测与评估）
**Harness / model:** DeepSeek Harness (deepseek-flash) · plus any other harness you personally used

> 这个文件是**证据**，不是日记。每条记录写清：你要什么（prompt）→ agent 给了什么 →
> **你**接受/否决/改了什么 → **你如何验证**（命令、数字、对比、artifact）。目标：到 12/06 有 4–6 条。
> 课件 P9 用 commits + agent 轨迹估每人工作量；只写你真正做过的事，不要复制别人的。
> 表格里已有一行“脚手架”记录（2026-11-11 全组共同完成），其余由你填写。

## Session log

| # | Date | Task / goal | Prompt used (short) | Agent proposal (2–5 sentences) | Human decision (accepted / rejected / changed + why) | Verification (command, number, comparison) | Artifact / commit |
|---|---|---|---|---|---|---|---|
| 0 | 2026-11-11 | Group scaffold: reproducible pipeline + report + deck | "Design and implement the full CDS3004 pipeline on UCI Online Retail and verify it runs top-to-bottom" | Agent produced notebook, 23 figures, 29 tables, metrics JSON, report draft, 20-slide deck | **Group decision:** accepted as scaffold, not final work; each member must verify their module (tasks below) | Notebook executed twice from a clean kernel: 0 errors, identical metrics.json (only runtime_sec differs) | scaffold commit |
| 1 | 2026-11-16 | Verify Section S6 baseline evaluation metrics (CV AUC, T1 Test AUC, T2 OOT AUC, and top-decile lift) | Show me how to run the Task 1 verification code cell in Section S6 | Agent provided a verification script targeting ../results/tables/ to load t08_model_comparison.csv and t09_lift_deciles.csv. Verified LogReg CV AUC 0.7593, DT 0.7397, RF 0.7505, T1 Test AUC 0.7227, T2 OOT AUC 0.7392, and top-decile lift 1.6916. Confirmed Logistic Regression generalizes better on out-of-time data than tree models. | Accepted as written; successfully executed code cell to cross-check local results against project benchmarks. | Executed notebook cell in Section S6; verified LogReg T2 OOT AUC = 0.7392 vs RF = 0.5947, confirming robust generalization. | notebooks/CDS3004_Project.ipynb |
| 2 | 2026-11-16 | Run threshold experiment shifting capacity cutoff from top-10% to top-20% high-risk customers | Show me how to run the threshold experiment code cell in Section S6 | Agent provided an evaluation function calculating precision, recall, F1, and lift at top-10% and top-20% risk percentiles. Results showed expanding outreach to top-20% increases total churners caught (recall) while moderating precision and lift. Recommended top-10% for strict budget constraints or top-20% for maximizing retention coverage. | Accepted; executed the controlled comparison cell locally and analyzed the trade-offs between precision and recall. | Evaluated top-10% (Lift: 1.6916) vs top-20% capacity threshold; verified increased capture rate for vulnerable customers. | notebooks/CDS3004_Project.ipynb |
| 3 | 2026-11-16 | Analyze business impact of False Negatives vs. False Positives under F1 optimal threshold | Draft S6 error analysis for False Negatives vs False Positives | Agent structured the business cost breakdown: False Negatives represent missed churners leading to high LTV loss and increased replacement CAC, whereas False Positives represent low-cost promotional vouchers sent to loyal customers. Concluded that the error ratio is acceptable given high potential customer lifetime value retention. | Accepted; documented the error analysis into the S6 Markdown cell and report structure. | Inspected confusion matrix outputs at threshold 0.2665; confirmed operational feasibility of error tolerance. | report/REPORT.md & notebooks/CDS3004_Project.ipynb |

## Verification summary

| Suggested task | Covered by | Key evidence |
|---|---|---|
| Reproduce the three evaluation numbers | Row 1 | CV AUC 0.759/0.740/0.751; T1 test AUC 0.723; T2 out-of-time AUC 0.739; top-decile lift 1.69 |
| Threshold experiment | Row 2 | compared the top-10% and top-20% capacity cut-offs on precision, recall and F1 |
| Explain the confusion matrix | Row 3 | false-negative versus false-positive business cost at the F1-optimal threshold |

All suggested tasks are covered by rows 1–3 above.
