# START HERE — CDS3004 Group F (CRN 234)

> Built 2026-11-11 for **Group F, CRN 234** (5-person group), presentation **Thursday 19 November 2026**,
> final materials **Sunday 6 December 2026, 23:59**. Read this first (~6 minutes).

---

## 0. What has already been filled in for Group F

- Group ID: **Group F** (report cover, slide deck, README, contribution table)
- CRN: **234** (file names, submission checklist)
- Repository URL: `https://github.com/AaaaaronLIN/CDS3004_online_retail`
  → **replace `GITHUB-USERNAME` once you create the repo** (5 files: report, slides, README, contribution table, this file)
- Member names: still **Member A–E** — fill them in the contribution table and slides when known
  (report §11 Table 20, `CONTRIBUTIONS.md`, `slides/SLIDES.md` speaker lines, and the file names in `agent-trajectories/`)

---

## 1. The repo to create (exact settings)

On GitHub → **New repository**:

| Field | Value |
|---|---|
| Repository name | `cds3004-online-retail` |
| Description | `CDS3004 Data Mining — Group F — Agent-assisted customer segmentation, churn prediction and cross-sell decision system` |
| Visibility | **Public** (required: the grader must open it without an invite) |
| Initialize with README | **No** |
| Add .gitignore | **No** |
| Choose a license | **No** (leave empty; one less merge conflict) |

Then push from this folder:

```bash
cd cds3004-project
git init
git add .
git commit -m "scaffold: reproducible pipeline, report, and slide deck"
git branch -M main
git remote add origin https://github.com/<your-username>/cds3004-online-retail.git
git push -u origin main
```

> `data/Online_Retail.xlsx` (23 MB) is excluded by `.gitignore`; users download it with
> `data/download_data.py`. After the first push, **each member commits their own work** — the
> course estimates individual workload from GitHub commits (deck p.9).

---

## 2. What is in this package

| Folder / file | What it is | Status |
|---|---|---|
| `code/notebooks/CDS3004_Project.ipynb` | Executed analysis pipeline (52 cells, 17 inline figures, ~30 s) | done |
| `code/results/` | 23 figures, 29 tables, `metrics.json`, `metrics_extra.json`, `ARTIFACTS.md` | done |
| `report/CDS3004_GroupF_CRN234_Report.pdf` | 19-page submission report | done (names pending) |
| `report/REPORT.md` | Markdown source, regenerate with `code/tools/build_pdf.py` | done |
| `slides/CDS3004_GroupF_CRN234_Slides.pptx` | 20-slide deck, 19:40, notes on every slide | done (names pending) |
| `slides/SLIDES.md` | 20-minute slide plan, speaker script, timings | done |
| `slides/CDS3004_GroupF_CRN234_CueCards.pdf` | One-page-per-slide speaker cards | done |
| `slides/QandA-TABLE.md` | Per-section Q&A table (27 likely questions + hostile questions) | done |
| `HOST-BRIEF.md` | Host cheat sheet: 12 numbers, 5 decisions, 8 answers, 30-minute study plan | done |
| `HOST-REPRO.md` | Reproduction guide: run it yourself in 30 min, 3 controlled experiments, reset instructions | done |
| `agent-trajectories/member-A..E.md` | Per-person trajectory skeleton with verification tasks | **you fill them** |
| `project-management/PLAN.md` | Day-by-day plan to 19 Nov / 6 Dec | done |
| `project-management/RUBRIC-MATRIX.md` | Every rubric item → evidence | done |
| `project-management/SUBMISSION-CHECKLIST.md` | ZIP structure, deadlines, acceptance tests | done |
| `project-management/COMMIT-PLAN.md` | Who commits what, with suggested messages | done |
| `CONTRIBUTIONS.md` | 5-member role / rubric / commit ownership | names pending |

---

## 3. Do these 6 things today (about 90 minutes)

1. Create the public repo with the settings above and push (§1).
2. Fill member names (search `Member A` … `Member E`).
3. **Run the notebook yourself**: `jupyter nbconvert --to notebook --execute --inplace notebooks/CDS3004_Project.ipynb`
   (or upload `Online_Retail.xlsx` to Colab → Run all).
4. Ask the TA: exact talk duration (10 min? Q&A?), PPT upload deadline, English or Cantonese.
5. Each member opens their `agent-trajectories/member-X.md`, does the **three verification tasks** listed
   inside, and records what they actually did. Workload is judged from commits + trajectories.
6. Read `project-management/PLAN.md` §4–6 and confirm your module.

---

## 4. Regenerating the deliverables after you edit

```bash
cd code
python tools/build_pdf.py  --src ../report/REPORT.md  --out ../report/CDS3004_GroupF_CRN234_Report.pdf
python tools/build_pptx.py --out ../slides/CDS3004_GroupF_CRN234_Slides.pptx
```

The PDF build needs `pandoc` and Google Chrome (already installed here); the PPTX build needs
`python-pptx` and `Pillow`. Both scripts read figures/tables from `results/`.

---

## 5. Before the final submission (6 Dec)

Search the whole package:

```bash
grep -R "\[GROUP-ID\]\|\[CRN\]\|GITHUB-USERNAME\|Member [A-E]" .   # must return nothing
grep -R "{{" report slides README.md                                  # must return nothing
```

Then follow `project-management/SUBMISSION-CHECKLIST.md` line by line (17 acceptance tests).
