#!/usr/bin/env python3
"""
Apply the 1521 rename and Claire's 22 September markups to the v2 skeleton.

Reads   v2/skeleton_v2.html    output of tools/apply_v2.py
Writes  v3/skeleton_v3.html    the edited page, still token-ised

v2 is frozen: Claire's 22 pins from 8 to 10 September anchor to its DOM, so
nothing under v2/ is edited. v3 is a separate build at a separate path with its
own markup-tool store.

Every replacement is asserted on an exact expected count, so a silent miss
becomes a hard failure instead of a wrong page.

Rebuild:  python3 tools/apply_v3.py && python3 tools/inflate.py --target v3

Sources for the changes:
  Claire Bodrug, 22 markups submitted 8 to 10 September 2026 via ?review
  Meeting of 8 September 2026 (Tyler: no offers before pre-leasing)
  BSaR rename of 10 September 2026: "The 501" becomes "1521"
  BSaR-Inbound/2026-09-15_logo-assets/1521_wordmark_BSaR_draft.png
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "v2" / "skeleton_v2.html"
OUT = ROOT / "v3" / "skeleton_v3.html"

_edits = 0


def sub(html, old, new, count=1, label=""):
    """Exact-string replace with an asserted occurrence count."""
    global _edits
    found = html.count(old)
    if found != count:
        raise SystemExit(
            "apply_v3: %s: expected %d occurrence(s), found %d\n  needle: %r"
            % (label or "edit", count, found, old[:160])
        )
    _edits += 1
    return html.replace(old, new)


def resub(html, pattern, new, count=1, label="", flags=0):
    """Regex replace with an asserted match count. `new` may be a callable."""
    global _edits
    rx = re.compile(pattern, flags)
    found = len(rx.findall(html))
    if found != count:
        raise SystemExit(
            "apply_v3: %s: expected %d match(es), found %d\n  pattern: %s"
            % (label or "edit", count, found, pattern[:160])
        )
    _edits += 1
    return rx.sub(new, html)


def cut_block(html, start_marker, end_marker, label=""):
    """Remove everything from start_marker through end_marker inclusive."""
    global _edits
    i = html.find(start_marker)
    j = html.find(end_marker, i + 1)
    if i == -1 or j == -1:
        raise SystemExit("apply_v3: %s: block not found" % (label or "cut"))
    _edits += 1
    return html[:i] + html[j + len(end_marker):]


# ==========================================================================
#  HEAD: title, description, JSON-LD. Markup 8, plus the meeting note.
# ==========================================================================

OLD_HEAD = '''<title>The 501 | Queen West Rentals</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="The 501 at 1521 Queen Street West. Queen West apartments for rent in Toronto: studio to three bedroom Parkdale rentals, steps from the 501 streetcar, Roncesvalles Village and the waterfront.">
<meta name="robots" content="noindex, nofollow, noarchive">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ApartmentComplex",
  "name": "The 501",
  "alternateName": "The 501 Queen West",
  "description": "Landmark rental living on Queen West. Ninety-five purpose-built studio to three bedroom residences at 1521 Queen Street West, Toronto, steps from the 501 streetcar, Roncesvalles Village and the waterfront.",
  "numberOfAccommodationUnits": 95,
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "1521 Queen Street West",
    "addressLocality": "Toronto",
    "addressRegion": "ON",
    "addressCountry": "CA"
  },'''

NEW_HEAD = '''<title>1521 | Luxury Rentals on Queen West</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="1521 at 1521 Queen Street West. Luxury rentals on Queen West, Toronto: ninety-five purpose-built studio to three bedroom residences, steps from the 501 streetcar, Roncesvalles Village and the waterfront. Coming Soon Summer 2027.">
<meta name="robots" content="noindex, nofollow, noarchive">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ApartmentComplex",
  "name": "1521",
  "alternateName": "1521 Queen West",
  "description": "Luxury rentals on Queen West. Ninety-five purpose-built studio to three bedroom residences at 1521 Queen Street West, Toronto, steps from the 501 streetcar, Roncesvalles Village and the waterfront. Coming Soon Summer 2027.",
  "numberOfAccommodationUnits": 95,
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "1521 Queen Street West",
    "addressLocality": "Toronto",
    "addressRegion": "ON",
    "postalCode": "M6R 1A5",
    "addressCountry": "CA"
  },'''


def main():
    if not SRC.exists():
        raise SystemExit(
            "apply_v3: %s missing. Run tools/deflate.py then tools/apply_v2.py first." % SRC)
    h = SRC.read_text(encoding="utf-8")

    h = sub(h, OLD_HEAD, NEW_HEAD, 1, "head")

    h = apply_css(h)
    h = apply_body(h)
    h = apply_js(h)
    h = apply_fonts(h)
    h = apply_watermark(h)

    # Nothing may still call the building "The 501" or quote a rent. The 501
    # streetcar is a real TTC route and stays as a transit reference.
    for pat in (r"[Tt]he 501(?! streetcar)", r"THE 501", r"Premium Rentals",
                r"Parkdale House"):
        m = re.search(pat, h)
        if m:
            raise SystemExit("apply_v3: %r survived at offset %d: ...%s..."
                             % (m.group(0), m.start(),
                                h[max(0, m.start() - 90):m.start() + 90]))
    money = re.findall(r"\$[0-9][0-9,]*", h)
    if money:
        raise SystemExit("apply_v3: rent figures survived: %s" % sorted(set(money)))

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(h, encoding="utf-8")
    bad = [(i, c) for i, c in enumerate(h) if ord(c) > 127]
    if bad:
        raise SystemExit("apply_v3: %d non-ASCII characters in output" % len(bad))
    print("apply_v3: %d edits, wrote %s (%.1f KB)"
          % (_edits, OUT.relative_to(ROOT), len(h.encode()) / 1024))
    return 0


def apply_css(h):
    from v3_css import run
    return run(h, sub, resub, cut_block)


def apply_body(h):
    from v3_body import run
    return run(h, sub, resub, cut_block)


def apply_js(h):
    from v3_js import run
    return run(h, sub, resub, cut_block)


def apply_watermark(h):
    from v3_watermark import run
    return run(h, sub, resub, cut_block)


def apply_fonts(h):
    from v3_fonts import run
    return run(h, sub, resub, cut_block)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
