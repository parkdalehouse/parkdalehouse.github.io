#!/usr/bin/env python3
"""
Build v2/index.html from the edited skeleton.

  1. substitute the {{DU_n}} image tokens back from v2/assets.json
  2. substitute the {{FONT_*}} tokens from the woff2 files in v2/fonts/
  3. splice in the client markup tool, re-skinned and keyed for v2
  4. refuse to write if a forbidden dash or a non-ASCII byte got in

Nothing here touches the root index.html.
"""

import base64
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKELETON = ROOT / "v2" / "skeleton_v2.html"
ASSETS = ROOT / "v2" / "assets.json"
FONTS = ROOT / "v2" / "fonts"
TOOL = ROOT / "review-tool.html"
OUT = ROOT / "v2" / "index.html"

FONT_FILES = {
    "{{FONT_LB400}}": "LibreBaskerville-Regular-latin.woff2",
    "{{FONT_LB400I}}": "LibreBaskerville-Italic-latin.woff2",
    "{{FONT_LB700}}": "LibreBaskerville-Bold-latin.woff2",
    "{{FONT_DM}}": "DMSans-Variable-latin.woff2",
    "{{FONT_DMI}}": "DMSans-Italic-latin.woff2",
}

# U+2014, U+2013 and every entity form of them. The literals are written as
# escapes so this file itself stays free of the characters it rejects.
FORBIDDEN = [
    ("\u2014", "em dash"),
    ("\u2013", "en dash"),
    ("&mdash;", "&mdash;"),
    ("&ndash;", "&ndash;"),
    ("&#8212;", "&#8212;"),
    ("&#8211;", "&#8211;"),
    ("&#x2014;", "&#x2014;"),
    ("&#x2013;", "&#x2013;"),
    ("&#X2014;", "&#X2014;"),
    ("&#X2013;", "&#X2013;"),
]

# ---------------------------------------------------------------------------
#  review tool, v2 flavour
# ---------------------------------------------------------------------------
TOOL_PATCHES = [
    # identity and storage. Same endpoint and token; a different store key so
    # v2 pins never mix with the pins Claire left on the original page.
    ("project: 'Parkdale House, 1521 Queen Street West',",
     "project: 'The 501, 1521 Queen Street West',", 1),
    ("storeKey: 'pdh_review_v1',", "storeKey: 'the501_review_v2',", 1),
    ("onKey: 'pdh_review_on',", "onKey: 'the501_review_on',", 1),
    ("introKey: 'pdh_review_intro',", "introKey: 'the501_review_intro',", 1),
    ("Parkdale House :: client markup tool", "The 501 :: client markup tool", 1),
    ("<b>Parkdale House</b>", "<b>The 501</b>", 1),
    ("a.download = 'Parkdale_House_markups_'", "a.download = 'The_501_markups_'", 1),
    ("encodeURIComponent('Parkdale House landing page markups from '",
     "encodeURIComponent('The 501 landing page markups from '", 1),
    ("// deep link: parkdalehouse.github.io/?review#m-3 jumps to markup 3",
     "// deep link: parkdalehouse.github.io/v2/?review#m-3 jumps to markup 3", 1),
    ("perks: 'Resident Perks',", "perks: 'Residents',", 1),
    # skin: follow the page palette so the tool matches whichever option is on
    ('  --rv-ink:#14201B; --rv-pine:#1E3A2F; --rv-linen:#FBF8F1; --rv-brass:#C4A634;\n'
     '  --rv-surface:rgba(18,29,25,.94);',
     '  --rv-ink:var(--deep-2, #2E0745); --rv-pine:var(--deep, #480B6A);\n'
     '  --rv-linen:var(--cream, #FCF6ED); --rv-brass:var(--orange, #FE5000);\n'
     '  --rv-surface:rgba(var(--deep-2-rgb, 46,7,69),.95);', 1),
    ('  --rv-sans:"Avenir Next","Avenir","Helvetica Neue",Helvetica,Arial,sans-serif;\n'
     '  --rv-serif:"Fraunces","Didot","Georgia",serif;',
     '  --rv-sans:"DM Sans","Helvetica Neue",Helvetica,Arial,sans-serif;\n'
     '  --rv-serif:"Libre Baskerville","Georgia","Times New Roman",serif;', 1),
]

TOOL_GLOBAL = [
    ("rgba(251,248,241,", "rgba(var(--cream-rgb, 252,246,237),"),
    ("rgba(20,32,27,", "rgba(var(--deep-2-rgb, 46,7,69),"),
    ("rgba(196,166,52,", "rgba(var(--orange-rgb, 254,80,0),"),
    ("#d4b647", "var(--burnt, #BE5103)"),
]


def data_uri(path):
    mime = "font/woff2"
    return "data:%s;base64,%s" % (mime, base64.b64encode(path.read_bytes()).decode("ascii"))


def build_tool():
    t = TOOL.read_text(encoding="utf-8").strip()
    for old, new, n in TOOL_PATCHES:
        if t.count(old) != n:
            raise SystemExit("inflate: review tool patch missed: %r" % old[:80])
        t = t.replace(old, new)
    for old, new in TOOL_GLOBAL:
        t = t.replace(old, new)
    bad = [c for c in t if ord(c) > 127]
    if bad:
        raise SystemExit("inflate: %d non-ASCII characters in the review tool" % len(bad))
    return t


def main():
    for p in (SKELETON, ASSETS, TOOL):
        if not p.exists():
            raise SystemExit("inflate: missing %s" % p)

    html = SKELETON.read_text(encoding="utf-8")
    assets = json.loads(ASSETS.read_text(encoding="utf-8"))

    # --- fonts -----------------------------------------------------------
    for token, name in FONT_FILES.items():
        f = FONTS / name
        if not f.exists():
            raise SystemExit("inflate: missing font %s" % f)
        if html.count(token) != 1:
            raise SystemExit("inflate: font token %s appears %d times"
                             % (token, html.count(token)))
        html = html.replace(token, data_uri(f))

    # --- images ----------------------------------------------------------
    used = set(re.findall(r"\{\{DU_\d+\}\}", html))
    missing = used - set(assets)
    if missing:
        raise SystemExit("inflate: unknown asset tokens %s" % sorted(missing))
    html = re.sub(r"\{\{DU_\d+\}\}", lambda m: assets[m.group(0)], html)

    left = re.findall(r"\{\{[A-Z_0-9]+\}\}", html)
    if left:
        raise SystemExit("inflate: unsubstituted tokens %s" % sorted(set(left)))

    # --- review tool -----------------------------------------------------
    html = html.rstrip() + "\n\n" + build_tool() + "\n"

    # --- guards ----------------------------------------------------------
    for needle, label in FORBIDDEN:
        n = html.count(needle)
        if n:
            i = html.find(needle)
            raise SystemExit("inflate: %d x forbidden %s, first at offset %d: ...%s..."
                             % (n, label, i, html[max(0, i - 70):i + 70]))
    bad = [(i, c) for i, c in enumerate(html) if ord(c) > 127]
    if bad:
        i, c = bad[0]
        raise SystemExit("inflate: %d non-ASCII characters, first %r at %d"
                         % (len(bad), c, i))

    OUT.write_text(html, encoding="utf-8")
    print("inflate: wrote %s" % OUT.relative_to(ROOT))
    print("  images   %d" % len(used))
    print("  fonts    %d" % len(FONT_FILES))
    print("  size     %.1f KB" % (len(html.encode()) / 1024))
    print("  dashes   clean, ASCII clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
