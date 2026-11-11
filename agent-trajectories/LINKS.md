# Agent-Use Trajectory Links

One row per member. Collect the public share link (or the local transcript path) and test every link in an incognito window while logged out before submission. See `agent-logs/README.md` §3 for export instructions from ChatGPT, DeepSeek Harness, Claude Code and Codex/Copilot.

| Member | Tool / harness | Model | Public link or local transcript | Date range | Tested in incognito? |
|---|---|---|---|---|---|
| Member A | DeepSeek Harness | `deepseek-flash` | [link or `agent-logs/raw/MemberA_...md`] | 2026-10-[..] to 2026-11-[..] | [yes/no] |
| Member B | [tool] | [model] | [link or path] | [range] | [yes/no] |
| Member C | [tool] | [model] | [link or path] | [range] | [yes/no] |
| Member D | [tool] | [model] | [link or path] | [range] | [yes/no] |
| Member E | [tool] | [model] | [link or path] | [range] | [yes/no] |

## Notes

- A link must open **without a login**. If the tool cannot produce a public link, keep a redacted transcript in `agent-logs/raw/` and point to it here.
- If a member used more than one tool, add a second row for that member.
- Do not paste links that expose secrets, private conversations or other courses' content; redact first and re-check the link.
- The submitted ZIP contains `agent-trajectories/` with one file or link list per member; this file is the working index behind it.
