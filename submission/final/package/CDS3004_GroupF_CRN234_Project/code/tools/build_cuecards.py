#!/usr/bin/env python3
"""Generate speaker cue cards (one page per slide) from slides/SLIDES.md."""
from __future__ import annotations
import pathlib, re, sys

PROJ = pathlib.Path(__file__).resolve().parents[1]
SRC = PROJ / "slides" / "SLIDES.md"
OUT = PROJ / "slides" / "CUE-CARDS.md"


def parse(md: str) -> list[dict]:
    slides, cur, section = [], None, None
    for raw in md.splitlines():
        line = raw.rstrip()
        m = re.match(r"^##\s+Slide\s+(\d+)\s*[—\-–]\s*(.+)$", line)
        if m:
            cur = {"num": int(m.group(1)), "title": m.group(2).strip(),
                   "bullets": [], "notes": "", "speaker": "", "timing": "", "visual": ""}
            slides.append(cur); section = None; continue
        if cur is None:
            continue
        if line.startswith("**Cumulative timing:**"):
            cur["timing"] = line.split("**Cumulative timing:**", 1)[1].strip()
            sm = re.search(r"\*\*Speaker:\*\*\s*(.+)", cur["timing"])
            if sm:
                cur["speaker"] = sm.group(1).strip()
            continue
        if line.startswith("**On-slide bullets**"):
            section = "bullets"; continue
        if line.startswith("**Visual:**"):
            cur["visual"] = line.split("**Visual:**", 1)[1].strip(); section = None; continue
        if line.startswith("**Speaker notes"):
            cur["notes"] = line.split(":**", 1)[1].strip() if ":**" in line else ""
            section = "notes"; continue
        if line.startswith("**Presentation rubric focus:**"):
            section = None; continue
        if line.startswith("---"):
            section = None; continue
        if section == "bullets" and re.match(r"^[-*]\s+", line):
            cur["bullets"].append(re.sub(r"^[-*]\s+", "", line).strip())
        elif section == "notes" and line.strip():
            cur["notes"] += " " + line.strip()
    for s in slides:
        s["notes"] = re.sub(r"\s+", " ", s["notes"]).strip().strip('"“”')
    return slides


def main() -> int:
    slides = parse(SRC.read_text())
    parts = ["# CDS3004 Group F — Speaker Cue Cards\n",
             "**Group F · CRN 234 · 19 November 2026 · total 9:35**\n",
             "One page per slide. Upper block = what the audience sees; lower block = what you say.\n"]
    for s in slides:
        timing = s["timing"].split("·")[0].replace("**Cumulative timing:**", "").strip()
        parts.append(f"\n<div style=\"page-break-after: always;\"></div>\n")
        parts.append(f"## Slide {s['num']} — {s['title']}\n")
        parts.append(f"**{timing}** · **Speaker:** {s['speaker']}\n")
        parts.append("\n**On screen**\n")
        for b in s["bullets"]:
            parts.append(f"- {b}\n")
        if s["visual"]:
            parts.append(f"\n**Visual:** {s['visual']}\n")
        parts.append(f"\n**Say (verbatim from the plan):**\n\n> {s['notes']}\n")
        parts.append("\n**Do:** look up at the audience here; do not read the slide.\n")
    OUT.write_text("".join(parts))
    print(f"wrote {OUT} ({len(slides)} cards)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
