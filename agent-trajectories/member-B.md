# Agent-use trajectory — Member B  — Weng Zhi Chao (4589896)

**Group:** F · **CRN:** 234 · **Course:** CDS3004 Data Mining, Lingnan University, 2026/27 Term 1
**Role:** Feature engineering and segmentation lead
**Module:** 特征选择/变换、K-means 客户分层、距离度量（notebook S3–S5）
**Presents:** slides 7–10（pipeline、特征工程、K-means 分层、分层画像）
**Harness / model:** DeepSeek Harness (deepseek-flash) · plus any other harness you personally used

> 这个文件是**证据**，不是日记。每条记录写清：你要什么（prompt）→ agent 给了什么 →
> **你**接受/否决/改了什么 → **你如何验证**（命令、数字、对比、artifact）。目标：到 12/06 有 4–6 条。
> 课件 P9 用 commits + agent 轨迹估每人工作量；只写你真正做过的事，不要复制别人的。
> 表格里已有一行“脚手架”记录（2026-11-11 全组共同完成），其余由你填写。

## Session log

| # | Date | Task / goal | Prompt used (short) | Agent proposal (2–5 sentences) | Human decision (accepted / rejected / changed + why) | Verification (command, number, comparison) | Artifact / commit |
|---|---|---|---|---|---|---|---|
| 0 | 2026-11-11 | Group scaffold: reproducible pipeline + report + deck | "Design and implement the full CDS3004 pipeline on UCI Online Retail and verify it runs top-to-bottom" | Agent produced notebook, 23 figures, 29 tables, metrics JSON, report draft, 20-slide deck | **Group decision:** accepted as scaffold, not final work; each member must verify their module (tasks below) | Notebook executed twice from a clean kernel: 0 errors, identical metrics.json (only runtime_sec differs) | scaffold commit |
| 1 | 2026-11-15 | Inspect & verify distance metrics and initial features (S3) | "Inspect S3 distance metrics and initial behavioral features in CDS3004_Project.ipynb" | Agent explained log1p + StandardScaler preprocessing and compared Euclidean, Cosine, and Manhattan metrics on T1/T2 snapshots. | Accepted: verified S3 outputs match expected matrix shapes (2809x15) and reference K=5 sizes. | Executed cells [12]-[13] in Jupyter; confirmed 0 errors and committed initial feature inspection. | `88ccf3c` |
| 2 | 2026-11-15 | Validate feature selection & PR-AUC pipeline (S4) | "Check S4 feature selection pipeline and summarize PR-AUC validation without leakage" | Agent verified scikit-learn Pipeline encapsulation (log1p + StandardScaler + MI/correlation filter) and drafted S4 summary markdown. | Accepted & added summary block: confirmed validation PR-AUC as headline metric for class imbalance. | Executed S4 cells (train 1,901 / val 407 / test 408); validation PR-AUC 0.6966 (all features) → 0.7036 (selected), matching `results/tables/t05b_feature_evidence.csv`. | `0b76782` |
| 3 | 2026-11-15 | Document K-means clustering & K=5 rationale (S5) | "Analyze S5 K-means clustering and justify why K=5 is selected over K=2..8" | Agent summarized silhouette separation, cross-snapshot ARI stability, and business interpretability for 5 customer segments. | Accepted & documented: added K=5 rationale markdown block at the end of S5. | Executed S5 cells: silhouette 0.3279 at K=5, bootstrap ARI 0.9699, segments 755/582/520/535/417 (all ≥10%), matching `t06_cluster_metrics.csv`. | `0407f8d` |
| 4 | 2026-11-16 | Synthesize B module key takeaways & retention plan in report | "Draft concise key takeaways on leakage-free feature engineering, K=5 segmentation, and retention actions for REPORT.md" | Agent drafted structured takeaways covering Pipeline leakage prevention, K=5 stability, and segment-specific retention actions. | Accepted & integrated: added takeaways and action plan into report/REPORT.md. | Verified the rendered report: takeaways in §5 and retention actions in §9.6; pushed `f32d2d6`. | `f32d2d6` |
| 5 | 2026-11-16 | Refine S3 distance metric & S4 correlation filter documentation | "Document Euclidean vs Cosine trade-offs in S3 and multicollinearity pruning in S4.2" | Agent provided technical notes explaining Euclidean distance in the standardized feature space (used for clustering) versus cosine similarity (used for lookalikes/products), and why correlation pruning stabilizes the models. | Accepted & added to notebook: inserted explanatory markdown cells in S3 and S4.2. | Verified markdown cells in S3 and S4.2, no code or result changes; pushed `86aaa88` and `a1ce2ac`. | `86aaa88`, `a1ce2ac` |

## Verification summary

| Suggested task | Covered by | Key numbers checked |
|---|---|---|
| Feature-selection funnel | Row 2 | PR-AUC 0.6966 → 0.6973 → 0.7032 → 0.7036 |
| K=5 defence | Row 3 | silhouette 0.3279 at K=5; bootstrap ARI 0.9699; every segment ≥10% |
| Distance metrics | Rows 1 and 5 | cosine 0.3283 > manhattan 0.2183 > euclidean 0.1844; kNN agreement 0.936–0.944 |

All three verification tasks are covered by rows 1–3; rows 4–5 record the report and documentation work that followed.
