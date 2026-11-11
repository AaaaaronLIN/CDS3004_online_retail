# Agent-Use Trajectory — [MEMBER LABEL]

> Copy this file to `agent-logs/MemberX_agent-trajectory.md`, fill every field, and delete this instruction block. Keep entries in date order. Redact secrets and private data (see `agent-logs/README.md` §4). One entry per substantial task; at least three entries; at least one where you changed or rejected the agent's proposal.

## Header

| Field | Value |
|---|---|
| Member label | Member [A/B/C/D/E] |
| Name and student ID | [full name] / [student ID]*(fill only in the submitted copy if required by the course; labels are fine otherwise)* |
| Role in the project | [see `CONTRIBUTIONS.md`] |
| Tools, harnesses and models used | [e.g. DeepSeek Harness + deepseek-flash; ChatGPT + GPT-5; Claude Code + Sonnet; VS Code Copilot] |
| Repository | `https://github.com/<org>/<repo>` |
| Date range covered | [YYYY-MM-DD] to [YYYY-MM-DD] |
| Commits covered | [hash range or list] |
| Public link(s) | [share URL(s), or "local transcript in raw/"] |

## Trajectory summary

| # | Date | Task | Tool / model | Commit | Verified? |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

---

## Entry [N] — [short task title]

**Date and time:** [YYYY-MM-DD, HH:MM] · **Tool / model:** [harness + model] · **Commit(s):** [`a1b2c3d`]

**Task / goal.** [One sentence: what the team needed from this task and why.]

**Prompt used.**
> [Paste the actual prompt, or a faithful shortened version if very long. Write it in the same words you used; do not clean it up into something better than it was.]

**Agent proposal.** [2–5 sentences: what the agent proposed or produced. If it produced code, name the files/notebook cells. If it produced analysis, state the method and the headline claim it made.]

**Human review and decision.** [Accepted / rejected / changed. State the specific change and the reason: e.g. "Accepted the plan but rejected the cleaning rule because it silently dropped 25% of lines; changed to quantify the dropped revenue first." This is the most important field for the rubric.]

**Implementation.** [Files changed, commit hash, what was actually merged. If nothing was merged, say so and explain why.]

**Verification.** [Exactly how you checked the output: fresh-kernel re-run, independent recomputation (state the check you wrote), code review (what you looked for), cross-check of figure against table, comparison with `metrics.json`, spot-check against raw rows. State the result: matched / corrected / rejected.]

**Artifact / evidence.** [Figure, table, notebook cell, commit URL, shared-link URL, or file path.]

**Lesson / caveat.** [Optional, one line: what you would do differently, or what limitation this exposed.]

---

## Entry [N+1] — [short task title]

**Date and time:** [YYYY-MM-DD, HH:MM] · **Tool / model:** [harness + model] · **Commit(s):** [`a1b2c3d`]

**Task / goal.** [One sentence.]

**Prompt used.**
> [Paste the prompt.]

**Agent proposal.** [2–5 sentences.]

**Human review and decision.** [Accepted / rejected / changed — and why.]

**Implementation.** [Files, commit, what was merged.]

**Verification.** [How checked; outcome.]

**Artifact / evidence.** [Link or path.]

---

## Self-check before submitting this file

- [ ] At least three dated entries, each with prompt, proposal, decision, verification and artifact.
- [ ] At least one entry where I changed or rejected the agent's proposal, with the reason.
- [ ] Every entry links to a commit hash or a file contained in a commit.
- [ ] At least two entries show an independent verification, not just "it looked right".
- [ ] No API keys, tokens, passwords, private contact details or unrelated conversations.
- [ ] Public links open in an incognito window; a local fallback exists in `raw/`.
- [ ] File named `MemberX_agent-trajectory.md`; header table complete; English.
