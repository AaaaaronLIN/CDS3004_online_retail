# Agent-use trajectory — Member D  — Huang Hao Lin (4455930)

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
| 0 | 2026-11-11 | Group scaffold: reproducible pipeline + report + deck | "Design and implement the full CDS3004 pipeline on UCI Online Retail and verify it runs top-to-bottom" | Agent produced notebook, 23 figures, 29 tables, metrics JSON, report draft, 20-slide deck | **Group decision:** accepted as scaffold, not final work; each member must verify their module (tasks below) | Notebook executed twice from a clean kernel: 0 errors, identical metrics.json (only runtime_sec differs) | scaffold commit |
| 1 | 2026-11-16 | Task 1 — reproduce the S7 headline numbers and explain why the mean lift is not the headline | "Read ONBOARDING.md (I am Huang Hao Lin) and re-check my module: 5,441 rules kept, 5,402 evaluated out of time, median holdout lift 12.174, 99.8% above lift 1, 593 business rules. Explain why mean 28.1957 must not be the headline; do not touch other members' modules." | Agent proposed headlining the mean holdout lift (28.1957) because it is larger than the median and "shows the rules generalise"; it also proposed executing the whole notebook and committing the regenerated results and artifact index. | **Rejected both.** The headline stays the median: 282 rules (5.2%) exceed lift 100, all of them symmetric variant pairs, and they carry 38.5% of the summed lift; without them the mean is 18.31, the 10%-trimmed mean 15.46 and the support-weighted mean 19.18, all bracketing 12.174. Also rejected committing regenerated artifacts (it would rewrite other members' tables) and asked for a stand-alone verification script instead. | `PYTHONPATH=.deps python code/verify_member_d.py` → 44 checks, 0 mismatches: 3,792 itemsets, 8,884 raw rules, 5,441 kept, 5,402 evaluated (27 + 12 excluded), median 12.174, 99.78% above lift 1, 593 business rules, top business rule 22697 → 22699. Distribution and tail in `s07_holdout_lift_quantiles.csv` / `s07_mean_lift_tail.csv`. | `code/verify_member_d.py`, `results/tables/s07_rule_headline.csv`, `s07_holdout_lift_quantiles.csv`, `s07_mean_lift_tail.csv`, `s07_variant_duplicates.csv` — commit `d904a92` |
| 2 | 2026-11-16 | Task 2 — hand-recompute the holdout lift of one rule | "Take GREEN REGENCY TEACUP (22697) → ROSES REGENCY TEACUP (22699) and recompute its holdout lift from the holdout baskets by hand; compare with the 21.5569 in the table." | Agent first returned 16.4, argued the holdout number could not be hand-computed from the exported table, and treated the training lift as a sufficient proxy; it also proposed reporting confidence and baseline as 0.79 and 0.34. | **Changed.** Holdout lift must divide by the holdout *consequent* support — 200/261 ÷ 296/8,327 — not by training support or by antecedent support. 16.4 is the training lift and cannot be presented as out-of-time evidence; the baseline is 0.03555, not 0.34. | 261 holdout baskets contain 22697, 200 contain both items, 296 contain 22699, N_HOLD = 8,327 → P(consequent given antecedent) = 0.7663, P(consequent) = 0.03555, holdout lift = 21.5569, identical to the t10 table (`s07_hand_lift_22697_22699.csv`). | `results/tables/s07_hand_lift_22697_22699.csv`, notebook markdown S7.4 — commit `d904a92` |
| 3 | 2026-11-16 | Task 3 — verify the similarity analysis | "Reproduce one cosine lookalike top-5 example and one product-product cosine top-5 example from the raw workbook, and say what each view is used for." | Agent read the numbers off `t04_lookalikes.csv` / `t05_similar_products.csv` and called that verification; it also suggested switching the metric to Euclidean because its kNN agreement was highest (0.9442), and described lookalikes as "customers who will churn together". | **Rejected / changed.** Reading a saved CSV is not verification, so the views were recomputed from the raw workbook. Euclidean's +0.2pp agreement does not outweigh its 0.14 silhouette deficit (0.1844 vs 0.3283), so cosine stays. Lookalikes are a targeting / cold-start device, not a churn predictor. | Rebuilt T2 (2,809 customers, 39.55% churn) and KMeans(5, seed 42): silhouettes 0.3283 / 0.2183 / 0.1844, kNN agreement 0.9359 / 0.9442 / 0.9419; all 15 lookalike IDs and scores exact (14646 → 14156 0.9877, 18102 → 17450 0.9833, 12415 → 17511 0.9640); 5 product neighbourhoods exact (85123A → 21733 0.3943, 22423 → 22699 0.3637, 85099B → 22386 0.4625, 47566 → 23298 0.3298, 84879 → 21136 0.3665). | `results/tables/s07_similarity_check.csv`, notebook markdown S3.5 — commit `7d0e2c7` |
| 4 | 2026-11-16 | Write the verification into the notebook and report, keep the artifact index honest | "Add short verification notes to my two sections and register the new tables, without adding pages to the report or regenerating other members' outputs." | Agent proposed a new report section "Verification", plus regenerating `results/ARTIFACTS.md` and re-executing the whole notebook so the numbers "come from the pipeline". | **Changed.** No new section (page budget): one Verification paragraph inside §7.3 and one inside §8.4. `ARTIFACTS.md` is notebook-generated, so only its Supplementary block is edited by hand, and the notebook gets two markdown cells instead of a full re-execution. | Notebook diff is +54 lines with no code cell changed; every number in the two paragraphs traces to an s07 table (21.5569, 12.174, 0.3283, 0.9359); `grep` for those values in report, notebook and CSVs agrees. | `agent-trajectories/member-D.md` (this file) plus commits `d904a92`, `7d0e2c7` |

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
