# 复现指南（Host / Member E 专用）

> 目标：**30 分钟跑通 → 60 分钟看懂你的模块 → 90 分钟做 2 个受控实验**。
> 你不是要重写分析，而是要能回答"它是怎么跑起来的、改一个假设会怎样、数字从哪来"。
> 所有命令在 macOS / Linux 通用；Windows 把 `python3` 换成 `python`。

---

## 0. 环境准备（一次性，约 5 分钟）

```bash
git clone https://github.com/AaaaaronLIN/CDS3004_online_retail.git
cd CDS3004_online_retail

python3 -m pip install -r requirements.txt
python3 data/download_data.py        # 23MB 数据，带行数校验
```

> 没有本地环境也行：把 `notebooks/CDS3004_Project.ipynb` 传到 Google Colab，
> 把 `Online_Retail.xlsx` 上传到 `data/`，然后 Runtime → Run all。

---

## 1. 跑通全流程（约 1 分钟）

```bash
python3 -m jupyter nbconvert --to notebook --execute --inplace \
        notebooks/CDS3004_Project.ipynb
```

或者打开 Jupyter，逐个 cell 执行（推荐第一次这样做，能看清中间输出）。

**跑完你应该看到这些终端输出**（数值是验收标准，对不上说明环境有问题）：

```
raw rows 541,909 -> clean rows 391,150; customers 4,334
T1 n=2,716 churn=0.5044 | T2 n=2,809 churn=0.3955
best model: logreg | T1 test AUC 0.7227 PR-AUC 0.6744 | T2 OOT AUC 0.7392 PR-AUC 0.5947 lift@10% 1.69
segments K=5 silhouette=0.3279 stability ARI=0.9699
top-200 campaign net EV GBP 33,799.89
integrity check passed: 23 figures, 25 tables, ...
```

同时会重新生成 `results/figures/`、`results/tables/`、`results/metrics.json`。

---

## 2. 看懂"它是怎么运行的"：10 个 section 在干什么

打开 notebook，按这个表对照阅读（每节 2–5 分钟）：

| Section | 做什么 | 关键变量 / 输出 |
|---|---|---|
| S0 | 环境、随机种子、工具函数 | `RANDOM_STATE=42`；`save_fig()` / `save_table()` |
| S1 | 数据审计 + 清洗漏斗 | `df_raw → df`；`funnel`；`t01/t02/t03`；`f01` |
| S2 | 两个时间快照 + 流失标签 | `build_snapshot()`；`T1`、`T2`；`AS_OF_T1=2011-05-31`、`AS_OF_T2=2011-08-31` |
| S3 | 相似度 / 距离 | `X_T2`、`X_T1`；欧氏/余弦/曼哈顿对比；`f11` |
| S4 | 特征工程与选择 | `SNAP_FEATURES` → `MODEL_FEATURES`；`f02`；`t05b` |
| S5 | K-means 分层 | `K_CHOSEN=5`；`km_final`；`ARI_STABILITY`；`f04–f06` |
| S6 | 流失模型与评估 | `MODEL_GRIDS`；`TUNED`；`BEST_MODEL="logreg"`；`f07–f09`；`t08` |
| S7 | 关联规则 | `MIN_SUPPORT=0.005`、`MIN_CONFIDENCE=0.2`、`MIN_LIFT=1.2`；`f10`；`t10/t10b` |
| S8 | 决策层（**你的模块**） | `T2["churn_prob"]`、`priority_score`、`CAMPAIGN_TARGETS=200`、`SCENARIOS`、`campaign_value()`；`f12/f13`；`t12–t16` |
| S9 | 汇总与产物 | `metrics.json`、`metrics_extra.json`、`metrics_summary.md`、`ARTIFACTS.md` |

**你只需要精读 S8**，其他能说出"做什么、关键数字"即可。

---

## 3. 逐 cell 读懂你的 S8（约 20 分钟）

按顺序执行并观察：

1. **打分**：`deploy_model` 在 T1 train+val 上重新拟合，然后 `T2["churn_prob"] = predict_proba(...)`。
2. **优先级**：`priority_score = churn_prob × monetary`（价值加权，不只是风险）。
3. **分层×风险表**：`seg_risk` → `t12_segment_risk_matrix.csv`（含 `risk_tier`）。
4. **top-200 名单**：`top_targets = T2_ranked.head(200)`；`t11_top200_targets.csv`。
5. **ROI 计算**：`campaign_value(n, p_churn, avg_monetary, save_rate, cost, margin)` — **读这个函数**，它是你答辩时最该讲清的一段。
6. **三档场景**：`SCENARIOS = {pessimistic, base, optimistic}`；`t16_targeting_comparison.csv`。
7. **保守口径**：`VALIDATED_*` 用清单内**真实流失率 0.31** 重算，得到 GBP 14,802.58；这是报告的头条。
8. **图表**：`f12`（segment×risk）、`f13`（targeted vs random 敏感性）。

**自检**：合上 notebook，用 3 句话讲清 `campaign_value()` 的输入、公式、输出。

---

## 4. 三个受控实验（每个 15–30 分钟）

> 实验会改写 `results/`；做完一定要恢复，别把实验数字提交上去。

### 实验 1：改一个 ROI 假设（最推荐，答辩必问）
在 S8 找到 `SCENARIOS`，把 `base` 改成悲观档：
```python
"base": {"save_rate": 0.05, "cost": 12.0, "margin": 0.30},
```
然后从 S8 的第一个 cell 重新 Run to end（或在 Jupyter 里 Run → Run All Below）。
**预期结果**：净收益 ≈ **GBP 12,771.38**，ROI ≈ **532%**（应接近 `t16` 的 pessimistic 行）。
记录：改了什么 → 数字变了多少 → 你的判断（campaign 是否还值得做）。

### 实验 2：换掉被选中的模型（验证"为什么是 logreg"）
在 S8 打分前强制：
```python
BEST_MODEL = "random_forest"
```
重跑 S8。
**预期结果**：top-200 名单变化；`p_churn_targeted` 从 0.669 降到 0.626（T2 top-decile precision 0.6263），
净收益随之下降（约 GBP 31.5k，实际以运行结果为准）。
记录：AUC 只差 0.007，但 top-10% 精度差 4 个百分点 → 这就是"为什么选 logreg"的实证。

### 实验 3：改营销容量（理解阈值与预算）
把 `CAMPAIGN_TARGETS` 从 200 改成 100 或 400，重跑 S8。
**预期**：收益随人数近似线性增长，但人均价值下降（名单变长 → 平均 monetary 降低）；
记录 100 / 200 / 400 三档的 net 与人均价值，说明"容量是业务决策，不是模型决策"。

**可选实验 4**：把 S7 的 `MIN_SUPPORT` 从 0.005 改成 0.01，记录规则数量变化（会更少、更常见）。

### 实验后恢复（重要）
```bash
git status                       # 看哪些文件被改了
git restore notebooks results    # 恢复被追踪的文件
python3 -m jupyter nbconvert --to notebook --execute --inplace notebooks/CDS3004_Project.ipynb  # 可选：重跑回原值
```

---

## 5. 证明你"真懂"的 10 个问题（自测）

1. T1 和 T2 的 as-of 日期、标签窗口分别是什么？
2. 为什么要有 T2？只用 CV 不行吗？
3. `priority_score` 为什么乘 monetary，而不是只按 churn 概率排？
4. `campaign_value()` 的公式是什么？`p_churn_targeted` 从哪来？
5. 为什么报告头条用 14,802.58 而不是 33,799.89？
6. 随机投放 200 人的净收益是多少？为什么差这么多？
7. 盈亏平衡挽回率 0.452% 是怎么算的？
8. 如果 contact cost 从 8 涨到 12，结论会变吗？
9. 为什么 K=5 不是 silhouette 最大？
10. 关联规则为什么报中位数而不是均值？

答不上来的，回到 `slides/QandA-TABLE.md` 对应行。

---

## 6. 把复现写进你的 agent 轨迹（模板）

在 `agent-trajectories/member-E.md` 增加一条：

| 日期 | 任务 | Prompt | Agent 输出 | 你的决定 | 验证 | 产物 |
|---|---|---|---|---|---|---|
| 2026-11-1x | 复现 ROI 并对假设做敏感性实验 | "把 base 场景改为 cost 12 / save 5% / margin 30%，重跑 S8 并报告净收益变化" | agent 给出修改点与预期数字 | 采纳并手动核对 `campaign_value()` | 重跑后净收益 ≈ 12,771.38，与 t16 pessimistic 一致 | commit / 截图 |

> 只记录你真正做过的；数字以你运行结果为准。

---

## 7. 常见问题

| 现象 | 原因 | 解决 |
|---|---|---|
| `ModuleNotFoundError: mlxtend` | 依赖没装 | `python3 -m pip install mlxtend` 或 Colab `%pip install -q mlxtend` |
| 找不到 `data/Online_Retail.xlsx` | 没下载数据 | `python3 data/download_data.py` |
| 运行很慢 | 首次下载/字体缓存 | 首次可接受；全流程应 < 1 分钟 |
| 图表中文乱码 | 无（全部英文标签） | 无需处理 |
| 实验后 `git status` 一堆改动 | 实验覆盖了 `results/` | `git restore notebooks results` 恢复 |
