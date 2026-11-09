#!/usr/bin/env python3
"""
Build the Phase 1 registration page from the v3 skeleton.

Reads   v3/skeleton_v3.html              output of tools/apply_v3.py
Writes  register/skeleton_register.html  still token-ised

Second build, 21 September 2026, to Claire Bodrug's markup of 18 September on
the registration page (review tool, one pin, n8n executions 44870 and 44871):

    "Preference was to have a full registration page on the beige background
     with the blue credit band at the bottom. Top left to have logo, luxury
     rentals and coming soon. Under that have the Registration/Register now
     section and form. To the right of the registration form have a carousel
     of images in a call out box on the beige background to flip through.
     This can show on a cell phone as a carousel below the registration form."

    "Our primary concern is the functionality and layout of the registration
     page on phone screens. This is likely how most leads will view the page,
     and it does not currently work as designed."

So the 15 September build (a rendering behind a card) is replaced: cream page,
one column of mark, tagline, date line and the form on the left, a framed
image carousel on the right, the blue partner band at the foot. On a phone it
is one column in that order, mark, form, carousel, band, and nothing fixed
sits over the intake. The 8 September scope holds: no menu, no gallery
section, no map, no realtor section, no suite types, no offers.

The carousel carries the exterior renderings and illustrative neighbourhood
images that already exist in the site build. BSaR's edited photography is due
25 September and replaces the illustrative slides in the same six slots.

Third build, 2 October 2026, to Claire's eight pins of 25 September (n8n
execution 52221), her logo selects of 29 September and Jacob Cote's final
neighbourhood photography:

    pin 1  layout as built on 21 September, kept
    pin 2  "Remove or use full word mark": the small 1521 in the top bar is gone
    pin 3  "Coming Soon Summer 2027" reads "Move-In Summer 2027"
    pin 4  the streetcar exterior leads the carousel (sky and neighbours re-rendered)
    pin 5  the line reads "Boutique residences at 1521 Queen Street West."
    pin 6  the carousel note is gone; image, rendering and move-in disclaimer
           sit in small print at the base of the page, with the photo credit
    pin 7  no phone number until BSaR's forwarding line exists
    pin 8  the 15/21 placeholder is replaced by the selected logo system

The mark is C23, the primary wordmark, in Blue 072 C on cream, drawn inline from
brand/1521_marks.json (tools/logo_1521.py), as BSaR approved on 15 October. The
round four logo control, the C05 badge and the C24 stacked cut are gone from the
page, and the build fails if either of the last two comes back. The C02 dot is
the favicon.

The carousel is the exterior rendering plus six of Jacob's landscape frames,
served as files from /photos/ (original filenames and embedded copyright kept,
long edge 1800 px) rather than inlined, which also takes the page off the
2.7 MB single file.

Fifth build, 8 November 2026, for go-live, to Claire's emails of 2 and 3
November (thread "1521 Queen - Hoarding and Registration Page"):

    "Please see below link to the renderings for use on the Registration
     Page: Co-Working Lounge (Please crop to remove the red chair from view),
     Suite Rendering (Medium Palette), Party Room ... Please include a photo
     credit under each for Truong Ly Design Inc. and disclaimer noting the
     images are renderings and subject to change. Once we have the final
     images we can go live with the Registration Page."   (2 November)
    "Please see link for the remaining gym and terrace renders ... Please
     send the final proof of the website for sign-off."   (3 November)

    1  five render slots after the exterior: suite, co-working lounge, party
       room, fitness studio, terrace. Each slide carries its own credit line
       under the caption; a Truong Ly render reads "Rendering by Truong Ly
       Design Inc. Subject to change." The files come from tools/prep_images.py,
       which refuses the co-working lounge until its crop is set.
    2  the form is live: it posts to the n8n intake (Ventures/BSAR/
       Registration-Intake), a bot trap, an email consent box (CASL) and a
       privacy line. "Preview only" is gone.
    3  the carousel loads each image when it is about to show, from a 960 px
       copy on a phone, and the 444 KB amenity image and eight switcher fonts
       v3 carried are stripped, so the page itself drops to about a fifth.
    4  a second skeleton, register/skeleton_live.html, is the page for
       https://1521queenwest.ca: indexable, canonical and share tags, paths
       from the site root, no review tool (tools/build_live.py).

A render whose file is missing is left out of both pages; --placeholders draws
a labelled tile in its place for a proof. tools/build_live.py refuses to stage
the live site while any render is missing.

Rebuild:
    python3 tools/apply_v3.py \\
      && python3 tools/apply_register.py \\
      && python3 tools/inflate.py --target register \\
      && python3 tools/inflate.py --target live
"""

import argparse
import base64
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from logo_1521 import inline  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "v3" / "skeleton_v3.html"
OUT = ROOT / "register" / "skeleton_register.html"
OUT_LIVE = ROOT / "register" / "skeleton_live.html"

ENDPOINT = "https://propertymanagementto.app.n8n.cloud/webhook/1521-register"
LIVE_URL = "https://1521queenwest.ca/"
LEASING_TEL = "tel:+14167259222"
LEASING_SHOWN = "416-725-9222"
PRIVACY_URL = "https://www.propertymanagementto.com/privacy-policy/"

HEAD_END = "</style>\n<script>document.documentElement.className += ' js';</script>\n"
FSW_START = '<div class="fsw" id="fsw">'
PAL_JS = "<script>\n/* Palette switcher."
FSW_JS = "<script>\n/* Font switcher."


def take(html, start, end, label, include_end=True):
    """Return the slice from start through end. Both markers must be unique."""
    if html.count(start) != 1:
        raise SystemExit("apply_register: %s: start marker appears %d times"
                         % (label, html.count(start)))
    i = html.index(start)
    j = html.index(end, i + len(start))
    return html[i:j + (len(end) if include_end else 0)]


# ==========================================================================
#  HEAD
# ==========================================================================

OLD_TITLE = "<title>1521 | Luxury Rentals on Queen West</title>"
NEW_TITLE = "<title>1521 | Luxury Rentals on Queen West | Register</title>"

# the v3 head as tools/v3_r4.py leaves it
OLD_DESC = ('<meta name="description" content="1521 at 1521 Queen Street West. Luxury rentals '
            'on Queen West, Toronto: boutique studio to three bedroom residences, steps from the '
            '501 streetcar, Roncesvalles Village and the waterfront. Move-in Summer 2027.">')
DESC_TEXT = ("Boutique residences at 1521 Queen Street West. Luxury Rentals on Queen West, "
             "Toronto. Move-In Summer 2027. Register now.")
NEW_DESC = '<meta name="description" content="%s">' % DESC_TEXT

# the JSON-LD description inherited from v3 names the streetcar; the one-screen
# page says less, and the guard below refuses any "the 501" anyway.
OLD_LD_DESC = (', steps from the 501 streetcar, Roncesvalles Village and the waterfront. '
               'Move-in Summer 2027.",')
NEW_LD_DESC = '. Move-in Summer 2027.",'

# The v3 JSON-LD also states pets, suite types and five amenities. None of that
# is on this page, so the registration page publishes the address and nothing
# it does not show.
LD_RE = re.compile(r'<script type="application/ld\+json">.*?</script>', re.S)


def ld_block(live: bool) -> str:
    extra = ""
    if live:
        extra = ('  "url": "%s",\n  "image": "%sphotos/1521-exterior-streetcar-r2.jpg",\n'
                 % (LIVE_URL, LIVE_URL))
    return ('<script type="application/ld+json">\n{\n'
            '  "@context": "https://schema.org",\n'
            '  "@type": "ApartmentComplex",\n'
            '  "name": "1521",\n'
            '  "alternateName": "1521 Queen West",\n'
            '  "description": "Boutique residences at 1521 Queen Street West, Toronto. '
            'Move-in Summer 2027.",\n'
            + extra +
            '  "address": {\n'
            '    "@type": "PostalAddress",\n'
            '    "streetAddress": "1521 Queen Street West",\n'
            '    "addressLocality": "Toronto",\n'
            '    "addressRegion": "ON",\n'
            '    "postalCode": "M6R 1A5",\n'
            '    "addressCountry": "CA"\n'
            '  },\n'
            '  "geo": {"@type": "GeoCoordinates", "latitude": 43.6389, "longitude": -79.4426}\n'
            '}\n</script>')


ROBOTS_PREVIEW = '<meta name="robots" content="noindex, nofollow, noarchive">'


def live_meta() -> str:
    """Indexing, canonical and share tags for https://1521queenwest.ca only."""
    img = LIVE_URL + "photos/1521-exterior-streetcar-r2.jpg"
    desc = DESC_TEXT
    return "\n".join([
        '<meta name="robots" content="index, follow">',
        '<link rel="canonical" href="%s">' % LIVE_URL,
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="1521 Queen West">',
        '<meta property="og:title" content="1521 | Luxury Rentals on Queen West">',
        '<meta property="og:description" content="%s">' % desc,
        '<meta property="og:url" content="%s">' % LIVE_URL,
        '<meta property="og:image" content="%s">' % img,
        '<meta property="og:image:width" content="1477">',
        '<meta property="og:image:height" content="1065">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="theme-color" content="#FCF6ED">',
    ])


# Switcher faces v3 carries for its font control. The registration page has no
# switcher and draws its mark as outlines, so it uses Libre Baskerville and
# DM Sans only. Eight @font-face rules, about 220 KB of base64.
UNUSED_FACES = re.compile(
    r'@font-face\{font-family:"(?:Instrument Sans|Inter|Open Sans|Manrope|Montserrat|Jost|Poppins)";'
    r'src:url\("\{\{FONT_[A-Z0-9]+\}\}"\)[^}]*\}[ \t]*\n?')
# v3's amenity band background, 444 KB inlined, on a section this page lacks.
AMEN_BG = 'url("{{DU_2}}")'


# ==========================================================================
#  CSS
# ==========================================================================

REG_CSS = '''
  /* ======================= PHASE 1 REGISTRATION ========================
     Claire, 18 September: cream page, the mark and the form on the left,
     an image carousel in a framed call-out on the right, the blue partner
     band at the foot. One column on a phone: mark, form, carousel, band.
     ==================================================================== */
  body.reg-page{overflow-x:hidden}
  .reg{position:relative;min-height:100svh;display:flex;flex-direction:column;
    background:var(--cream);color:var(--ink);
    --fg:var(--ink);
    --fg-70:rgba(var(--ink-rgb),.74);
    --fg-45:rgba(var(--ink-rgb),.54);
    --hair:rgba(var(--deep-rgb),.22);
    --accent:var(--burnt); --em:var(--deep);
    --btn-on-accent:var(--cream); --btn-hover-bg:var(--deep); --btn-hover-fg:var(--cream)}

  .reg-main{flex:1 0 auto;display:grid;grid-template-columns:minmax(340px,480px) 1fr;
    gap:4.5rem;align-items:start;padding:3rem 2.4rem 2.4rem;max-width:1280px;
    width:100%;margin:0 auto}

  /* the C23 primary wordmark, all Blue 072 C on the cream ground: BSaR's
     approval of 15 October and its colour standard for cream grounds */
  :root{--lg-num:var(--deep);--lg-word:var(--deep)}
  .lg .lg-n{fill:var(--lg-num)}
  .lg .lg-w{fill:var(--lg-word)}
  .reg-logo{display:block;line-height:0}
  .reg-logo .lg-c23{display:block;height:auto;width:clamp(150px,14vw,186px)}
  .reg-tag{font-family:var(--display);font-size:clamp(1.05rem,1.8vw,1.4rem);
    letter-spacing:.04em;color:var(--deep);margin-top:1.5rem}
  .reg-soon{display:inline-flex;align-items:center;gap:.9rem;color:var(--accent);
    font-size:.7rem;font-weight:600;letter-spacing:.24em;text-transform:uppercase;margin-top:.9rem}
  .reg-soon::before{content:"";flex:0 0 40px;height:2px;background:var(--accent)}
  .reg-line{color:var(--fg-70);max-width:44ch;margin-top:1.1rem;font-size:.98rem}

  /* the form, under the mark */
  .reg-form{margin-top:2.2rem;padding-top:1.8rem;border-top:1px solid var(--hair)}
  .reg-form .label{color:var(--accent);display:block;margin-bottom:.55rem;font-size:.6rem}
  .reg-form h2{font-size:1.5rem;line-height:1.2}
  .reg-form form{gap:.9rem;max-width:none;margin-top:1.3rem}
  .reg-form label{font-size:.58rem;letter-spacing:.18em;margin-bottom:.32rem}
  .reg-form input{padding:.72rem .85rem;font-size:.95rem}
  .reg-form .btn{width:100%;justify-content:center;padding:.95rem 1rem}
  .reg-form .form-done{margin-top:1.25rem;padding:1.4rem;max-width:none}
  .reg-fine{font-size:.72rem;line-height:1.55;color:var(--fg-70);margin-top:.85rem}
  .reg-fine a{color:var(--fg);border-bottom:1px solid var(--accent);
    text-decoration:none;padding-bottom:.08rem;white-space:nowrap}
  .reg-fine a:hover{color:var(--accent)}
  .reg-note{color:var(--fg-45);letter-spacing:.06em;text-transform:uppercase;font-size:.58rem;margin-top:.7rem}

  /* the carousel call-out: a framed box on the cream, sticky beside the form */
  .reg-gal{position:sticky;top:1.6rem;border:1px solid var(--hair);padding:.9rem;
    background:rgba(255,255,255,.35)}
  .gal-frame{position:relative;aspect-ratio:4/3;overflow:hidden;background:#E6DED0;
    touch-action:pan-y}
  .gal-frame img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
    opacity:0;transition:opacity .9s var(--ease);user-select:none;-webkit-user-drag:none}
  .gal-frame img.is-on{opacity:1}
  .gal-btn{position:absolute;top:50%;transform:translateY(-50%);z-index:2;width:40px;height:40px;
    padding:0;border:0;cursor:pointer;background:rgba(var(--cream-rgb),.88);color:var(--deep);
    display:grid;place-items:center;transition:background .25s,color .25s}
  .gal-btn:hover{background:var(--deep);color:var(--cream)}
  .gal-btn::before{content:"";width:9px;height:9px;border-left:2px solid currentColor;
    border-bottom:2px solid currentColor;transform:rotate(45deg);margin-left:4px}
  .gal-btn.next::before{transform:rotate(-135deg);margin-left:-4px}
  .gal-btn.prev{left:.6rem}
  .gal-btn.next{right:.6rem}
  .gal-meta{display:flex;align-items:center;justify-content:space-between;gap:1rem;
    margin-top:.8rem;min-height:1.2rem}
  .gal-cap{font-size:.66rem;letter-spacing:.06em;text-transform:uppercase;color:var(--fg-70);
    font-weight:500;margin:0;flex:1 1 auto;min-width:0}
  /* Claire, 2 November: a credit under each image, and for a rendering the
     note that it is a rendering and subject to change */
  .gal-credit{font-size:.66rem;line-height:1.45;color:var(--fg-70);margin:.3rem 0 0;min-height:1em}
  .gal-dots{display:flex;gap:.3rem;flex:0 0 auto}
  .gal-dots button{position:relative;width:16px;height:24px;padding:0;border:0;cursor:pointer;
    background:none}
  .gal-dots button::before{content:"";position:absolute;left:0;right:0;top:50%;height:3px;
    margin-top:-1.5px;background:rgba(var(--deep-rgb),.22);transition:background .3s}
  .gal-dots button[aria-current="true"]::before{background:var(--accent)}
  .gal-dots button:focus-visible{outline:2px solid var(--deep);outline-offset:1px}
  .gal-btn:focus-visible{outline:2px solid var(--deep);outline-offset:2px}

  /* the live form: consent, the bot trap, the sending and error states */
  .reg-form input:focus-visible{box-shadow:0 0 0 3px rgba(var(--deep-rgb),.18)}
  .reg-form .opt{text-transform:none;letter-spacing:.02em;font-weight:400;color:var(--fg-45)}
  .reg-consent{display:grid;grid-template-columns:auto 1fr;gap:.7rem;align-items:start;margin-top:.15rem}
  .reg-consent input{width:18px;height:18px;margin:.12rem 0 0;padding:0;accent-color:var(--deep);cursor:pointer}
  .reg-form .reg-consent label{text-transform:none;letter-spacing:0;font-size:.76rem;font-weight:400;
    line-height:1.5;color:var(--fg-70);margin:0;cursor:pointer}
  .reg-hp{position:absolute!important;left:-10000px;width:1px;height:1px;overflow:hidden}
  .reg-form .btn[disabled]{opacity:.65;cursor:progress}
  .reg-err{margin:0;padding:.75rem .9rem;border-left:3px solid var(--burnt);
    background:rgba(var(--deep-rgb),.05);font-size:.82rem;line-height:1.5;color:var(--ink)}
  .reg-err[hidden]{display:none}
  .reg-err a{color:var(--deep)}
  .form-done:focus{outline:none}
  .reg-small{max-width:1280px;width:100%;margin:0 auto;padding:0 2.4rem 1.6rem;
    font-size:.62rem;line-height:1.6;color:var(--fg-45)}
  .reg-small p{max-width:120ch}
  .reg-small p+p{margin-top:.35rem}
  .reg-small a{color:var(--fg-70);text-decoration:none;border-bottom:1px solid var(--hair)}
  .reg-small a:hover{color:var(--accent)}

  /* the blue credit band at the foot */
  .reg-foot{display:flex;align-items:center;gap:2.6rem;flex-wrap:wrap;
    padding:1.1rem 2.4rem 1.2rem;background:var(--deep-2);color:var(--cream)}
  .reg-foot-in{display:flex;align-items:center;gap:2.6rem;flex-wrap:wrap;
    max-width:1280px;width:100%;margin:0 auto}
  .reg-lock{display:flex;align-items:center;gap:.8rem}
  .reg-lock small{font-size:.52rem;letter-spacing:.22em;text-transform:uppercase;
    color:rgba(var(--cream-rgb),.55);font-weight:600;white-space:nowrap}
  .reg-lock img{height:24px;width:auto;opacity:.92;display:block}
  .reg-lock img.tall{height:25px}
  .reg-legal{margin-left:auto;font-size:.52rem;letter-spacing:.06em;color:rgba(var(--cream-rgb),.4)}
  @media(max-width:1080px){
    .reg-main{grid-template-columns:minmax(320px,440px) 1fr;gap:3rem}
  }
  @media(max-width:860px){
    .reg-main{grid-template-columns:1fr;gap:1.8rem;padding:1.6rem 1.25rem 1.6rem}
    .reg-logo .lg-c23{width:140px}
    .reg-small{padding:0 1.25rem 1.3rem}
    .reg-tag{margin-top:1.1rem;font-size:.98rem;letter-spacing:.03em}
    .reg-soon{margin-top:.7rem;font-size:.64rem}
    .reg-line{max-width:none;margin-top:.8rem;font-size:.92rem}
    .reg-form{margin-top:1.5rem;padding-top:1.3rem}
    .reg-form h2{font-size:1.35rem}
    .reg-form form{gap:.7rem;margin-top:1rem}
    .reg-form label{margin-bottom:.24rem}
    .reg-form input{padding:.7rem .8rem;font-size:1rem}
    .reg-form .btn{padding:.9rem 1rem}
    .reg-gal{position:static;padding:.6rem}
    .gal-dots{gap:.2rem}
    .gal-dots button{width:11px}
    .gal-btn{width:36px;height:36px}
    .reg-foot{padding:1rem 1.25rem 1.1rem}
    .reg-foot-in{gap:1.1rem}
    .reg-legal{margin-left:0;flex:1 0 100%}
  }
  @media(prefers-reduced-motion:reduce){.gal-frame img{transition:none}}

  /* Review of 8 November (Codex, Opus): read outdoors on a phone.
     Contrast to WCAG 2.2 AA on cream: the burnt orange is darkened a shade
     for text and the button (4.47:1 to 4.77:1), small print and the footer
     line lifted, field edges at 3.2:1, type and targets one step larger. */
  .reg{--accent:#B84D03}
  .reg-small,.reg-form .opt{color:var(--fg-70)}
  .reg-small{font-size:.75rem}
  .reg-legal{color:rgba(var(--cream-rgb),.72);font-size:.66rem}
  .reg-lock small{font-size:.66rem;color:rgba(var(--cream-rgb),.72)}
  .reg-form .form-done b{font-size:1.22rem}
  .reg-form label{font-size:.72rem}
  .reg-form input:not([type="checkbox"]){border-color:rgba(var(--deep-rgb),.5)}
  .reg-form input:focus-visible{outline:2px solid var(--deep);outline-offset:2px;box-shadow:none}
  .reg-form input[aria-invalid="true"]{border-color:var(--burnt);border-width:2px}
  .reg-form .reg-consent label{font-size:.84rem}
  .reg-consent input{width:20px;height:20px}
  .reg-casl{margin:-.35rem 0 0 calc(20px + .7rem);font-size:.72rem;line-height:1.5;color:var(--fg-70)}
  .reg-casl a{color:var(--fg);text-decoration:none;border-bottom:1px solid var(--accent);white-space:nowrap}
  .reg-form .btn{min-height:48px}
  .reg-form.is-done .label,.reg-form.is-done h2{display:none}
  .reg-form.is-done .form-done{margin-top:0}
  .gal-text{flex:1 1 auto;min-width:0}
  .gal-meta{align-items:flex-start}
  .gal-cap,.gal-credit{font-size:.75rem}
  .gal-ctl{display:flex;align-items:center;gap:.35rem;flex:0 0 auto;margin-top:-.25rem}
  .gal-play{position:absolute;right:.6rem;bottom:.6rem;z-index:2;width:32px;height:32px;padding:0;
    border:0;cursor:pointer;background:rgba(var(--cream-rgb),.88);color:var(--deep);transition:background .25s,color .25s}
  .gal-play:hover{background:var(--deep);color:var(--cream)}
  .gal-play::before,.gal-play::after{content:"";position:absolute;top:11px;width:3px;height:10px;
    background:currentColor}
  .gal-play::before{left:12px}
  .gal-play::after{left:17px}
  .gal-play[data-state="paused"]::before{left:13px;top:11px;width:0;height:0;background:none;
    border-style:solid;border-width:5px 0 5px 8px;border-color:transparent transparent transparent currentColor}
  .gal-play[data-state="paused"]::after{display:none}
  .gal-play:focus-visible{outline:2px solid var(--deep);outline-offset:2px}
  .gal-dots button::before{background:rgba(var(--deep-rgb),.5)}
  .gal-frame.is-loading::after{content:"";position:absolute;left:50%;top:50%;width:26px;height:26px;
    margin:-13px 0 0 -13px;border:2px solid rgba(var(--cream-rgb),.5);border-top-color:var(--cream);
    border-radius:50%;animation:galspin .8s linear infinite;z-index:1}
  @keyframes galspin{to{transform:rotate(360deg)}}
  .reg-foot-in{max-width:calc(1280px - 4.8rem)}
  @media(max-width:860px){
    .gal-meta{flex-wrap:wrap;gap:.4rem}
    .gal-text{flex:1 0 100%}
    .gal-ctl{width:100%;margin-top:0}
    .gal-dots{flex:1 1 auto;flex-wrap:wrap;gap:0}
    .gal-dots button::before{left:3px;right:3px}
    .gal-play{width:36px;height:36px}
    .gal-play::before,.gal-play::after{top:13px}
    .gal-play::before{left:14px}
    .gal-play::after{left:19px}
    .gal-play[data-state="paused"]::before{left:15px;top:13px}
    .gal-dots button{width:24px;height:24px}
    .gal-btn{width:44px;height:44px}
    .reg-foot-in{max-width:none}
  }
'''


# ==========================================================================
#  The body
# ==========================================================================

@dataclass(frozen=True)
class Slide:
    """One carousel image. file is relative to the site root."""
    file: str
    cap: str
    credit: str
    alt: str
    render: bool = False      # a Truong Ly render BSaR supplies; go-live needs it


EXT_CREDIT = "Artist&#39;s rendering. Subject to change."
TL_CREDIT = "Rendering by Truong Ly Design Inc. Subject to change."
JC_CREDIT = "Photo by Jacob C&ocirc;t&eacute; Photography."
PH = "photos/1521-queen-st-jacobcotephotography-web-%d.jpg"

# The streetcar exterior first (pin 4), then Claire's five renders of 2 and 3
# November (suite, then the amenities), then six landscape frames from Jacob
# Cote's final set. Photos are files with their original names and embedded
# copyright, as his credit guidelines ask.
SLIDES = (
    Slide("photos/1521-exterior-streetcar-r2.jpg", "1521 Queen Street West.", EXT_CREDIT,
          "Rendering of 1521 Queen Street West with a streetcar passing"),
    Slide("renders/1521-suite-interior.jpg", "Suite interior.", TL_CREDIT,
          "Rendering of a suite interior at 1521 Queen Street West", True),
    Slide("renders/1521-co-working-lounge.jpg", "Co-working lounge.", TL_CREDIT,
          "Rendering of the co-working lounge at 1521 Queen Street West", True),
    Slide("renders/1521-party-room.jpg", "Party room.", TL_CREDIT,
          "Rendering of the party room at 1521 Queen Street West", True),
    Slide("renders/1521-fitness-studio.jpg", "Fitness studio.", TL_CREDIT,
          "Rendering of the fitness studio at 1521 Queen Street West", True),
    Slide("renders/1521-terrace.jpg", "Terrace lounge.", TL_CREDIT,
          "Rendering of the outdoor terrace lounge at 1521 Queen Street West", True),
    Slide(PH % 2, "Queen Street West.", JC_CREDIT, "Queen Street West"),
    Slide(PH % 7, "Parkdale.", JC_CREDIT, "Parkdale"),
    Slide(PH % 9, "Neighbourhood patios.", JC_CREDIT, "Neighbourhood patios"),
    Slide(PH % 13, "Sunnyside, on the waterfront.", JC_CREDIT, "Sunnyside, on the waterfront"),
    Slide(PH % 12, "The waterfront trail.", JC_CREDIT, "The waterfront trail"),
    Slide(PH % 14, "Lake Ontario.", JC_CREDIT, "Lake Ontario"),
)

SIZES = "(max-width: 860px) 100vw, 60vw"


def small_of(file: str) -> str:
    """The 960 px copy tools/prep_images.py writes beside each image."""
    return re.sub(r"\.jpg$", "-960.jpg", file)


def width(path: Path) -> int:
    """The true pixel width, for the srcset w descriptor."""
    from PIL import Image
    with Image.open(path) as im:
        return im.size[0]


def missing_renders() -> list[str]:
    return [s.file for s in SLIDES if s.render and not (ROOT / s.file).exists()]


def placeholder(slide: Slide) -> str:
    """A labelled tile for a proof, never for the live site."""
    name = slide.cap.rstrip(".")
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900">'
           '<rect width="1200" height="900" fill="#ECE4D6"/>'
           '<rect x="36" y="36" width="1128" height="828" fill="none" stroke="#10069F" '
           'stroke-opacity=".35" stroke-width="3" stroke-dasharray="16 12"/>'
           '<text x="600" y="425" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" '
           'font-size="50" fill="#10069F">%s</text>'
           '<text x="600" y="495" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" '
           'font-size="30" fill="#10069F" fill-opacity=".7">Truong Ly rendering goes here</text>'
           '</svg>') % name
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("ascii")).decode("ascii")


def slides_html(prefix: str, placeholders: bool) -> tuple[str, str, list[Slide]]:
    """The <img> stack and the dots. Only the first image loads with the page;
    the script fills in each of the others just before it shows."""
    shown: list[tuple[Slide, str, str]] = []
    for s in SLIDES:
        exists = (ROOT / s.file).exists()
        if s.render and not exists:
            if placeholders:
                shown.append((s, placeholder(s), ""))
            continue
        if not exists:
            raise SystemExit("apply_register: missing image %s" % s.file)
        small = small_of(s.file)
        srcset = ""
        if (ROOT / small).exists():
            srcset = "%s%s %dw, %s%s %dw" % (prefix, small, width(ROOT / small),
                                             prefix, s.file, width(ROOT / s.file))
        shown.append((s, prefix + s.file, srcset))

    imgs, dots = [], []
    n = len(shown)
    for i, (s, src, srcset) in enumerate(shown):
        common = 'alt="%s" data-cap="%s" data-credit="%s" draggable="false" decoding="async"' % (
            s.alt, s.cap, s.credit)
        if i == 0:
            set_attr = ' srcset="%s" sizes="%s"' % (srcset, SIZES) if srcset else ""
            imgs.append('    <img class="gal-shot is-on" src="%s"%s fetchpriority="high" %s>'
                        % (src, set_attr, common))
        else:
            set_attr = ' data-srcset="%s" data-sizes="%s"' % (srcset, SIZES) if srcset else ""
            imgs.append('    <img class="gal-shot" data-src="%s"%s aria-hidden="true" %s>'
                        % (src, set_attr, common))
        dots.append('      <button type="button" aria-label="Image %d of %d"%s></button>'
                    % (i + 1, n, ' aria-current="true"' if i == 0 else ""))
    return "\n".join(imgs), "\n".join(dots), [s for s, _, _ in shown]


CONSENT = ("Yes, send me email updates about 1521 Queen West from Property Management "
           "Toronto Inc. on behalf of BS&#228;R Group of Companies. I can unsubscribe at any time.")
# Marketing Services Agreement s. 14.2: separate from the 1521 registration, unchecked,
# optional. Only people who tick it may stay on PMT's own list after the term.
CONSENT_PMT = ("Optional: also send me emails from Property Management Toronto Inc. and its "
               "affiliates, including PMT Realty Inc., Brokerage, about other rentals. "
               "I can unsubscribe at any time.")


def body(prefix: str, placeholders: bool) -> tuple[str, int]:
    imgs, dots, shown = slides_html(prefix, placeholders)
    first = shown[0]
    html = '''<div class="reg" id="top">

  <main class="reg-main">
    <div class="reg-say">
      <h1 class="reg-logo" aria-label="1521 Queen West">''' + inline("C23", "lg-c23") + '''</h1>
      <p class="reg-tag">Luxury Rentals on Queen West</p>
      <p class="reg-soon">Move-In Summer 2027</p>
      <p class="reg-line">Boutique residences at 1521 Queen Street West.</p>

      <div class="reg-form">
        <span class="label">Registration</span>
        <h2>Register <em>Now.</em></h2>
        <noscript><style>#waitlist{display:none}</style><p class="reg-err">Registration needs JavaScript turned on in your browser. To register by phone, call <a href="''' + LEASING_TEL + '''">''' + LEASING_SHOWN + '''</a>.</p></noscript>
        <form id="waitlist" data-endpoint="''' + ENDPOINT + '''" method="post" novalidate>
          <div><label for="fn">First Name</label><input id="fn" name="first_name" autocomplete="given-name" maxlength="60" required></div>
          <div><label for="ln">Last Name</label><input id="ln" name="last_name" autocomplete="family-name" maxlength="60" required></div>
          <div class="full"><label for="em">Email</label><input id="em" name="email" type="email" autocomplete="email" inputmode="email" maxlength="120" required></div>
          <div class="full"><label for="ph">Phone <span class="opt">(optional)</span></label><input id="ph" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="40"></div>
          <div class="full reg-consent"><input id="cs" name="consent" type="checkbox" value="yes" required aria-describedby="cscasl"><label for="cs" id="cslabel">''' + CONSENT + '''</label></div>
          <div class="full reg-consent"><input id="cp" name="consent_pmt" type="checkbox" value="yes" aria-describedby="cscasl"><label for="cp" id="cplabel">''' + CONSENT_PMT + '''</label></div>
          <p class="full reg-casl" id="cscasl">Property Management Toronto Inc., 200 - 141 Bathurst Street, Toronto, ON M5V 2R2, <a href="''' + LEASING_TEL + '''">''' + LEASING_SHOWN + '''</a>. <a href="''' + PRIVACY_URL + '''" target="_blank" rel="noopener noreferrer">Privacy policy</a></p>
          <div class="reg-hp" aria-hidden="true"><label for="co">Company</label><input id="co" name="company" tabindex="-1" autocomplete="off"></div>
          <div class="full"><button class="btn btn-solid btn-mag" type="submit" id="regbtn">Register Now</button></div>
          <p class="full reg-err" id="regerr" role="alert" hidden></p>
        </form>
        <div class="form-done tone-deep" id="done" tabindex="-1"><b>Thank you, you&#39;re registered.</b><br>We&#39;ll email you updates on 1521 as move-in approaches.</div>
        <p class="reg-fine">Realtors are welcome to register on behalf of a client, using their own contact details.</p>
        <p class="reg-fine">Leasing inquiries: <a href="''' + LEASING_TEL + '''">''' + LEASING_SHOWN + '''</a>. PMT Realty Inc., Brokerage.</p>
      </div>
    </div>

    <aside class="reg-gal" id="gal" role="group" aria-roledescription="carousel" aria-label="Images of 1521 Queen West and the neighbourhood">
      <div class="gal-frame" id="galframe">
''' + imgs + '''
        <button type="button" class="gal-btn prev" id="galprev" aria-label="Previous image"></button>
        <button type="button" class="gal-btn next" id="galnext" aria-label="Next image"></button>
        <button type="button" class="gal-play" id="galplay" aria-label="Pause the slideshow"></button>
      </div>
      <div class="gal-meta">
        <div class="gal-text" id="galtext" aria-live="off">
          <p class="gal-cap" id="galcap">''' + first.cap + '''</p>
          <p class="gal-credit" id="galcredit">''' + first.credit + '''</p>
        </div>
        <div class="gal-ctl">
          <div class="gal-dots" id="galdots" role="group" aria-label="Choose an image">
''' + dots + '''
          </div>
        </div>
      </div>
    </aside>
  </main>

  <div class="reg-small">
    <p>Renderings are artist&#39;s concepts of the building, suites and amenities and are subject to change. Neighbourhood images show the surrounding area, not the property. The move-in date is an estimate and may change. Features, finishes and availability are subject to change without notice.</p>
    <p>Images by: <a href="https://jacobcotephotography.com" target="_blank" rel="noopener noreferrer">Jacob C&ocirc;t&eacute; Photography</a>. Suite and amenity renderings by: Truong Ly Design Inc.</p>
    <p>Privacy: your registration is collected by BS&#228;R Group of Companies (BSAR (Queen) LP), the owner of 1521 Queen West, together with Property Management Toronto Inc. and PMT Realty Inc., Brokerage, which run its marketing and leasing. We use your name, email and phone number to send you updates about 1521 and to contact you about leasing, and we keep a record of your consent and of how you reached this page. If you tick the optional box, Property Management Toronto Inc. and its affiliates may also email you about other rentals. We do not sell your information. Our service providers may store it outside Canada. Unsubscribe from any email, or call ''' + LEASING_SHOWN + ''' to be removed. See our <a href="''' + PRIVACY_URL + '''" target="_blank" rel="noopener noreferrer">privacy policy</a>.</p>
  </div>

  <footer class="reg-foot">
    <div class="reg-foot-in">
      <span class="reg-lock"><small>A Development By</small>
        <a href="https://www.bsargroup.com" target="_blank" rel="noopener noreferrer"><img src="{{DU_25}}" alt="BS&#228;R Group of Companies"></a></span>
      <span class="reg-lock"><small>Leasing Management By</small>
        <a href="https://www.propertymanagementto.com" target="_blank" rel="noopener noreferrer"><img class="tall" src="{{DU_26}}" alt="PMT Property Management Toronto"></a></span>
      <span class="reg-legal">Site design copyright 2026 Property Management Toronto Inc.</span>
    </div>
  </footer>
</div>

'''
    return html, len(shown)


# ==========================================================================
#  The only script this page needs
# ==========================================================================

REG_JS = '''<script>
/* Image carousel in the call-out box (Claire, 18 September): arrows, dots
   and a swipe, and it turns on its own every five seconds (Ahmed, 8 November).
   The turning waits while the pointer is over it, while anyone is in the form
   or the carousel with the keyboard, while it is off screen or the tab is
   hidden; the pause button stops it, and a reader who prefers reduced motion
   starts paused. Captions are announced for a person's own clicks only.
   Only the first image comes with the page. A slide changes once its image
   has loaded, so the frame never shows a caption over an empty box; a failed
   image keeps the current slide. */
(function(){
  var frame = document.getElementById('galframe');
  var shots = [].slice.call(document.querySelectorAll('.gal-shot'));
  var dots = [].slice.call(document.querySelectorAll('#galdots button'));
  var cap = document.getElementById('galcap');
  var credit = document.getElementById('galcredit');
  if(!frame || shots.length < 2 || dots.length !== shots.length) return;
  var i = 0, want = 0;
  var gal = document.getElementById('gal');
  var form = document.getElementById('waitlist');
  var text = document.getElementById('galtext');
  var playBtn = document.getElementById('galplay');
  var reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function ready(s){ return s.getAttribute('src') && !s.getAttribute('data-failed') && s.complete && s.naturalWidth > 0; }
  function load(s){
    if(s.getAttribute('data-failed')){
      s.removeAttribute('data-failed'); s.removeAttribute('srcset'); s.removeAttribute('src');
    }
    if(s.getAttribute('src')) return;
    if(s.getAttribute('data-srcset')){
      s.setAttribute('sizes', s.getAttribute('data-sizes') || '100vw');
      s.setAttribute('srcset', s.getAttribute('data-srcset'));
    }
    s.setAttribute('src', s.getAttribute('data-src'));
  }
  function paint(k){
    i = k;
    shots.forEach(function(s, n){
      s.classList.toggle('is-on', n === i);
      s.setAttribute('aria-hidden', n === i ? 'false' : 'true');
    });
    dots.forEach(function(d, n){
      if(n === i) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current');
    });
    if(cap) cap.textContent = shots[i].getAttribute('data-cap') || '';
    if(credit) credit.textContent = shots[i].getAttribute('data-credit') || '';
    [shots[(i + 1) % shots.length], shots[(i - 1 + shots.length) % shots.length]].forEach(function(s){
      if(s.getAttribute('src')) return;
      s.addEventListener('error', function(){ s.setAttribute('data-failed', '1'); }, {once: true});
      load(s);
    });
  }
  function go(n){
    var k = (n + shots.length) % shots.length, s = shots[k];
    want = k;
    if(ready(s)){ frame.classList.remove('is-loading'); paint(k); return; }
    frame.classList.add('is-loading');
    function done(ok){
      s.removeEventListener('load', onload); s.removeEventListener('error', onerr);
      if(!ok) s.setAttribute('data-failed', '1');
      if(want !== k) return;              /* a later click won */
      frame.classList.remove('is-loading');
      if(ok) paint(k); else want = i;     /* stay put; a later click retries */
    }
    function onload(){ done(true); }
    function onerr(){ done(false); }
    s.addEventListener('load', onload);
    s.addEventListener('error', onerr);
    load(s);
    if(ready(s)) done(true);
  }
  /* a person's own move: announce it and restart the five seconds */
  function user(n){ if(text) text.setAttribute('aria-live', 'polite'); go(n); restart(); }
  dots.forEach(function(d, k){ d.addEventListener('click', function(){ user(k); }); });
  document.getElementById('galprev').addEventListener('click', function(){ user(want - 1); });
  document.getElementById('galnext').addEventListener('click', function(){ user(want + 1); });

  /* swipe: a horizontal move of 40 px or more between pointer down and up */
  var x0 = null;
  frame.addEventListener('pointerdown', function(e){ x0 = e.clientX; });
  frame.addEventListener('pointerup', function(e){
    if(x0 === null) return;
    var dx = e.clientX - x0; x0 = null;
    if(Math.abs(dx) < 40) return;
    user(dx < 0 ? want + 1 : want - 1);
  });
  frame.addEventListener('pointercancel', function(){ x0 = null; });

  paint(0);

  /* automatic turning */
  var stopped = reducedMotion, hover = false, typing = false, seen = true, timer = null;
  function tick(){
    if(stopped || hover || typing || !seen || document.hidden) return;
    if(text) text.setAttribute('aria-live', 'off');
    go(want + 1);
  }
  function restart(){ clearInterval(timer); timer = setInterval(tick, 5000); }
  function showState(){
    if(!playBtn) return;
    playBtn.setAttribute('data-state', stopped ? 'paused' : 'playing');
    playBtn.setAttribute('aria-label', stopped ? 'Play the slideshow' : 'Pause the slideshow');
  }
  if(playBtn) playBtn.addEventListener('click', function(){ stopped = !stopped; showState(); restart(); });
  if(gal){
    gal.addEventListener('pointerenter', function(e){ if(e.pointerType === 'mouse') hover = true; });
    gal.addEventListener('pointerleave', function(){ hover = false; });
  }
  function inside(el){ return el && ((gal && gal.contains(el) && el !== playBtn) || (form && form.contains(el))); }
  document.addEventListener('focusin', function(e){ typing = inside(e.target); });
  document.addEventListener('focusout', function(e){ typing = inside(e.relatedTarget); });
  if(gal && window.IntersectionObserver){
    new IntersectionObserver(function(es){ seen = es[0].isIntersecting; }, {threshold: .35}).observe(gal);
  }
  showState();
  restart();

  /* the magnetic pull on the submit button, as on the main site */
  var fine = matchMedia('(hover:hover) and (pointer:fine)').matches;
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(fine && !reduced){
    document.querySelectorAll('.btn-mag').forEach(function(b){
      b.addEventListener('pointermove', function(e){
        var r = b.getBoundingClientRect();
        b.style.transform = 'translate(' + ((e.clientX - r.left - r.width/2) * .12).toFixed(2)
          + 'px,' + ((e.clientY - r.top - r.height/2) * .22).toFixed(2) + 'px)';
      });
      b.addEventListener('pointerleave', function(){ b.style.transform = ''; });
    });
  }
})();

/* Registration: posts to the PMT intake as a plain form body, so the browser
   sends it without a preflight. The thank you shows only when the intake
   answers ok. A field to fix is named and focused. When the answer is lost
   (network, timeout) the page says it could not confirm, never that it
   failed: a retry of the same email is recognised by the intake as one
   registration. The ?src= tag (hoarding QR and the like) rides along. */
(function(){
  var form = document.getElementById('waitlist');
  var box = form ? form.parentNode : null;
  var done = document.getElementById('done');
  var err = document.getElementById('regerr');
  var btn = document.getElementById('regbtn');
  var consent = document.getElementById('cs');
  var consentText = document.getElementById('cslabel');
  if(!form || !done || !err || !btn) return;
  var t0 = Date.now(), busy = false, label = btn.textContent;
  var q = new URLSearchParams(location.search);
  var src = (q.get('src') || q.get('utm_source') || '').slice(0, 80);
  var CALL = ' or call <a href="''' + LEASING_TEL + '''">''' + LEASING_SHOWN + '''</a>';
  var FIELDS = {
    first_name: ['fn', 'Enter your first name.'],
    last_name: ['ln', 'Enter your last name.'],
    email: ['em', 'Enter a valid email address, such as name@example.com.'],
    phone: ['ph', 'Enter a phone number with the area code, or leave it blank.'],
    consent: ['cs', 'Tick the box to receive email updates, which is how we keep you posted.']
  };

  function clearMarks(){
    Object.keys(FIELDS).forEach(function(f){
      var el = document.getElementById(FIELDS[f][0]);
      el.removeAttribute('aria-invalid');
      el.removeAttribute('aria-errormessage');
    });
  }
  function showFields(list){
    clearMarks();
    var msgs = [];
    list.forEach(function(f){
      if(!FIELDS[f]) return;
      var el = document.getElementById(FIELDS[f][0]);
      el.setAttribute('aria-invalid', 'true');
      el.setAttribute('aria-errormessage', 'regerr');
      msgs.push(FIELDS[f][1]);
    });
    err.textContent = msgs.join(' ');
    err.hidden = false;
    var first = FIELDS[list[0]] && document.getElementById(FIELDS[list[0]][0]);
    if(first) first.focus();
  }
  function local(){
    var bad = [];
    var v = function(id){ return (document.getElementById(id).value || '').trim(); };
    if(!v('fn')) bad.push('first_name');
    if(!v('ln')) bad.push('last_name');
    if(!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$/.test(v('em'))) bad.push('email');
    var digits = v('ph').replace(/\\D/g, '');
    if(v('ph') && (digits.length < 10 || digits.length > 15)) bad.push('phone');
    if(!consent.checked) bad.push('consent');
    return bad;
  }
  function settle(){ busy = false; btn.disabled = false; btn.textContent = label; }
  function unsure(){
    settle();
    err.innerHTML = 'We could not confirm your registration. Please try again,' + CALL + '.';
    err.hidden = false;
  }
  function ok(){
    form.style.display = 'none';
    if(box) box.classList.add('is-done');
    done.style.display = 'block';
    done.focus();
  }
  ['fn', 'ln', 'em', 'ph', 'cs'].forEach(function(id){
    var el = document.getElementById(id);
    el.addEventListener(id === 'cs' ? 'change' : 'input', function(){
      if(el.getAttribute('aria-invalid')){ el.removeAttribute('aria-invalid'); el.removeAttribute('aria-errormessage'); }
    });
  });
  form.addEventListener('submit', function(e){
    e.preventDefault();
    if(busy) return;
    err.hidden = true;
    var bad = local();
    if(bad.length) return showFields(bad);
    clearMarks();
    var body = new URLSearchParams();
    ['first_name', 'last_name', 'email', 'phone', 'company'].forEach(function(n){
      body.append(n, (form.elements[n].value || '').trim());
    });
    body.append('consent', consent.checked ? 'yes' : 'no');
    var pmt = document.getElementById('cp');
    body.append('consent_pmt', pmt && pmt.checked ? 'yes' : 'no');
    body.append('consent_text', consentText ? consentText.textContent.replace(/\\s+/g, ' ').trim() : '');
    body.append('source', src);
    body.append('page', location.origin + location.pathname + location.search);
    body.append('referrer', (document.referrer || '').slice(0, 300));
    body.append('elapsed', String(Date.now() - t0));
    busy = true; btn.disabled = true; btn.textContent = 'Sending...';
    var over = false;
    var ctl = window.AbortController ? new AbortController() : null;
    var guard = setTimeout(function(){ over = true; if(ctl) ctl.abort(); unsure(); }, 15000);
    fetch(form.getAttribute('data-endpoint'), {method: 'POST', body: body, mode: 'cors', credentials: 'omit',
                        signal: ctl ? ctl.signal : undefined})
      .then(function(r){
        return r.json().then(function(j){ return {s: r.status, j: j}; },
                             function(){ return {s: r.status, j: {}}; });
      })
      .then(function(res){
        if(over) return;
        clearTimeout(guard);
        if(res.s === 200 && res.j && res.j.ok === true){ settle(); return ok(); }
        if(res.s === 422 && res.j && res.j.fields && res.j.fields.length){ settle(); return showFields(res.j.fields); }
        unsure();
      }, function(){ if(over) return; clearTimeout(guard); unsure(); });
  });
})();
</script>
'''


def build_head(src: str, live: bool) -> str:
    if src.count(HEAD_END) != 1:
        raise SystemExit("apply_register: head marker appears %d times" % src.count(HEAD_END))
    head = src[:src.index(HEAD_END) + len(HEAD_END)]
    if head.lstrip().lower().startswith("<!doctype"):
        raise SystemExit("apply_register: v3 now carries a doctype; drop the one added here")
    # standards mode and a document language (the v3 skeleton has neither)
    head = '<!doctype html>\n<html lang="en">\n' + head
    # the palette and font switchers stay on v3 only: Blue 072 C and DM Sans
    # are settled
    take(src, FSW_START, "\n<script>", "switcher markup", include_end=False)

    for old, new, label in ((OLD_TITLE, NEW_TITLE, "title"),
                            (OLD_DESC, NEW_DESC, "description"),
                            (OLD_LD_DESC, NEW_LD_DESC, "json-ld description")):
        if head.count(old) != 1:
            raise SystemExit("apply_register: %s: expected 1, found %d"
                             % (label, head.count(old)))
        head = head.replace(old, new)

    if len(LD_RE.findall(head)) != 1:
        raise SystemExit("apply_register: expected one JSON-LD block")
    head = LD_RE.sub(lambda m: ld_block(live), head)

    if head.count(ROBOTS_PREVIEW) != 1:
        raise SystemExit("apply_register: robots meta not found")
    if live:
        head = head.replace(ROBOTS_PREVIEW, live_meta())

    # weight v3 carries that this page never draws
    faces = len(UNUSED_FACES.findall(head))
    if faces != 8:
        raise SystemExit("apply_register: expected 8 switcher @font-face rules, found %d" % faces)
    head = UNUSED_FACES.sub("", head)
    css = head[head.index("<style>"):head.rindex("</style>")]
    if css.count("{") != css.count("}") or "@font-face{font-family:\"Poppins\"" in css:
        raise SystemExit("apply_register: stylesheet braces unbalanced after the font strip")
    if head.count(AMEN_BG) != 1:
        raise SystemExit("apply_register: amenity background token not found once")
    head = head.replace(AMEN_BG, "none")

    if head.count("\n</style>") != 1:
        raise SystemExit("apply_register: cannot find the end of the stylesheet")
    head = head.replace("\n</style>", "\n" + REG_CSS + "</style>")
    head = head.replace("<script>document.documentElement.className += ' js';</script>",
                        "<script>document.documentElement.className += ' js';"
                        "document.addEventListener('DOMContentLoaded',function(){"
                        "document.body.classList.add('reg-page');});</script>")
    return head


def check(h: str, n_slides: int, live: bool, placeholders: bool) -> None:
    for pat in (r"[Tt]he 501", r"THE 501", r"Premium Rentals", r"Parkdale House",
                r"\$[0-9]", r"answered live", r"24 hours", r"24/7", r"follow up within",
                r"resident portal", r"Emergency", r"leased and managed by"):
        m = re.search(pat, h)
        if m:
            raise SystemExit("apply_register: %r survived at %d: ...%s..."
                             % (m.group(0), m.start(), h[max(0, m.start() - 90):m.start() + 90]))

    body_only = re.sub(r"<script\b[^>]*>.*?</script>", "", h[h.index("</style>"):], flags=re.S)
    for banned, why in (('id="plangrid"', "floor plans"),
                        ("data-bedfilter", "bedroom filter"),
                        ('class="amen-list"', "amenity list"),
                        ('id="offer"', "offer section"),
                        ("Founding Resident", "offers"),
                        ("Starting From", "pricing"),
                        ("Suite Type", "suite types"),
                        ("Bedroom Type", "suite types"),
                        ('id="st"', "the bedroom select"),
                        ('id="cm"', "the message box"),
                        ('id="nbmap"', "the map"),
                        ('id="gallery"', "the gallery section"),
                        ('id="realtors"', "the realtor section"),
                        ('class="nav-links"', "the nav menu"),
                        ("sec-eyebrow", "section headings")):
        if banned in body_only:
            raise SystemExit("apply_register: %s survived (%s)" % (banned, why))
    for need in ('id="fn"', 'id="ln"', 'id="em"', 'id="ph"', 'id="waitlist"', 'id="cs"',
                 'id="co"', 'id="regerr"', 'id="done"', 'class="reg-logo"', 'lg-c23',
                 LEASING_TEL, LEASING_SHOWN, ENDPOINT,
                 'id="gal"', 'id="galdots"', 'id="galprev"', 'id="galcredit"', 'id="galplay"',
                 'class="reg-foot"', 'class="reg-small"', "Privacy:",
                 "Move-In Summer 2027", "Boutique residences at 1521 Queen Street West.",
                 "Truong Ly Design Inc.", "subject to change", 'id="cp"', "BSAR (Queen) LP",
                 "PMT Realty Inc., Brokerage", "Site design copyright",
                 "jacobcotephotography.com", "bsargroup.com", "propertymanagementto.com"):
        if need not in body_only:
            raise SystemExit("apply_register: %s is missing" % need)
    # pins 3, 5, 6, 7 and the preview form: none of the replaced lines may come back
    for gone in ("Coming Soon", "Ninety-five", "Photography to follow", "451.9499",
                 'class="wm-stack"', 'class="reg-bar"', "lg-c05", "lg-c24", "lsw",
                 "pmt-preview", "Preview.", "Preview only", "not yet being captured",
                 "onsubmit="):
        if gone in body_only:
            raise SystemExit("apply_register: %r is back on the page" % gone)
    if re.search(r"first access", h, re.I):
        raise SystemExit("apply_register: 'first access' is back (Claire's pin 5 replaced it)")
    if "{{DU_2}}" in h:
        raise SystemExit("apply_register: the 444 KB amenity image is back in the stylesheet")
    if body_only.count('class="gal-shot') != n_slides:
        raise SystemExit("apply_register: expected %d slides" % n_slides)
    if body_only.count('aria-label="Image ') != n_slides:
        raise SystemExit("apply_register: dots do not match the slides")
    if live:
        if "data:image/svg+xml;base64" in body_only.split('class="reg-foot"')[0]:
            raise SystemExit("apply_register: a placeholder reached the live page")
        if 'content="index, follow"' not in h or LIVE_URL not in h or "noindex" in h:
            raise SystemExit("apply_register: live head is not indexable or has no canonical")
        if "../photos/" in h:
            raise SystemExit("apply_register: live page points above the site root")
    else:
        if "noindex" not in h:
            raise SystemExit("apply_register: preview page must stay noindex")
    bad = [(i, c) for i, c in enumerate(h) if ord(c) > 127]
    if bad:
        raise SystemExit("apply_register: %d non-ASCII characters in output" % len(bad))


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the 1521 registration page skeletons")
    ap.add_argument("--placeholders", action="store_true",
                    help="draw a labelled tile for each missing render (proofs only)")
    args = ap.parse_args()
    if not SRC.exists():
        raise SystemExit("apply_register: %s missing. Run tools/apply_v3.py first." % SRC)
    src = SRC.read_text(encoding="utf-8")

    for live, out, prefix in ((False, OUT, "../"), (True, OUT_LIVE, "")):
        html_body, n = body(prefix, args.placeholders and not live)
        h = build_head(src, live) + "\n" + html_body + REG_JS
        check(h, n, live, args.placeholders)
        out.parent.mkdir(exist_ok=True)
        out.write_text(h, encoding="utf-8")
        print("apply_register: wrote %s (%.1f KB, %d slides)"
              % (out.relative_to(ROOT), len(h.encode()) / 1024, n))
    gone = missing_renders()
    if gone:
        print("apply_register: %d render(s) not in the build yet: %s%s"
              % (len(gone), ", ".join(Path(g).name for g in gone),
                 " (placeholders on the preview)" if args.placeholders else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
