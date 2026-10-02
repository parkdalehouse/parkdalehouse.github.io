#!/usr/bin/env python3
"""
The 1521 logo system as inline SVG, for the register page and v3.

brand/1521_marks.json holds the four marks BSaR selected on 29 September 2026,
lifted as exact outlines from Tyler's selects PDF by
Ventures/BSAR/Identity-1521/System-2026-10/extract_marks.py:

    C23 Justified       primary wordmark   QUEEN / 1521 / WEST
    C24 Stacked centre  stacked cut        QUEEN / 15 / 21 / WEST
    C05 Double ring     badge
    C02 Solid dot       favicon and icon

Every part carries a class so CSS colours it, which is what lets the review
switcher show the same mark in each brand colour without a second file:

    .lg-n   the numerals           fill  var(--lg-num)
    .lg-w   QUEEN and WEST         fill  var(--lg-word)
    .lg-a   the accent letters     fill  var(--lg-acc)
    .lg-r1  the outer ring         stroke var(--lg-num)
    .lg-r2  the inner ring         stroke var(--lg-acc)
"""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKS = json.loads((ROOT / "brand" / "1521_marks.json").read_text(encoding="utf-8"))

PAD = {"C23": 0.02, "C24": 0.02, "C05": 0.015, "C02": 0.0}


def _height(d):
    nums = d.replace("M", " ").replace("L", " ").replace("C", " ").replace("Z", " ").split()
    ys = [float(v) for v in nums[1::2]]
    return max(ys) - min(ys)


def inline(name, cls, label="1521 Queen West"):
    m = MARKS[name]
    x0, y0, x1, y1 = m["bbox"]
    pad = PAD[name] * (y1 - y0)
    vb = "%.2f %.2f %.2f %.2f" % (x0 - pad, y0 - pad, x1 - x0 + 2 * pad, y1 - y0 + 2 * pad)
    out = ['<svg class="lg %s" viewBox="%s" role="img" aria-label="%s" focusable="false">'
           % (cls, vb, label)]
    for p in m["parts"]:
        if p["kind"] == "ring":
            c = "lg-r1" if p["role"] == "ink" else "lg-r2"
            out.append('<circle class="%s" cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke-width="%.3f"/>'
                       % (c, p["cx"], p["cy"], p["r"], p["w"]))
        elif p["kind"] == "disc":
            out.append('<circle class="lg-a" cx="%.2f" cy="%.2f" r="%.2f"/>' % (p["cx"], p["cy"], p["r"]))
        else:
            if p["role"] == "accent":
                c = "lg-a"
            elif p["role"] == "knock":
                c = "lg-k"
            else:
                c = "lg-w" if _height(p["d"]) < 9.0 else "lg-n"
            out.append('<path class="%s" d="%s"/>' % (c, p["d"]))
    out.append("</svg>")
    return "".join(out)


def icon_svg(dot="#FD5100", num="#FCF6ED"):
    """C02, the dot alone, as a standalone file: the favicon and social avatar."""
    m = MARKS["C02"]
    disc = [p for p in m["parts"] if p["kind"] == "disc"][0]
    r, cx, cy = disc["r"], disc["cx"], disc["cy"]
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="%.2f %.2f %.2f %.2f">'
           % (cx - r, cy - r, 2 * r, 2 * r),
           '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>' % (cx, cy, r, dot)]
    for p in m["parts"]:
        if p.get("role") == "knock":
            out.append('<path d="%s" fill="%s"/>' % (p["d"], num))
    out.append("</svg>")
    return "".join(out)


def favicon_links():
    svg = icon_svg()
    href = "data:image/svg+xml;base64," + base64.b64encode(svg.encode("ascii")).decode("ascii")
    png = ROOT / "brand" / "1521_icon_orange_180.png"
    links = ['<link rel="icon" type="image/svg+xml" href="%s">' % href]
    if png.exists():
        links.append('<link rel="apple-touch-icon" href="data:image/png;base64,%s">'
                     % base64.b64encode(png.read_bytes()).decode("ascii"))
    return "\n".join(links)


if __name__ == "__main__":
    for n in ("C23", "C24", "C05"):
        print(n, len(inline(n, "x")), "bytes")
    print(favicon_links()[:120])
