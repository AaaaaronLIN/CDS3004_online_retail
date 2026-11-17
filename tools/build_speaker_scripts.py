"""Build the per-speaker reading scripts (PDF) from slides/SLIDES.md.

The original PDFs in presentation/scripts/ were rendered on macOS with
tools/render_pdf.swift + headless Chrome, which is not reproducible on this
machine. This script keeps the same visual language (navy headings, quote box,
run-of-show table) but renders with PyMuPDF, so any member can rebuild their
script from slides/SLIDES.md:

    PYTHONPATH=.deps python tools/build_speaker_scripts.py            # all speakers
    PYTHONPATH=.deps python tools/build_speaker_scripts.py huang-hao-lin

Speaker metadata (role line, preamble, Q&A prompt) lives in
slides/speaker-scripts.json. The spoken text itself is never duplicated here:
it is read from the `**Speaker notes**` block of each slide.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "slides" / "SLIDES.md"
META = ROOT / "slides" / "speaker-scripts.json"

NAVY = "#22355C"
RULE = "#22355C"
GREY_BAR = "#33507E"
BOX_BG = "#F4F5F7"
HAIRLINE = "#C9D0DD"
MUTED = "#5A6472"

PAGE_W, PAGE_H = 595.0, 842.0
MARGIN_L, MARGIN_R, TOP, BOTTOM = 56.0, 56.0, 62.0, 56.0
W = PAGE_W - MARGIN_L - MARGIN_R

def C(hex_colour: str) -> tuple[float, float, float]:
    """MuPDF wants rgb components; PyMuPDF's helper returns None in this build."""
    h = hex_colour.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


BODY = 'font-family: Georgia, serif; color: #1B1F27;'
HEAD = 'font-family: Helvetica, sans-serif; color: #22355C;'


# ---------------------------------------------------------------- parsing
def parse_slides(text: str) -> list[dict]:
    slides: list[dict] = []
    cur: dict | None = None
    mode = ""
    for raw in text.splitlines():
        line = raw.rstrip()
        m = re.match(r"^## Slide (\d+) — (.+)$", line)
        if m:
            cur = {"num": int(m.group(1)), "title": m.group(2).strip(),
                   "bullets": [], "notes": [], "timing": "", "speaker": "",
                   "takeaway": "", "visual": ""}
            slides.append(cur)
            mode = ""
            continue
        if cur is None:
            continue
        if line == "---":
            mode = ""
            continue
        m = re.match(r"^\*\*Cumulative timing:\*\* (\d{2}:\d{2})[–-](\d{2}:\d{2}) \((\d+) s\)"
                     r" · \*\*Speaker:\*\* (.+)$", line)
        if m:
            cur["start"], cur["end"], cur["secs"] = m.group(1), m.group(2), int(m.group(3))
            cur["speaker"] = m.group(4).strip()
            cur["timing"] = f"{m.group(1)}–{m.group(2)} ({m.group(3)} s)"
            continue
        if line.startswith("**On-slide bullets"):
            mode = "bullets"
            continue
        if line.startswith("**Takeaway:**"):
            cur["takeaway"] = line.split(":**", 1)[1].strip()
            mode = ""
            continue
        if line.startswith("**Visual:**"):
            cur["visual"] = line.split(":**", 1)[1].strip()
            mode = ""
            continue
        if line.startswith("**Speaker notes"):
            mode = "notes"
            rest = line.split(":**", 1)[1].strip()
            cur["notes"].append(rest)
            continue
        if line.startswith("**"):
            mode = ""
            continue
        if not line.strip():
            continue
        if mode == "bullets" and line.startswith("- "):
            cur["bullets"].append(line[2:].strip())
        elif mode == "notes":
            cur["notes"].append(line.strip())
    return slides


def split_notes(lines: list[str]) -> list[str]:
    """Notes arrive as one paragraph per line, wrapped in opening/closing quotes."""
    paras = []
    for i, ln in enumerate(lines):
        ln = ln.strip()
        if i == 0 and ln.startswith('"'):
            ln = ln[1:]
        if i == len(lines) - 1 and ln.endswith('"'):
            ln = ln[:-1]
        ln = ln.strip()
        if ln:
            paras.append(ln)
    return paras


def hm_to_secs(t: str) -> int:
    h, m = t.split(":")
    return int(h) * 3600 + int(m) * 60


def mmss(secs: int) -> str:
    return f"{secs // 60}:{secs % 60:02d}"


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace("\u2014", "&#8212;").replace("\u2013", "&#8211;")
             .replace("\u00d7", "&#215;").replace("\u2265", "&#8805;"))


def wrap(css: str) -> str:
    """PyMuPDF's htmlbox css must be a rule set, not bare declarations."""
    return "body { " + css + " }"


# ---------------------------------------------------------------- text flow
class Flow:
    def __init__(self) -> None:
        self.doc = pymupdf.open()
        self.page = None
        self.y = TOP
        self.pages: list[pymupdf.Page] = []
        self._new_page()

    def _new_page(self) -> None:
        self.page = self.doc.new_page(width=PAGE_W, height=PAGE_H)
        self.pages.append(self.page)
        self.y = TOP

    def page_break(self) -> None:
        if self.y > TOP + 1:
            self._new_page()

    def room(self) -> float:
        return PAGE_H - BOTTOM - self.y

    def need(self, h: float) -> None:
        if h > self.room():
            self._new_page()

    # -- measuring -----------------------------------------------------
    @staticmethod
    def measure(html: str, css: str, width: float = W) -> float:
        d = pymupdf.open()
        p = d.new_page(width=width, height=3000)
        spare, _ = p.insert_htmlbox(pymupdf.Rect(0, 0, width, 3000), html, css=wrap(css))
        d.close()
        return max(0.0, 3000 - spare)

    def html(self, html: str, css: str, width: float = W, gap: float = 0.0,
             x: float = 0.0) -> float:
        h = self.measure(html, css, width)
        self.need(h)
        rect = pymupdf.Rect(MARGIN_L + x, self.y, MARGIN_L + x + width, self.y + h)
        self.page.insert_htmlbox(rect, html, css=wrap(css))
        self.y += h + gap
        return h

    # -- blocks --------------------------------------------------------
    def h1(self, text: str, size: float = 21.5, gap: float = 8.0) -> None:
        css = f"{HEAD} font-size: {size}px; font-weight: bold; line-height: 1.2;"
        self.html(f"<div>{esc(text)}</div>", css, gap=gap)

    def h2(self, text: str, size: float = 14.5, before: float = 14.0, gap: float = 6.0,
           width: float = W, x: float = 0.0) -> None:
        self.y += before
        self.need(size * 1.4 + 2)
        css = f"{HEAD} font-size: {size}px; font-weight: bold; line-height: 1.25;"
        self.html(f"<div>{esc(text)}</div>", css, width=width, x=x, gap=3.0)
        self.hairline(gap=gap)

    def hairline(self, color: str = RULE, thickness: float = 0.7, gap: float = 6.0) -> None:
        self.page.draw_line(pymupdf.Point(MARGIN_L, self.y),
                            pymupdf.Point(MARGIN_L + W, self.y),
                            color=C(color), width=thickness)
        self.y += gap

    def rule_tight(self, gap: float = 4.0) -> None:
        self.page.draw_line(pymupdf.Point(MARGIN_L, self.y),
                            pymupdf.Point(MARGIN_L + W, self.y),
                            color=C(RULE), width=1.2)
        self.y += gap

    def para(self, text: str, size: float = 9.6, leading: float = 1.42,
             gap: float = 5.0, color: str = "#1B1F27", width: float = W) -> None:
        css = (f'font-family: Georgia, serif; color: {color};'
               f" font-size: {size}px; line-height: {leading};")
        self.html(f"<div>{esc(text)}</div>", css, width=width, gap=gap)

    def label(self, text: str, size: float = 9.4, gap: float = 2.5,
              color: str = "#1B1F27") -> None:
        css = (f'font-family: Helvetica, sans-serif; color: {color};'
               f" font-size: {size}px; font-weight: bold; line-height: 1.3;")
        self.html(f"<div>{esc(text)}</div>", css, gap=gap)

    def bullets(self, items: list[str], size: float = 8.9, gap: float = 3.0,
                label: str | None = None) -> None:
        """Keep a bullet list (and its label) on one page: measure first, then draw."""
        indent = 10.5
        css = (f'font-family: Georgia, serif; color: #1B1F27;'
               f" font-size: {size}px; line-height: 1.38;")
        heights = [self.measure(f"<div>{esc(it)}</div>", css, W - indent) for it in items]
        if label:
            # keep the label with its first bullet, then let the list break
            self.need(16.0 + heights[0] + 2)
            self.label(label, size=9.4, gap=4.0)
        first_page = len(self.pages)
        for it, h in zip(items, heights):
            self.need(h + 1)
            if label and len(self.pages) != first_page:
                # the list continued onto a new page: re-state the label
                self.label(f"{label.rstrip(':')} (continued):", size=8.6, gap=3.0,
                           color=MUTED)
                first_page = len(self.pages)
            rect = pymupdf.Rect(MARGIN_L + indent, self.y, MARGIN_L + W, self.y + h)
            self.page.insert_htmlbox(rect, f"<div>{esc(it)}</div>", css=wrap(css))
            cy = self.y + size * 0.62
            self.page.draw_circle(pymupdf.Point(MARGIN_L + 4.6, cy), radius=1.5,
                                  color=None, fill=C(NAVY))
            self.y += h + gap

    def quote(self, paras: list[str], size: float = 9.8, leading: float = 1.5,
              pad: float = 11.0) -> None:
        inner_w = W - 2 * pad - 4
        css = (f'font-family: Georgia, serif; color: #1B1F27;'
               f" font-size: {size}px; line-height: {leading};")
        gaps = 7.0
        body_parts = [f"<div>{esc(p)}</div>" for p in paras]
        html = f"<div>{''.join(body_parts)}</div>"
        # mupdf collapses margins between divs; add explicit spacer divs
        html = "<div>" + "<div style='height:7px'></div>".join(
            f"<div>{esc(p)}</div>" for p in paras) + "</div>"
        h = self.measure(html, css, inner_w)
        box_h = h + 2 * pad
        self.need(box_h + gaps)
        top = self.y
        self.page.draw_rect(pymupdf.Rect(MARGIN_L, top, MARGIN_L + W, top + box_h),
                            color=None, fill=C(BOX_BG))
        self.page.draw_rect(pymupdf.Rect(MARGIN_L, top, MARGIN_L + 2.6, top + box_h),
                            color=None, fill=C(GREY_BAR))
        self.page.insert_htmlbox(pymupdf.Rect(MARGIN_L + pad + 2, top + pad,
                                             MARGIN_L + W - pad, top + box_h - pad),
                                 html, css=wrap(css))
        self.y = top + box_h + gaps

    def tip_box(self, text: str) -> None:
        pad = 11.0
        css = ('font-family: Georgia, serif; color: #2A3342;'
               " font-size: 9.0px; line-height: 1.45;")
        inner_w = W - 2 * pad - 4
        h = self.measure(f"<div>{esc(text)}</div>", css, inner_w)
        box_h = h + 2 * pad
        self.need(box_h)
        top = self.y
        self.page.draw_rect(pymupdf.Rect(MARGIN_L, top, MARGIN_L + W, top + box_h),
                            color=None, fill=C("#EFF1F5"))
        self.page.draw_rect(pymupdf.Rect(MARGIN_L, top, MARGIN_L + 2.6, top + box_h),
                            color=None, fill=C(GREY_BAR))
        self.page.insert_htmlbox(pymupdf.Rect(MARGIN_L + pad + 2, top + pad,
                                             MARGIN_L + W - pad, top + box_h - pad),
                                 f"<div>{esc(text)}</div>", css=wrap(css))
        self.y = top + box_h + 8

    def table(self, header: list[str], rows: list[list[str]], widths: list[float],
              size: float = 8.3) -> None:
        pad_x, pad_y = 5.0, 4.4
        css_body = ('font-family: Georgia, serif; color: #1B1F27;'
                    f" font-size: {size}px; line-height: 1.3;")
        css_head = ('font-family: Helvetica, sans-serif;'
                    f" color: #22355C; font-size: {size}px; font-weight: bold; line-height: 1.3;")

        def row_h(cells: list[str], css: str) -> float:
            hh = 0.0
            for c, w in zip(cells, widths):
                hh = max(hh, self.measure(f"<div>{esc(c)}</div>", css, w - 2 * pad_x))
            return hh + 2 * pad_y

        h_head = row_h(header, css_head)
        heights = [h_head] + [row_h(r, css_body) for r in rows]
        self.need(sum(heights) + 2)
        top = self.y
        x = MARGIN_L
        for i, r in enumerate([header] + rows):
            css = css_head if i == 0 else css_body
            y = top + sum(heights[:i])
            if i == 0:
                self.page.draw_rect(pymupdf.Rect(MARGIN_L, y, MARGIN_L + W, y + heights[0]),
                                    color=None, fill=C("#E7EAF0"))
            cx = MARGIN_L
            for c, w in zip(r, widths):
                self.page.insert_htmlbox(
                    pymupdf.Rect(cx + pad_x, y + pad_y, cx + w - pad_x, y + heights[i] - pad_y),
                    f"<div>{esc(c)}</div>", css=wrap(css))
                cx += w
            y2 = y + heights[i]
            self.page.draw_line(pymupdf.Point(MARGIN_L, y2), pymupdf.Point(MARGIN_L + W, y2),
                                color=C(HAIRLINE), width=0.5)
            x = cx
        self.y = top + sum(heights) + 9

    def finish(self, footer_left: str) -> None:
        total = self.doc.page_count
        for i in range(total):
            p = self.doc[i]
            p.draw_line(pymupdf.Point(MARGIN_L, PAGE_H - BOTTOM + 12),
                        pymupdf.Point(MARGIN_L + W, PAGE_H - BOTTOM + 12),
                        color=C(HAIRLINE), width=0.5)
            p.insert_text(pymupdf.Point(MARGIN_L, PAGE_H - BOTTOM + 24), footer_left,
                          fontname="helv", fontsize=7.2,
                          color=C(MUTED))
            lab = f"page {i + 1} of {total}"
            tw = pymupdf.get_text_length(lab, fontname="helv", fontsize=7.2)
            p.insert_text(pymupdf.Point(MARGIN_L + W - tw, PAGE_H - BOTTOM + 24), lab,
                          fontname="helv", fontsize=7.2,
                          color=C(MUTED))


# ---------------------------------------------------------------- build
def build(key: str, conf: dict, slides: list[dict], all_slides: list[dict]) -> Path:
    mine = [s for s in slides if s["speaker"] == conf["speaker"]]
    if not mine:
        raise SystemExit(f"no slides for speaker {conf['speaker']!r}")

    total_secs = sum(s["secs"] for s in mine)
    # Backup slides and opening slides carry no cumulative timing, so the talk
    # end is the latest end time that any slide declares.
    talk_end = max(s["end"] for s in all_slides if s.get("end"))
    nums = [str(s["num"]) for s in mine]
    meta_line = (f"{conf['role_line']} · " + "slides " + ", ".join(nums[:-1]) + " and " + nums[-1]
                 + f" · speaking time {mmss(total_secs)} · full talk {talk_end} (20:00 limit)")

    flow = Flow()
    flow.h1(conf["title"], size=21.5, gap=6.0)
    flow.rule_tight(gap=9.0)
    flow.para(meta_line, size=8.8, gap=9.0)
    flow.tip_box(conf["preamble"])

    flow.h2("Run of show", size=14.5, before=10.0)
    flow.table(["Slide", "Time", "Title"],
               [[str(s["num"]), s["timing"], s["title"]] for s in mine],
               [40.0, 132.0, W - 172.0])
    flow.y += 8

    for s in mine:
        flow.need(150.0)
        flow.h2(f"Slide {s['num']} — {s['title']}", size=13.6, before=6.0, gap=5.0)
        flow.label(f"Time: {s['timing']}", size=8.9, gap=9.0)
        flow.label("Say:", size=9.4, gap=4.0)
        flow.quote(split_notes(s["notes"]))

        flow.bullets(s["bullets"], label="On screen:")

        if s.get("takeaway"):
            flow.y += 6
            css = ('font-family: Georgia, serif; color: #1B1F27;'
                   " font-size: 9.2px; line-height: 1.42;")
            flow.html(
                '<div><b style="font-family: Helvetica, sans-serif; color: #22355C;">'
                f"Takeaway to land:</b> {esc(s['takeaway'])}</div>", css, gap=5.0)

    if conf.get("handoff"):
        flow.y += 4
        flow.para(conf["handoff"], size=9.0, gap=6.0, color="#2A3342")

    flow.need(90.0)
    flow.h2("Q&A you must be able to answer", size=14.2, before=12.0)
    flow.bullets(conf["qa"], size=9.2, gap=4.5)
    if conf.get("qa_footer"):
        flow.y += 4
        flow.para(conf["qa_footer"], size=8.4, gap=2.0, color=MUTED)

    flow.finish(conf["footer"])
    try:
        # the CJK fallback font is embedded in full otherwise (~8 MB per PDF)
        flow.doc.subset_fonts()
    except Exception as exc:  # pragma: no cover - depends on the font set
        print(f"font subsetting skipped: {exc}")
    out = ROOT / conf["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    flow.doc.save(out, deflate=True, garbage=3)
    flow.doc.close()
    print(f"wrote {out} ({len(flow.pages)} pages)")
    return out


def main() -> int:
    confs = json.loads(META.read_text(encoding="utf-8"))
    slides = parse_slides(SRC.read_text(encoding="utf-8"))
    if not slides:
        raise SystemExit(f"no slides parsed from {SRC}")
    wanted = sys.argv[1:] or list(confs)
    for key in wanted:
        if key not in confs:
            raise SystemExit(f"unknown speaker key {key!r}; known: {', '.join(confs)}")
        build(key, confs[key], slides, slides)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
