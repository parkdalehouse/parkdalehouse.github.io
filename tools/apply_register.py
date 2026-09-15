#!/usr/bin/env python3
"""
Build the Phase 1 registration page from the v3 skeleton.

Reads   v3/skeleton_v3.html            output of tools/apply_v3.py
Writes  register/skeleton_register.html  still token-ised

This is the page the hoarding points at. Tyler's brief from 8 September 2026:
one rendering, the wordmark, the tagline, the occupancy date, the form, a
teaser carousel (Claire's markup 3), the neighbourhood map with the corrected
filter, and a line for realtors. No floor plans, no suite types, no pricing,
no offers, no amenity list.

It is cut from the same skeleton as v3 rather than written separately, so the
palette, the type, the form ids and the map behaviour can never drift apart.

Rebuild:
    python3 tools/apply_v3.py \\
      && python3 tools/apply_register.py \\
      && python3 tools/inflate.py --target register
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "v3" / "skeleton_v3.html"
OUT = ROOT / "register" / "skeleton_register.html"

_edits = 0


def sub(html, old, new, count=1, label=""):
    global _edits
    found = html.count(old)
    if found != count:
        raise SystemExit(
            "apply_register: %s: expected %d occurrence(s), found %d\n  needle: %r"
            % (label or "edit", count, found, old[:160]))
    _edits += 1
    return html.replace(old, new)


def take_block(html, start_marker, end_marker, label=""):
    """Remove start..end inclusive and hand back (rest, removed)."""
    global _edits
    i = html.find(start_marker)
    j = html.find(end_marker, i + 1)
    if i == -1 or j == -1:
        raise SystemExit("apply_register: %s: block not found" % (label or "cut"))
    _edits += 1
    j += len(end_marker)
    return html[:i] + html[j:], html[i:j]


def cut(html, start_marker, end_marker, label=""):
    rest, _ = take_block(html, start_marker, end_marker, label)
    return rest


# ==========================================================================
#  HEAD
# ==========================================================================

OLD_TITLE = '''<title>1521 | Luxury Rentals on Queen West</title>'''
NEW_TITLE = '''<title>1521 | Register for Phase 1</title>'''

OLD_DESC = '''<meta name="description" content="1521 at 1521 Queen Street West. Luxury rentals on Queen West, Toronto: ninety-five purpose-built studio to three bedroom residences, steps from the 501 streetcar, Roncesvalles Village and the waterfront. Coming Soon Summer 2027.">'''
NEW_DESC = '''<meta name="description" content="Register for Phase 1 at 1521, 1521 Queen Street West. Luxury rentals on Queen West, Toronto. Coming Soon Summer 2027.">'''


# ==========================================================================
#  NAV: only the sections this page actually has
# ==========================================================================

OLD_NAVLINKS = '''  <div class="nav-links">
    <a href="#suites">Suites</a>
    <a href="#amenities">Amenities</a>
    <a href="#neighbourhood">Neighbourhood</a>
    <a href="#perks">Residents</a>
    <a class="nav-tel" href="tel:+14164519499">416.451.9499</a>
    <a class="nav-cta btn-mag" href="#contact">Register Now</a>
  </div>'''

NEW_NAVLINKS = '''  <div class="nav-links">
    <a href="#gallery">Gallery</a>
    <a href="#map">Neighbourhood</a>
    <a href="#realtors">Realtors</a>
    <a class="nav-tel" href="tel:+14164519499">416.451.9499</a>
    <a class="nav-cta btn-mag" href="#contact">Register Now</a>
  </div>'''


# ==========================================================================
#  HERO: one still, no two-image cycle
# ==========================================================================

OLD_HERO_MEDIA = '''  <img hidden id="himg1" src="{{DU_4}}" alt="">
  <canvas id="hcv" aria-hidden="true"></canvas>
'''

OLD_HERO_SUB = '''      <p class="hero-sub">Ninety-five purpose-built residences at 1521 Queen Street West. Studio to three bedroom, steps from the 501 streetcar, Roncesvalles Village and the waterfront.</p>'''
NEW_HERO_SUB = '''      <p class="hero-sub">Ninety-five purpose-built residences at 1521 Queen Street West. Register for Phase 1 and you will be first to see floor plans, finishes and rents when they are released.</p>'''


# ==========================================================================
#  GALLERY (Claire's markup 3)
# ==========================================================================

GALLERY_CSS = '''  /* ---- teaser carousel, markup 3 --------------------------------------
     Renderings now, photography as it is captured. Scroll-snap so it works
     with a trackpad, a finger and the two buttons, with no library. */
  .gal{background:var(--deep);border-top:1px solid var(--hair);border-bottom:1px solid var(--hair);
    padding:5.5rem 0 4.5rem}
  .gal-head{max-width:calc(1280px + 4.8rem);margin:0 auto;padding:0 2.4rem;
    display:flex;justify-content:space-between;align-items:flex-end;gap:2rem;flex-wrap:wrap}
  .gal-head h2{font-size:clamp(1.5rem,2.8vw,2.2rem)}
  .gal-nav{display:flex;gap:.6rem}
  .gal-nav button{width:44px;height:44px;border:1px solid var(--hair);background:transparent;
    color:var(--fg);cursor:pointer;font-size:1rem;line-height:1;transition:all .25s}
  .gal-nav button:hover:not(:disabled){border-color:var(--accent);color:var(--accent)}
  .gal-nav button:disabled{opacity:.3;cursor:default}
  /* scroll-padding matches the gutter, so a slide snaps flush with the page
     gutter instead of one gutter short of it, and the button offsets and the
     snap points agree. */
  .gal-track{display:flex;gap:1.4rem;overflow-x:auto;scroll-snap-type:x mandatory;
    margin-top:2.4rem;padding:0 2.4rem 1.2rem;scroll-padding-left:2.4rem;
    scrollbar-width:none;-ms-overflow-style:none}
  .gal-track::-webkit-scrollbar{display:none}
  @media(min-width:1408px){.gal-track{padding-inline:calc((100vw - 1280px)/2);
    scroll-padding-left:calc((100vw - 1280px)/2)}}
  .gal-slide{flex:0 0 min(640px, 82vw);scroll-snap-align:start}
  .gal-slide .frame{aspect-ratio:3/2;background:rgba(var(--cream-rgb),.05)}
  .gal-slide .frame img{min-height:0;height:100%;width:100%;object-fit:cover}
  .gal-ph{width:100%;height:100%;display:flex;align-items:center;justify-content:center;
    text-align:center;padding:1.5rem;border:1px dashed var(--hair);
    background:repeating-linear-gradient(45deg,rgba(var(--cream-rgb),.045) 0 10px,transparent 10px 20px)}
  .gal-dots{display:flex;gap:.5rem;justify-content:center;margin-top:1.4rem}
  .gal-dots i{width:24px;height:2px;background:rgba(var(--cream-rgb),.24);transition:background .3s}
  .gal-dots i.on{background:var(--accent)}
  @media(max-width:700px){.gal{padding:3.6rem 0 3rem}
    .gal-track{padding:0 1.2rem 1.2rem;scroll-padding-left:1.2rem}
    .gal-head{padding:0 1.2rem}.gal-slide{flex-basis:86vw}}

  /* ---- realtor line ---------------------------------------------------- */
  .realtor{border-top:1px solid var(--hair)}
  .realtor .wrap{display:grid;grid-template-columns:1fr 1fr;gap:3.5rem;align-items:center}
  @media(max-width:860px){.realtor .wrap{grid-template-columns:1fr;gap:2rem}}
  .realtor h2{font-size:clamp(1.45rem,2.6vw,2.1rem)}
  .realtor .lede{max-width:46ch}
  .realtor-do{display:flex;flex-direction:column;gap:1rem;align-items:flex-start}
  .realtor-do .btn{align-self:flex-start}
  .realtor-tel{font-size:.86rem;color:var(--fg-70);text-decoration:none}
  .realtor-tel b{color:var(--fg);border-bottom:1px solid var(--accent);padding-bottom:.15rem}
  .realtor-note{font-size:.72rem;color:var(--fg-45);max-width:44ch}
'''

GALLERY = '''<section class="gal tone-deep" id="gallery">
  <div class="gal-head">
    <div>
      <div class="label sec-eyebrow reveal">Gallery</div>
      <h2 class="reveal" style="--d:.08s">Renderings now, <em>photography to come.</em></h2>
    </div>
    <div class="gal-nav">
      <button type="button" id="galprev" aria-label="Previous image">&#8249;</button>
      <button type="button" id="galnext" aria-label="Next image">&#8250;</button>
    </div>
  </div>
  <div class="gal-track" id="galtrack" tabindex="0" role="group" aria-label="Renderings and photography">
    <div class="gal-slide">
      <div class="frame"><img src="{{DU_24}}" alt="Concept rendering: the wood-canopied entrance at evening, with the 1521 address plate" loading="lazy"></div>
      <div class="frame-caption"><span>The Entrance</span><span>Concept Rendering</span></div>
    </div>
    <div class="gal-slide">
      <div class="frame"><img src="{{DU_7}}" alt="Concept rendering: a suite living room with oak floors, a walnut kitchen and the red brick church across the street" loading="lazy"></div>
      <div class="frame-caption"><span>Suite Interior</span><span>Concept Rendering</span></div>
    </div>
    <div class="gal-slide">
      <div class="frame"><img src="{{DU_8}}" alt="Concept rendering: boutique lobby with a limestone feature wall, wood slat ceiling and mailboxes" loading="lazy"></div>
      <div class="frame-caption"><span>Lobby</span><span>Concept Rendering</span></div>
    </div>
    <div class="gal-slide">
      <div class="frame"><div class="gal-ph"><span class="ph-cap">Photography to come</span></div></div>
      <div class="frame-caption"><span>Rooftop Terrace</span><span>To Be Confirmed</span></div>
    </div>
    <div class="gal-slide">
      <div class="frame"><div class="gal-ph"><span class="ph-cap">Photography to come</span></div></div>
      <div class="frame-caption"><span>Queen West</span><span>To Be Confirmed</span></div>
    </div>
  </div>
  <div class="gal-dots" id="galdots" aria-hidden="true"></div>
</section>

'''

GALLERY_JS = '''
<script>
/* Teaser carousel, markup 3. Buttons and dots over a scroll-snap track, so a
   trackpad or a finger drives the same thing the buttons do. The index is
   held in a variable rather than read back off scrollLeft, so three quick
   clicks on Next advance three slides instead of fighting the smooth scroll
   already in flight. */
(function(){
  var track = document.getElementById('galtrack');
  if(!track) return;
  var slides = [].slice.call(track.querySelectorAll('.gal-slide'));
  var dots = document.getElementById('galdots');
  if(!slides.length || !dots) return;
  slides.forEach(function(){ dots.appendChild(document.createElement('i')); });
  var marks = [].slice.call(dots.children);
  var idx = 0;

  function paint(){
    marks.forEach(function(m, n){ m.classList.toggle('on', n === idx); });
    document.getElementById('galprev').disabled = idx === 0;
    document.getElementById('galnext').disabled = idx === slides.length - 1;
  }
  function offsetOf(i){ return slides[i].offsetLeft - slides[0].offsetLeft; }
  function go(n){
    idx = Math.max(0, Math.min(slides.length - 1, n));
    track.scrollTo({left: offsetOf(idx), behavior: 'smooth'});
    paint();
  }
  document.getElementById('galprev').addEventListener('click', function(){ go(idx - 1); });
  document.getElementById('galnext').addEventListener('click', function(){ go(idx + 1); });
  track.addEventListener('keydown', function(e){
    if(e.key === 'ArrowRight'){ e.preventDefault(); go(idx + 1); }
    if(e.key === 'ArrowLeft'){ e.preventDefault(); go(idx - 1); }
  });
  /* a finger or a trackpad moves the track without going through go() */
  var t = null;
  track.addEventListener('scroll', function(){
    clearTimeout(t);
    t = setTimeout(function(){
      var best = 0, bd = Infinity;
      slides.forEach(function(s, i){
        var d = Math.abs(offsetOf(i) - track.scrollLeft);
        if(d < bd){ bd = d; best = i; }
      });
      idx = best;
      paint();
    }, 120);
  }, {passive:true});
  paint();
})();
</script>
'''


# ==========================================================================
#  REALTORS
# ==========================================================================

REALTORS = '''<section class="realtor" id="realtors">
  <div class="wrap">
    <div>
      <div class="label sec-eyebrow reveal">Realtors</div>
      <h2 class="reveal" style="--d:.08s">Register your <em>client.</em></h2>
      <p class="lede reveal" style="--d:.14s">Cooperating agents are welcome at 1521. Register your client before they tour and your registration stays on file through the Phase 1 release.</p>
    </div>
    <div class="realtor-do reveal" style="--d:.2s">
      <a class="btn btn-solid btn-mag" href="#contact">Register Your Client</a>
      <a class="realtor-tel" href="tel:+14164519499">Or call <b>416.451.9499</b> and ask for the leasing team</a>
      <p class="realtor-note">Use the registration form and put your name, brokerage and your client's name in the message field. Commission terms will be published with the Phase 1 release.</p>
    </div>
  </div>
</section>

'''


# ==========================================================================
#  FOOTER tweaks
# ==========================================================================

OLD_FOOT_LINKS = '''      <a href="#contact">Register Now</a><br><a href="/register/">Phase 1 Registration Page</a></p>'''
NEW_FOOT_LINKS = '''      <a href="#contact">Register Now</a><br><a href="#realtors">Realtor Registration</a></p>'''

OLD_FOOT_LEGAL = '''    Partner marks illustrate a proposed resident-perks program; partner perks are proposed programs pending final agreements.
    The PRESTO program is provided through the City of Toronto and is subject to program terms. Suite mix, floor plan
    types, rents and the occupancy date are not final and are subject to change. E.&amp;O.E.'''
NEW_FOOT_LEGAL = '''    Suite mix, floor plan types, rents and the occupancy date are not final and are subject to change. E.&amp;O.E.'''


def main():
    if not SRC.exists():
        raise SystemExit("apply_register: %s missing. Run tools/apply_v3.py first." % SRC)
    h = SRC.read_text(encoding="utf-8")

    # ---- head -----------------------------------------------------------
    h = sub(h, OLD_TITLE, NEW_TITLE, 1, "title")
    h = sub(h, OLD_DESC, NEW_DESC, 1, "description")

    # ---- nav ------------------------------------------------------------
    h = sub(h, OLD_NAVLINKS, NEW_NAVLINKS, 1, "nav links")

    # ---- hero: one still ------------------------------------------------
    h = sub(h, OLD_HERO_MEDIA, "", 1, "hero cycle out")
    h = sub(h, OLD_HERO_SUB, NEW_HERO_SUB, 1, "hero sub")

    # ---- everything this page does not carry ----------------------------
    h = cut(h, '<section id="about">', "</section>\n\n", "about out")
    h = cut(h, '<section class="suites" id="suites">', "</section>\n\n", "suites out")
    h = cut(h, '<section class="amen tone-deep" id="amenities">', "</section>\n\n",
            "amenities out")
    h = cut(h, '<section class="hood" id="neighbourhood">', "</section>\n\n", "hood out")
    h = cut(h, '<section id="perks">', "</section>\n\n", "perks out")
    h = cut(h, '<section class="trust tone-deep">', "</section>\n\n", "trust strip out")
    h = cut(h, '<div class="marq tone-deep" aria-hidden="true">', "</div></div>\n\n",
            "marquee out")
    h = cut(h, '<div class="arrive">', "</div>\n\n", "arrive frame out")

    # ---- the map moves below the form -----------------------------------
    h, mapblock = take_block(h, '<section class="mapsec tone-deep" id="map">',
                             "  apply();\n})();\n</script>", "map block")
    h = sub(h, '<footer class="tone-deep">', mapblock.rstrip() + "\n\n" + REALTORS
            + '<footer class="tone-deep">', 1, "map and realtors before the footer")

    # ---- gallery --------------------------------------------------------
    h = sub(h, "\n</style>", "\n" + GALLERY_CSS + "</style>", 1, "gallery css")
    h = sub(h, '<section class="contact" id="contact">',
            GALLERY + '<section class="contact" id="contact">', 1, "gallery markup")
    h = sub(h, '<div class="pal" role="group" aria-label="Brand palette preview">',
            GALLERY_JS.strip() + '\n\n<div class="pal" role="group" aria-label="Brand palette preview">',
            1, "gallery js")

    # ---- footer ---------------------------------------------------------
    h = sub(h, OLD_FOOT_LINKS, NEW_FOOT_LINKS, 1, "footer links")
    h = sub(h, OLD_FOOT_LEGAL, NEW_FOOT_LEGAL, 1, "footer legal")

    # ---- guards ---------------------------------------------------------
    for pat in (r"[Tt]he 501(?! streetcar)", r"THE 501", r"Premium Rentals",
                r"Parkdale House", r"\$[0-9]"):
        m = re.search(pat, h)
        if m:
            raise SystemExit("apply_register: %r survived at %d: ...%s..."
                             % (m.group(0), m.start(), h[max(0, m.start() - 90):m.start() + 90]))
    # Only the markup is checked. Unused rules left in the shared stylesheet
    # are inert and cost a few hundred bytes; carrying them is the price of
    # cutting this page from the same skeleton as v3, which is what keeps the
    # two from drifting apart.
    body = re.sub(r"<script\b[^>]*>.*?</script>", "", h[h.rindex("</style>"):],
                  flags=re.S)
    for banned, why in (('id="plangrid"', "floor plans"),
                        ("data-bedfilter", "bedroom filter"),
                        ('class="amen-list"', "amenity list"),
                        ('id="offer"', "offer section"),
                        ('id="offer-band"', "offer band"),
                        ("Founding Resident", "offers"),
                        ("Starting From", "pricing"),
                        ("Suite Type", "suite types")):
        if banned in body:
            raise SystemExit("apply_register: %s markup survived (%s)" % (banned, why))

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(h, encoding="utf-8")
    bad = [(i, c) for i, c in enumerate(h) if ord(c) > 127]
    if bad:
        raise SystemExit("apply_register: %d non-ASCII characters in output" % len(bad))
    print("apply_register: %d edits, wrote %s (%.1f KB)"
          % (_edits, OUT.relative_to(ROOT), len(h.encode()) / 1024))
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
