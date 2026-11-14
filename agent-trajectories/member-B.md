# Agent-use trajectory — Member B  (name: ____)

**Group:** F · **CRN:** 234 · **Course:** CDS3004 Data Mining, Lingnan University, 2026/27 Term 1
**Role:** Feature engineering and segmentation lead
**Module:** 特征选择/变换、K-means 客户分层、距离度量（notebook S3–S5）
**Presents:** 6（特征工程）、7（客户分层）
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

### Task 1: 复现特征选择漏斗

**做什么：** 读取 results/tables/t05b_feature_evidence.csv：全特征验证 PR-AUC 0.6966 → 相关性过滤 0.6973 → 互信息 Top-12 0.7032 → RFE Top-10 0.7036。解释“提升很小但仍保留”的理由。

**要贴的证据：** 贴四段数字 + 你的解释（为什么小提升也值得做）。

### Task 2: 为 K=5 做辩护（这是答辩必问）

**做什么：** 读 results/tables/t06_cluster_metrics.csv：silhouette 在 K=2 最高（0.4223）、K=4 为 0.347、K=5 为 0.3279；但 K=5 的 bootstrap ARI 为 0.9699，且规则要求每段 ≥10%。写两句为什么 K=5 仍是最优选择。

**要贴的证据：** 贴出 K=2/4/5 三行数据 + 你的两句话辩护。

### Task 3: 比较三种距离度量

**做什么：** 复现 silhouette：cosine 0.3283 vs manhattan 0.2183 vs euclidean 0.1844，并检查 kNN 标签一致率。说明为什么 lookalike 客户/商品用 cosine。

**要贴的证据：** 记录三个数字 + 一句业务含义。


## 写好一条的标准

- 你能不看着屏幕讲出这个数字的含义。
- 至少有一条记录里，你**否决或修改**了 agent 的建议。
- 每条都能指向一个 artifact：表格某行、某张图、某个 commit、某条命令输出。
- 不编造；没做的任务直接删掉，不要留假记录。
