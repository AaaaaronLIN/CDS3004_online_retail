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
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |

## 你的三个验证任务（做完把结果填进上表）

### Task 1: 复现三组关键评估数字

**做什么：** 核对：5 折 CV ROC-AUC logreg 0.7593 / DT 0.7397 / RF 0.7505；T1 测试集 logreg AUC 0.7227、PR-AUC 0.6744；T2 时间外 AUC 0.7392、PR-AUC 0.5947、top-10% lift 1.6916。用 val PR-AUC（0.7079）解释为什么最终选 logreg 而不是 RF。

**要贴的证据：** 贴数字 + 一句话说明“为什么不是更花哨的模型”。

### Task 2: 阈值实验：top-10% 改成 top-20%

**做什么：** 当前 F1 最优阈值 0.2665、容量阈值 0.7382。把营销容量改成 top-20%，记录 precision/recall 怎么变、决策是否改变。

**要贴的证据：** 贴两行对比（top-10% vs top-20%）+ 你的建议。

### Task 3: 解释混淆矩阵的业务含义

**做什么：** 在 F1 阈值下画/读混淆矩阵：false negative = 该挽回没联系到的人；false positive = 白花的联系成本。给出你对“这个错误比例能否接受”的判断。

**要贴的证据：** 贴混淆矩阵数字 + 两句判断。


## 写好一条的标准

- 你能不看着屏幕讲出这个数字的含义。
- 至少有一条记录里，你**否决或修改**了 agent 的建议。
- 每条都能指向一个 artifact：表格某行、某张图、某个 commit、某条命令输出。
- 不编造；没做的任务直接删掉，不要留假记录。
