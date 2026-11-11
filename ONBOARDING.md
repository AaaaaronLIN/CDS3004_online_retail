# ONBOARDING — Group F 组员操作指南

> 每个组员**第一次**加入这个仓库时，按顺序执行下面的命令即可。
> macOS / Windows 通用（Windows 用 PowerShell 或 Git Bash；把 `python3` 换成 `python`）。

---

## 0. 接受邀请

去邮箱或 GitHub 通知里点 **Accept invitation**。
（没接受的话，`git push` 会报 `Permission denied (403)`。）

## 1. 确认有 git

```bash
git --version
```

没有的话：macOS 执行 `xcode-select --install`；Windows 安装 Git for Windows。

## 2. clone 仓库

```bash
git clone https://github.com/AaaaaronLIN/CDS3004_online_retail.git
cd CDS3004_online_retail
```

## 3. 设置自己的身份（最重要，别跳过）

```bash
git config user.name  "你的名字"
git config user.email "你GitHub账号绑定的邮箱"
```

- 邮箱在 GitHub → Settings → Emails 里看；用绑定邮箱，commit 才会关联到你的头像。
- **不要加 `--global`**：如果是多人共用一台电脑，`--global` 会互相覆盖。
- 这一步决定 `git log` 里每个 commit 的作者是谁；老师按 GitHub commits 估算每个人的工作量（课件 P9）。

## 4. 验证身份

```bash
git config user.name
git config user.email
```

应输出你自己的名字和邮箱。

## 5. 拉取最新代码 + 安装环境 + 下载数据

```bash
git pull
python3 -m pip install -r requirements.txt
python3 data/download_data.py      # 下载 23MB 数据集并校验行数
```

数据文件已被 `.gitignore` 排除，**不会**被推送。

## 6. 跑一遍 notebook，确认你能复现

```bash
python3 -m jupyter nbconvert --to notebook --execute --inplace notebooks/CDS3004_Project.ipynb
```

或者用 Google Colab：打开 notebook → 把 `Online_Retail.xlsx` 上传到 `data/` → Run all。
完整执行约 30 秒。

## 7. 领任务 → 改文件 → 提交

分工见 `project-management/COMMIT-PLAN.md` 与 `agent-trajectories/member-*.md`：

| 成员 | 负责模块 | 先改哪里 | 第一次 commit 示例 |
|---|---|---|---|
| Member A | 问题定义 / 报告统稿 / PPT | `report/REPORT.md` | `docs(report): tighten problem definition` |
| Member B | 数据清洗与快照（S1–S2） | `notebooks/CDS3004_Project.ipynb` | `feat(data): verify cleaning funnel and snapshot coverage` |
| Member C | 聚类 + 相似度 + 图表（S3, S5） | notebook + `results/figures/` | `feat(seg): document K choice with stability evidence` |
| Member D | 特征工程 + 分类评估（S4, S6） | notebook | `exp(eval): compare feature sets on validation PR-AUC` |
| Member E | 关联规则 + 决策层（S7–S8） | notebook + `results/tables/` | `feat(decision): churn-conditional campaign value` |

提交：

```bash
git pull                     # 先拉，避免冲突
git add .
git commit -m "feat(data): verify cleaning funnel and snapshot coverage"
git push
```

## 8. 确认提交成功

```bash
git log --oneline -3
git log -1 --format="%an <%ae>"      # 应显示你自己的名字
```

再去仓库页面 **Insights → Contributors**，应该能看到你的头像和 commit 数。

---

## 每天固定动作

```bash
git pull                                  # 开工前
# …只改自己负责的文件…
git add . && git commit -m "…" && git push   # 收工前
```

---

## 常见报错对照

| 报错 | 原因 | 解决 |
|---|---|---|
| `Permission denied (403)` | 没接受 collaborator 邀请 / 账号不对 | 接受邀请；确认 `git config user.email` 是被邀请的账号 |
| `Authentication failed` | HTTPS 需要 token | 用 GitHub Desktop（Sign in with browser）或 VS Code 登录后 push |
| `Updates were rejected / fetch first` | 别人先推了 | `git pull --rebase` 再 `git push` |
| `fatal: not a git repository` | 不在仓库目录 | `cd CDS3004_online_retail` |
| 提交里出现 `data/Online_Retail.xlsx` | 误加数据文件 | `git rm --cached data/Online_Retail.xlsx`，确认 `.gitignore` 含 `data/*.xlsx` |
| push 后没出现在 Contributors | 邮箱没绑定 GitHub | 把 `git config user.email` 改成绑定邮箱，之后的 commit 会关联 |

---

## 硬性规则（5 条）

1. 每人**至少 3 次有意义 commit**（`update`、`fix`、`123` 不算）。
2. **只改自己负责的文件**；改 notebook 前先 `git pull`，减少冲突。
3. **不提交 `data/*.xlsx`**（已忽略，别用 `git add -f` 强行加）。
4. **不要 `git push --force`**、不删别人文件、不乱改 `.gitignore`。
5. 每天把自己的 prompt / agent 输出 / 验证结果写进 `agent-trajectories/member-X.md`。

---

## 答辩与提交节点（2026）

| 日期 | 事项 |
|---|---|
| 2026-11-19（周四） | 小组答辩（PPT 截止日以 TA 通知为准，按 11/18 23:59 预留） |
| 2026-12-06（周日）23:59 | 最终材料 ZIP 提交 |

详见 `project-management/PLAN.md`、`project-management/SUBMISSION-CHECKLIST.md`。

---

# 5 人分工（建议版，还没定谁做哪块就按这个认领）

> **现在还只是 Member A–E 占位，不代表已经分好。** 组内商量后，把名字填进 3 处即可：
> `CONTRIBUTIONS.md`、`report/REPORT.md`（Table 21）、`slides/SLIDES.md`（每页 `**Speaker:**` 行 + 开头 Speakers 那段）；
> 并把 `agent-trajectories/member-X.md` 的文件名/标题改成自己的名字。改完告诉组长，组长统一重出 PDF/PPT。

| 成员 | 角色 | 负责模块（notebook 章节） | 主要文件 / 产物 | 答辩页 | 今天第一件事 |
|---|---|---|---|---|---|
| **A** | 数据与质量负责人 | S1–S2：数据审计、清洗、退货台账、T1/T2 快照 | `t02_data_quality_issues`、`t03_cleaning_decisions`、`t02_cohort_summary`、`f01`；report §2 | 4、5（数据段）、12（数据局限） | 跑 S1–S2，记录 24.93%、135,080、13.57% |
| **B** | 特征工程与分层负责人 | S4–S5（+S3 距离支撑）：16 特征、相关性/MI/RFE、K-means、分层画像 | `t04`–`t07`、`f02`–`f08`；report §4–§5 | 6、7 | 读 `t05b_feature_evidence.csv`，核对 0.6966→0.7036 |
| **C** | 流失建模与评估负责人 | S6：三模型、70/15/15、5 折 CV、验证集选型、双阈值、时间外验证、lift | `t08`、`t09_lift_deciles`、`s06_threshold_analysis`、`f07`–`f09`；report §6 | 8 | 核对 CV/T1/T2 三组 AUC 与 lift 1.6916 |
| **D** | 关联规则与相似度负责人 | S3、S7：距离度量、lookalike、相似商品、FP-Growth、holdout 验证 | `t03`、`t04_lookalikes`、`t05_similar_products`、`t09_top_rules`、`t10_association_rules`、`f10`–`f11`；report §7–§8 | 9、10 | 核对 5,441 / 5,402 / median 12.174 / 593 条 |
| **E** | 集成、决策与仓库负责人 | S8–S9：T2 打分、segment×risk、优先级、ROI、指标汇总、仓库与提交 | `t10_decision`–`t15`、`f12`–`f13`、README、CONTRIBUTIONS、提交清单；report §1/§3/§9–§10/§13 | 1–3、5、11、13–14 | 复算 ROI 三档 + 盈亏平衡率 |

**认领建议**：按兴趣最快；有人编程弱就配一个强的同组；**E 这块必须有一个人负责**（集成/ROI/仓库/提交，工作量不小但最容易出彩）。

---

## 每个人接下来 7 天的具体步骤

> 下面的 Member A–E 换成你的名字。通用第一步（clone、设置身份、跑通 notebook）见本文第 0–6 节。

### Member A — 数据与质量
- **今天（30 分钟）**：跑 S1–S2；核对 24.93%（135,080 行）、匿名交易占收入 13.57%、取消单 9,288、非商品 2,916、重复行 5,268；T1=2,716 人（流失率 0.5044）、T2=2,809 人（0.3955）。
- **本周三个任务**（详见 `agent-trajectories/member-A.md`）：
  1. 重算清洗漏斗，解释“审计数 vs 漏斗删除数”为什么不同
  2. 改一条清洗规则做对比实验，给出你的取舍
  3. 找出 S2 里防止标签泄漏的两行代码
- **改什么文件**：`notebooks/CDS3004_Project.ipynb`（S1–S2 的 markdown/注释）、`results/tables/t02*`、`t03*`、`data/README.md`、`report/REPORT.md` §2
- **commit 示例**：`feat(data): document cleaning funnel`, `exp(data): test zero-price retention`
- **答辩讲**：Slides 4、5（数据段）、12（数据局限）
- **完成判据**：三个任务填进轨迹；≥3 次 commit；能脱稿讲 1 分钟数据质量

### Member B — 特征工程与分层
- **今天**：读 `t05b_feature_evidence.csv` 与 `t06_cluster_metrics.csv`；核对 16→10 特征、验证 PR-AUC 0.6966→0.7036；silhouette K=2 0.4223 / K=4 0.347 / K=5 0.3279；K=5 的 ARI 0.9699。
- **本周三个任务**：① 复现特征选择漏斗；② **为 K=5 做辩护**（答辩必问）；③ 比较 cosine/manhattan/euclidean（0.3283/0.2183/0.1844）
- **改什么文件**：notebook S3–S5、`t04`–`t07`、`f02`–`f08`、`report/REPORT.md` §4–§5
- **commit 示例**：`feat(seg): document K choice with stability evidence`, `exp(feat): compare selection stages`
- **答辩讲**：Slides 6、7
- **完成判据**：能解释“为什么不是 K=2（silhouette 最高）”

### Member C — 流失建模与评估
- **今天**：核对 CV AUC（logreg 0.7593 / DT 0.7397 / RF 0.7505）、T1 测试（0.7227 / 0.6744）、T2 时间外（0.7392 / 0.5947）、lift 1.6916、阈值 0.2665 / 0.7382。
- **本周三个任务**：① 复现三组数字并解释为何选 logreg；② 把 top-10% 改成 top-20% 做阈值实验；③ 解释混淆矩阵的 false negative / positive 业务含义
- **改什么文件**：notebook S6、`t08`、`t09_lift_deciles`、`s06_threshold_analysis`、`f07`–`f09`、`report/REPORT.md` §6
- **commit 示例**：`exp(eval): threshold at top-20 percent`, `docs(eval): error analysis`
- **答辩讲**：Slide 8
- **完成判据**：能回答“为什么不是随机森林”“lift 1.69 什么意思”

### Member D — 关联规则与相似度
- **今天**：核对 5,441 条规则、5,402 条 holdout 评估、median holdout lift 12.174、99.8%>1、593 条 business rules；cosine 0.3283。
- **本周三个任务**：① 解释为什么不报 mean lift 28.1957；② 手算一条规则的 holdout lift；③ 核对 lookalike 客户与相似商品示例
- **改什么文件**：notebook S3/S7、`t03`、`t04_lookalikes`、`t05_similar_products`、`t09_top_rules`、`t10_association_rules`、`f10`–`f11`、`report/REPORT.md` §7–§8
- **commit 示例**：`feat(rules): validate rules on later holdout`, `docs(sim): lookalike examples`
- **答辩讲**：Slides 9、10
- **完成判据**：能解释“高 lift 为什么可能是假象”“相似度怎么用于冷启动”

### Member E — 集成、决策与仓库
- **今天**：复算 ROI：base 33,799.89、validated 14,802.58、random-200 1,925.76、uplift 31,874.13、盈亏平衡 0.452% vs 4.538%。
- **本周三个任务**：① 重算 ROI 三档并给判断；② 核对 t12/t13 与报告 §9 一致性；③ 走一遍 `SUBMISSION-CHECKLIST.md` 找缺口
- **改什么文件**：notebook S8–S9、`t10_decision`–`t15`、`f12`–`f13`、`README.md`、`CONTRIBUTIONS.md`、`submission/`
- **commit 示例**：`feat(decision): churn-conditional campaign value`, `chore(repo): submission checklist gaps`
- **答辩讲**：Slides 1–3、5、11、13–14
- **完成判据**：能解释“为什么 ROI 用保守口径”“为什么随机投放不划算”

---

## 答辩时间轴（10 分钟，与 slides/SLIDES.md 一致）

| 时间 | 讲者 | 幻灯片 |
|---|---|---|
| 0:00–1:50 | E | 1–3 标题/议程/问题框架 |
| 1:50–2:40 | A | 4 数据与质量 |
| 2:40–3:25 | E | 5 pipeline |
| 3:25–5:05 | B | 6–7 特征 + 分层 |
| 5:05–6:15 | C | 8 流失预测与评估 |
| 6:15–7:30 | D | 9–10 关联规则 + 相似度 |
| 7:30–8:30 | E | 11 决策与 ROI |
| 8:30–9:00 | A | 12 局限 |
| 9:00–9:35 | E | 13–14 贡献 + 收尾 |

> 若 TA 给的时长不是 10 分钟，组长告诉我，我按实际时长重排。

---

## 本周完成判据（周日晚检查）

- [ ] **Contributors 显示 5 个人**（每人至少 push 过一次）
- [ ] 每人 **≥3 次有意义 commit**
- [ ] 每人把自己的 **3 个验证任务**填进 `agent-trajectories/member-X.md`
- [ ] 报告/PPT 里的数字与 `results/metrics.json` 一致
- [ ] 全组完成 **2 次计时排练**（目标 ≤10:00，最好 9:35）
- [ ] 5 位成员姓名已填进 CONTRIBUTIONS / REPORT Table 21 / SLIDES

