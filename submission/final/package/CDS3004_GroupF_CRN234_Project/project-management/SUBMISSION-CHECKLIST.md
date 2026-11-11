# Submission Checklist — CDS3004 Group Project

**Project:** From Transactions to a Customer Operating System (UCI Online Retail)
**Team:** Group F, CDS3004 Data Mining, 2026/27 Term 1, Prof. Daoyuan Wu
**This checklist is owned by:** Member E (repository and submission lead); every member must sign off before upload.

> Replace every `[SQUARE-BRACKET]` field before submission. Confirm all dates, the CRN and the presentation order with the course announcement and the TA. The two dates below are the ones in the course deck; the exact PPT deadline is announced later.

---

## 1. Deadlines

| Milestone | Deadline | Status / action |
|---|---|---|
| Group formation | 11 October 2026, 23:59 | Already completed via the session spreadsheet. |
| **PPT submission (presentation)** | **Thursday 19 November 2026** — exact upload time/date TBA in the course announcement. Plan to submit by **18 November 2026, 23:59** as a safety margin. | Submit the slide deck in the format the announcement requires (PPTX and PDF backup). Confirm whether the TA wants PPTX, PDF or both. |
| **Final project materials (ZIP)** | **Sunday 6 December 2026, 23:59** (hard deadline) | One ZIP, uploaded to the course submission channel. Do not rely on a network-share or email copy. |
| Presentation day | Week 12/13; our group presents Thursday 19 November 2026 | Confirm room, time, presentation order and whether the talk is 10 minutes + Q&A. Arrive 15 minutes early with slides on the room computer and a USB backup. |

**Time zone:** all deadlines are Hong Kong time (UTC+8). Do not assume the portal uses another time zone.

---

## 2. Final ZIP structure (exact)

One file, named:

```text
CDS3004_GroupF_CRN234_Project.zip
```

`F` = the group number from the course spreadsheet; `234` = 234 or 235. Use ASCII characters only, no spaces.

Inside the ZIP, exactly this top-level folder and contents:

```text
CDS3004_GroupF_CRN234_Project/
├── README.md                          # REQUIRED: includes the PUBLIC GitHub repo URL
├── code/                              # folder of the project code downloaded from GitHub
│   ├── notebooks/CDS3004_Project.ipynb    # executed notebook with visible outputs
│   ├── code/                              # helper modules and pipeline notes
│   ├── results/figures/                   # all generated PNG figures
│   ├── results/tables/                    # all generated CSV tables
│   ├── results/metrics.json               # primary numbers
│   ├── results/metrics_extra.json         # supporting diagnostics used in the report
│   ├── results/metrics_summary.md         # human-readable headline numbers
│   ├── results/ARTIFACTS.md               # authoritative file inventory
│   ├── requirements.txt
│   └── (data/README.md — data download instructions; do not rely on shipping raw data)
├── report/
│   └── CDS3004_GroupF_Report.pdf # REQUIRED: PDF ONLY, contributions listed
├── agent-trajectories/
│   ├── MemberA_agent-trajectory.md        # one per member (or .pdf / link list)
│   ├── MemberB_agent-trajectory.md
│   ├── MemberC_agent-trajectory.md
│   ├── MemberD_agent-trajectory.md
│   └── MemberE_agent-trajectory.md
└── SUBMISSION-MANIFEST.txt            # optional but recommended: file list + sizes + checksums
```

**Rules for each item**

1. **`README.md` (top level of the ZIP).** Must contain the **public** GitHub URL, e.g. `https://github.com/AaaaaronLIN/CDS3004_online_retail`, in plain text so the grader can click it from the PDF viewer or browser. Test it in an incognito window, logged out. The same README should also state the course, project title, team and how to reproduce.
2. **`code/`.** A fresh download of the team repository (ZIP download or `git clone`), not a working copy with `.git/`, `__MACOSX/`, `.DS_Store`, caches or IDE folders. The notebook must be the **executed** version with outputs visible. Do not modify code after the final commit; if you re-run, commit and re-download.
3. **`report/`.** **PDF only** — no `.docx`/`.md`/`.pages`. The PDF must include a **contribution statement listing each member's work**, the agent-usage and verification section, the rubric-coverage appendix, and every figure and table. Check that all fields `F`, member names, student IDs and the repo URL have been filled in, and that no authoring notes (draft notes, placeholder indexes, "replace before export" comments) remain.
4. **`agent-trajectories/`.** One file or one link list per member. Links must be publicly openable without a login (e.g. a ChatGPT shared link). If a tool cannot produce a public link, include an exported transcript file. Each trajectory must show the human–agent loop, not only a final prompt. Export steps per tool (ChatGPT, DeepSeek Harness, Claude Code, Codex/Copilot) and the redaction/naming rules are in `agent-logs/README.md` §3–§5.
5. **`SUBMISSION-MANIFEST.txt`.** List every file, its size and a SHA-256 checksum (`shasum -a 256`), plus the ZIP creation date. This is your evidence if the upload is corrupted.

Do **not** include: `.git/`, virtual environments, caches, raw data copies over 50 MB unless the README says where they came from, API keys, tokens, any file that was not regenerated or reviewed, or internal working notes (`PLAN.md`, `RUBRIC-MATRIX.md`, `report/PLACEHOLDERS.md`). Move internal notes out of the public repository or into an ignored folder before the code snapshot is taken.

---

## 3. Pre-submission acceptance tests (run every one)

| # | Test | How to check | Pass criterion |
|---|---|---|---|
| 1 | ZIP opens cleanly | Unzip into an empty temporary folder on a second machine or after a reboot | No errors; exactly one top-level folder; no `__MACOSX`/`.DS_Store` |
| 2 | Public repo reachable | Open the README URL in an **incognito/private** browser window, logged out | Repository loads over HTTPS with no login prompt; code visible; default branch is `main` |
| 3 | README URL matches | Compare the ZIP README URL with the actual repository | Character-for-character match; not a local path and not a private clone URL |
| 4 | Report is PDF only | List the `report/` folder; open the PDF on a machine without the source documents | Exactly one PDF; opens and renders; fonts embedded; pages numbered |
| 5 | Contributions listed | Search the PDF for "Contribution" | Each of the five members named with role, rubric/artifact ownership and slides |
| 6 | One trajectory per member | List `agent-trajectories/`; open each link in incognito | Five files/links; each opens; each shows prompts, human review and verification |
| 7 | Notebook runs from scratch | `jupyter nbconvert --to notebook --execute --inplace notebooks/CDS3004_Project.ipynb` on a clean environment | Exit code 0; no errors; all outputs present; runtime under 10 minutes |
| 8 | Outputs regenerate | After the run, diff the new `results/` against the committed one | Same file names; metrics within floating-point tolerance; figures/tables not empty |
| 9 | No placeholders or authoring notes left | `grep -R "{{" report/ slides/ README.md`; search the exported PDF text for `Draft note`, `placeholder index`, `F`, `PLACEHOLDERS` | Zero matches; no internal notes in the PDF |
| 10 | Numbers consistent | Spot-check 10 numbers in the PDF against `metrics.json` | Exact match to the stated precision; no number appears in the report that is absent from the pipeline output |
| 11 | No secrets or absolute paths | `grep -RIn "sk-\|api[_-]key\|token\|/Users/\|C:\\\\" .` excluding data/figures | Zero hits; notebook paths are relative |
| 12 | File names ASCII, no spaces | `find . -name "* *"` and inspect non-ASCII names | No spaces or non-ASCII in filenames/paths |
| 13 | ZIP size manageable | Check the ZIP size before upload | Well under the portal limit (target < 100 MB); note the raw data size if included |
| 14 | Slides ready | Open the submitted deck and a PDF backup on the room computer | 14 slides; English; 10:00 or less; fonts render; no placeholder token or missing image; timing rehearsed to 9:35–10:00 |
| 15 | Commits reflect each member | `git shortlog -sne` and `git log --author="<member>" --oneline` | Every member has meaningful commits spread across weeks (not one dump at the end) |
| 16 | Uploaded copy is the tested copy | Download the uploaded ZIP and re-run tests 1, 2, 4, 7 | The downloaded file is the tested file; checksum matches the manifest |
| 17 | Backup kept | Copy the final ZIP and the PDF to two members' cloud storage and a USB stick | Two independent copies exist after submission |

**Final 20-minute protocol before upload:** run tests 1–4, 7, 9, 10 and 15 on the exact file to be uploaded; screenshot the results; have a second member repeat tests 1, 2 and 7. Only the second member clicks submit.

---

## 4. Risk list and mitigations

| # | Risk | Likelihood | Impact | Mitigation / owner |
|---|---|---|---|---|
| 1 | GitHub repository is private or URL wrong at submission | Medium | High — the grader cannot see any code | Owner Member E; incognito test the exact URL; set repo public at least 48 h before submission; re-test on the day |
| 2 | A member's agent trajectory is missing or the share link requires login | High | Medium — workload and validity evidence incomplete | Owner each member; collect links one week before; export a transcript fallback; test every link in incognito |
| 3 | Report exported as `.docx` or a placeholder remains in the PDF | Medium | High — rubric item and course requirement | Owner Member E; run test 4 and test 9 on the exported PDF; search the PDF text for placeholder braces and `[GROUP` |
| 4 | Notebook fails from a fresh kernel on the grader's machine | Medium | High — reproducibility criterion | Owner Member C; pin `requirements.txt`; run on a second machine/venv; keep runtime under 10 min; avoid absolute paths |
| 5 | Zoomed numbers drift between report and pipeline after a late re-run | Medium | High — credibility and rubric item 9 | Owner Member C; freeze the pipeline 72 h before submission; re-run, then re-fill the report in one pass and re-check test 10 |
| 6 | PPT deadline is earlier than assumed, or requires PDF rather than PPTX | Medium | High — presentation mark | Confirm with TA/course announcement this week; submit both PPTX and PDF by 18 Nov; owner Member E |
| 7 | Presentation overruns 10 minutes | Medium | Medium — timing rubric item | Rehearse with a timer (target 9:35); timekeeper cuts slides 9–10 if needed; owner all presenters |
| 8 | A presenter is ill on the day | Low | High — role rubric item | Every member knows the full deck; a designated backup can present any slide; owner Member E |
| 9 | ZIP is corrupted, incomplete, or the portal rejects it | Low | High — nothing is graded | Build the ZIP on one machine; checksum manifest; upload early (6 Dec morning) and re-download to verify; keep a second copy |
| 10 | Secrets or home-directory paths leak into notebooks or logs | Low | High — academic-integrity and privacy issue | Run test 11; redact API keys, tokens, emails and private paths; owner each member, checked by Member E |
| 11 | Report/slides still contain numbers not in `metrics.json` | Low | High — grading and honesty | Fill step is the only source of numbers; test 10 spot-check; owner Member E |
| 12 | Contribution statement unfair or names/IDs wrong | Medium | Medium — rubric item | Each member reviews Table 21 in the report and `CONTRIBUTIONS.md`; owner Member E |
| 13 | Data licence or attribution missing from README | Low | Low–Medium | README cites UCI dataset and licence; owner Member E |
| 14 | Repository size or large files cause GitHub push/upload issues | Low | Medium | Do not commit raw data if over 50 MB; add `.gitignore`; keep generated PNGs small; owner Member E |
| 15 | Internal working notes (PLAN.md, RUBRIC-MATRIX.md, report/PLACEHOLDERS.md) end up in the ZIP or public repo | Medium | Medium — looks unpolished and leaks internal notes | Keep them out of the ZIP; exclude or move them before the code snapshot; owner Member E |

---

## 5. Roles on submission day

| Role | Owner | Responsibility |
|---|---|---|
| Submission lead | Member E | Run the acceptance tests, build the ZIP, upload, keep the manifest and confirmation screenshot |
| Reproducibility check | Member C | Fresh-kernel run on a second machine; confirm metrics and figures |
| Report check | Member B | PDF contents, contributions, figures/tables, English, no placeholders |
| Trajectory check | Member D | Collect and test all five trajectories in incognito |
| Backup and attendance | Member A | USB + cloud backups of ZIP, PDF and slides; presentation-day logistics |

**Sign-off before upload:** all five members confirm in the group chat that tests 1–10 pass and that their own trajectory and contribution lines are correct. No submission without the second-member double-check.
