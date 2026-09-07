#!/usr/bin/env python3
"""
Apply the BSaR v2 direction to the deflated skeleton.

Reads   v2/skeleton.html      pristine output of tools/deflate.py
Writes  v2/skeleton_v2.html   the edited page, still token-ised

Every replacement is asserted on an exact expected count, so a silent miss
becomes a hard failure instead of a wrong page. Run tools/deflate.py first
if v2/skeleton.html is missing.

Sources for the changes:
  BSaR-Inbound/2026-08-28_landing-page-markups_claire.md   (the 43 markups)
  BSaR-Inbound/2026-08-28_branding-direction/*.pdf         (name, palette, type)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "v2" / "skeleton.html"
OUT = ROOT / "v2" / "skeleton_v2.html"

RV_BEGIN = "<!-- PMT REVIEW TOOL v1 :: BEGIN"
RV_END = "<!-- PMT REVIEW TOOL v1 :: END -->"

_edits = 0


def sub(html, old, new, count=1, label=""):
    """Exact-string replace with an asserted occurrence count."""
    global _edits
    found = html.count(old)
    if found != count:
        raise SystemExit(
            "apply_v2: %s: expected %d occurrence(s), found %d\n  needle: %r"
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
            "apply_v2: %s: expected %d match(es), found %d\n  pattern: %s"
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
        raise SystemExit("apply_v2: %s: block not found" % (label or "cut"))
    _edits += 1
    return html[:i] + html[j + len(end_marker):]


# ==========================================================================
#  NEW HEAD: title, charset, description, JSON-LD
# ==========================================================================

NEW_HEAD = '''<meta charset="utf-8">
<title>The 501 | Queen West Rentals</title>
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
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 43.6389,
    "longitude": -79.4426
  },
  "telephone": "+1-416-451-9499",
  "petsAllowed": true,
  "amenityFeature": [
    {"@type": "LocationFeatureSpecification", "name": "Rooftop terrace", "value": true},
    {"@type": "LocationFeatureSpecification", "name": "Multipurpose fitness studio", "value": true},
    {"@type": "LocationFeatureSpecification", "name": "Automated parcel delivery", "value": true},
    {"@type": "LocationFeatureSpecification", "name": "Secure bike room", "value": true},
    {"@type": "LocationFeatureSpecification", "name": "In-suite laundry", "value": true}
  ]
}
</script>'''

OLD_HEAD = '''<title>Parkdale House</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">'''


# ==========================================================================
#  NEW FONT AND PALETTE BLOCK
# ==========================================================================

OLD_ROOT = '''  @font-face{font-family:"Fraunces";src:url("{{DU_0}}") format("woff2");
    font-weight:300 700;font-style:normal;font-display:swap}
  @font-face{font-family:"Fraunces";src:url("{{DU_1}}") format("woff2");
    font-weight:300 700;font-style:italic;font-display:swap}
  :root{
    --pine:#1E3A2F; --ink:#14201B; --linen:#FBF8F1; --brass:#C4A634;
    --linen-70:rgba(251,248,241,.72); --linen-45:rgba(251,248,241,.45);
    --line:rgba(251,248,241,.16); --line-dark:rgba(20,32,27,.16);
    --pine-70:rgba(30,58,47,.78);
    --serif:"Fraunces","Didot","Georgia",serif;
    --sans:"Avenir Next","Avenir","Helvetica Neue",Helvetica,Arial,sans-serif;
    --ease:cubic-bezier(.22,1,.36,1);
    --ease-io:cubic-bezier(.77,0,.175,1);
  }'''

NEW_ROOT = '''  /* Wordmark and display: Libre Baskerville. Body and UI: DM Sans.
     Both OFL, embedded as data URIs so the page loads nothing off-host. */
  @font-face{font-family:"Libre Baskerville";src:url("{{FONT_LB400}}") format("woff2");
    font-weight:400;font-style:normal;font-display:swap}
  @font-face{font-family:"Libre Baskerville";src:url("{{FONT_LB400I}}") format("woff2");
    font-weight:400;font-style:italic;font-display:swap}
  @font-face{font-family:"Libre Baskerville";src:url("{{FONT_LB700}}") format("woff2");
    font-weight:700;font-style:normal;font-display:swap}
  @font-face{font-family:"DM Sans";src:url("{{FONT_DM}}") format("woff2");
    font-weight:400 700;font-style:normal;font-display:swap}
  @font-face{font-family:"DM Sans";src:url("{{FONT_DMI}}") format("woff2");
    font-weight:400;font-style:italic;font-display:swap}

  /* ================= BSaR brand direction, 28 August 2026 =================
     One deep colour + Pantone Orange 021 C + Burnt Orange + Cream White.
     Deep-colour hexes read off page 2 of the branding PDF.
       A  Pantone Saratoga Signature Blue  #0032AD
       B  Pantone Blue 072 C               #10069F
       C  Pantone Deep Purple 2617 C       #480B6A   (default)
       D  Pantone Purple PMS 3555 C        #512079
     The switcher at the bottom left swaps [data-palette] on <html>.
     ====================================================================== */
  :root{
    --deep:#480B6A;   --deep-rgb:72,11,106;
    --deep-2:#2E0745; --deep-2-rgb:46,7,69;

    --cream:#FCF6ED;  --cream-rgb:252,246,237;
    --orange:#FE5000; --orange-rgb:254,80,0;
    --burnt:#BE5103;  --burnt-rgb:190,81,3;
    --ink:#1C1A17;    --ink-rgb:28,26,23;

    /* surface tokens. Cream is the default page surface; .tone-deep flips them. */
    --bg:var(--cream);
    --fg:var(--ink);
    --fg-70:rgba(28,26,23,.74);
    --fg-45:rgba(28,26,23,.54);
    --hair:rgba(72,11,106,.20);
    --accent:var(--burnt);
    --em:var(--deep);
    --btn-on-accent:var(--cream);
    --btn-hover-bg:var(--deep);
    --btn-hover-fg:var(--cream);

    --serif:"Libre Baskerville","Georgia","Times New Roman",serif;
    --sans:"DM Sans","Helvetica Neue",Helvetica,Arial,sans-serif;
    --ease:cubic-bezier(.22,1,.36,1);
    --ease-io:cubic-bezier(.77,0,.175,1);
  }
  :root[data-palette="A"]{--deep:#0032AD;--deep-rgb:0,50,173;--deep-2:#001E68;--deep-2-rgb:0,30,104;
    --hair:rgba(0,50,173,.20)}
  :root[data-palette="B"]{--deep:#10069F;--deep-rgb:16,6,159;--deep-2:#0A0461;--deep-2-rgb:10,4,97;
    --hair:rgba(16,6,159,.20)}
  :root[data-palette="C"]{--deep:#480B6A;--deep-rgb:72,11,106;--deep-2:#2E0745;--deep-2-rgb:46,7,69;
    --hair:rgba(72,11,106,.20)}
  :root[data-palette="D"]{--deep:#512079;--deep-rgb:81,32,121;--deep-2:#33144C;--deep-2-rgb:51,20,76;
    --hair:rgba(81,32,121,.20)}

  /* deep bands: header, footer and the major full-width sections */
  .tone-deep{
    --fg:var(--cream);
    --fg-70:rgba(var(--cream-rgb),.76);
    --fg-45:rgba(var(--cream-rgb),.50);
    --hair:rgba(var(--cream-rgb),.18);
    --accent:var(--orange);
    --em:var(--orange);
    --btn-on-accent:var(--deep-2);
    --btn-hover-bg:var(--cream);
    --btn-hover-fg:var(--deep-2);
    color:var(--fg);
  }'''


def main():
    if not SRC.exists():
        raise SystemExit("apply_v2: %s missing. Run tools/deflate.py first." % SRC)
    h = SRC.read_text(encoding="utf-8")

    # The review tool is re-injected by tools/inflate.py with v2 config, so the
    # copy that came along inside index.html is stripped here.
    h = cut_block(h, RV_BEGIN, RV_END, "strip review tool")

    h = sub(h, OLD_HEAD, NEW_HEAD, 1, "head")
    h = sub(h, OLD_ROOT, NEW_ROOT, 1, "fonts and palette")

    h = apply_css(h)
    h = apply_body(h)
    h = apply_js(h)

    OUT.write_text(h, encoding="utf-8")
    bad = [(i, c) for i, c in enumerate(h) if ord(c) > 127]
    if bad:
        raise SystemExit("apply_v2: %d non-ASCII characters in output" % len(bad))
    print("apply_v2: %d edits, wrote %s (%.1f KB)"
          % (_edits, OUT.relative_to(ROOT), len(h.encode()) / 1024))
    return 0


# placeholders filled in by the other modules of this script
def apply_css(h):
    from v2_css import run
    return run(h, sub, resub, cut_block)


def apply_body(h):
    from v2_body import run
    return run(h, sub, resub, cut_block)


def apply_js(h):
    from v2_js import run
    return run(h, sub, resub, cut_block)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
