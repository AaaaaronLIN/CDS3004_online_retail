# Agent-use trajectory — Member E  (name: ____)

**Group:** F · **CRN:** 234 · **Course:** CDS3004 Data Mining, Lingnan University, 2026/27 Term 1
**Role:** Integration, decision framework and repository lead
**Module:** 决策层（segment×risk、优先级、ROI）、指标汇总、仓库与提交合规（notebook S8–S9）
**Presents:** 1–3（开场/问题/框架）、5（pipeline 总览）、11（决策与 ROI）、13–14（贡献/结尾）
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

### Task 1: 复算 ROI 三档场景与盈亏平衡

**做什么：** 核对：base 净 33,799.89（乐观上界）、validated 净 14,802.58（保守口径）、random-200 净 1,925.76、uplift 31,874.13；盈亏平衡挽回率 0.452%（targeted）vs 4.538%（random）。再把 contact cost 改成 £12、save rate 5% 重算一遍。

**要贴的证据：** 贴你的重算结果 + 一句“这个 campaign 还值不值得做”的判断。

### Task 2: 核对决策表与风险矩阵的一致性

**做什么：** 检查 t12_segment_risk_matrix 与 t13_action_table：5 个分层、风险档位、动作、期望值是否与报告 §9 一致；确认优先级 = churn_prob × monetary。

**要贴的证据：** 贴一张对照表（segment / action / 值），指出你发现的任何不一致。

### Task 3: 走一遍提交合规清单

**做什么：** 对照 project-management/SUBMISSION-CHECKLIST.md：public repo、README 含 URL、报告 PDF only、5 份轨迹、ZIP 结构。列出还缺什么。

**要贴的证据：** 贴清单勾选结果 + 缺口列表。


## 写好一条的标准

- 你能不看着屏幕讲出这个数字的含义。
- 至少有一条记录里，你**否决或修改**了 agent 的建议。
- 每条都能指向一个 artifact：表格某行、某张图、某个 commit、某条命令输出。
- 不编造；没做的任务直接删掉，不要留假记录。
