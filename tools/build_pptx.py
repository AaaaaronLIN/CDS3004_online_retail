#!/usr/bin/env python3
"""Build the CDS3004 group-presentation PPTX from slides/SLIDES.md.

The slide plan (slides/SLIDES.md) is the single source of truth; this script
parses it and renders a clean 16:9 deck, embedding the results figures named in
the plan. Wide figures get a full-width "figure on top" layout so they stay
legible; everything else uses a bullets/figure split.

Run with the bundled runtime python that has python-pptx:

    /Users/aronlin/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/python/bin/python3 \
        tools/build_pptx.py --out submission/final/CDS3004_Slides.pptx
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

PROJ = pathlib.Path(__file__).resolve().parents[1]
SLIDES_MD = PROJ / "slides" / "SLIDES.md"
FIG_DIR = PROJ / "results" / "figures"
ARTIFACTS_MD = PROJ / "results" / "ARTIFACTS.md"

NAVY = RGBColor(0x10, 0x24, 0x3F)
TEAL = RGBColor(0x0F, 0x76, 0x6E)
GREY = RGBColor(0x44, 0x4F, 0x5A)
LIGHT = RGBColor(0xE8, 0xEE, 0xF4)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Arial"
SLIDE_W = 13.333
SLIDE_H = 7.5


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def load_artifact_descriptions() -> dict[str, str]:
    desc: dict[str, str] = {}
    if not ARTIFACTS_MD.exists():
        return desc
    for line in ARTIFACTS_MD.read_text().splitlines():
        m = re.match(
            r"^-\s+`([ft]\d+[a-z]?_[A-Za-z0-9_]+)\.(png|csv)`\s+[—-]\s+(.+?)(\s+\[OK\])?$",
            line.strip(),
        )
        if m:
            text = m.group(3).strip()
            if text.lower().startswith("alias of"):
                continue
            desc[m.group(1)] = text
    return desc


def find_figure(visual: str) -> pathlib.Path | None:
    if not FIG_DIR.exists():
        return None
    stems = sorted(p.stem for p in FIG_DIR.glob("*.png"))
    tokens = re.findall(r"[ft]\d{2}[a-z]?_[A-Za-z0-9_]+", visual)
    for tok in tokens:
        for stem in stems:
            if stem == tok or stem.startswith(tok) or tok.startswith(stem):
                return FIG_DIR / f"{stem}.png"
    m = re.search(r"\b([ft])(\d{2})\b", visual)
    if m:
        prefix = f"{m.group(1)}{m.group(2)}"
        for stem in stems:
            if stem.startswith(prefix):
                return FIG_DIR / f"{stem}.png"
    return None


def display_caption(stem: str, descr: dict[str, str]) -> str:
    if stem in descr:
        text = re.split(r"\s*\(", descr[stem])[0].strip()
        if len(text) > 92:
            text = text[:89].rstrip() + "…"
        return text[0].upper() + text[1:]
    words = re.sub(r"^[ft]\d+[a-z]?_", "", stem).replace("_", " ")
    return (words[0].upper() + words[1:]) if words else stem


def add_bg_rect(slide, x, y, w, h, color):
    from pptx.enum.shapes import MSO_SHAPE

    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def add_text(slide, x, y, w, h, text, size, color, bold=False, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, line_spacing=1.0, italic=False):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line_spacing
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = FONT
    return tb


def add_bullets(slide, x, y, w, h, bullets, size=16, head_color=NAVY,
                body_color=GREY, mark_color=TEAL):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(7)
        p.line_spacing = 1.02
        r0 = p.add_run()
        r0.text = "▸  "
        r0.font.size = Pt(size)
        r0.font.color.rgb = mark_color
        r0.font.bold = True
        r0.font.name = FONT
        if ":" in b and len(b.split(":", 1)[0]) < 44:
            head, tail = b.split(":", 1)
            for text, bold, color in ((head + ":", True, head_color), (tail, False, body_color)):
                r = p.add_run()
                r.text = text
                r.font.size = Pt(size)
                r.font.bold = bold
                r.font.color.rgb = color
                r.font.name = FONT
        else:
            r = p.add_run()
            r.text = b
            r.font.size = Pt(size)
            r.font.color.rgb = body_color
            r.font.name = FONT
    return tb


def fit_bullet_size(bullets: list[str], base: int, min_size: int) -> int:
    chars = sum(len(b) for b in bullets)
    size = base
    while size > min_size and chars > 430 - (base - size) * 40:
        size -= 1
    return size


def set_notes(slide, text: str):
    if text:
        slide.notes_slide.notes_text_frame.text = text


def footer(slide, num: int, total: int, course="CDS3004 Data Mining · Group Project"):
    add_bg_rect(slide, 0, Inches(7.12), Inches(SLIDE_W), Inches(0.38), NAVY)
    add_text(slide, Inches(0.5), Inches(7.2), Inches(9), Inches(0.25), course, 10, LIGHT)
    add_text(slide, Inches(11.3), Inches(7.2), Inches(1.55), Inches(0.25),
             f"{num} / {total}", 10, LIGHT, align=PP_ALIGN.RIGHT)


def header(slide, title: str, timing: str | None):
    add_bg_rect(slide, 0, 0, Inches(SLIDE_W), Inches(0.95), NAVY)
    add_bg_rect(slide, Inches(0.5), Inches(1.02), Inches(1.1), Inches(0.055), TEAL)
    add_text(slide, Inches(0.5), Inches(0.17), Inches(11.4), Inches(0.72),
             title, 25, WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    if timing:
        t = re.match(r"(\d+:\d+[–-]\d+:\d+)", timing)
        if t:
            add_text(slide, Inches(11.7), Inches(0.36), Inches(1.4), Inches(0.3),
                     t.group(1), 10.5, LIGHT, align=PP_ALIGN.RIGHT)


# --------------------------------------------------------------------------- #
# slide renderers
# --------------------------------------------------------------------------- #
def title_slide(prs, s, total, descr):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg_rect(slide, 0, 0, Inches(SLIDE_W), Inches(SLIDE_H), NAVY)
    add_text(slide, Inches(0.9), Inches(1.15), Inches(11.6), Inches(0.35),
             "CDS3004 DATA MINING  ·  GROUP PROJECT  ·  2026/27 TERM 1", 12.5,
             RGBColor(0x9F, 0xB6, 0xCC), bold=True)
    add_bg_rect(slide, Inches(0.9), Inches(1.75), Inches(1.6), Inches(0.07), TEAL)
    add_text(slide, Inches(0.9), Inches(2.05), Inches(11.6), Inches(1.55),
             "From Transactions to a Customer Operating System", 38, WHITE,
             bold=True, line_spacing=1.0)
    add_text(slide, Inches(0.9), Inches(3.55), Inches(11.4), Inches(0.45),
             "An agent-assisted data-mining study of online retail customer behaviour",
             17, RGBColor(0xB9, 0xC8, 0xD8))
    hook = next((b for b in s["bullets"] if "?" in b), None)
    if hook:
        add_text(slide, Inches(0.9), Inches(4.25), Inches(10.8), Inches(0.8),
                 f"“{hook}”", 15, RGBColor(0xD5, 0xE0, 0xEA), italic=True)
    add_text(slide, Inches(0.9), Inches(5.35), Inches(6.6), Inches(0.4),
             "Group F  ·  Thursday 19 November 2026", 13, LIGHT)
    add_text(slide, Inches(0.9), Inches(5.75), Inches(9), Inches(0.35),
             "Public repository: github.com/AaaaaronLIN/CDS3004_online_retail", 10.5,
             RGBColor(0x9F, 0xB6, 0xCC))
    footer(slide, 1, total, course="Lingnan University  ·  School of Data Science")
    set_notes(slide, s["notes"])
    return slide


def content_slide(prs, s, idx, total, descr):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header(slide, s["title"], s["timing"])
    fig = find_figure(s["visual"])
    bullets = s["bullets"]
    if fig:
        with Image.open(fig) as im:
            w_px, h_px = im.size
        aspect = w_px / h_px
        if aspect >= 2.05:  # wide figure -> full width on top, bullets below
            fig_w = 12.15
            fig_h = fig_w / aspect
            if fig_h > 3.15:
                fig_h = 3.15
                fig_w = fig_h * aspect
            slide.shapes.add_picture(str(fig), Inches((SLIDE_W - fig_w) / 2),
                                     Inches(1.2), width=Inches(fig_w))
            add_text(slide, Inches(0.55), Inches(1.2 + fig_h + 0.08),
                     Inches(12.2), Inches(0.26), display_caption(fig.stem, descr),
                     9.5, RGBColor(0x6B, 0x76, 0x82), align=PP_ALIGN.CENTER)
            b_y = 1.2 + fig_h + 0.42
            add_bullets(slide, Inches(0.6), Inches(b_y), Inches(12.1),
                        Inches(7.0 - b_y), bullets,
                        size=fit_bullet_size(bullets, 15, 11))
        else:  # square/portrait figure -> bullets left, figure right
            add_bullets(slide, Inches(0.55), Inches(1.3), Inches(5.45), Inches(5.5),
                        bullets, size=fit_bullet_size(bullets, 16, 11))
            box_x, box_y, box_w, box_h = 6.25, 1.25, 6.55, 4.9
            if aspect >= box_w / box_h:
                fig_w = box_w
                fig_h = fig_w / aspect
            else:
                fig_h = box_h
                fig_w = fig_h * aspect
            slide.shapes.add_picture(
                str(fig), Inches(box_x + (box_w - fig_w) / 2),
                Inches(box_y + (box_h - fig_h) / 2), width=Inches(fig_w))
            add_text(slide, Inches(6.25), Inches(6.33), Inches(6.55), Inches(0.28),
                     display_caption(fig.stem, descr), 9.5,
                     RGBColor(0x6B, 0x76, 0x82), align=PP_ALIGN.CENTER)
    else:
        add_bullets(slide, Inches(0.6), Inches(1.4), Inches(12.1), Inches(5.4),
                    bullets, size=fit_bullet_size(bullets, 20, 14))
        if s["visual"]:
            add_text(slide, Inches(0.6), Inches(6.6), Inches(12.1), Inches(0.3),
                     "Visual: " + re.sub(r"[`*]", "", s["visual"])[:150], 8.5,
                     RGBColor(0x8A, 0x95, 0xA1))
    footer(slide, idx, total)
    set_notes(slide, s["notes"])
    return slide


def closing_slide(prs, s, total, descr):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg_rect(slide, 0, 0, Inches(SLIDE_W), Inches(SLIDE_H), NAVY)
    add_text(slide, Inches(0.9), Inches(1.25), Inches(11.5), Inches(0.9),
             s["title"], 32, WHITE, bold=True)
    add_bg_rect(slide, Inches(0.9), Inches(2.15), Inches(1.4), Inches(0.06), TEAL)
    add_bullets(slide, Inches(0.9), Inches(2.55), Inches(11.3), Inches(3.6),
                s["bullets"], size=fit_bullet_size(s["bullets"], 19, 14),
                head_color=WHITE, body_color=RGBColor(0xD5, 0xE0, 0xEA),
                mark_color=RGBColor(0x4F, 0xC3, 0xB8))
    add_text(slide, Inches(0.9), Inches(6.55), Inches(10), Inches(0.35),
             "Thank you — questions welcome.", 13, RGBColor(0xB9, 0xC8, 0xD8),
             italic=True)
    footer(slide, total, total, course="Lingnan University  ·  School of Data Science")
    set_notes(slide, s["notes"])
    return slide


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
                   "bullets": [], "notes": "", "visual": "", "speaker": "",
                   "timing": "", "rubric": ""}
            slides.append(cur)
            section = None
            continue
        if cur is None:
            continue
        if line.startswith("**Cumulative timing:**"):
            txt = line.split("**Cumulative timing:**", 1)[1].strip()
            cur["timing"] = txt
            sm = re.search(r"\*\*Speaker:\*\*\s*(.+)", txt)
            if sm:
                cur["speaker"] = sm.group(1).strip()
            continue
        if line.startswith("**On-slide bullets**"):
            section = "bullets"
            continue
        if line.startswith("**Visual:**"):
            cur["visual"] = line.split("**Visual:**", 1)[1].strip()
            section = None
            continue
        if line.startswith("**Speaker notes"):
            cur["notes"] = line.split(":**", 1)[1].strip() if ":**" in line else ""
            section = "notes"
            continue
        if line.startswith("**Presentation rubric focus:**"):
            cur["rubric"] = line.split("**Presentation rubric focus:**", 1)[1].strip()
            section = None
            continue
        if line.startswith("---"):
            section = None
            continue
        if section == "bullets" and re.match(r"^[-*]\s+", line):
            cur["bullets"].append(re.sub(r"^[-*]\s+", "", line).strip())
        elif section == "notes" and line.strip():
            cur["notes"] += " " + line.strip()
    for s in slides:
        s["notes"] = re.sub(r"\s+", " ", s["notes"]).strip().strip('"“”')
    return slides


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", default=str(SLIDES_MD))
    ap.add_argument("--out", default=str(PROJ / "submission" / "final" / "CDS3004_Slides.pptx"))
    args = ap.parse_args()

    src = pathlib.Path(args.src)
    if not src.exists():
        print(f"ERROR: {src} not found", file=sys.stderr)
        return 2
    slides = parse_slides(src.read_text())
    if not slides:
        print("ERROR: no slides parsed", file=sys.stderr)
        return 2
    descr = load_artifact_descriptions()
    print(f"parsed {len(slides)} slides, {len(descr)} artifact descriptions")

    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    total = len(slides)
    for i, s in enumerate(slides, start=1):
        if i == 1:
            title_slide(prs, s, total, descr)
        elif i == total:
            closing_slide(prs, s, total, descr)
        else:
            content_slide(prs, s, i, total, descr)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    print(f"OK -> {out}  ({out.stat().st_size / 1e6:.2f} MB, {total} slides)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
