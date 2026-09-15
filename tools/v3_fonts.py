#!/usr/bin/env python3
"""Typography layer of the v3 build. Imported by tools/apply_v3.py.

Tyler, 8 September: "the equivalent of a colour toggle with different fonts
available". Claire: show the combinations from the 28 August board.

The board lists wordmark faces (Instrument Sans, Montserrat, Futura, Poppins)
and text faces (Inter, Open Sans, DM Sans, Manrope, and Libre Baskerville as
the serif for subheadings). All of them are embedded and switchable in three
independent rows, so BSaR can try any combination on the live page.

Futura is not open licence and cannot be embedded, so Jost stands in for it
and the chip says so.

The whole page runs off three custom properties:

    --wordmark   the nav mark, the footer mark, the stacked hero mark
                 and the footer watermark
    --display    every heading and subheading, the hero tagline, the pull
                 quotes, the card titles
    --body       body copy, labels, nav items, form labels, buttons, chips

The old --serif and --sans simply alias --display and --body, so every rule
already written follows the switch with no further edits.

Wordmark geometry follows Route 1 of the identity routes sheet
(../Identity-1521/README.md), measured off BSaR's own drawing: tracking 0.11
cap, leading 1.232 cap, bar 0.797 cap wide by 0.042 cap thick, dropped 0.312
cap below the lower baseline. Those are cap-height units, so the mark has to
be normalised on cap height rather than font size, or it would change size
every time the face changes. Each face therefore carries its cap ratio and
its typographic ascent and descent, and the CSS works in cap units from there.
"""

# --------------------------------------------------------------------------
#  Faces. cap/asc/desc are fractions of the em, read off the built woff2 by
#  tools/build_fonts.py; every one of these fonts sets USE_TYPO_METRICS, so
#  asc and desc are the OS/2 typographic values the browser lays lines out on.
# --------------------------------------------------------------------------

STACKS = {
    "instrument":  '"Instrument Sans","Helvetica Neue",Helvetica,Arial,sans-serif',
    "montserrat":  '"Montserrat","Helvetica Neue",Helvetica,Arial,sans-serif',
    "jost":        '"Jost","Futura","Century Gothic",sans-serif',
    "poppins":     '"Poppins","Helvetica Neue",Helvetica,Arial,sans-serif',
    "baskerville": '"Libre Baskerville","Georgia","Times New Roman",serif',
    "dmsans":      '"DM Sans","Helvetica Neue",Helvetica,Arial,sans-serif',
    "inter":       '"Inter","Helvetica Neue",Helvetica,Arial,sans-serif',
    "opensans":    '"Open Sans","Helvetica Neue",Helvetica,Arial,sans-serif',
    "manrope":     '"Manrope","Helvetica Neue",Helvetica,Arial,sans-serif',
}

# Per face: (cap, baseline inset). Both are fractions of the em.
#
#   cap  ink height of the digit "1", read off the built woff2. The mark is
#        sized on this, so changing face changes the drawing and not the size.
#   bb   from the bottom of a line box set at 1.232 cap back up to the
#        baseline. The analytic value is (line-height - asc - desc)/2 + desc
#        from the OS/2 typographic metrics, but browsers round ascent and
#        descent to whole pixels before laying the line out, so these are the
#        values measured in the browser at hero size, which land the bar drop
#        on 0.312 cap exactly rather than 1.9 per cent under it.
METRICS = {
    "instrument":  (0.720, 0.08777),
    "montserrat":  (0.700, 0.07786),
    "jost":        (0.709, 0.09418),
    "poppins":     (0.723, 0.09598),
    "baskerville": (0.780, 0.13703),
    "dmsans":      (0.700, 0.09100),
}

WORDMARK_ROW = [
    ("instrument", "Instrument Sans"),
    ("montserrat", "Montserrat"),
    ("jost", "Jost (Futura style)"),
    ("poppins", "Poppins"),
    ("baskerville", "Libre Baskerville"),
]
DISPLAY_ROW = [
    ("baskerville", "Libre Baskerville"),
    ("instrument", "Instrument Sans"),
    ("manrope", "Manrope"),
    ("inter", "Inter"),
    ("opensans", "Open Sans"),
    ("dmsans", "DM Sans"),
]
BODY_ROW = [
    ("dmsans", "DM Sans"),
    ("inter", "Inter"),
    ("opensans", "Open Sans"),
    ("manrope", "Manrope"),
]

DEFAULTS = {"wm": "instrument", "dp": "baskerville", "bd": "dmsans"}


# --------------------------------------------------------------------------
#  @font-face for the faces the 28 August board adds
# --------------------------------------------------------------------------

ANCHOR_FACES = '''  @font-face{font-family:"DM Sans";src:url("{{FONT_DMI}}") format("woff2");
    font-weight:400;font-style:italic;font-display:swap}
'''

NEW_FACES = '''
  /* ---- the 28 August board, for the font switcher ----------------------
     Every face is Open Font Licence, subset and embedded here; nothing is
     fetched at run time. The three wordmark-only faces carry digits alone,
     because the wordmark variable never draws anything but 1521.
     Licences are in fonts/ beside the woff2 files. */
  @font-face{font-family:"Instrument Sans";src:url("{{FONT_IS}}") format("woff2");
    font-weight:400 700;font-style:normal;font-display:swap}
  @font-face{font-family:"Inter";src:url("{{FONT_INTER}}") format("woff2");
    font-weight:400 700;font-style:normal;font-display:swap}
  @font-face{font-family:"Open Sans";src:url("{{FONT_OS}}") format("woff2");
    font-weight:400 700;font-style:normal;font-display:swap}
  @font-face{font-family:"Manrope";src:url("{{FONT_MANROPE}}") format("woff2");
    font-weight:400 700;font-style:normal;font-display:swap}
  @font-face{font-family:"Montserrat";src:url("{{FONT_MONT}}") format("woff2");
    font-weight:400;font-style:normal;font-display:swap}
  @font-face{font-family:"Jost";src:url("{{FONT_JOST}}") format("woff2");
    font-weight:400;font-style:normal;font-display:swap}
  @font-face{font-family:"Poppins";src:url("{{FONT_POP400}}") format("woff2");
    font-weight:400;font-style:normal;font-display:swap}
  @font-face{font-family:"Poppins";src:url("{{FONT_POP600}}") format("woff2");
    font-weight:600 700;font-style:normal;font-display:swap}
'''


# --------------------------------------------------------------------------
#  :root
# --------------------------------------------------------------------------

OLD_ROOT_TYPE = '''    --serif:"Libre Baskerville","Georgia","Times New Roman",serif;
    --sans:"DM Sans","Helvetica Neue",Helvetica,Arial,sans-serif;'''

NEW_ROOT_TYPE = '''    /* three switchable roles. --serif and --sans are kept as aliases so
       every rule written against them follows the switch. */
    --wordmark:%s;
    --display:%s;
    --body:%s;
    --wm-cap:%.3f; --wm-bb:%.5f;
    --serif:var(--display);
    --sans:var(--body);''' % (
    STACKS[DEFAULTS["wm"]], STACKS[DEFAULTS["dp"]], STACKS[DEFAULTS["bd"]],
    METRICS[DEFAULTS["wm"]][0], METRICS[DEFAULTS["wm"]][1])


def _selector_block():
    out = []
    out.append("  /* font switcher: one attribute per row on <html> */")
    for key, _ in WORDMARK_ROW:
        cap, bb = METRICS[key]
        out.append('  :root[data-wm="%s"]{--wordmark:%s;--wm-cap:%.3f;--wm-bb:%.5f}'
                   % (key, STACKS[key], cap, bb))
    for key, _ in DISPLAY_ROW:
        out.append('  :root[data-dp="%s"]{--display:%s}' % (key, STACKS[key]))
    for key, _ in BODY_ROW:
        out.append('  :root[data-bd="%s"]{--body:%s}' % (key, STACKS[key]))
    return "\n".join(out)


# --------------------------------------------------------------------------
#  Wordmark, normalised on cap height so a face change does not change size
# --------------------------------------------------------------------------

OLD_WORDMARK = '''  .wordmark{font-family:var(--sans);font-weight:400;color:var(--cream);font-size:1.16rem;
    letter-spacing:.36em;text-decoration:none;white-space:nowrap;
    font-variant-numeric:lining-nums tabular-nums;transition:color .3s}
  .wordmark:hover{color:var(--accent)}
  .wm-stack{display:inline-block;font-family:var(--sans);font-weight:400;
    font-variant-numeric:lining-nums tabular-nums;letter-spacing:.02em;line-height:.9;
    color:var(--cream);text-decoration:none}
  .wm-stack .wm-d{display:block}
  .wm-stack .wm-rule{display:block;width:1.2ch;height:.042em;min-height:2px;
    background:var(--accent);margin:.36em auto 0}'''

NEW_WORDMARK = '''  /* -------------------- 1521 wordmark, Route 1 geometry -----------------
     Proportions measured off BSaR's own drawing and used by the identity
     routes sheet: tracking 0.11 cap, leading 1.232 cap, bar 0.797 cap wide,
     0.042 cap thick, dropped 0.312 cap below the lower baseline.

     Those are cap heights, not ems, so the mark is sized by cap height:
     font-size is the wanted cap divided by the face's cap ratio. Swapping
     the face then changes the drawing and nothing else.

     The bar sits below the second line box, so its margin has to give back
     the distance from the bottom of that box up to the baseline (--wm-bb)
     before dropping the 0.312 cap the drawing asks for. Both terms are
     per-face; see the METRICS table in tools/v3_fonts.py. */
  .wordmark{font-family:var(--wordmark);font-weight:400;color:var(--cream);
    font-size:calc(.812rem / var(--wm-cap));
    letter-spacing:calc(.51 * var(--wm-cap) * 1em);
    text-indent:calc(.51 * var(--wm-cap) * 1em);
    text-decoration:none;white-space:nowrap;
    font-variant-numeric:lining-nums tabular-nums;transition:color .3s}
  .wordmark:hover{color:var(--accent)}
  .wm-stack{display:inline-block;font-family:var(--wordmark);font-weight:400;
    font-variant-numeric:lining-nums tabular-nums;
    letter-spacing:calc(.11 * var(--wm-cap) * 1em);
    text-indent:calc(.11 * var(--wm-cap) * 1em);
    line-height:calc(1.232 * var(--wm-cap));
    text-align:center;color:var(--cream);text-decoration:none}
  .wm-stack .wm-d{display:block}
  .wm-stack .wm-rule{display:block;background:var(--accent);
    width:calc(.797 * var(--wm-cap) * 1em);
    height:calc(.042 * var(--wm-cap) * 1em);min-height:2px;
    margin:calc((.312 * var(--wm-cap) - var(--wm-bb)) * 1em) auto 0}'''

OLD_HERO_WM = '''  /* the stacked hero wordmark, at hero scale */
  .hero .wm-stack{font-size:clamp(3.6rem,10.5vw,8.2rem);letter-spacing:.015em}'''

NEW_HERO_WM = '''  /* the stacked hero wordmark. The clamp is the cap height, not the font
     size, so every face draws 15 over 21 at the same optical size. */
  .hero .wm-stack{font-size:calc(clamp(2.55rem,7.4vw,5.8rem) / var(--wm-cap))}'''

OLD_GIANT = '''  .foot-giant{font-family:var(--sans);font-weight:400;font-size:clamp(3.4rem,15vw,12rem);line-height:.82;'''
NEW_GIANT = '''  .foot-giant{font-family:var(--wordmark);font-weight:400;
    font-size:calc(clamp(2.4rem,10.5vw,8.4rem) / var(--wm-cap));line-height:.82;'''


# --------------------------------------------------------------------------
#  The switcher itself
# --------------------------------------------------------------------------

SWITCHER_CSS = '''
  /* ---- font switcher, a review aid like the palette dots ---------------
     Sits directly above the palette switcher, collapses to a single button
     so it never covers the page on a phone, and is hidden in print. It
     comes out with the palette switcher before launch. */
  .fsw{position:fixed;left:1rem;bottom:3.3rem;z-index:70;
    background:rgba(var(--deep-2-rgb),.9);backdrop-filter:blur(8px);
    border:1px solid rgba(var(--cream-rgb),.2);max-width:calc(100vw - 2rem)}
  .fsw-head{display:flex;align-items:center;gap:.5rem;background:none;border:0;
    color:rgba(var(--cream-rgb),.8);cursor:pointer;padding:.42rem .62rem;
    font-family:var(--body);font-size:.5rem;letter-spacing:.18em;
    text-transform:uppercase;font-weight:600;white-space:nowrap}
  .fsw-head:hover{color:var(--cream)}
  .fsw-head i{font-style:normal;font-size:.72rem;letter-spacing:0;
    text-transform:none;font-weight:400;line-height:1}
  /* a triangle rather than a plus and minus pair: nothing on this page is
     allowed to look like a dash. */
  .fsw-head::after{content:"\\25B8";margin-left:.15rem;font-size:.66rem;line-height:1}
  .fsw.open .fsw-head::after{content:"\\25BE"}
  .fsw-body{display:none;padding:0 .62rem .62rem;max-height:56vh;overflow-y:auto}
  .fsw.open .fsw-body{display:block}
  .fsw-row{display:flex;align-items:center;flex-wrap:wrap;gap:.26rem;
    padding-top:.5rem;margin-top:.5rem;border-top:1px solid rgba(var(--cream-rgb),.14)}
  .fsw-row:first-child{border-top:0;margin-top:0}
  .fsw-lbl{flex:0 0 100%;font-family:var(--body);font-size:.46rem;
    letter-spacing:.2em;text-transform:uppercase;font-weight:600;
    color:rgba(var(--cream-rgb),.5);margin-bottom:.12rem}
  .fsw button[data-fsw]{border:1px solid rgba(var(--cream-rgb),.26);
    background:transparent;color:rgba(var(--cream-rgb),.82);cursor:pointer;
    padding:.28rem .5rem;font-size:.58rem;line-height:1.25;white-space:nowrap;
    transition:border-color .2s,background .2s,color .2s}
  .fsw button[data-fsw]:hover{border-color:var(--orange);color:var(--cream)}
  .fsw button[data-fsw][aria-pressed="true"]{background:var(--orange);
    border-color:var(--orange);color:var(--deep-2);font-weight:600}
  .fsw-reset{display:block;margin-top:.55rem;background:none;border:0;padding:0;
    color:rgba(var(--cream-rgb),.55);cursor:pointer;font-family:var(--body);
    font-size:.5rem;letter-spacing:.16em;text-transform:uppercase;font-weight:600}
  .fsw-reset:hover{color:var(--orange)}
  @media(max-width:560px){.fsw{left:.6rem;bottom:2.9rem;max-width:calc(100vw - 1.2rem)}
    .fsw-body{max-height:50vh}}
  @media print{.fsw{display:none}}
'''


def _row(attr, label, options):
    out = ['    <div class="fsw-row">',
           '      <span class="fsw-lbl">%s</span>' % label]
    for key, name in options:
        pressed = "true" if DEFAULTS[attr] == key else "false"
        out.append('      <button type="button" data-fsw="%s" data-val="%s" '
                   'aria-pressed="%s" style="font-family:%s">%s</button>'
                   % (attr, key, pressed, STACKS[key], name))
    out.append("    </div>")
    return "\n".join(out)


SWITCHER_HTML = '''<div class="fsw" id="fsw">
  <button class="fsw-head" type="button" id="fswhead" aria-expanded="false" aria-controls="fswbody"><i>Aa</i>Type</button>
  <div class="fsw-body" id="fswbody" role="group" aria-label="Typeface preview">
%s
%s
%s
    <button class="fsw-reset" type="button" id="fswreset">Reset to default</button>
  </div>
</div>

''' % (_row("wm", "Wordmark", WORDMARK_ROW),
       _row("dp", "Headings and subheadings", DISPLAY_ROW),
       _row("bd", "Body", BODY_ROW))


SWITCHER_JS = '''
<script>
/* Font switcher. Three independent rows from BSaR's 28 August board, asked
   for on the 8 September call. Each row writes one attribute on <html>, and
   the stylesheet does the rest. Remembered per browser, like the palette. */
(function(){
  var KEY = 'q1521_fonts';
  var DEF = {wm:'%s', dp:'%s', bd:'%s'};
  var VALID = {wm:{%s}, dp:{%s}, bd:{%s}};
  var root = document.documentElement;
  var panel = document.getElementById('fsw');
  if(!panel) return;
  var btns = [].slice.call(panel.querySelectorAll('[data-fsw]'));

  function apply(state, persist){
    Object.keys(DEF).forEach(function(row){
      var v = VALID[row][state[row]] ? state[row] : DEF[row];
      state[row] = v;
      root.setAttribute('data-' + row, v);
    });
    btns.forEach(function(b){
      b.setAttribute('aria-pressed',
        state[b.dataset.fsw] === b.dataset.val ? 'true' : 'false');
    });
    if(persist){ try { localStorage.setItem(KEY, JSON.stringify(state)); } catch(e){} }
    return state;
  }

  var saved = null;
  try { saved = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch(e){}
  var S = apply({wm:(saved && saved.wm) || DEF.wm,
                 dp:(saved && saved.dp) || DEF.dp,
                 bd:(saved && saved.bd) || DEF.bd}, false);

  btns.forEach(function(b){
    b.addEventListener('click', function(){
      S[b.dataset.fsw] = b.dataset.val;
      S = apply(S, true);
    });
  });
  document.getElementById('fswreset').addEventListener('click', function(){
    S = apply({wm:DEF.wm, dp:DEF.dp, bd:DEF.bd}, true);
  });
  var head = document.getElementById('fswhead');
  head.addEventListener('click', function(){
    var open = panel.classList.toggle('open');
    head.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
})();
</script>
''' % (DEFAULTS["wm"], DEFAULTS["dp"], DEFAULTS["bd"],
       ",".join("%s:1" % k for k, _ in WORDMARK_ROW),
       ",".join("%s:1" % k for k, _ in DISPLAY_ROW),
       ",".join("%s:1" % k for k, _ in BODY_ROW))


def run(h, sub, resub, cut_block):
    # ---- faces ----------------------------------------------------------
    h = sub(h, ANCHOR_FACES, ANCHOR_FACES + NEW_FACES, 1, "board font faces")

    # ---- roles ----------------------------------------------------------
    h = sub(h, OLD_ROOT_TYPE, NEW_ROOT_TYPE, 1, "type roles")
    h = sub(h, '  :root[data-palette="B"]{--deep:#10069F;--deep-rgb:16,6,159;'
               '--deep-2:#0A0461;--deep-2-rgb:10,4,97;\n    --hair:rgba(16,6,159,.20)}',
            '  :root[data-palette="B"]{--deep:#10069F;--deep-rgb:16,6,159;'
            '--deep-2:#0A0461;--deep-2-rgb:10,4,97;\n    --hair:rgba(16,6,159,.20)}\n'
            + _selector_block(), 1, "per-face selectors")

    # ---- wordmark geometry ----------------------------------------------
    h = sub(h, OLD_WORDMARK, NEW_WORDMARK, 1, "wordmark on cap height")
    h = sub(h, OLD_HERO_WM, NEW_HERO_WM, 1, "hero wordmark scale")
    h = sub(h, OLD_GIANT, NEW_GIANT, 1, "footer watermark on the wordmark face")

    # ---- the switcher ---------------------------------------------------
    h = sub(h, "\n</style>", SWITCHER_CSS + "</style>", 1, "switcher css")
    h = sub(h, '<div class="pal" role="group" aria-label="Brand palette preview">',
            SWITCHER_HTML + '<div class="pal" role="group" aria-label="Brand palette preview">',
            1, "switcher markup")
    h = sub(h,
            "  btns.forEach(function(b){\n"
            "    b.addEventListener('click', function(){ set(b.dataset.pal, true); });\n"
            "  });\n"
            "})();\n"
            "</script>",
            "  btns.forEach(function(b){\n"
            "    b.addEventListener('click', function(){ set(b.dataset.pal, true); });\n"
            "  });\n"
            "})();\n"
            "</script>\n" + SWITCHER_JS.rstrip(),
            1, "switcher js")
    return h
