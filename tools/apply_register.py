#!/usr/bin/env python3
"""
Build the Phase 1 registration page from the v3 skeleton.

Reads   v3/skeleton_v3.html              output of tools/apply_v3.py
Writes  register/skeleton_register.html  still token-ised

This is the page the hoarding points at, and Ahmed's brief for it from the
8 September call is exact:

    "simply just one rendering and a lead intake form, like the register now
     ... we can start off with something super simple ... we'll just compress
     it into a lead intake form and then have it point there until phase two."

Tyler, same call: "just the register now", and no offers, suite types or
selections. So: one screen. No nav menu, no gallery section, no map, no
realtor section, no amenities, no section headings, nothing to argue with.

Claire's markup 3 asked for a rendering and photography carousel. It is
honoured as the background itself: three renders cross-fading behind the
page with three dots and one caption line, rather than a gallery section that
would have made this a second website.

Rather than cut the v3 page down section by section, this takes v3's head,
stylesheet and the two review switchers, and writes a new body. Everything
that matters stays shared with v3: the palette, the type roles and the font
switcher, the wordmark geometry, the button and form styling, and the review
tool. Only the layout is this page's own.

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
NEW_TITLE = "<title>1521 | Register for Phase 1</title>"

OLD_DESC = ('<meta name="description" content="1521 at 1521 Queen Street West. '
            'Luxury rentals on Queen West, Toronto: ninety-five purpose-built studio '
            'to three bedroom residences, steps from the 501 streetcar, Roncesvalles '
            'Village and the waterfront. Coming Soon Summer 2027.">')
NEW_DESC = ('<meta name="description" content="Register for Phase 1 at 1521, '
            '1521 Queen Street West. Luxury rentals on Queen West, Toronto. '
            'Coming Soon Summer 2027.">')

# the JSON-LD description inherited from v3 names the streetcar; the one-screen
# page says less, and the guard below refuses any "the 501" anyway.
OLD_LD_DESC = (', steps from the 501 streetcar, Roncesvalles Village and the waterfront. '
               'Coming Soon Summer 2027.",')
NEW_LD_DESC = '. Coming Soon Summer 2027.",'



# ==========================================================================
#  CSS for the one screen
# ==========================================================================

REG_CSS = '''
  /* ======================= PHASE 1 REGISTRATION ========================
     One screen. A rendering behind, the mark and one sentence on the left,
     the intake card on the right, a thin partner strip at the foot. On a
     phone it becomes one column and scrolls a little, which is the only
     concession.
     ==================================================================== */
  body.reg-page{overflow-x:hidden}
  .reg{position:relative;min-height:100svh;display:grid;
    grid-template-rows:auto 1fr auto auto;background:var(--deep-2);isolation:isolate}
  .reg-bg{position:absolute;inset:0;z-index:0;overflow:hidden}
  .reg-shot{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
    object-position:center 38%;opacity:0;transition:opacity 1.5s var(--ease)}
  .reg-shot.is-on{opacity:1}
  /* markup 14 again: no colour cast over the render, only what the type needs */
  .reg-scrim{position:absolute;inset:0;z-index:1;pointer-events:none;
    background:linear-gradient(180deg,rgba(0,0,0,.42) 0%,rgba(0,0,0,.12) 26%,
      rgba(0,0,0,.28) 62%,rgba(0,0,0,.72) 100%)}
  @media(min-width:861px){
    .reg-scrim{background:
      linear-gradient(90deg,rgba(0,0,0,.62) 0%,rgba(0,0,0,.30) 46%,rgba(0,0,0,.12) 70%),
      linear-gradient(180deg,rgba(0,0,0,.34) 0%,rgba(0,0,0,0) 22%,rgba(0,0,0,.52) 100%)}
  }
  .reg>:not(.reg-bg):not(.reg-scrim){position:relative;z-index:2}

  .reg-bar{display:flex;align-items:center;justify-content:space-between;
    gap:1rem;padding:1.5rem 2.4rem 0}
  .reg-tel{color:var(--cream);text-decoration:none;font-size:.7rem;
    letter-spacing:.18em;font-weight:600;white-space:nowrap;
    font-variant-numeric:lining-nums tabular-nums;transition:color .3s}
  .reg-tel:hover{color:var(--orange)}

  .reg-main{display:grid;grid-template-columns:1fr minmax(360px,420px);
    gap:3.5rem;align-items:center;padding:2.2rem 2.4rem;max-width:1280px;
    width:100%;margin:0 auto}
  .reg-say .wm-stack{font-size:calc(clamp(2.1rem,5.4vw,4.1rem) / var(--wm-cap))}
  .reg-tag{font-family:var(--display);font-size:clamp(1rem,2vw,1.5rem);
    letter-spacing:.04em;color:rgba(var(--cream-rgb),.95);margin-top:1.1rem;
    text-shadow:0 1px 16px rgba(0,0,0,.6)}
  .reg-soon{display:inline-flex;align-items:center;gap:.9rem;color:var(--cream);
    font-size:.72rem;font-weight:600;letter-spacing:.24em;margin-top:1.1rem;
    text-shadow:0 1px 14px rgba(0,0,0,.8)}
  .reg-soon::before{content:"";flex:0 0 40px;height:2px;background:var(--orange)}
  .reg-line{color:rgba(var(--cream-rgb),.9);max-width:40ch;margin-top:1.3rem;
    font-size:.98rem;text-shadow:0 1px 14px rgba(0,0,0,.6)}

  /* the card puts the cream surface tokens back, so the form, the labels and
     the button look exactly as they do on the main site */
  .reg-card{--fg:var(--ink);
    --fg-70:rgba(var(--ink-rgb),.74);
    --fg-45:rgba(var(--ink-rgb),.54);
    --hair:rgba(var(--deep-rgb),.22);
    --accent:var(--burnt); --em:var(--deep);
    --btn-on-accent:var(--cream); --btn-hover-bg:var(--deep); --btn-hover-fg:var(--cream);
    color:var(--fg);background:var(--cream);padding:1.9rem 1.9rem 1.6rem;
    box-shadow:0 30px 70px -30px rgba(0,0,0,.6)}
  .reg-card h2{font-size:1.32rem;line-height:1.2}
  .reg-card .label{color:var(--accent);display:block;margin-bottom:.55rem;font-size:.6rem}
  .reg-card form{gap:.85rem;max-width:none;margin-top:1.25rem}
  .reg-card label{font-size:.58rem;letter-spacing:.18em;margin-bottom:.32rem}
  .reg-card input{padding:.68rem .8rem;font-size:.9rem}
  .reg-card .btn{width:100%;justify-content:center;padding:.92rem 1rem}
  .reg-card .form-done{margin-top:1.25rem;padding:1.4rem;max-width:none}
  .reg-fine{font-size:.7rem;line-height:1.55;color:var(--fg-70);margin-top:.85rem}
  .reg-fine a{color:var(--fg);border-bottom:1px solid var(--accent);
    text-decoration:none;padding-bottom:.08rem;white-space:nowrap}
  .reg-fine a:hover{color:var(--accent)}

  .reg-meta{display:flex;align-items:center;justify-content:space-between;gap:1rem;
    flex-wrap:wrap;padding:0 2.4rem 1rem;max-width:1280px;width:100%;margin:0 auto}
  .reg-dots{display:flex;gap:.45rem}
  .reg-dots button{width:26px;height:3px;padding:0;border:0;cursor:pointer;
    background:rgba(var(--cream-rgb),.3);transition:background .3s}
  .reg-dots button[aria-selected="true"]{background:var(--orange)}
  .reg-cap{color:rgba(var(--cream-rgb),.62);text-align:right}

  .reg-foot{display:flex;align-items:center;gap:2.6rem;flex-wrap:wrap;
    padding:.9rem 2.4rem 1.1rem;border-top:1px solid rgba(var(--cream-rgb),.16);
    background:rgba(var(--deep-2-rgb),.86);backdrop-filter:blur(6px)}
  .reg-lock{display:flex;align-items:center;gap:.8rem}
  .reg-lock small{font-size:.52rem;letter-spacing:.22em;text-transform:uppercase;
    color:rgba(var(--cream-rgb),.55);font-weight:600;white-space:nowrap}
  .reg-lock img{height:17px;width:auto;opacity:.92;display:block}
  .reg-lock img.tall{height:25px}
  .reg-legal{margin-left:auto;font-size:.52rem;letter-spacing:.06em;color:rgba(var(--cream-rgb),.4)}

  /* the two review switchers sit fixed at the bottom left; keep the lockups
     and, on a phone, the last of the page clear of them */
  @media(min-width:861px){.reg-foot{padding-left:190px}}
  .reg-note{color:var(--fg-45);letter-spacing:.06em;text-transform:uppercase;font-size:.58rem;margin-top:.7rem}
  @media(max-width:860px){
    .reg{grid-template-rows:auto auto auto auto;padding-bottom:0}
    .reg-main{grid-template-columns:1fr;gap:1.2rem;padding:1rem 1.4rem 1.2rem}
    .reg-say .wm-stack{font-size:calc(1.9rem / var(--wm-cap))}
    .reg-tag{margin-top:.7rem;font-size:1.05rem}
    .reg-soon{margin-top:.7rem;font-size:.66rem}
    .reg-line{max-width:none;margin-top:.8rem;font-size:.9rem}
    .reg-card{padding:1.3rem 1.25rem 1.2rem}
    .reg-card h2{font-size:1.2rem}
    .reg-card form{gap:.6rem;margin-top:.9rem}
    .reg-card label{margin-bottom:.24rem}
    .reg-card input{padding:.56rem .7rem}
    .reg-card .btn{padding:.8rem 1rem}
    .reg-fine{margin-top:.6rem}
    .reg-bar{padding:1rem 1.4rem 0}
    .reg-meta{padding:0 1.4rem .7rem}
    .reg-cap{text-align:left;flex:1 0 100%}
    .reg-foot{gap:1.2rem;padding:.9rem 1.4rem 1rem}
    /* review controls: out of the fixed corner, into the flow under the
       footer, so nothing sits on top of the intake on a phone */
    .reg-page .pal,.reg-page .fsw{position:static;display:inline-flex;margin:.8rem 0 0 1.4rem;
      box-shadow:none;max-width:calc(100vw - 2.8rem)}
    .reg-page .fsw{display:block;margin-bottom:1.2rem}
    .reg-page .fsw-body{max-height:none}
  }
  @media(prefers-reduced-motion:reduce){.reg-shot{transition:none}}
'''


# ==========================================================================
#  The body
# ==========================================================================

BODY = '''<div class="pmt-preview" aria-hidden="true"></div>
<div class="reg tone-deep" id="top">
  <div class="reg-bg" aria-hidden="true">
    <img class="reg-shot is-on" src="{{DU_3}}" alt="">
    <img class="reg-shot" src="{{DU_24}}" alt="">
    <img class="reg-shot" src="{{DU_7}}" alt="">
  </div>
  <div class="reg-scrim" aria-hidden="true"></div>

  <header class="reg-bar">
    <a class="wordmark" href="#top" aria-label="1521, Luxury Rentals on Queen West">1521</a>
    <a class="reg-tel" href="tel:+14164519499">416.451.9499</a>
  </header>

  <main class="reg-main">
    <div class="reg-say">
      <span class="wm-stack" role="img" aria-label="1521">
        <span class="wm-d" aria-hidden="true"><span>15</span></span>
        <span class="wm-d" aria-hidden="true"><span>21</span></span>
        <span class="wm-rule" aria-hidden="true"></span>
      </span>
      <p class="reg-tag">Luxury Rentals on Queen West</p>
      <p class="reg-soon">Coming Soon Summer 2027</p>
      <p class="reg-line">Ninety-five purpose-built residences at 1521 Queen Street West. Register for first access.</p>
    </div>

    <div class="reg-card">
      <span class="label">Registration</span>
      <h2>Register <em>Now.</em></h2>
      <form id="waitlist" onsubmit="event.preventDefault();this.style.display='none';document.getElementById('done').style.display='block';">
        <div><label for="fn">First Name</label><input id="fn" required></div>
        <div><label for="ln">Last Name</label><input id="ln" required></div>
        <div class="full"><label for="em">Email</label><input id="em" type="email" required></div>
        <div class="full"><label for="ph">Phone</label><input id="ph" type="tel"></div>
        <div class="full"><button class="btn btn-solid btn-mag" type="submit">Register Now</button></div>
      </form>
      <div class="form-done tone-deep" id="done"><b>Preview only.</b><br>This form is not connected yet and nothing was sent. Registrations will be captured once the page is live at the final domain.</div>
      <p class="reg-fine reg-note">Design preview. Registrations are not yet being captured.</p>
      <p class="reg-fine">Realtors are welcome to register on behalf of a client.</p>
      <p class="reg-fine">Prefer to talk? Call <a href="tel:+14164519499">416.451.9499</a>.</p>
    </div>
  </main>

  <div class="reg-meta">
    <div class="reg-dots" id="regdots" role="tablist" aria-label="Renderings">
      <button type="button" role="tab" aria-selected="true" aria-label="Rendering 1 of 3"></button>
      <button type="button" role="tab" aria-selected="false" aria-label="Rendering 2 of 3"></button>
      <button type="button" role="tab" aria-selected="false" aria-label="Rendering 3 of 3"></button>
    </div>
    <p class="reg-cap ph-cap">Concept renderings. Photography to come.</p>
  </div>

  <footer class="reg-foot">
    <span class="reg-lock"><small>A Development By</small>
      <a href="https://www.bsargroup.com" target="_blank" rel="noopener noreferrer"><img src="{{DU_25}}" alt="BS&#228;R Group of Companies"></a></span>
    <span class="reg-lock"><small>Leasing Management By</small>
      <a href="https://www.propertymanagementto.com" target="_blank" rel="noopener noreferrer"><img class="tall" src="{{DU_26}}" alt="PMT Property Management Toronto"></a></span>
    <span class="reg-legal">Design and content copyright 2026 Property Management Toronto Inc. Preview.</span>
  </footer>
</div>

'''


# ==========================================================================
#  The only script this page needs
# ==========================================================================

REG_JS = '''<script>
/* Markup 3, compressed. Claire asked for a rendering and photography
   carousel; on a one-screen intake page that is the background itself.
   Three renders, a six second hold, three dots to drive it by hand. A
   reader who prefers reduced motion gets the first render and the dots. */
(function(){
  var shots = [].slice.call(document.querySelectorAll('.reg-shot'));
  var dots = [].slice.call(document.querySelectorAll('#regdots button'));
  if(shots.length < 2 || dots.length !== shots.length) return;
  var i = 0, timer = null;
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function show(n){
    i = (n + shots.length) % shots.length;
    shots.forEach(function(s, k){ s.classList.toggle('is-on', k === i); });
    dots.forEach(function(d, k){ d.setAttribute('aria-selected', k === i ? 'true' : 'false'); });
  }
  function play(){
    if(reduced) return;
    clearInterval(timer);
    timer = setInterval(function(){
      if(!document.hidden) show(i + 1);
    }, 6000);
  }
  dots.forEach(function(d, k){
    d.addEventListener('click', function(){ show(k); play(); });
  });
  show(0);
  play();

  /* the magnetic pull on the submit button, as on the main site */
  var fine = matchMedia('(hover:hover) and (pointer:fine)').matches;
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
</script>
'''


def main():
    if not SRC.exists():
        raise SystemExit("apply_register: %s missing. Run tools/apply_v3.py first." % SRC)
    src = SRC.read_text(encoding="utf-8")

    # ---- the pieces v3 lends this page ----------------------------------
    if src.count(HEAD_END) != 1:
        raise SystemExit("apply_register: head marker appears %d times" % src.count(HEAD_END))
    head = src[:src.index(HEAD_END) + len(HEAD_END)]
    switchers = take(src, FSW_START, "\n<script>", "switcher markup", include_end=False)
    pal_js = take(src, PAL_JS, "</script>", "palette switcher js")
    fsw_js = take(src, FSW_JS, "</script>", "font switcher js")

    # ---- head edits ------------------------------------------------------
    for old, new, label in ((OLD_TITLE, NEW_TITLE, "title"),
                            (OLD_DESC, NEW_DESC, "description"),
                            (OLD_LD_DESC, NEW_LD_DESC, "json-ld description")):
        if head.count(old) != 1:
            raise SystemExit("apply_register: %s: expected 1, found %d"
                             % (label, head.count(old)))
        head = head.replace(old, new)

    # ---- the one-screen stylesheet --------------------------------------
    if head.count("\n</style>") != 1:
        raise SystemExit("apply_register: cannot find the end of the stylesheet")
    head = head.replace("\n</style>", "\n" + REG_CSS + "</style>")
    head = head.replace("<script>document.documentElement.className += ' js';</script>",
                        "<script>document.documentElement.className += ' js';"
                        "document.addEventListener('DOMContentLoaded',function(){"
                        "document.body.classList.add('reg-page');});</script>")

    h = head + "\n" + BODY + switchers + "\n" + pal_js + "\n\n" + fsw_js + "\n\n" + REG_JS

    # ---- guards ----------------------------------------------------------
    for pat in (r"[Tt]he 501", r"THE 501", r"Premium Rentals", r"Parkdale House",
                r"\$[0-9]", r"answered live", r"24 hours", r"24/7", r"follow up within"):
        m = re.search(pat, h)
        if m:
            raise SystemExit("apply_register: %r survived at %d: ...%s..."
                             % (m.group(0), m.start(), h[max(0, m.start() - 90):m.start() + 90]))

    body_only = re.sub(r"<script\b[^>]*>.*?</script>", "", h[h.rindex("</style>"):], flags=re.S)
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
    for need in ('id="fn"', 'id="ln"', 'id="em"', 'id="ph"', 'id="waitlist"',
                 'id="done"', 'class="wm-stack"', 'id="regdots"', 'reg-note',
                 'Preview only.',
                 "Coming Soon Summer 2027", "bsargroup.com", "propertymanagementto.com"):
        if need not in body_only:
            raise SystemExit("apply_register: %s is missing" % need)

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(h, encoding="utf-8")
    bad = [(i, c) for i, c in enumerate(h) if ord(c) > 127]
    if bad:
        raise SystemExit("apply_register: %d non-ASCII characters in output" % len(bad))
    print("apply_register: wrote %s (%.1f KB)" % (OUT.relative_to(ROOT), len(h.encode()) / 1024))
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
