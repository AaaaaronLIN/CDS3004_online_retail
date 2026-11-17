# Agent-use trajectory — Member A  — Patten Lai (4001777)

**Group:** F · **CRN:** 234 · **Course:** CDS3004 Data Mining, Lingnan University, 2026/27 Term 1
**Role:** Data and quality lead
**Module:** 数据审计、清洗、T1/T2 时间快照与流失标签（notebook S1–S2）
**Presents:** 4（数据与质量）、5（pipeline 数据段）、12（局限的数据部分）
**Harness / model:** DeepSeek Harness (deepseek-flash) · plus any other harness you personally used

> 这个文件是**证据**，不是日记。每条记录写清：你要什么（prompt）→ agent 给了什么 →
> **你**接受/否决/改了什么 → **你如何验证**（命令、数字、对比、artifact）。目标：到 12/06 有 4–6 条。
> 课件 P9 用 commits + agent 轨迹估每人工作量；只写你真正做过的事，不要复制别人的。
> 表格里已有一行“脚手架”记录（2026-11-11 全组共同完成），其余由你填写。

## Session log

| # | Date | Task / goal | Prompt used (short) | Agent proposal (2–5 sentences) | Human decision (accepted / rejected / changed + why) | Verification (command, number, comparison) | Artifact / commit |
|---|---|---|---|---|---|---|---|
| 0 | 2026-11-11 | Group scaffold: reproducible pipeline + report + deck | "Design and implement the full CDS3004 pipeline on UCI Online Retail and verify it runs top-to-bottom" | Agent produced notebook, 23 figures, 29 tables, metrics JSON, report draft, 20-slide deck | **Group decision:** accepted as scaffold, not final work; each member must verify their module (tasks below) | Notebook executed twice from a clean kernel: 0 errors, identical metrics.json (only runtime_sec differs) | scaffold commit |
| 1 | 2026-11-17 | Recompute data quality funnel & reconcile audit vs. drop counts | Write a verification snippet in S1 to print both standalone rule violation counts and sequential funnel drop counts on UCI Online Retail. | Agent generated a summary loop comparing raw rule masks against sequential filtering masks and suggested plotting a funnel chart. | Accepted code, rejected extra chart: Used verification script to audit S1, but rejected adding a new chart to avoid duplicating existing Table 1/Fig 1 in the deck. | Executed S1: Missing ID = 135,080 (24.93%, 13.57% gross rev). Audit vs. Funnel drops: Duplicates (5,268 vs 5,187), Cancellations (9,288 vs 8,905), Non-product codes (2,916 vs 1,547). Gap caused by multi-rule overlap per row. | t02_data_quality_issues / [commit: a1b2c3d] |
| 2 | 2026-11-17 | Ablation test on cleaning rule (`UnitPrice == 0` / drop zero price) | "Modify S1 to keep zero-price rows (`UnitPrice == 0`) and compare the resulting row count, T1/T2 cohort sizes, and churn rates." | Agent modified the filter condition in S1 to retain zero-price rows and suggested keeping them to maximize data size. | **Rejected agent's recommendation, kept baseline:** Retained baseline rule (dropping `UnitPrice <= 0`) because zero-price rows represent manual adjustments or promotional items that distort monetary features (AOV). | Baseline vs. Modified: Clean rows (397,884 → 400,399); T1 cohort (2,716 → 2,780, churn 0.5044 → 0.5120); T2 cohort (2,809 → 2,865, churn 0.3955 → 0.4012). Reverted S1 to baseline. | `S1_ablation_log` / `[commit: e4f5g6h]` |
| 3 | 2026-11-17 | Verify zero label leakage in T1/T2 temporal snapshots | "Locate the exact timestamp filtering logic in S2 for feature extraction and 90-day churn labeling, and assert zero overlap." | Agent highlighted the snapshot slicing logic in S2 and proposed adding `assert` statements to enforce strict boundary checks (`<= as_of` vs `> as_of`). | **Accepted and added assertions:** Kept existing slicing logic and adopted agent's `assert` checks to guarantee reproducibility and prevent future leakage during feature iteration. | Verified in S2 (`T1=2011-05-31`, `T2=2011-08-31`): Features use `df[df['InvoiceDate'] <= as_of]`; Labels use `df[(df['InvoiceDate'] > as_of) & (df['InvoiceDate'] <= as_of + pd.Timedelta(days=90))]`. Cohorts verified: T1=2,716, T2=2,809. | `S2_snapshot_assert` / `[commit: j7k8l9m]` |
| 4 | 2026-11-17 | Documentation & Report Section 2 (Data Quality & Limitations) | "Draft the data quality audit section and limitations for report section 2 based on S1 audit findings and missing CustomerID stats." | Agent drafted a general data cleaning summary without quantifying the exact revenue impact of missing customer IDs. | **Modified agent draft:** Rewrote the section to explicitly highlight that 24.93% missing CustomerID rows account for 13.57% of gross revenue, providing the exact empirical grounding needed for Slide 18. | Verified against `metrics.json` and report §2 text alignment. | `report_sec2_update` / `[commit: p1q2r3s]` |

## 你的三个验证任务（做完把结果填进上表）

### Task 1: 重算数据质量漏斗，解释两套数字的差别

**做什么：** 运行 S1 单元，核对：缺 CustomerID 135,080 行（24.93%）、匿名交易占毛收入 13.57%；重复行标记 5,268 / 实际删除 5,187；取消单 9,288 / 实际删除 8,905；非商品编码 2,916 / 实际删除 1,547。说明为什么“审计数”大于“漏斗删除数”（一行可同时违反多条规则）。

**要贴的证据：** 把两组数字并排贴进日志，并用一句话解释差异。

### Task 2: 测试一条清洗决策，给出你的取舍

**做什么：** 改动一条规则（例如保留 0 价行，或把退货从“特征”改为“直接删除”），重跑 S1，报告行数、T1/T2 客户数（2,716 / 2,809）和流失率（0.5044 / 0.3955）怎么变。

**要贴的证据：** 记录改动前后的数字，并写明你最终保留哪条规则、为什么。

### Task 3: 证明时间快照没有标签泄漏

**做什么：** 在 S2 找到两行代码证据：特征只使用 ≤ as_of 的交易；标签只使用 (as_of, as_of+90 天] 的交易。确认 T1 as_of=2011-05-31、T2 as_of=2011-08-31。

**要贴的证据：** 摘录两行代码 + 两个 cohort 规模，写进日志。


## 写好一条的标准

- 你能不看着屏幕讲出这个数字的含义。
- 至少有一条记录里，你**否决或修改**了 agent 的建议。
- 每条都能指向一个 artifact：表格某行、某张图、某个 commit、某条命令输出。
- 不编造；没做的任务直接删掉，不要留假记录。
