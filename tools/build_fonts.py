#!/usr/bin/env python3
"""
Cut the switchable typefaces for the v3 font switcher.

BSaR's 28 August branding board names wordmark faces (Instrument Sans,
Montserrat, Futura, Poppins) and text faces (Inter, Open Sans, DM Sans,
Manrope, Libre Baskerville). Tyler asked on 8 September for "the equivalent of
a colour toggle with different fonts available", so every one of those faces
has to be in the page, with nothing loaded from a third party at run time.

This downloads each family from the google/fonts repository, pins or narrows
its variable axes, subsets it and writes a woff2 into fonts/ with its OFL
licence beside it. tools/inflate.py then inlines them as data URIs.

Two subset sizes, because page weight matters more than completeness here:

  text faces      latin, the range the page actually renders
  wordmark faces  digits only, because the wordmark variable is only ever
                  used to draw "1521" and the stacked "15" over "21"

Futura is not open licence and cannot be embedded. Jost is the usual open
stand-in for it and is labelled that way in the switcher.

Run:  python3 tools/build_fonts.py
It skips any file it has already cut. Pass --force to redo them.
"""

import argparse
import shutil
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.subset import Subsetter, Options, parse_unicodes

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "fonts"
CACHE = ROOT.parent / "Identity-1521" / "fonts"      # the identity build's copies
RAW = "https://raw.githubusercontent.com/google/fonts/main/ofl/%s/%s"

# The characters the page renders. It is pure ASCII markup, but a handful of
# entities resolve to punctuation and symbols, so those are kept where a face
# has them. pyftsubset drops any codepoint the font does not carry.
LATIN = (
    "U+0020-007E,U+00A0-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,"
    "U+02DC,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+21BA,"
    "U+2715,U+25C6,U+FEFF,U+FFFD"
)
DIGITS = "U+0020,U+0030-0039"

# family dir, source file, local cache name, axis limits, charset, output
JOBS = [
    # ---- text faces: headings, subheadings and body -----------------------
    dict(out="InstrumentSans-latin.woff2", dir="instrumentsans",
         src="InstrumentSans[wdth,wght].ttf", cache="InstrumentSans-VF.ttf",
         axes={"wdth": 100, "wght": (400, 700)}, chars=LATIN,
         licence="OFL-InstrumentSans.txt"),
    dict(out="Inter-latin.woff2", dir="inter",
         src="Inter[opsz,wght].ttf", cache=None,
         axes={"opsz": 16, "wght": (400, 700)}, chars=LATIN,
         licence="OFL-Inter.txt"),
    dict(out="OpenSans-latin.woff2", dir="opensans",
         src="OpenSans[wdth,wght].ttf", cache=None,
         axes={"wdth": 100, "wght": (400, 700)}, chars=LATIN,
         licence="OFL-OpenSans.txt"),
    dict(out="Manrope-latin.woff2", dir="manrope",
         src="Manrope[wght].ttf", cache="Manrope-VF.ttf",
         axes={"wght": (400, 700)}, chars=LATIN,
         licence="OFL-Manrope.txt"),
    # ---- wordmark-only faces: digits are all they ever draw ---------------
    dict(out="Montserrat-digits.woff2", dir="montserrat",
         src="Montserrat[wght].ttf", cache=None,
         axes={"wght": 400}, chars=DIGITS,
         licence="OFL-Montserrat.txt"),
    # Jost at weight 326 is the cut the identity routes sheet uses to match
    # the stem weight of BSaR's own drawing.
    dict(out="Jost-digits.woff2", dir="jost",
         src="Jost[wght].ttf", cache="Jost-VF.ttf",
         axes={"wght": 326}, chars=DIGITS,
         licence="OFL-Jost.txt"),
    dict(out="Poppins-Regular-digits.woff2", dir="poppins",
         src="Poppins-Regular.ttf", cache=None,
         axes=None, chars=DIGITS, licence="OFL-Poppins.txt"),
    dict(out="Poppins-SemiBold-digits.woff2", dir="poppins",
         src="Poppins-SemiBold.ttf", cache=None,
         axes=None, chars=DIGITS, licence="OFL-Poppins.txt"),
]


def fetch(job, tmp):
    """Prefer the copy the identity build already pulled; else google/fonts."""
    if job["cache"] and (CACHE / job["cache"]).exists():
        dst = tmp / job["cache"]
        shutil.copyfile(CACHE / job["cache"], dst)
        return dst, "cache"
    url = RAW % (job["dir"], urllib.parse.quote(job["src"]))
    dst = tmp / job["src"].replace("[", "_").replace("]", "_")
    with urllib.request.urlopen(url, timeout=60) as r:
        dst.write_bytes(r.read())
    return dst, "google/fonts"


def fetch_licence(job):
    dst = OUT / job["licence"]
    if dst.exists():
        return
    local = CACHE / job["licence"]
    if local.exists():
        shutil.copyfile(local, dst)
        return
    with urllib.request.urlopen(RAW % (job["dir"], "OFL.txt"), timeout=60) as r:
        dst.write_bytes(r.read())


def cut(job, src, dst):
    f = TTFont(src)
    if job["axes"] and "fvar" in f:
        f = instancer.instantiateVariableFont(f, job["axes"], updateFontNames=False)
        # Partial instancing can leave gvar and the glyph order out of step,
        # which the subsetter then trips over. A save and reopen normalises it.
        mid = Path(str(dst) + ".tmp.ttf")
        f.save(mid)
        f.close()
        f = TTFont(mid)
    opts = Options()
    opts.flavor = "woff2"
    opts.desubroutinize = False
    # No tabular or lining figure features: the page never asks for them, and
    # their alternate glyphs drag in variation data for glyphs we then drop.
    opts.layout_features = ["kern", "liga", "calt", "ccmp", "locl", "mark",
                            "mkmk", "rlig"]
    opts.name_IDs = [1, 2, 3, 4, 5, 6, 16, 17]
    opts.notdef_outline = False
    opts.drop_tables += ["DSIG"]
    opts.recalc_bounds = True
    s = Subsetter(options=opts)
    s.populate(unicodes=parse_unicodes(job["chars"]))
    s.subset(f)
    f.flavor = "woff2"
    f.save(dst)
    f.close()
    mid = Path(str(dst) + ".tmp.ttf")
    if mid.exists():
        mid.unlink()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    OUT.mkdir(exist_ok=True)
    tmp = OUT / "_src"
    tmp.mkdir(exist_ok=True)
    total = 0
    for job in JOBS:
        dst = OUT / job["out"]
        if dst.exists() and not args.force:
            total += dst.stat().st_size
            print("  keep   %-34s %6.1f KB" % (job["out"], dst.stat().st_size / 1024))
            continue
        src, where = fetch(job, tmp)
        cut(job, src, dst)
        fetch_licence(job)
        total += dst.stat().st_size
        print("  cut    %-34s %6.1f KB   from %s" % (job["out"], dst.stat().st_size / 1024, where))
    shutil.rmtree(tmp, ignore_errors=True)
    print("  ----")
    print("  total  %6.1f KB raw, about %.1f KB once base64 encoded into a page"
          % (total / 1024, total * 4 / 3 / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
