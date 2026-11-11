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
