#!/usr/bin/env python3
"""
Build a single-file page from an edited skeleton.

  1. substitute the {{DU_n}} image tokens back from v2/assets.json
  2. substitute the {{FONT_*}} tokens from the woff2 files in v2/fonts/
  3. substitute the partner-brand tokens from the files in v2/brand/
  4. splice in the client markup tool, re-skinned and keyed for the target
  5. refuse to write if a forbidden dash or a non-ASCII byte got in

Targets
  --target v2         v2/skeleton_v2.html         -> v2/index.html   (default)
  --target v3         v3/skeleton_v3.html         -> v3/index.html
  --target register   register/skeleton_reg.html  -> register/index.html

v2/assets.json and v2/fonts/ are shared by every target: assets.json is the
regenerable output of tools/deflate.py and the fonts are tracked files, so
there is one copy of each rather than one per build.

Nothing here touches the root index.html, and nothing but v2/index.html is
written when the target is v2.
"""

import argparse
import base64
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "v2" / "assets.json"
FONTS = ROOT / "v2" / "fonts"
BRAND = ROOT / "v2" / "brand"
TOOL = ROOT / "review-tool.html"

FONT_FILES = {
    "{{FONT_LB400}}": "LibreBaskerville-Regular-latin.woff2",
    "{{FONT_LB400I}}": "LibreBaskerville-Italic-latin.woff2",
    "{{FONT_LB700}}": "LibreBaskerville-Bold-latin.woff2",
    "{{FONT_DM}}": "DMSans-Variable-latin.woff2",
    "{{FONT_DMI}}": "DMSans-Italic-latin.woff2",
}

# Partner marks that are not part of the original page. Built for v2 and
# switched off there; see tools/v2_flags.py.
BRAND_FILES = {
    "{{NEZAM_LOCKUP}}": ("nezam_lockup_on_dark.svg", "image/svg+xml"),
}

# U+2014, U+2013 and every entity form of them. The literals are written as
# escapes so this file itself stays free of the characters it rejects.
FORBIDDEN = [
    ("—", "em dash"),
    ("–", "en dash"),
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
#  review tool, one flavour per target
#
#  Same endpoint and same token every time, so Claire's workflow never
#  changes. Only the local storage keys and the project label move, which is
#  what keeps each build's pins in their own bucket.
# ---------------------------------------------------------------------------

SKIN_PATCHES = [
    # follow the page palette so the tool matches whichever option is on
    ('  --rv-ink:#14201B; --rv-pine:#1E3A2F; --rv-linen:#FBF8F1; --rv-brass:#C4A634;\n'
     '  --rv-surface:rgba(18,29,25,.94);',
     '  --rv-ink:var(--deep-2, #2E0745); --rv-pine:var(--deep, #480B6A);\n'
     '  --rv-linen:var(--cream, #FCF6ED); --rv-brass:var(--orange, #FE5000);\n'
     '  --rv-surface:rgba(var(--deep-2-rgb, 46,7,69),.95);', 1),
    ('  --rv-sans:"Avenir Next","Avenir","Helvetica Neue",Helvetica,Arial,sans-serif;\n'
     '  --rv-serif:"Fraunces","Didot","Georgia",serif;',
     '  --rv-sans:"DM Sans","Helvetica Neue",Helvetica,Arial,sans-serif;\n'
     '  --rv-serif:"Libre Baskerville","Georgia","Times New Roman",serif;', 1),
    ("perks: 'Resident Perks',", "perks: 'Residents',", 1),
]


def tool_patches(name, project, store, deeplink, filestem):
    """The per-target identity and storage patches, plus the shared skin."""
    return [
        ("project: 'Parkdale House, 1521 Queen Street West',",
         "project: '%s'," % project, 1),
        ("storeKey: 'pdh_review_v1',", "storeKey: '%s'," % store, 1),
        ("onKey: 'pdh_review_on',", "onKey: '%s_on'," % store, 1),
        ("introKey: 'pdh_review_intro',", "introKey: '%s_intro'," % store, 1),
        ("Parkdale House :: client markup tool", "%s :: client markup tool" % name, 1),
        ("<b>Parkdale House</b>", "<b>%s</b>" % name, 1),
        ("a.download = 'Parkdale_House_markups_'",
         "a.download = '%s_markups_'" % filestem, 1),
        ("encodeURIComponent('Parkdale House landing page markups from '",
         "encodeURIComponent('%s landing page markups from '" % name, 1),
        ("// deep link: parkdalehouse.github.io/?review#m-3 jumps to markup 3",
         "// deep link: %s jumps to markup 3" % deeplink, 1),
    ] + SKIN_PATCHES


TARGETS = {
    "v2": {
        "skeleton": ROOT / "v2" / "skeleton_v2.html",
        "out": ROOT / "v2" / "index.html",
        # v2 is frozen. Its store key is spelled out rather than generated so
        # a later edit to the generator can never move Claire's pins.
        "patches": [
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
        ] + SKIN_PATCHES,
    },
    "v3": {
        "skeleton": ROOT / "v3" / "skeleton_v3.html",
        "out": ROOT / "v3" / "index.html",
        "patches": tool_patches(
            name="1521",
            project="1521, 1521 Queen Street West",
            store="q1521_review_v3",
            deeplink="parkdalehouse.github.io/v3/?review#m-3",
            filestem="1521_markups",
        ),
    },
    "register": {
        "skeleton": ROOT / "register" / "skeleton_register.html",
        "out": ROOT / "register" / "index.html",
        "patches": tool_patches(
            name="1521 Registration",
            project="1521 Phase 1 Registration Page, 1521 Queen Street West",
            store="q1521_register_v3",
            deeplink="parkdalehouse.github.io/register/?review#m-3",
            filestem="1521_registration_markups",
        ),
    },
}

# The v3 store key the change log quotes. Asserted at write time so a later
# edit to the generator cannot silently mix v3 pins in with another build's.
V3_STORE_KEY = "q1521_review_v3"

TOOL_GLOBAL = [
    ("rgba(251,248,241,", "rgba(var(--cream-rgb, 252,246,237),"),
    ("rgba(20,32,27,", "rgba(var(--deep-2-rgb, 46,7,69),"),
    ("rgba(196,166,52,", "rgba(var(--orange-rgb, 254,80,0),"),
    ("#d4b647", "var(--burnt, #BE5103)"),
]


def data_uri(path, mime="font/woff2"):
    return "data:%s;base64,%s" % (mime, base64.b64encode(path.read_bytes()).decode("ascii"))


def build_tool(patches):
    t = TOOL.read_text(encoding="utf-8").strip()
    for old, new, n in patches:
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
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--target", default="v2", choices=sorted(TARGETS),
                    help="which build to inflate (default: v2)")
    args = ap.parse_args()
    cfg = TARGETS[args.target]
    skeleton, out = cfg["skeleton"], cfg["out"]

    for p in (skeleton, ASSETS, TOOL):
        if not p.exists():
            raise SystemExit("inflate: missing %s" % p)

    html = skeleton.read_text(encoding="utf-8")
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

    # --- partner brand marks ---------------------------------------------
    inlined = 0
    for token, (name, mime) in BRAND_FILES.items():
        n = html.count(token)
        # a mark can be built and switched off (see tools/v2_flags.py), so an
        # absent token is fine; more than one is not
        if n == 0:
            continue
        if n != 1:
            raise SystemExit("inflate: brand token %s appears %d times" % (token, n))
        f = BRAND / name
        if not f.exists():
            raise SystemExit("inflate: missing brand asset %s" % f)
        html = html.replace(token, data_uri(f, mime))
        inlined += 1

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
    tool = build_tool(cfg["patches"])
    if args.target == "v3" and ("storeKey: '%s'" % V3_STORE_KEY) not in tool:
        raise SystemExit("inflate: v3 review tool is not keyed %s" % V3_STORE_KEY)
    html = html.rstrip() + "\n\n" + tool + "\n"

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

    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("inflate: wrote %s" % out.relative_to(ROOT))
    print("  images   %d" % len(used))
    print("  fonts    %d" % len(FONT_FILES))
    print("  brand    %d of %d available" % (inlined, len(BRAND_FILES)))
    print("  size     %.1f KB" % (len(html.encode()) / 1024))
    print("  dashes   clean, ASCII clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
