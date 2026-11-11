# Agent-Use Trajectories — Why They Matter and How to Produce Them

This folder holds each member's **agent-use trajectory**: an honest, date-stamped record of how you used an AI agent (the harness *and* model), what it proposed, what you as the human accepted, rejected or changed, and how you verified the result.

## 1. Why this folder exists

The course assesses this project from four sources: **Presentation, Code (GitHub), Report, and Agent Trajectories**. Two consequences follow.

1. **Workload is estimated from GitHub commits and agent trajectories.** The course deck says the group size is balanced across sessions by using GitHub commits and agent trajectories to roughly determine each student's workload. A member with no commits and no trajectory is invisible to that estimate.
2. **"Checked whether the agent-generated analysis was valid" is part of the project rubric.** The rubric rewards a strong human–agent workflow: human defines → agent proposes → human reviews → agent implements → human verifies → revise. A trajectory that contains only a final prompt and a final answer does not demonstrate that workflow; a trajectory that shows the plan, the human's changes and the verification does.

The trajectories are therefore *evidence*, not a diary. Write them so that a reader who has never met the team can see, for each task: what was delegated, what the human decided, and how the output was checked.

## 2. What a complete trajectory contains

For each substantial task, record:

| Field | What to write |
|---|---|
| Date and time | ISO date, e.g. `2026-10-28` |
| Task / goal | One sentence: what the team needed |
| Tool, harness and model | e.g. DeepSeek Harness + deepseek-flash, ChatGPT GPT-5, Claude Code + Sonnet, Codex, Copilot |
| Prompt used | The actual prompt (or a faithful shortened version if it is very long) |
| Agent proposal | What the agent proposed or produced, in 2–5 sentences |
| Human decision | Accepted / rejected / changed — **and why** |
| Implementation | Files changed and commit hash, e.g. `notebooks/CDS3004_Project.ipynb`, `a1b2c3d` |
| Verification | Exactly how you checked it: fresh-kernel re-run, independent recomputation, code review, comparison with `metrics.json`, spot-check against raw rows |
| Artifact / evidence | Figure, table, commit, notebook cell, or shared-link URL |

A trajectory with **three or more entries** covering different tasks (for example: data audit, a modelling decision, a verification) is the minimum we expect per member. Five or more is better. At least one entry per member should show a proposal the human **rejected or changed**, because that is the clearest evidence of human judgement.

## 3. How to export logs from common tools

The aim is a file or public link that a grader can open. Exact menus vary by version; if a menu has moved, search the tool's help for "export conversation" / "share chat". Always note the tool and model in the header.

**ChatGPT (web)**
- Open the conversation → **Share** → **Create link** → copy the public link. Paste it in your trajectory header and in `agent-logs/LINKS.md`.
- Full archive alternative: **Settings → Data controls → Export data** produces a ZIP of your conversations; extract the relevant conversation JSON and keep only the relevant part.
- Test the link in an incognito window while logged out before submitting.

**DeepSeek Harness (the tool used in this project)**
- Open the session, copy the full conversation transcript into your trajectory file (or export the session transcript if your build offers an export/save action), and record the harness name, the model (e.g. `deepseek-flash`) and the date.
- If the harness stores session logs on disk, copy the relevant session file and redact it; do not copy the whole workspace or unrelated sessions.
- Keep the raw export small: copy only the relevant task(s), not every session of the term.

**Claude Code**
- Claude Code stores session transcripts as JSONL files under `~/.claude/projects/<project-slug>/`. Copy the relevant session file (or use the `/export` command if your version provides it), then convert/redact it into your trajectory file.
- Record the model used and the working directory; keep the commit hashes from the same sessions.

**OpenAI Codex / GitHub Copilot (VS Code)**
- In the VS Code Chat panel, use the chat history menu to open the conversation and copy the transcript, or use any available "Export chat" action.
- Copilot chat sessions are stored in VS Code's workspace storage; if there is no export button, copy the visible transcript into your trajectory file with timestamps.
- Record the model shown in the chat (e.g. GPT-5, Claude Sonnet) and the workspace folder.

**Any other harness**
- A text file containing the conversation plus a header naming the harness, model and date is sufficient. If a tool cannot export, type/markdown the key turns manually: prompt → proposal → your decision → verification.

## 4. What to redact

Do not submit anything that would create a privacy or security problem:

- **Remove** API keys, access tokens, passwords, cookies, connection strings and any `.env` content.
- **Remove** personal contact details, home addresses, phone numbers and unrelated private conversations.
- **Remove or crop** screenshots containing raw customer rows (the dataset is pseudonymous, but avoid publishing `CustomerID`-level rows unnecessarily), other courses' materials, or other people's messages.
- **Keep** the technical content: prompts, plans, code snippets, review comments, verification steps and commit hashes.
- Blur or omit absolute home-directory paths in screenshots; relative repository paths are fine.

Redaction is normal and does not weaken the record. A redacted prompt with a clear note ("address removed") is better than omitting the entry.

## 5. File naming and layout

```text
agent-logs/
├── README.md                      # this file
├── TEMPLATE.md                    # per-person template
├── EXAMPLE_member1.md             # filled example (clearly marked as an example)
├── LINKS.md                       # table: member -> tool -> public link -> date
├── MemberA_agent-trajectory.md
├── MemberB_agent-trajectory.md
├── MemberC_agent-trajectory.md
├── MemberD_agent-trajectory.md
├── MemberE_agent-trajectory.md
└── raw/                           # optional: exported transcripts (redacted)
    ├── MemberA_2026-10-28_chatgpt.md
    └── ...
```

- Use the member label in the filename (`MemberA`, `MemberB`, …) until names are confirmed, then rename consistently in the report, `CONTRIBUTIONS.md` and the folder.
- One file per member is the submitted artifact; keep long raw exports in `raw/` and link to them from the trajectory file.
- `LINKS.md` collects public share links so the grader can open them without hunting through files.

## 6. Quality bar for submission

Each member's file should satisfy all of the following before the ZIP is built:

- [ ] Header states member label, tool(s), model(s), date range and repository commit range.
- [ ] At least three dated entries, each with prompt, proposal, human decision and verification.
- [ ] At least one entry where the human **changed or rejected** the agent's proposal, with the reason.
- [ ] Every entry links to a commit hash or a file that the commit contains.
- [ ] At least two entries show an **independent verification** (fresh-kernel run, recomputation, code review, cross-artifact check).
- [ ] No secrets, tokens, private contact details or unrelated personal content.
- [ ] Public links (if used) open in an incognito window without login; a local transcript fallback exists.
- [ ] English, readable by an outsider, no unexplained internal shorthand.

## 7. A note on honesty

Do not retroactively invent a trajectory, and do not paste a single giant prompt with no human turns. If a task was done without an agent, say so. If an agent's output was wrong and you caught it, record that — it is the strongest possible evidence for the rubric item on verifying agent-generated analysis. The report's agent-usage section (§12) summarises this folder; the folder itself is the primary evidence.
