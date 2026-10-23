#!/usr/bin/env python3
"""
The 1521 logo system as inline SVG, for the register page and v3.

brand/1521_marks.json holds the logo system as BSaR marked it up on 15 and 23
October 2026 (round six, Ventures/BSAR/Identity-1521/System-2026-10-23/build_marks_r6.py,
from Tyler's selects of 29 September):

    C23 Justified       primary wordmark   QUEEN / 1521 / WEST
    C24 Stacked centre  stacked cut        QUEEN / 15 / 21 / WEST, C23's own numerals,
                                           QUEEN and WEST at equal gaps
    C02 Solid dot       favicon and icon   C23's 1521 in an Orange 021 C dot
    (the C05 badge is out of the system)

Every part carries a class so CSS colours it:

    .lg-n   the numerals           fill  var(--lg-num)
    .lg-w   QUEEN and WEST         fill  var(--lg-word)
    .lg-a   the C02 dot            fill  var(--lg-acc)
    .lg-k   C02's numerals         fill  cream, knocked out of the dot
"""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKS = json.loads((ROOT / "brand" / "1521_marks.json").read_text(encoding="utf-8"))

PAD = {"C23": 0.02, "C24": 0.02, "C02": 0.0}


def inline(name, cls, label="1521 Queen West"):
    m = MARKS[name]
    x0, y0, x1, y1 = m["bbox"]
    pad = PAD[name] * (y1 - y0)
    vb = "%.2f %.2f %.2f %.2f" % (x0 - pad, y0 - pad, x1 - x0 + 2 * pad, y1 - y0 + 2 * pad)
    out = ['<svg class="lg %s" viewBox="%s" role="img" aria-label="%s" focusable="false">'
           % (cls, vb, label)]
    for p in m["parts"]:
        if p["kind"] == "disc":
            out.append('<circle class="lg-a" cx="%.2f" cy="%.2f" r="%.2f"/>' % (p["cx"], p["cy"], p["r"]))
        else:
            if p["role"] == "word":
                c = "lg-w"
            elif name == "C02":
                c = "lg-k"
            else:
                c = "lg-n"
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
        if p.get("role") == "num":
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
    for n in ("C23", "C24", "C02"):
        print(n, len(inline(n, "x")), "bytes")
    print(favicon_links()[:120])
