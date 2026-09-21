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

  .reg-bar{display:flex;align-items:center;justify-content:space-between;gap:1rem;
    padding:1.4rem 2.4rem 0;max-width:1280px;width:100%;margin:0 auto}
  .reg-bar .wordmark{color:var(--deep)}
  .reg-bar .wordmark:hover{color:var(--accent)}
  .reg-tel{color:var(--deep);text-decoration:none;font-size:.7rem;
    letter-spacing:.18em;font-weight:600;white-space:nowrap;
    font-variant-numeric:lining-nums tabular-nums;transition:color .3s}
  .reg-tel:hover{color:var(--accent)}

  .reg-main{flex:1 0 auto;display:grid;grid-template-columns:minmax(340px,480px) 1fr;
    gap:4.5rem;align-items:start;padding:2.2rem 2.4rem 3rem;max-width:1280px;
    width:100%;margin:0 auto}

  /* the mark, on cream: deep blue digits, burnt orange bar */
  .reg-say .wm-stack{font-size:calc(clamp(2.2rem,4.6vw,3.6rem) / var(--wm-cap));color:var(--deep)}
  .reg-tag{font-family:var(--display);font-size:clamp(1.05rem,1.8vw,1.4rem);
    letter-spacing:.04em;color:var(--deep);margin-top:1rem}
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
  .gal-frame{position:relative;aspect-ratio:4/3;overflow:hidden;background:var(--deep-2);
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
    font-weight:500;margin:0}
  .gal-dots{display:flex;gap:.4rem;flex:0 0 auto}
  .gal-dots button{width:22px;height:3px;padding:0;border:0;cursor:pointer;
    background:rgba(var(--deep-rgb),.22);transition:background .3s}
  .gal-dots button[aria-selected="true"]{background:var(--accent)}
  .gal-note{font-size:.6rem;letter-spacing:.04em;color:var(--fg-45);margin:.6rem 0 0}

  /* the blue credit band at the foot */
  .reg-foot{display:flex;align-items:center;gap:2.6rem;flex-wrap:wrap;
    padding:1.1rem 2.4rem 1.2rem;background:var(--deep-2);color:var(--cream)}
  .reg-foot-in{display:flex;align-items:center;gap:2.6rem;flex-wrap:wrap;
    max-width:1280px;width:100%;margin:0 auto}
  .reg-lock{display:flex;align-items:center;gap:.8rem}
  .reg-lock small{font-size:.52rem;letter-spacing:.22em;text-transform:uppercase;
    color:rgba(var(--cream-rgb),.55);font-weight:600;white-space:nowrap}
  .reg-lock img{height:17px;width:auto;opacity:.92;display:block}
  .reg-lock img.tall{height:25px}
  .reg-legal{margin-left:auto;font-size:.52rem;letter-spacing:.06em;color:rgba(var(--cream-rgb),.4)}
  /* the two review switchers move to the bottom right on this page, so they
     never sit over the form column; the band keeps clear of them */
  @media(min-width:861px){
    .reg-page .pal,.reg-page .fsw{left:auto;right:1rem}
    .reg-foot-in{padding-right:190px}
  }

  @media(max-width:1080px){
    .reg-main{grid-template-columns:minmax(320px,440px) 1fr;gap:3rem}
  }
  @media(max-width:860px){
    .reg-bar{padding:1rem 1.25rem 0}
    .reg-main{grid-template-columns:1fr;gap:1.8rem;padding:1.2rem 1.25rem 2rem}
    .reg-say .wm-stack{font-size:calc(2rem / var(--wm-cap))}
    .reg-tag{margin-top:.7rem;font-size:.98rem;letter-spacing:.03em}
    .reg-soon{margin-top:.7rem;font-size:.64rem}
    .reg-line{max-width:none;margin-top:.8rem;font-size:.92rem}
    .reg-form{margin-top:1.5rem;padding-top:1.3rem}
    .reg-form h2{font-size:1.35rem}
    .reg-form form{gap:.7rem;margin-top:1rem}
    .reg-form label{margin-bottom:.24rem}
    .reg-form input{padding:.7rem .8rem;font-size:1rem}
    .reg-form .btn{padding:.9rem 1rem}
    .reg-gal{position:static;padding:.6rem}
    .gal-btn{width:36px;height:36px}
    .reg-foot{padding:1rem 1.25rem 1.1rem}
    .reg-foot-in{gap:1.1rem}
    .reg-legal{margin-left:0;flex:1 0 100%}
    /* review controls: out of the fixed corner, into the flow under the
       band, so nothing sits on top of the intake on a phone */
    .reg-page .pal,.reg-page .fsw{position:static;display:inline-flex;margin:.8rem 0 0 1.25rem;
      box-shadow:none;max-width:calc(100vw - 2.5rem)}
    .reg-page .fsw{display:block;margin-bottom:1.2rem}
    .reg-page .fsw-body{max-height:none}
  }
  @media(prefers-reduced-motion:reduce){.gal-frame img{transition:none}}
'''


# ==========================================================================
#  The body
# ==========================================================================

# Six slots. The photography due 25 September replaces slots 4 to 6 first.
SLIDES = [
    ("{{DU_3}}",  "1521 Queen Street West. Concept rendering."),
    ("{{DU_12}}", "The streetcar at the front door. Concept rendering."),
    ("{{DU_24}}", "The entrance on Queen Street West. Concept rendering."),
    ("{{DU_18}}", "Queen West at street level. Illustrative image."),
    ("{{DU_20}}", "Parks and markets nearby. Illustrative image."),
    ("{{DU_22}}", "The waterfront, minutes south. Illustrative image."),
]


def slides_html():
    imgs = []
    dots = []
    for i, (tok, cap) in enumerate(SLIDES):
        on = " is-on" if i == 0 else ""
        imgs.append('    <img class="gal-shot%s" src="%s" alt="%s" data-cap="%s" draggable="false">'
                    % (on, tok, cap.replace('"', ""), cap))
        dots.append('      <button type="button" role="tab" aria-selected="%s" aria-label="Image %d of %d"></button>'
                    % ("true" if i == 0 else "false", i + 1, len(SLIDES)))
    return "\n".join(imgs), "\n".join(dots)


IMGS, DOTS = slides_html()

BODY = '''<div class="pmt-preview" aria-hidden="true"></div>
<div class="reg" id="top">

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

      <div class="reg-form">
        <span class="label">Registration</span>
        <h2>Register <em>Now.</em></h2>
        <form id="waitlist" onsubmit="event.preventDefault();this.style.display='none';document.getElementById('done').style.display='block';">
          <div><label for="fn">First Name</label><input id="fn" name="fn" autocomplete="given-name" required></div>
          <div><label for="ln">Last Name</label><input id="ln" name="ln" autocomplete="family-name" required></div>
          <div class="full"><label for="em">Email</label><input id="em" name="em" type="email" autocomplete="email" inputmode="email" required></div>
          <div class="full"><label for="ph">Phone</label><input id="ph" name="ph" type="tel" autocomplete="tel" inputmode="tel"></div>
          <div class="full"><button class="btn btn-solid btn-mag" type="submit">Register Now</button></div>
        </form>
        <div class="form-done tone-deep" id="done"><b>Preview only.</b><br>This form is not connected yet and nothing was sent. Registrations will be captured once the page is live at the final domain.</div>
        <p class="reg-fine reg-note">Design preview. Registrations are not yet being captured.</p>
        <p class="reg-fine">Realtors are welcome to register on behalf of a client.</p>
        <p class="reg-fine">Prefer to talk? Call <a href="tel:+14164519499">416.451.9499</a>.</p>
      </div>
    </div>

    <aside class="reg-gal" id="gal" aria-label="Images">
      <div class="gal-frame" id="galframe">
''' + IMGS + '''
        <button type="button" class="gal-btn prev" id="galprev" aria-label="Previous image"></button>
        <button type="button" class="gal-btn next" id="galnext" aria-label="Next image"></button>
      </div>
      <div class="gal-meta">
        <p class="gal-cap" id="galcap">''' + SLIDES[0][1] + '''</p>
        <div class="gal-dots" id="galdots" role="tablist" aria-label="Choose an image">
''' + DOTS + '''
        </div>
      </div>
      <p class="gal-note">Concept renderings and illustrative images. Photography to follow.</p>
    </aside>
  </main>

  <footer class="reg-foot">
    <div class="reg-foot-in">
      <span class="reg-lock"><small>A Development By</small>
        <a href="https://www.bsargroup.com" target="_blank" rel="noopener noreferrer"><img src="{{DU_25}}" alt="BS&#228;R Group of Companies"></a></span>
      <span class="reg-lock"><small>Leasing Management By</small>
        <a href="https://www.propertymanagementto.com" target="_blank" rel="noopener noreferrer"><img class="tall" src="{{DU_26}}" alt="PMT Property Management Toronto"></a></span>
      <span class="reg-legal">Design and content copyright 2026 Property Management Toronto Inc. Preview.</span>
    </div>
  </footer>
</div>

'''


# ==========================================================================
#  The only script this page needs
# ==========================================================================

REG_JS = '''<script>
/* Image carousel in the call-out box: six slides, a five second hold,
   arrows, dots, a swipe on touch, pause while the pointer is over it. A
   reader who prefers reduced motion gets the first image and the controls. */
(function(){
  var frame = document.getElementById('galframe');
  var shots = [].slice.call(document.querySelectorAll('.gal-shot'));
  var dots = [].slice.call(document.querySelectorAll('#galdots button'));
  var cap = document.getElementById('galcap');
  if(!frame || shots.length < 2 || dots.length !== shots.length) return;
  var i = 0, timer = null, hover = false;
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function show(n){
    i = (n + shots.length) % shots.length;
    shots.forEach(function(s, k){ s.classList.toggle('is-on', k === i); });
    dots.forEach(function(d, k){ d.setAttribute('aria-selected', k === i ? 'true' : 'false'); });
    if(cap) cap.textContent = shots[i].getAttribute('data-cap') || '';
  }
  function play(){
    clearInterval(timer);
    if(reduced) return;
    timer = setInterval(function(){
      if(!document.hidden && !hover) show(i + 1);
    }, 5000);
  }
  dots.forEach(function(d, k){
    d.addEventListener('click', function(){ show(k); play(); });
  });
  document.getElementById('galprev').addEventListener('click', function(){ show(i - 1); play(); });
  document.getElementById('galnext').addEventListener('click', function(){ show(i + 1); play(); });
  frame.addEventListener('pointerenter', function(){ hover = true; });
  frame.addEventListener('pointerleave', function(){ hover = false; });

  /* swipe: a horizontal move of 40 px or more between pointer down and up */
  var x0 = null;
  frame.addEventListener('pointerdown', function(e){ x0 = e.clientX; });
  frame.addEventListener('pointerup', function(e){
    if(x0 === null) return;
    var dx = e.clientX - x0; x0 = null;
    if(Math.abs(dx) < 40) return;
    show(dx < 0 ? i + 1 : i - 1); play();
  });
  frame.addEventListener('pointercancel', function(){ x0 = null; });

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

    # ---- the stylesheet --------------------------------------------------
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
                r"\$[0-9]", r"answered live", r"24 hours", r"24/7", r"follow up within",
                r"resident portal", r"Emergency", r"leased and managed by"):
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
                 'id="done"', 'class="wm-stack"', 'id="gal"', 'id="galdots"', 'id="galprev"',
                 'reg-note', 'Preview only.', 'class="reg-foot"',
                 "Coming Soon Summer 2027", "bsargroup.com", "propertymanagementto.com"):
        if need not in body_only:
            raise SystemExit("apply_register: %s is missing" % need)
    if body_only.count('class="gal-shot') != len(SLIDES):
        raise SystemExit("apply_register: expected %d slides" % len(SLIDES))

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(h, encoding="utf-8")
    bad = [(i, c) for i, c in enumerate(h) if ord(c) > 127]
    if bad:
        raise SystemExit("apply_register: %d non-ASCII characters in output" % len(bad))
    print("apply_register: wrote %s (%.1f KB)" % (OUT.relative_to(ROOT), len(h.encode()) / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
