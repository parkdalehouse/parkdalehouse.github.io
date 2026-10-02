"""
v3 round four, 2 October 2026: the logo system, Jacob Cote's photography and
the copy decisions from Claire's register pins, carried onto the landing page.

Sources
  Claire's eight register pins of 25 September (n8n execution 52221): the full
    wordmark instead of a bare 1521, "Move-In Summer 2027", "Boutique
    residences at 1521 Queen Street West.", phone number TBC until BSaR's
    forwarding line exists, image and move-in disclaimer in small print.
  Her logo selects of 29 September: C23 primary, C24 stacked, C05 badge, C02
    favicon, "intended to be used as a system". Drawn inline from
    brand/1521_marks.json by tools/logo_1521.py.
  The 29 September call: Blue 072 C is locked, so the palette dot gives way to
    a logo control (primary, badge, stacked) in the same corner.
  Jacob Cote's final neighbourhood set, served from /photos/ with his credit.

Two neighbourhood cards (Sorauren Park, High Park) keep their illustrative
images: the set has no frame of either, and the footer says so.

Called last from tools/apply_v3.py. tools/apply_register.py reads the head this
module writes, so its OLD_DESC and OLD_LD_DESC must match NEW_DESC and NEW_LD.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from logo_1521 import inline, favicon_links  # noqa: E402

PH = "../photos/1521-queen-st-jacobcotephotography-web-%d.jpg"


def logos(label="1521 Queen West"):
    return (inline("C23", "lg-c23", label) + inline("C05", "lg-c05", label)
            + inline("C24", "lg-c24", label))


NEW_DESC = ('<meta name="description" content="1521 at 1521 Queen Street West. Luxury rentals '
            'on Queen West, Toronto: boutique studio to three bedroom residences, steps from the '
            '501 streetcar, Roncesvalles Village and the waterfront. Move-in Summer 2027.">')
NEW_LD = ('  "description": "Luxury rentals on Queen West. Boutique studio to three bedroom '
          'residences at 1521 Queen Street West, Toronto, steps from the 501 streetcar, '
          'Roncesvalles Village and the waterfront. Move-in Summer 2027.",\n')

R4_CSS = '''
  /* ---- round four: the 1521 logo system (BSaR selects, 29 September) ----
     Every mark is inline SVG with classed parts. On the dark grounds of this
     page the mark is cream with the orange accent; the review control swaps
     which mark of the system shows: C23 primary, C05 badge, C24 stacked. */
  :root{--lg-num:var(--cream);--lg-word:var(--cream);--lg-acc:#FD5100}
  .lg .lg-n{fill:var(--lg-num)}
  .lg .lg-w{fill:var(--lg-word)}
  .lg .lg-a{fill:var(--lg-acc)}
  .lg .lg-k{fill:var(--cream)}
  .lg .lg-r1{stroke:var(--lg-num)}
  .lg .lg-r2{stroke:var(--lg-acc)}
  .lgx{display:block;line-height:0}
  .lgx .lg{display:none;height:auto}
  .lgx .lg-c23{display:block}
  :root[data-logo="c05"] .lgx .lg-c23,:root[data-logo="c24"] .lgx .lg-c23{display:none}
  :root[data-logo="c05"] .lgx .lg-c05,:root[data-logo="c24"] .lgx .lg-c24{display:block}
  .nav-logo{color:inherit;transition:opacity .3s}
  .nav-logo:hover{opacity:.8}
  .nav-logo .lg-c23{width:66px}
  .nav-logo .lg-c05{width:52px}
  .nav-logo .lg-c24{width:30px}
  nav.scrolled .nav-logo .lg-c23{width:56px}
  .hero-logo{margin-bottom:1.6rem;opacity:0;animation:fadeUp 1.1s var(--ease) .1s forwards}
  .hero-logo .lg{filter:drop-shadow(0 2px 18px rgba(10,4,97,.55))}
  .hero-logo .lg-c23{width:clamp(190px,22vw,300px)}
  .hero-logo .lg-c05{width:clamp(170px,18vw,240px)}
  .hero-logo .lg-c24{width:clamp(96px,10vw,140px)}
  @keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
  .foot-logo .lg-c23{width:120px}
  .foot-logo .lg-c05{width:104px}
  .foot-logo .lg-c24{width:58px}
  .foot-legal a{color:inherit;border-bottom:1px solid rgba(var(--cream-rgb),.3);text-decoration:none}
  @media(max-width:860px){
    .nav-logo .lg-c23{width:54px}
    .hero-logo{margin-bottom:1.1rem}
  }
  @media(prefers-reduced-motion:reduce){.hero-logo{animation:none;opacity:1}}
  /* the logo control takes the palette dot's corner */
  .lsw{flex-wrap:wrap;border-radius:16px;max-width:calc(100vw - 2rem)}
  .lsw button{width:auto;height:auto;border-radius:999px;padding:.34rem .6rem;
    background:transparent;color:rgba(var(--cream-rgb),.86);border:1px solid rgba(var(--cream-rgb),.28);
    font:600 .56rem/1 var(--sans);letter-spacing:.06em}
  .lsw button:hover{transform:none;background:rgba(var(--cream-rgb),.12)}
  .lsw button[aria-pressed="true"]{background:var(--cream);color:var(--deep);box-shadow:none;transform:none}
'''

LSW = '''<div class="pal lsw" role="group" aria-label="Logo options for review">
  <span class="pal-lbl">Logo</span>
  <button type="button" data-logo="c23" aria-pressed="true" title="C23 primary wordmark">Primary</button>
  <button type="button" data-logo="c05" aria-pressed="false" title="C05 double ring badge">Badge</button>
  <button type="button" data-logo="c24" aria-pressed="false" title="C24 stacked cut">Stacked</button>
</div>'''

LSW_JS = '''<script>
/* Logo control. ?logo=c23|c05|c24 in the address wins and is not saved; a
   click is remembered per browser. Blue 072 C is locked, so no palette. */
(function(){
  var KEY = 'q1521_logo_v3';
  var VALID = {'c23':1, 'c05':1, 'c24':1};
  var root = document.documentElement;
  root.setAttribute('data-palette', 'B');
  var btns = [].slice.call(document.querySelectorAll('.lsw [data-logo]'));
  function set(v, persist){
    if(!VALID[v]) v = 'c23';
    root.setAttribute('data-logo', v);
    btns.forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.logo === v ? 'true' : 'false'); });
    if(persist){ try { localStorage.setItem(KEY, v); } catch(e){} }
  }
  var q = (location.search.match(/[?&]logo=([a-z0-9-]+)/) || [])[1];
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch(e){}
  set(q || saved || 'c23', false);
  btns.forEach(function(b){ b.addEventListener('click', function(){ set(b.dataset.logo, true); }); });
})();
</script>'''

FOOT_LEGAL = '''  <div class="foot-legal">
    Demonstration concept prepared by Property Management Toronto Inc. for BS&#228;R Group of Companies.
    Renderings are artist's concepts and may differ from the completed building; exterior renderings courtesy of
    BS&#228;R Group / Core Architects. Neighbourhood images show the surrounding area, not the property; the
    Sorauren Park and High Park images are illustrative until photography of each is chosen.
    Images by: <a href="https://jacobcotephotography.com" target="_blank" rel="noopener noreferrer">Jacob C&ocirc;t&eacute; Photography</a>.
    Partner marks illustrate a proposed resident-perks program; partner perks are proposed programs pending final agreements.
    The PRESTO program is provided through the City of Toronto and is subject to program terms. Suite mix, floor plan
    types, rents and the move-in date are not final and are subject to change. E.&amp;O.E.
  </div>'''


def card(n, alt, title, walk, text, delay):
    p = '<p>%s</p>' % text if text else ''
    return ('      <div class="hood-card reveal-img" style="--d:%s">\n'
            '        <div class="hood-shot"><img src="%s" alt="%s" loading="lazy"></div>\n'
            '        <div class="hood-txt"><b>%s</b><span class="walk">%s</span>%s</div>\n'
            '      </div>' % (delay, PH % n, alt, title, walk, p))


def run(h, sub, resub, cut_block):
    # ---- head ------------------------------------------------------------
    h = resub(h, r'<meta name="description" content="1521 at 1521 Queen Street West\.[^"]*">',
              NEW_DESC, 1, "r4 meta description")
    h = resub(h, r'  "description": "Luxury rentals on Queen West\. Ninety-five[^\n]*\n',
              NEW_LD, 1, "r4 json-ld description")
    h = sub(h, '  "numberOfAccommodationUnits": 95,\n', '', 1, "r4 json-ld unit count")
    h = sub(h, '  "telephone": "+1-416-451-9499",\n', '', 1, "r4 json-ld phone (pin 7)")
    h = sub(h, '<title>1521 | Luxury Rentals on Queen West</title>\n',
            '<title>1521 | Luxury Rentals on Queen West</title>\n' + favicon_links() + '\n',
            1, "r4 favicon")

    # ---- css -------------------------------------------------------------
    h = sub(h, '\n</style>', '\n' + R4_CSS + '</style>', 1, "r4 css")

    # ---- nav: the full wordmark, no phone --------------------------------
    h = sub(h, '<nav id="nav" class="tone-deep">\n'
               '  <a class="wordmark" href="#top" aria-label="1521, Luxury Rentals on Queen West">1521</a>',
            '<nav id="nav" class="tone-deep">\n'
            '  <a class="nav-logo lgx" href="#top" aria-label="1521 Queen West, home">'
            + logos() + '</a>', 1, "r4 nav logo")
    h = sub(h, '    <a class="nav-tel" href="tel:+14164519499">416.451.9499</a>\n', '',
            1, "r4 nav phone")

    # ---- hero ------------------------------------------------------------
    h = sub(h, '''        <span class="wm-stack" role="img" aria-label="1521">
          <span class="wm-d" aria-hidden="true"><span>15</span></span>
          <span class="wm-d" aria-hidden="true"><span>21</span></span>
          <span class="wm-rule" aria-hidden="true"></span>
        </span>''', '        <span class="hero-logo lgx">' + logos() + '</span>', 1, "r4 hero logo")
    h = sub(h, '<p class="label hero-soon">Coming Soon Summer 2027</p>',
            '<p class="label hero-soon">Move-In Summer 2027</p>', 1, "r4 hero date")
    h = sub(h, '<p class="hero-sub">Ninety-five purpose-built residences at 1521 Queen Street West. ',
            '<p class="hero-sub">Boutique residences at 1521 Queen Street West. ', 1, "r4 hero line")
    h = sub(h, '        <a class="hero-tel" href="tel:+14164519499">Or call <b>416.451.9499</b></a>\n',
            '', 1, "r4 hero phone")

    # ---- neighbourhood: Jacob's frames where the set has the place -------
    h = resub(h, r'      <div class="hood-card reveal-img" style="--d:\.05s">\n'
                 r'        <div class="hood-shot"><img src="\{\{DU_18\}\}"[^\n]*\n'
                 r'        (<div class="hood-txt"><b>Your stop on Queen West</b>[^\n]*)\n'
                 r'      </div>',
              lambda m: ('      <div class="hood-card reveal-img" style="--d:.05s">\n'
                         '        <div class="hood-shot"><img src="%s" alt="A TTC streetcar passing a '
                         'brick corner building in the neighbourhood" loading="lazy"></div>\n'
                         '        %s\n      </div>' % (PH % 10, m.group(1))),
              1, "r4 streetcar card")
    h = resub(h, r'      <div class="hood-card is-ph reveal-img" style="--d:\.1s">\n.*?\n      </div>\n'
                 r'(?=      <div class="hood-card reveal-img" style="--d:\.15s">\n'
                 r'        <div class="hood-shot"><img src="\{\{DU_20\}\})',
              card(7, "A painted Parkdale mural on a brick wall", "Parkdale", "All around you",
                   "Murals, independent shops, cafes and restaurants.", ".1s") + "\n",
              1, "r4 parkdale card", flags=__import__("re").S)
    h = resub(h, r'<img src="\{\{DU_22\}\}" alt="[^"]*">',
              '<img src="%s" alt="The Sunnyside pavilion across the water at sunset" loading="lazy">'
              % (PH % 13), 1, "r4 sunnyside card")
    h = resub(h, r'<img src="\{\{DU_23\}\}" alt="[^"]*">',
              '<img src="%s" alt="A Queen West fruit market with a streetcar at the curb" loading="lazy">'
              % (PH % 2), 1, "r4 queen west card")

    # ---- perks: the re-rendered exterior Claire chose ---------------------
    h = sub(h, '<img src="{{DU_12}}" alt="Illustrative image: a TTC streetcar passing the front of '
               'the building on Queen Street at dusk">',
            '<img src="../photos/1521-exterior-streetcar-r2.jpg" alt="Concept rendering: a TTC streetcar '
            'passing the front of 1521 on Queen Street West" loading="lazy">', 1, "r4 perks render")

    # ---- dates, contact, footer -----------------------------------------
    h = sub(h, '<span>Coming Soon <em>Summer 2027</em></span>',
            '<span>Move-In <em>Summer 2027</em></span>', 2, "r4 marquee date")
    h = sub(h, '<p class="label soon-line reveal" style="--d:.12s">Coming Soon Summer 2027</p>',
            '<p class="label soon-line reveal" style="--d:.12s">Move-In Summer 2027</p>', 1, "r4 contact date")
    h = sub(h, ' Prefer to talk? Call <a href="tel:+14164519499"><b>416.451.9499</b></a>.</p>',
            '</p>', 1, "r4 contact phone")
    h = sub(h, '''    <div>
      <a class="wordmark" href="#top" aria-label="1521, Luxury Rentals on Queen West">1521</a>''',
            '''    <div>
      <a class="foot-logo lgx" href="#top" aria-label="1521 Queen West, back to top">''' + logos() + '</a>',
            1, "r4 footer logo")
    h = sub(h, 'Toronto, Ontario M6R 1A5<br>Coming Soon Summer 2027</p>',
            'Toronto, Ontario M6R 1A5<br>Move-In Summer 2027</p>', 1, "r4 footer date")
    h = sub(h, '1521queenwest.ca<br><span class="ph-cap">Domain to be confirmed</span>',
            '<span class="ph-cap">Website address to be confirmed</span>', 1, "r4 footer domain")
    h = sub(h, '      <p><a href="tel:+14164519499">416.451.9499</a><br>\n', '      <p>',
            1, "r4 footer phone")
    h = resub(h, r'  <div class="foot-legal">\n.*?\n  </div>', FOOT_LEGAL, 1, "r4 footer legal",
              flags=__import__("re").S)

    # ---- review controls: logo replaces palette; no wordmark type row ------
    h = resub(h, r'<div class="pal" role="group" aria-label="Brand palette preview">.*?</div>',
              LSW, 1, "r4 logo control", flags=__import__("re").S)
    h = resub(h, r'<script>\n/\* Palette switcher\..*?</script>', LSW_JS, 1, "r4 logo control js",
              flags=__import__("re").S)
    h = resub(h, r'    <div class="fsw-row">\n      <span class="fsw-lbl">Wordmark</span>.*?\n    </div>\n',
              '', 1, "r4 drop wordmark type row", flags=__import__("re").S)

    # ---- guards ------------------------------------------------------------
    body = h[h.index("<body") if "<body" in h else h.index("</style>"):]
    for gone in ("Coming Soon", "Ninety-five", "451.9499", "4519499", 'class="wm-stack"',
                 'class="wordmark"', "{{DU_18}}", "{{DU_22}}", "{{DU_23}}", "{{DU_12}}",
                 "Neighbourhood photography to come"):
        if gone in body:
            raise SystemExit("v3_r4: %r is still on the page" % gone)
    for need in ("Move-In Summer 2027", "Boutique residences at 1521 Queen Street West.",
                 "jacobcotephotography.com", 'class="nav-logo lgx"', 'class="hero-logo lgx"',
                 'class="foot-logo lgx"', 'class="pal lsw"', "1521-exterior-streetcar-r2.jpg"):
        if need not in body:
            raise SystemExit("v3_r4: %r is missing" % need)
    return h
