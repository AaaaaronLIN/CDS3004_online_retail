# Agent-use trajectory — Member D  (name: ____)

**Group:** F · **CRN:** 234 · **Course:** CDS3004 Data Mining, Lingnan University, 2026/27 Term 1
**Role:** Association rules and similarity lead
**Module:** FP-Growth 关联规则、holdout 验证、相似度/距离（notebook S3, S7）
**Presents:** 9（关联规则）、10（相似度）
**Harness / model:** DeepSeek Harness (deepseek-flash) · plus any other harness you personally used

> 这个文件是**证据**，不是日记。每条记录写清：你要什么（prompt）→ agent 给了什么 →
> **你**接受/否决/改了什么 → **你如何验证**（命令、数字、对比、artifact）。目标：到 12/06 有 4–6 条。
> 课件 P9 用 commits + agent 轨迹估每人工作量；只写你真正做过的事，不要复制别人的。
> 表格里已有一行“脚手架”记录（2026-11-11 全组共同完成），其余由你填写。

## Session log

| # | Date | Task / goal | Prompt used (short) | Agent proposal (2–5 sentences) | Human decision (accepted / rejected / changed + why) | Verification (command, number, comparison) | Artifact / commit |
|---|---|---|---|---|---|---|---|
| 0 | 2026-11-11 | Group scaffold: reproducible pipeline + report + deck | "Design and implement the full CDS3004 pipeline on UCI Online Retail and verify it runs top-to-bottom" | Agent produced notebook, 23 figures, 29 tables, metrics JSON, report draft, 14-slide deck | **Group decision:** accepted as scaffold, not final work; each member must verify their module (tasks below) | Notebook executed twice from a clean kernel: 0 errors, identical metrics.json (only runtime_sec differs) | scaffold commit |
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |

## 你的三个验证任务（做完把结果填进上表）

### Task 1: 复现规则头条数字，并解释为什么不报 mean lift

**做什么：** 核对：5,441 条规则保留、5,402 条在后续 holdout 上被评估、median holdout lift 12.174、99.8% 保持 lift>1、593 条 business rules（support≥1%、lift≥2）。解释 mean holdout lift 28.1957 为什么不能当头条（多为同款不同色的稀有变体）。

**要贴的证据：** 贴数字 + 两句解释。

### Task 2: 拿一条规则手工复算 holdout lift

**做什么：** 选一条规则（例如 GREEN REGENCY TEACUP → ROSES REGENCY TEACUP，support 3.4%、lift 16.4、holdout lift 21.6），按 holdout 数据重算：P(consequent|antecedent) / P(consequent)。

**要贴的证据：** 贴你的手算过程与结果，和表格里的 21.6 对比。

### Task 3: 核对相似度分析

**做什么：** 复现：cosine 距离的 lookalike 客户 top-5 示例、商品-商品余弦 top-5；说明“相似客户”和“相似商品”分别用在哪（冷启动/替代品推荐）。

**要贴的证据：** 贴一个 lookalike 例子 + 一个相似商品例子 + 各一句用途。


## 写好一条的标准

- 你能不看着屏幕讲出这个数字的含义。
- 至少有一条记录里，你**否决或修改**了 agent 的建议。
- 每条都能指向一个 artifact：表格某行、某张图、某个 commit、某条命令输出。
- 不编造；没做的任务直接删掉，不要留假记录。
