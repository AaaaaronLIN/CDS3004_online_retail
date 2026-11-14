#!/usr/bin/env python3
"""Build the CDS3004 Group F presentation deck (20-minute version) from slides/SLIDES.md.

Design goals: assertion-style slide titles, one idea per slide, generous white
space, consistent navy/teal palette, KPI cards, tables and figures that carry the
evidence, speaker notes embedded on every slide.

Run with the bundled runtime python (has python-pptx + Pillow):
    /Users/aronlin/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/python/bin/python3 \
        tools/build_pptx.py --out submission/final/CDS3004_GroupF_CRN234_Slides.pptx
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

PROJ = pathlib.Path(__file__).resolve().parents[1]
SLIDES_MD = PROJ / "slides" / "SLIDES.md"
FIG_DIR = PROJ / "results" / "figures"
ARTIFACTS_MD = PROJ / "results" / "ARTIFACTS.md"

# palette
NAVY = RGBColor(0x0F, 0x21, 0x37)
INK = RGBColor(0x1F, 0x2A, 0x37)
TEAL = RGBColor(0x0E, 0x7C, 0x7B)
TEAL_LIGHT = RGBColor(0xE3, 0xF1, 0xF0)
AMBER = RGBColor(0xB7, 0x79, 0x1F)
GREY = RGBColor(0x4A, 0x55, 0x68)
MUTED = RGBColor(0x7A, 0x86, 0x96)
LIGHT = RGBColor(0xF2, 0xF5, 0xF8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Arial"

SW, SH = 13.333, 7.5
MARGIN = 0.62


# --------------------------------------------------------------------------- #
# markdown parsing
# --------------------------------------------------------------------------- #
def parse_slides(md: str) -> list[dict]:
    slides: list[dict] = []
    cur: dict | None = None
    section = None
    for raw in md.splitlines():
        line = raw.rstrip()
        m = re.match(r"^##\s+Slide\s+(\d+)\s*[—\-–]\s*(.+)$", line)
        if m:
            cur = {"num": int(m.group(1)), "title": m.group(2).strip(),
                   "section": "", "layout": "side", "bullets": [], "notes": "",
                   "visual": "", "timing": "", "speaker": "", "kpis": [],
                   "takeaway": "", "source": "", "table": [], "timeline": []}
            slides.append(cur)
            section = None
            continue
        if cur is None:
            continue
        if line.startswith("**Section:**"):
            cur["section"] = line.split("**Section:**", 1)[1].strip()
            continue
        if line.startswith("**Cumulative timing:**"):
            cur["timing"] = line.split("**Cumulative timing:**", 1)[1].strip()
            sm = re.search(r"\*\*Speaker:\*\*\s*(.+)", cur["timing"])
            if sm:
                cur["speaker"] = sm.group(1).strip()
            continue
        if line.startswith("**Layout:**"):
            cur["layout"] = line.split("**Layout:**", 1)[1].strip().lower()
            continue
        if line.startswith("**On-slide bullets**"):
            section = "bullets"
            continue
        if line.startswith("**KPI:**"):
            raw_kpi = line.split("**KPI:**", 1)[1].strip()
            for part in raw_kpi.split("|"):
                part = part.strip()
                if "=" in part:
                    k, v = part.split("=", 1)
                    cur["kpis"].append((k.strip(), v.strip()))
            continue
        if line.startswith("**Timeline:**"):
            raw_tl = line.split("**Timeline:**", 1)[1].strip()
            cur["timeline"] = [p.strip() for p in raw_tl.split("|") if p.strip()]
            continue
        if line.startswith("**Table:**"):
            section = "table"
            continue
        if line.startswith("**Visual:**"):
            cur["visual"] = line.split("**Visual:**", 1)[1].strip()
            section = None
            continue
        if line.startswith("**Takeaway:**"):
            cur["takeaway"] = line.split("**Takeaway:**", 1)[1].strip()
            section = None
            continue
        if line.startswith("**Source:**"):
            cur["source"] = line.split("**Source:**", 1)[1].strip()
            section = None
            continue
        if line.startswith("**Speaker notes"):
            cur["notes"] = line.split(":**", 1)[1].strip() if ":**" in line else ""
            section = "notes"
            continue
        if line.startswith("---"):
            section = None
            continue
        if section == "bullets" and re.match(r"^[-*]\s+", line):
            cur["bullets"].append(re.sub(r"^[-*]\s+", "", line).strip())
        elif section == "table" and "|" in line:
            cur["table"].append([c.strip() for c in line.strip("|").split("|")])
        elif section == "notes" and line.strip():
            cur["notes"] += " " + line.strip()
    for s in slides:
        s["notes"] = re.sub(r"\s+", " ", s["notes"]).strip().strip('"“”')
    return slides


# --------------------------------------------------------------------------- #
# drawing helpers
# --------------------------------------------------------------------------- #
def rect(slide, x, y, w, h, color, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(0.75)
    shp.shadow.inherit = False
    return shp


def tb(slide, x, y, w, h, text, size, color, bold=False, italic=False,
       align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.0, font=FONT):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = spacing
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    r.font.name = font
    return box


def bullets(slide, x, y, w, h, items, size=17, color=GREY, bullet_color=TEAL,
            space=9, head_color=INK):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(space)
        p.line_spacing = 1.03
        r = p.add_run()
        r.text = "•  "
        r.font.size = Pt(size)
        r.font.color.rgb = bullet_color
        r.font.name = FONT
        if ":" in item and len(item.split(":", 1)[0]) < 46:
            head, tail = item.split(":", 1)
            for txt, bold, col in ((head + ":", True, head_color), (tail, False, color)):
                rr = p.add_run()
                rr.text = txt
                rr.font.size = Pt(size)
                rr.font.bold = bold
                rr.font.color.rgb = col
                rr.font.name = FONT
        else:
            rr = p.add_run()
            rr.text = item
            rr.font.size = Pt(size)
            rr.font.color.rgb = color
            rr.font.name = FONT
    return box


def footer(slide, num, total):
    rect(slide, Inches(0), Inches(7.12), Inches(SW), Inches(0.38), NAVY)
    tb(slide, Inches(MARGIN), Inches(7.2), Inches(9), Inches(0.24),
       "CDS3004 Data Mining  ·  Group F  ·  CRN 234  ·  19 November 2026",
       9.5, RGBColor(0xC7, 0xD2, 0xDE))
    tb(slide, Inches(11.2), Inches(7.2), Inches(1.5), Inches(0.24),
       f"{num} / {total}", 9.5, RGBColor(0xC7, 0xD2, 0xDE), align=PP_ALIGN.RIGHT)


def header(slide, s):
    if s["section"]:
        tb(slide, Inches(MARGIN), Inches(0.34), Inches(9), Inches(0.25),
           s["section"].upper(), 10, TEAL, bold=True)
    tb(slide, Inches(MARGIN), Inches(0.58), Inches(11.4), Inches(0.95),
       s["title"], 24, NAVY, bold=True, spacing=1.0)
    rect(slide, Inches(MARGIN), Inches(1.56), Inches(1.15), Inches(0.045), TEAL)
    t = re.match(r"(\d+:\d+)\s*[–-]\s*(\d+:\d+)", s["timing"])
    if t:
        tb(slide, Inches(11.05), Inches(0.34), Inches(1.65), Inches(0.24),
           f"{t.group(1)}–{t.group(2)}", 9, MUTED, align=PP_ALIGN.RIGHT)


def takeaway_bar(slide, text):
    rect(slide, Inches(MARGIN), Inches(6.34), Inches(12.1), Inches(0.48), TEAL_LIGHT)
    rect(slide, Inches(MARGIN), Inches(6.34), Inches(0.055), Inches(0.48), TEAL)
    tb(slide, Inches(MARGIN + 0.17), Inches(6.43), Inches(11.8), Inches(0.32),
       text, 12, INK)


def source_line(slide, text):
    tb(slide, Inches(MARGIN), Inches(6.9), Inches(9.8), Inches(0.18),
       text, 7.5, MUTED)


def kpi_card(slide, x, y, w, h, value, label):
    rect(slide, x, y, w, h, LIGHT)
    rect(slide, x, y, w, Inches(0.055), TEAL)
    tb(slide, x + Inches(0.14), y + Inches(0.16), w - Inches(0.28), Inches(0.5),
       value, 23, NAVY, bold=True)
    tb(slide, x + Inches(0.14), y + Inches(0.72), w - Inches(0.28), h - Inches(0.78),
       label, 9.5, GREY, spacing=0.98)


def add_figure(slide, fig, box_x, box_y, box_w, box_h, caption=None):
    with Image.open(fig) as im:
        w_px, h_px = im.size
    aspect = w_px / h_px
    if aspect >= box_w / box_h:
        fw = box_w
        fh = fw / aspect
    else:
        fh = box_h
        fw = fh * aspect
    left = box_x + (box_w - fw) / 2
    top = box_y + (box_h - fh) / 2
    slide.shapes.add_picture(str(fig), Inches(left), Inches(top), width=Inches(fw))
    if caption:
        tb(slide, Inches(box_x), Inches(box_y + box_h - 0.02), Inches(box_w),
           Inches(0.22), caption, 8.5, MUTED, italic=True, align=PP_ALIGN.CENTER)


def find_figure(visual: str):
    if not visual:
        return None
    p = pathlib.Path(visual)
    if p.is_absolute() and p.exists():
        return p
    cand = PROJ / visual
    if cand.exists():
        return cand
    stems = sorted(x.stem for x in FIG_DIR.glob("*.png"))
    tokens = re.findall(r"[ft]\d{2}[a-z]?_[A-Za-z0-9_]+", visual)
    for tok in tokens:
        for stem in stems:
            if stem == tok or stem.startswith(tok) or tok.startswith(stem):
                return FIG_DIR / f"{stem}.png"
    return None


def add_table(slide, x, y, w, h, rows):
    if not rows:
        return
    n_rows, n_cols = len(rows), len(rows[0])
    shape = slide.shapes.add_table(n_rows, n_cols, Inches(x), Inches(y),
                                   Inches(w), Inches(h))
    table = shape.table
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = ""
            cell.margin_left = Inches(0.05)
            cell.margin_right = Inches(0.03)
            cell.margin_top = Inches(0.02)
            cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            run = p.add_run()
            run.text = val
            run.font.name = FONT
            run.font.size = Pt(10 if r else 10.5)
            run.font.bold = r == 0
            run.font.color.rgb = WHITE if r == 0 else INK
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY if r == 0 else (LIGHT if r % 2 == 0 else WHITE)


def draw_timeline(slide, items, y=1.95):
    n = len(items)
    gap = 0.35
    box_w = (12.1 - gap * (n - 1)) / n
    for i, item in enumerate(items):
        x = MARGIN + i * (box_w + gap)
        rect(slide, Inches(x), Inches(y), Inches(box_w), Inches(1.28), LIGHT)
        rect(slide, Inches(x), Inches(y), Inches(box_w), Inches(0.055), TEAL)
        parts = [p.strip() for p in item.split("::")]
        label = parts[0] if parts else item
        desc = parts[1] if len(parts) > 1 else ""
        tb(slide, Inches(x + 0.14), Inches(y + 0.16), Inches(box_w - 0.28), Inches(0.3),
           label, 12.5, NAVY, bold=True)
        if desc:
            tb(slide, Inches(x + 0.14), Inches(y + 0.52), Inches(box_w - 0.28), Inches(0.72),
               desc, 9.5, GREY, spacing=1.0)
        if i < n - 1:
            tb(slide, Inches(x + box_w - 0.02), Inches(y + 0.55), Inches(gap + 0.06),
               Inches(0.3), "▶", 9, TEAL, align=PP_ALIGN.CENTER)


# --------------------------------------------------------------------------- #
# slide renderers
# --------------------------------------------------------------------------- #
def title_slide(prs, s, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    rect(slide, Inches(0), Inches(0), Inches(SW), Inches(SH), WHITE)
    rect(slide, Inches(0), Inches(0), Inches(0.18), Inches(SH), TEAL)
    tb(slide, Inches(0.9), Inches(0.75), Inches(11.5), Inches(0.3),
       "LINGNAN UNIVERSITY  ·  SCHOOL OF DATA SCIENCE  ·  CDS3004 DATA MINING",
       10.5, MUTED, bold=True)
    tb(slide, Inches(0.9), Inches(1.55), Inches(11.6), Inches(1.9),
       "From transactions to a customer operating system",
       40, NAVY, bold=True, spacing=1.02)
    tb(slide, Inches(0.9), Inches(3.45), Inches(11.2), Inches(0.5),
       "An agent-assisted data-mining study of online retail customer behaviour",
       16, GREY)
    rect(slide, Inches(0.9), Inches(4.2), Inches(1.4), Inches(0.05), TEAL)
    tb(slide, Inches(0.9), Inches(4.55), Inches(6.6), Inches(0.35),
       "Group F  ·  CRN 234  ·  19 November 2026", 13, INK, bold=True)
    tb(slide, Inches(0.9), Inches(4.95), Inches(11), Inches(0.3),
       "Public repository: github.com/AaaaaronLIN/CDS3004_online_retail",
       10.5, MUTED)
    tb(slide, Inches(0.9), Inches(5.35), Inches(11), Inches(0.3),
       "Presented by LIN Xiaotong · Patten Lai · Weng Zhi Chao · Lim Man Tung Marcus · Huang Hao Lin",
       10.5, MUTED)
    tb(slide, Inches(0.9), Inches(6.55), Inches(11), Inches(0.3),
       "All figures, tables and numbers in this deck are regenerated by one notebook; "
       "every claim is traceable to results/metrics.json.",
       9, MUTED, italic=True)
    footer(slide, 1, total)
    slide.notes_slide.notes_text_frame.text = s["notes"]


def content_slide(prs, s, idx, total, backup=False):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header(slide, s)
    if backup:
        rect(slide, Inches(10.28), Inches(0.3), Inches(2.42), Inches(0.34), AMBER)
        tb(slide, Inches(10.28), Inches(0.37), Inches(2.42), Inches(0.22),
           "BACKUP · Q&A ONLY", 8.5, WHITE, bold=True, align=PP_ALIGN.CENTER)
    fig = find_figure(s["visual"])
    layout = s["layout"]
    bullets_y = 1.78
    bullets_h = 4.5 if s["takeaway"] else 5.0

    if layout == "kpi" and s["kpis"]:
        bullets(slide, Inches(MARGIN), Inches(bullets_y + 0.05), Inches(6.05),
                Inches(bullets_h), s["bullets"], size=15.5)
        cols = 2
        card_w, card_h = 2.72, 1.42
        gx, gy = 0.22, 0.22
        for i, (value, label) in enumerate(s["kpis"][:4]):
            r, c = divmod(i, cols)
            kpi_card(slide, Inches(6.95 + c * (card_w + gx)),
                     Inches(1.82 + r * (card_h + gy)),
                     Inches(card_w), Inches(card_h), value, label)
    elif layout == "timeline" and s["timeline"]:
        draw_timeline(slide, s["timeline"])
        bullets(slide, Inches(MARGIN), Inches(3.55), Inches(12.1), Inches(2.65),
                s["bullets"], size=14.5, space=7)
    elif layout == "table" and s["table"]:
        bullets(slide, Inches(MARGIN), Inches(bullets_y), Inches(5.0),
                Inches(bullets_h), s["bullets"], size=14)
        add_table(slide, 5.9, 1.95, 6.85, 3.4, s["table"])
    elif fig is not None and layout != "text":
        with Image.open(fig) as im:
            w_px, h_px = im.size
        aspect = w_px / h_px
        if layout == "wide" or aspect >= 2.05:
            box_w = 12.1
            fh = min(box_w / aspect, 2.75)
            fw = fh * aspect
            add_figure(slide, fig, MARGIN + (box_w - fw) / 2, 1.78, fw, fh)
            bullets(slide, Inches(MARGIN), Inches(1.78 + fh + 0.28),
                    Inches(12.1), Inches(1.75 if s["takeaway"] else 2.1),
                    s["bullets"], size=13.5, space=5)
        else:
            bullets(slide, Inches(MARGIN), Inches(bullets_y), Inches(5.15),
                    Inches(bullets_h), s["bullets"], size=15)
            add_figure(slide, fig, 6.15, 1.78, 6.55, 4.45)
    else:
        bullets(slide, Inches(MARGIN), Inches(bullets_y + 0.05), Inches(12.0),
                Inches(bullets_h), s["bullets"], size=17)

    if s["takeaway"]:
        takeaway_bar(slide, s["takeaway"])
    if s["source"]:
        source_line(slide, "Source: " + s["source"])
    footer(slide, idx, total)
    slide.notes_slide.notes_text_frame.text = s["notes"]


def closing_slide(prs, s, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    rect(slide, Inches(0), Inches(0), Inches(SW), Inches(SH), NAVY)
    rect(slide, Inches(0), Inches(0), Inches(0.18), Inches(SH), TEAL)
    tb(slide, Inches(0.9), Inches(1.15), Inches(11.4), Inches(0.3),
       "CLOSING", 10.5, RGBColor(0x9F, 0xB6, 0xCC), bold=True)
    tb(slide, Inches(0.9), Inches(1.55), Inches(11.4), Inches(1.0),
       s["title"], 34, WHITE, bold=True)
    bullets(slide, Inches(0.9), Inches(2.85), Inches(11.3), Inches(2.9),
            s["bullets"], size=16, color=RGBColor(0xD5, 0xE0, 0xEA),
            bullet_color=RGBColor(0x4F, 0xC3, 0xB8), space=10, head_color=WHITE)
    tb(slide, Inches(0.9), Inches(6.35), Inches(11), Inches(0.35),
       "Thank you — questions welcome.", 15, RGBColor(0xB9, 0xC8, 0xD8), italic=True)
    footer(slide, total, total)
    slide.notes_slide.notes_text_frame.text = s["notes"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", default=str(SLIDES_MD))
    ap.add_argument("--out", default=str(PROJ / "submission" / "final" / "CDS3004_GroupF_CRN234_Slides.pptx"))
    args = ap.parse_args()

    slides = parse_slides(pathlib.Path(args.src).read_text())
    if not slides:
        print("ERROR: no slides parsed", file=sys.stderr)
        return 2
    print(f"parsed {len(slides)} slides")
    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)
    total = len(slides)
    for i, s in enumerate(slides, start=1):
        if i == 1:
            title_slide(prs, s, total)
        elif s.get("layout") == "closing":
            closing_slide(prs, s, total)
        elif s.get("layout", "").startswith("backup") or s.get("section", "").upper().startswith("BACKUP"):
            content_slide(prs, s, i, total, backup=True)
        else:
            content_slide(prs, s, i, total)
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    print(f"OK -> {out} ({out.stat().st_size/1e6:.2f} MB, {total} slides)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
