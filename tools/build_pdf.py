#!/usr/bin/env python3
"""Render report/REPORT.md into a submission-quality PDF.

Pipeline:
  1. resolve {{METRIC:...}} placeholders from results/metrics.json
  2. resolve {{TABLE:...}} markers into HTML tables from results/tables/*.csv
  3. resolve {{FIGURE:...}} markers into embedded plots from results/figures/*.png
  4. convert markdown -> HTML5 with pandoc (styled by tools/style.css)
  5. print HTML -> PDF with headless Google Chrome (A4)

Usage:
    /opt/anaconda3/bin/python tools/build_pdf.py \
        [--src report/REPORT.md] [--out submission/final/CDS3004_Report.pdf]
"""
from __future__ import annotations

import argparse
import html
import json
import os
import pathlib
import re
import subprocess
import sys

import pandas as pd

PROJ = pathlib.Path(__file__).resolve().parents[1]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PANDOC = "/opt/anaconda3/bin/pandoc"

METRIC_RE = re.compile(r"\{\{METRIC:([^}]+)\}\}")
TABLE_RE = re.compile(r"\{\{TABLE:([^}]+)\}\}")
FIGURE_RE = re.compile(r"\{\{FIGURE:([^}]+)\}\}")


def _lookup(metrics: dict, dotted: str):
    cur = metrics
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def _fmt(key: str, value) -> str:
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        if any(t in key for t in ("pct", "roi_pct")):
            return f"{value:.1f}"
        if "lift" in key:
            return f"{value:.2f}"
        if any(t in key for t in ("auc", "silhouette", "ari", "rate", "ratio", "variance")):
            return f"{value:.3f}"
        if abs(value) >= 100:
            return f"{value:,.2f}"
        if abs(value) >= 1:
            return f"{value:.2f}"
        return f"{value:.3f}"
    return str(value)


def _md_escape(text: str) -> str:
    return str(text).replace("|", "\\|")


def csv_to_html_table(csv_path: pathlib.Path, max_rows: int = 40) -> str:
    df = pd.read_csv(csv_path)
    n = len(df)
    if n > max_rows:
        df = df.head(max_rows)
    cols = list(df.columns)
    head = "".join(f"<th>{html.escape(str(c))}</th>" for c in cols)
    body_rows = []
    for _, row in df.iterrows():
        cells = []
        for c in cols:
            val = row[c]
            if isinstance(val, float):
                text = f"{val:.3f}" if abs(val) < 1000 else f"{val:,.1f}"
            else:
                text = str(val)
            cells.append(f"<td>{html.escape(text)}</td>")
        body_rows.append("<tr>" + "".join(cells) + "</tr>")
    note = (
        f'<p class="table-note">Showing first {max_rows} of {n} rows.</p>'
        if n > max_rows
        else ""
    )
    return (
        '<table class="data-table"><thead><tr>'
        + head
        + "</tr></thead><tbody>"
        + "".join(body_rows)
        + "</tbody></table>"
        + note
    )


def build(
    src: pathlib.Path,
    out_pdf: pathlib.Path,
    keep_draft_note: bool = False,
    strict: bool = True,
) -> int:
    metrics_path = PROJ / "results" / "metrics.json"
    if not metrics_path.exists():
        print(f"ERROR: {metrics_path} not found — run the notebook first.", file=sys.stderr)
        return 2
    metrics = json.loads(metrics_path.read_text())

    text = src.read_text()
    missing_metrics: list[str] = []
    missing_artifacts: list[str] = []

    def repl_metric(m: re.Match) -> str:
        key = m.group(1).strip()
        if key in ("...", "section.key"):
            return "—"
        val = _lookup(metrics, key)
        if val is None:
            missing_metrics.append(key)
            return f'<span class="missing">[[{key}]]</span>'
        return _fmt(key, val)

    def repl_table(m: re.Match) -> str:
        name = m.group(1).strip()
        if name == "...":
            return "—"
        path = PROJ / "results" / "tables" / f"{name}.csv"
        if not path.exists():
            missing_artifacts.append(str(path.relative_to(PROJ)))
            return f'<span class="missing">[[missing table: {name}]]</span>'
        return "\n\n" + csv_to_html_table(path) + "\n\n"

    html_dir = (PROJ / "submission" / "final").resolve()

    def repl_figure(m: re.Match) -> str:
        name = m.group(1).strip()
        if name == "...":
            return "—"
        path = (PROJ / "results" / "figures" / f"{name}.png").resolve()
        if not path.exists():
            missing_artifacts.append(str(path.relative_to(PROJ)))
            return f'<span class="missing">[[missing figure: {name}]]</span>'
        rel = os.path.relpath(path, start=html_dir).replace(os.sep, "/")
        return f'\n\n<figure><img src="{rel}" /></figure>\n\n'

    text = METRIC_RE.sub(repl_metric, text)
    text = TABLE_RE.sub(repl_table, text)
    text = FIGURE_RE.sub(repl_figure, text)

    # drop the authoring-only draft note and placeholder index appendix
    if not keep_draft_note:
        text = re.sub(r"^> \*\*Draft note\.\*\*.*\n?(\n> .*\n?)*", "", text, flags=re.M)
        text = re.sub(
            r"\n#{1,3}\s*Appendix [A-Z][^\n]*[Pp]laceholder[^\n]*\n.*\Z",
            "\n",
            text,
            flags=re.S,
        )

    filled_md = PROJ / "submission" / "final" / f"{out_pdf.stem}.md"
    filled_md.parent.mkdir(parents=True, exist_ok=True)
    filled_md.write_text(text)

    if missing_metrics or missing_artifacts:
        print("WARNING — unresolved references:", file=sys.stderr)
        for k in sorted(set(missing_metrics)):
            print(f"  missing metric: {k}", file=sys.stderr)
        for a in sorted(set(missing_artifacts)):
            print(f"  missing artifact: {a}", file=sys.stderr)
        if strict:
            print("Strict mode: not rendering PDF.", file=sys.stderr)
            return 1

    html_path = PROJ / "submission" / "final" / f"{out_pdf.stem}.html"
    cmd = [
        PANDOC,
        str(filled_md),
        "-f", "gfm+raw_html",
        "-t", "html5",
        "-s",
        "--metadata", "lang=en",
        "--variable", f"pagetitle={out_pdf.stem}",
        "--css", str(PROJ / "tools" / "style.css"),
        "--resource-path", str(PROJ),
        "-o", str(html_path),
    ]
    (PROJ / ".cache" / "chrome").mkdir(parents=True, exist_ok=True)
    print("pandoc:", " ".join(cmd[:3]), "...")
    subprocess.run(cmd, check=True)

    if not pathlib.Path(CHROME).exists():
        print(f"ERROR: Chrome not found at {CHROME}", file=sys.stderr)
        return 3

    chrome = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--virtual-time-budget=5000",
        f"--user-data-dir={PROJ / '.cache' / 'chrome'}",
        f"--crash-dumps-dir={PROJ / '.cache' / 'chrome' / 'crash'}",
        f"--print-to-pdf={out_pdf}",
        html_path.as_uri(),
    ]
    print("chrome: printing", out_pdf.name, "...")
    subprocess.run(chrome, check=True, capture_output=True)
    print(f"OK -> {out_pdf}  ({out_pdf.stat().st_size / 1e6:.2f} MB)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", default=str(PROJ / "report" / "REPORT.md"))
    ap.add_argument("--out", default=str(PROJ / "submission" / "final" / "CDS3004_Report.pdf"))
    ap.add_argument("--keep-draft-note", action="store_true")
    ap.add_argument("--allow-missing", action="store_true")
    args = ap.parse_args()
    return build(
        pathlib.Path(args.src),
        pathlib.Path(args.out),
        keep_draft_note=args.keep_draft_note,
        strict=not args.allow_missing,
    )


if __name__ == "__main__":
    sys.exit(main())
