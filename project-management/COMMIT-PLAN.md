# Commit plan — Group F (CRN 234)

The course estimates individual workload from **GitHub commits + agent trajectories** (deck p.9).
So: every member commits their own files, with meaningful messages. No `update` / `fix` / `123`.

## Ground rules

- One commit = one coherent change. Message format: `type(scope): what changed`.
  Types: `feat`, `fix`, `docs`, `exp`, `chore`, `data`.
- Each member targets **≥3 meaningful commits** before the presentation and **≥5 before 6 Dec**.
- Never commit: `data/*.xlsx`, `.deps/`, `.cache/`, personal API keys or agent tokens.
- If two members edit the same file (e.g. the notebook), split by section and commit separately.

## Ownership and suggested commits

### Member A — lead, problem definition, report editor, main speaker
| # | Files | Suggested message |
|---|---|---|
| 1 | `report/REPORT.md` (sections 1–3) | `docs(report): tighten problem definition and alternative framings` |
| 2 | `report/REPORT.md` (sections 10–13) | `docs(report): add limitations, contributions and agent-usage section` |
| 3 | `slides/SLIDES.md`, `slides/*.pptx` | `docs(slides): finalise narrative and timings for 10-minute talk` |
| 4 | `CONTRIBUTIONS.md`, `README.md` | `docs: record group F member roles and public repository link` |

### Member B — data engineering (S1–S2)
| # | Files | Suggested message |
|---|---|---|
| 1 | `notebooks/CDS3004_Project.ipynb` (S1) | `feat(data): document cleaning funnel and cancellation handling` |
| 2 | `notebooks/CDS3004_Project.ipynb` (S2) | `feat(data): rebuild T1/T2 snapshots and report label coverage` |
| 3 | `results/tables/t01*.csv`, `t02*.csv` | `data: regenerate data-quality and cohort tables` |

### Member C — clustering, similarity, visualisation (S3, S5)
| # | Files | Suggested message |
|---|---|---|
| 1 | `notebooks/CDS3004_Project.ipynb` (S3) | `feat(sim): compare cosine/euclidean/manhattan with kNN agreement` |
| 2 | `notebooks/CDS3004_Project.ipynb` (S5) | `feat(seg): document K choice with elbow, silhouette and bootstrap ARI` |
| 3 | `results/figures/f04*, f05*, f06*, f11*` | `data: regenerate segmentation and similarity figures` |

### Member D — feature engineering, churn models, evaluation (S4, S6)
| # | Files | Suggested message |
|---|---|---|
| 1 | `notebooks/CDS3004_Project.ipynb` (S4) | `exp(feat): compare all-feature vs selected-feature validation PR-AUC` |
| 2 | `notebooks/CDS3004_Project.ipynb` (S6) | `feat(eval): add out-of-time evaluation and top-decile lift` |
| 3 | `results/figures/f07*, f08*, f09*`, `t08` | `data: regenerate model comparison and ROC/lift figures` |

### Member E — association rules, decision layer, repository (S7–S8)
| # | Files | Suggested message |
|---|---|---|
| 1 | `notebooks/CDS3004_Project.ipynb` (S7) | `feat(rules): validate FP-Growth rules on a later holdout period` |
| 2 | `notebooks/CDS3004_Project.ipynb` (S8) | `feat(decision): churn-conditional campaign value with random baseline` |
| 3 | `results/tables/t10*, t12–t16`, `results/figures/f10, f12, f13` | `data: regenerate rules and decision artefacts` |
| 4 | `README.md`, `.gitignore`, repo settings | `chore(repo): public repository, reproduction steps, ignore rules` |

## First commit (group-level scaffold)

```bash
git add .
git commit -m "scaffold: CDS3004 Group F — reproducible pipeline, report, and slide deck"
```

Then each member makes their own commits from the table above. Do not squash them away — the
history is evidence of who did what.
