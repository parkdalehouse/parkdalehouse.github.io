#!/usr/bin/env python3
"""
Inject (or refresh) the Parkdale House client markup tool inside index.html.

index.html is a 5.3 MB single-file build with the images and fonts inlined as
data URIs, so it is not hand-edited. The markup tool lives in review-tool.html
and this script splices it in between its BEGIN/END markers. Running it twice
replaces the previous block instead of stacking a second copy.

    python3 build_review.py            # inject / refresh
    python3 build_review.py --strip    # remove the tool entirely
"""

import re
import sys
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE = HERE / "index.html"
TOOL = HERE / "review-tool.html"

BEGIN = "<!-- PMT REVIEW TOOL v1 :: BEGIN"
END = "<!-- PMT REVIEW TOOL v1 :: END -->"
BLOCK_RE = re.compile(
    re.escape(BEGIN) + r".*?" + re.escape(END), re.S
)


def strip(html: str) -> str:
    """Remove any previously injected block."""
    return BLOCK_RE.sub("", html).rstrip() + "\n"


def main() -> int:
    if not PAGE.exists():
        print("error: index.html not found next to this script")
        return 1

    html = PAGE.read_text(encoding="utf-8")
    shutil.copy2(PAGE, HERE / "index.html.bak")

    base = strip(html)

    if "--strip" in sys.argv:
        PAGE.write_text(base, encoding="utf-8")
        print("removed the markup tool. index.html is %d bytes" % len(base.encode()))
        return 0

    if not TOOL.exists():
        print("error: review-tool.html not found")
        return 1

    tool = TOOL.read_text(encoding="utf-8").strip()

    # The page carries no <meta charset>, so keep the injected block pure ASCII.
    # Anything else risks mojibake if the host ever serves a different charset.
    bad = [(i, ch) for i, ch in enumerate(tool) if ord(ch) > 127]
    if bad:
        print("error: review-tool.html contains %d non-ASCII characters" % len(bad))
        for i, ch in bad[:10]:
            print("   offset %d: %r  ...%s..." % (i, ch, tool[max(0, i - 40):i + 40]))
        return 1

    # Sanity: the block must not already appear inside a data URI or script string.
    if base.count(BEGIN) or base.count(END):
        print("error: markers survived the strip, refusing to write")
        return 1

    out = base.rstrip() + "\n\n" + tool + "\n"
    PAGE.write_text(out, encoding="utf-8")

    print("injected the markup tool.")
    print("  tool      %6.1f KB" % (len(tool.encode()) / 1024))
    print("  page      %6.1f KB -> %.1f KB" % (
        len(html.encode()) / 1024, len(out.encode()) / 1024))
    print("  backup    index.html.bak")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
