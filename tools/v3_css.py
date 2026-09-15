#!/usr/bin/env python3
"""Style layer of the v3 build. Imported by tools/apply_v3.py.

Covers:
  the 1521 wordmark, set as live type so it scales (markups 8, 10)
  hero left gutter aligned to the section gutter (markup 19)
  neutral hero scrim, no colour hue over the render (markup 14)
  hero eyebrow and hero partner lockups removed (markups 9, 12, 13)
  amenity label box moved below the images, bubble treatment dropped (markup 16)
  pricing block restyled for "Pricing to be announced" (markup 20)
  palette reduced to A and B, default B (BSaR, 10 September 2026)
  offer band, offer section and offer banner styles removed (meeting note)
"""

# --------------------------------------------------------------------------
#  Palette: purple options C and D are out, Blue 072 C (B) is the default.
# --------------------------------------------------------------------------

OLD_PAL_DEFAULT = '''  :root{
    --deep:#480B6A;   --deep-rgb:72,11,106;
    --deep-2:#2E0745; --deep-2-rgb:46,7,69;

    --cream:#FCF6ED;  --cream-rgb:252,246,237;
    --orange:#FE5000; --orange-rgb:254,80,0;
    --burnt:#BE5103;  --burnt-rgb:190,81,3;
    --ink:#1C1A17;    --ink-rgb:28,26,23;'''

NEW_PAL_DEFAULT = '''  :root{
    --deep:#10069F;   --deep-rgb:16,6,159;
    --deep-2:#0A0461; --deep-2-rgb:10,4,97;

    --cream:#FCF6ED;  --cream-rgb:252,246,237;
    --orange:#FD5100; --orange-rgb:253,81,0;
    --burnt:#BE5103;  --burnt-rgb:190,81,3;
    --ink:#1C1A17;    --ink-rgb:28,26,23;'''

OLD_PAL_HAIR = "    --hair:rgba(72,11,106,.20);"
NEW_PAL_HAIR = "    --hair:rgba(16,6,159,.20);"

OLD_PAL_SETS = '''  :root[data-palette="A"]{--deep:#0032AD;--deep-rgb:0,50,173;--deep-2:#001E68;--deep-2-rgb:0,30,104;
    --hair:rgba(0,50,173,.20)}
  :root[data-palette="B"]{--deep:#10069F;--deep-rgb:16,6,159;--deep-2:#0A0461;--deep-2-rgb:10,4,97;
    --hair:rgba(16,6,159,.20)}
  :root[data-palette="C"]{--deep:#480B6A;--deep-rgb:72,11,106;--deep-2:#2E0745;--deep-2-rgb:46,7,69;
    --hair:rgba(72,11,106,.20)}
  :root[data-palette="D"]{--deep:#512079;--deep-rgb:81,32,121;--deep-2:#33144C;--deep-2-rgb:51,20,76;
    --hair:rgba(81,32,121,.20)}'''

NEW_PAL_SETS = '''  :root[data-palette="A"]{--deep:#0032AD;--deep-rgb:0,50,173;--deep-2:#001E68;--deep-2-rgb:0,30,104;
    --hair:rgba(0,50,173,.20)}
  :root[data-palette="B"]{--deep:#10069F;--deep-rgb:16,6,159;--deep-2:#0A0461;--deep-2-rgb:10,4,97;
    --hair:rgba(16,6,159,.20)}'''

OLD_PAL_DOTS = '''  .pal button[data-pal="A"]{background:#0032AD}
  .pal button[data-pal="B"]{background:#10069F}
  .pal button[data-pal="C"]{background:#480B6A}
  .pal button[data-pal="D"]{background:#512079}'''

NEW_PAL_DOTS = '''  .pal button[data-pal="A"]{background:#0032AD}
  .pal button[data-pal="B"]{background:#10069F}'''

# The v2 comment block still describes four options and names C as default.
OLD_PAL_NOTE = '''  /* ================= BSaR brand direction, 28 August 2026 =================
     One deep colour + Pantone Orange 021 C + Burnt Orange + Cream White.
     Deep-colour hexes read off page 2 of the branding PDF.
       A  Pantone Saratoga Signature Blue  #0032AD
       B  Pantone Blue 072 C               #10069F
       C  Pantone Deep Purple 2617 C       #480B6A   (default)
       D  Pantone Purple PMS 3555 C        #512079
     The switcher at the bottom left swaps [data-palette] on <html>.
     ====================================================================== */'''

NEW_PAL_NOTE = '''  /* ============ BSaR brand direction, 28 August and 10 September 2026 ======
     Deep blue + Pantone Orange 021 C + Burnt Orange + Cream White.
     The purple options are out. Two blues remain:
       A  Pantone Saratoga Signature Blue  #0032AD
       B  Pantone Blue 072 C               #10069F   (default)
     Orange 021 C is set to #FD5100, the hex printed in the BSaR PDF.
     The switcher at the bottom left swaps [data-palette] on <html>.
     ====================================================================== */'''


# --------------------------------------------------------------------------
#  Wordmark. BSaR's 15 September draft: thin geometric sans digits, "15" over
#  "21", a short rule beneath. Set as live type in DM Sans so it stays crisp
#  at every size; the PNG is a raster and would not.
# --------------------------------------------------------------------------

OLD_WORDMARK = '''  .wordmark{font-family:var(--serif);font-weight:400;color:var(--cream);font-size:1.06rem;
    letter-spacing:.24em;text-transform:uppercase;text-decoration:none;white-space:nowrap}
  .wordmark em{font-style:normal;font-weight:700;color:var(--accent);letter-spacing:.16em}'''

NEW_WORDMARK = '''  /* ---------------- 1521 wordmark (BSaR draft, 15 September 2026) --------
     Address as name. Inline in the nav and the footer, stacked in the hero,
     both drawn from the same geometric sans so they read as one mark. */
  .wordmark{font-family:var(--sans);font-weight:400;color:var(--cream);font-size:1.16rem;
    letter-spacing:.36em;text-decoration:none;white-space:nowrap;
    font-variant-numeric:lining-nums tabular-nums;transition:color .3s}
  .wordmark:hover{color:var(--accent)}
  .wm-stack{display:inline-block;font-family:var(--sans);font-weight:400;
    font-variant-numeric:lining-nums tabular-nums;letter-spacing:.02em;line-height:.9;
    color:var(--cream);text-decoration:none}
  .wm-stack .wm-d{display:block}
  .wm-stack .wm-rule{display:block;width:1.2ch;height:.042em;min-height:2px;
    background:var(--accent);margin:.36em auto 0}'''


# --------------------------------------------------------------------------
#  Hero
# --------------------------------------------------------------------------

# markup 14: the blue wash over the render comes off. What is left is a
# neutral dark gradient in the lower third, only as much as the type needs.
OLD_SCRIM = '''  .hero-scrim{position:absolute;inset:0;z-index:2;
    background:linear-gradient(180deg,rgba(var(--deep-2-rgb),.55) 0%,rgba(var(--deep-2-rgb),.1) 34%,rgba(var(--deep-2-rgb),.55) 60%,rgba(var(--deep-2-rgb),.95) 92%)}'''

NEW_SCRIM = '''  /* markup 14: no colour hue over the render. A neutral dark gradient in the
     lower third only, enough to hold the type and nothing more. */
  .hero-scrim{position:absolute;inset:0;z-index:2;
    background:linear-gradient(180deg,rgba(0,0,0,.28) 0%,rgba(0,0,0,0) 22%,rgba(0,0,0,0) 44%,rgba(0,0,0,.42) 72%,rgba(0,0,0,.82) 100%)}'''

# markup 19: the hero text sat on the centred 1280 box, which put it about 40px
# to the right of every section heading below. Full-bleed padding plus an inner
# .wrap puts the hero on the identical left gutter.
OLD_HERO_INNER = '''  .hero-inner{position:relative;z-index:3;width:100%;max-width:1280px;margin:0 auto;
    padding:7.5rem 2.4rem 4.4rem}'''

NEW_HERO_INNER = '''  /* markup 19: one left gutter for the whole page. The hero pads like a
     section and carries an inner .wrap, so the hero type, every section
     eyebrow and every H2 start on exactly the same vertical line. */
  .hero-inner{position:relative;z-index:3;width:100%;padding:7.5rem 2.4rem 4.4rem}
  .hero-inner>.wrap{text-align:left}'''

OLD_EYEBROW = '''  .hero-eyebrow{color:var(--accent);margin-bottom:1.4rem;display:flex;align-items:center;gap:1rem;
    text-shadow:0 1px 10px rgba(var(--deep-2-rgb),.75);opacity:0;animation:fadeIn 1s .5s forwards}
  .hero-eyebrow::before{content:"";flex:0 0 52px;height:1px;background:var(--accent)}
  @media(max-width:560px){
    .hero-eyebrow{font-size:.6rem;letter-spacing:.15em}
    .hero-eyebrow::before{display:none}
  }'''

NEW_EYEBROW = '''  /* markup 9 removed the "Queen West" eyebrow. The occupancy line takes the
     slot under the tagline instead, where it reads as a fact, not a label. */
  .hero-soon{display:inline-flex;align-items:center;gap:.9rem;color:var(--cream);
    font-size:.78rem;font-weight:600;letter-spacing:.26em;margin-top:1.5rem;
    text-shadow:0 1px 14px rgba(0,0,0,.8);opacity:0;animation:fadeIn 1s .8s forwards}
  .hero-soon::before{content:"";flex:0 0 46px;height:2px;background:var(--orange)}
  @media(max-width:560px){.hero-soon{font-size:.64rem;letter-spacing:.16em}
    .hero-soon::before{flex-basis:26px}}'''

OLD_H1 = '''  .hero h1{color:var(--cream);font-size:clamp(2.9rem,8vw,6.4rem);line-height:1.0;letter-spacing:-.02em;max-width:16ch;
    text-shadow:0 2px 22px rgba(var(--deep-2-rgb),.5)}'''

NEW_H1 = '''  .hero h1{color:var(--cream);font-size:clamp(2.9rem,8vw,6.4rem);line-height:1.0;letter-spacing:-.02em;max-width:16ch;
    text-shadow:0 2px 22px rgba(0,0,0,.45)}
  /* the stacked hero wordmark, at hero scale */
  .hero .wm-stack{font-size:clamp(3.6rem,10.5vw,8.2rem);letter-spacing:.015em}
  .hero .wm-stack .wm-d{overflow:hidden;padding-bottom:.04em;margin-bottom:-.04em}
  .hero .wm-stack .wm-d>span{display:block;transform:translateY(112%);
    animation:riseUp 1.15s var(--ease) forwards}
  .hero .wm-stack .wm-d:nth-child(2)>span{animation-delay:.14s}
  .hero .wm-stack .wm-rule{transform:scaleX(0);transform-origin:left;
    animation:ruleIn .9s var(--ease) .9s forwards}
  @keyframes ruleIn{to{transform:scaleX(1)}}'''

OLD_TAGLINE = '''  .hero h1 .tagline{display:block;font-size:clamp(.98rem,2.05vw,1.5rem);line-height:1.25;
    letter-spacing:.01em;color:rgba(var(--cream-rgb),.92);margin-top:.55rem;max-width:24ch}'''

NEW_TAGLINE = '''  .hero h1 .tagline{display:block;font-family:var(--serif);font-weight:400;
    font-size:clamp(1.02rem,2.15vw,1.58rem);line-height:1.25;letter-spacing:.01em;
    color:rgba(var(--cream-rgb),.94);margin-top:1.1rem;max-width:26ch;letter-spacing:.04em}'''

# markups 12 and 13 take both partner lockups out of the hero. They live in the
# footer only, so the hero lockup styles go with them.
OLD_LOCKUPS = '''  .hero-lockups{display:flex;align-items:center;gap:2.2rem;flex-wrap:wrap;margin-top:2.4rem;
    padding-top:1.4rem;border-top:1px solid var(--hair);opacity:0;animation:fadeIn 1.2s 1.5s forwards}
  .lockup{display:flex;align-items:center;gap:.9rem}
  .lockup small{font-size:.56rem;letter-spacing:.24em;text-transform:uppercase;color:var(--fg-45);font-weight:500;white-space:nowrap}
  .lockup img{height:20px;width:auto;opacity:.92}
  .lockup img.tall{height:30px}
  .lockup-sep{width:1px;height:26px;background:var(--hair)}
  @media(max-width:640px){.lockup-sep{display:none}.hero-lockups{gap:1.2rem}}
'''

OLD_HERO_SUB = '''  .hero-sub{color:rgba(var(--cream-rgb),.84);max-width:54ch;margin:1.3rem 0 2.1rem;font-size:1.02rem;
    opacity:0;animation:fadeIn 1s .9s forwards}'''

NEW_HERO_SUB = '''  .hero-sub{color:rgba(var(--cream-rgb),.88);max-width:52ch;margin:1.5rem 0 2.2rem;font-size:1.02rem;
    text-shadow:0 1px 14px rgba(0,0,0,.55);opacity:0;animation:fadeIn 1s 1s forwards}'''


# --------------------------------------------------------------------------
#  Offer band, offer section and offer banner: out (meeting of 8 September)
# --------------------------------------------------------------------------

OLD_INCENTIVE_CSS = '''  /* INCENTIVE BAND */
  .incentive{position:relative;background:var(--deep-2);padding:2.6rem 2.4rem;text-align:center}
  .incentive::before,.incentive::after{content:"";position:absolute;left:0;right:0;height:1px;background:var(--accent);
    transform:scaleX(0);transition:transform 1.2s var(--ease) .15s;transform-origin:center}
  .incentive::before{top:0}
  .incentive::after{bottom:0}
  .incentive.in::before,.incentive.in::after{transform:scaleX(1)}
  .incentive .label{color:var(--accent);display:block;margin-bottom:.9rem}
  .incentive p.big{font-family:var(--serif);font-weight:360;font-size:clamp(1.25rem,2.6vw,1.9rem);
    line-height:1.32;color:var(--cream);max-width:44ch;margin:0 auto}
  .incentive p.fine{font-size:.68rem;color:var(--fg-45);margin-top:1rem;letter-spacing:.04em}

'''

OLD_PERKBANNER_CSS = '''  .perk-banner{display:flex;justify-content:space-between;align-items:center;gap:2rem;flex-wrap:wrap;
    border:1px solid var(--hair);padding:1.7rem 2.4rem;margin-top:1.4rem}
  .perk-banner p{font-size:.95rem;color:var(--fg)}
  .perk-banner p b{font-family:var(--serif);font-weight:700;color:var(--accent)}
  .perk-banner a{font-size:.62rem;letter-spacing:.16em;text-transform:uppercase;font-weight:600;
    color:var(--fg);text-decoration:none;border-bottom:1px solid var(--accent);padding-bottom:.2rem;white-space:nowrap}
  .perk-banner a:hover{color:var(--accent)}
'''


# --------------------------------------------------------------------------
#  Suites (markups 20, 21, 22)
# --------------------------------------------------------------------------

OLD_KICKER = '''  .suites-kicker{font-family:var(--serif);font-size:clamp(1.05rem,2vw,1.35rem);
    color:var(--em);margin-top:1.1rem}
'''

OLD_PRICE = '''  .plan .price b{font-family:var(--sans);font-weight:600;font-size:1.25rem;color:var(--fg);
    font-variant-numeric:lining-nums tabular-nums}
  .plan .price b small{font-size:.62rem;font-weight:500;color:var(--fg-70);letter-spacing:.1em;text-transform:uppercase;display:block}'''

NEW_PRICE = '''  /* markup 20: all pricing TBD. The slot stays so the card keeps its rhythm,
     and carries the status line instead of a rent. */
  .plan .price b{font-family:var(--sans);font-weight:600;font-size:.68rem;color:var(--fg-70);
    letter-spacing:.14em;text-transform:uppercase}'''


# --------------------------------------------------------------------------
#  Amenities (markup 16): the floating label box comes off the image and sits
#  below the gallery as an ordinary section block, like everything else.
# --------------------------------------------------------------------------

OLD_AMEN_CARD = '''  .amen-card{position:relative;max-width:600px;background:var(--deep);border:1px solid var(--hair);
    padding:3rem;margin:-14rem 2.4rem 0 auto;z-index:2}
  @media(min-width:1360px){.amen-card{margin-right:calc((100vw - 1280px)/2)}}
  .amen-list{margin-top:1.8rem;columns:2;column-gap:2.4rem}
  .amen-list li{list-style:none;break-inside:avoid;padding:.6rem 0;border-bottom:1px solid var(--hair);
    font-size:.88rem;color:var(--fg-70)}
  .amen-list li b{color:var(--fg);font-weight:500}
  @media(max-width:700px){.amen-card{margin:-8rem 1.2rem 0;padding:2rem}.amen-list{columns:1}}'''

NEW_AMEN_CARD = '''  /* markup 16: the amenity label box moved below the images and lost the
     floating-bubble treatment, which appeared nowhere else on the page. It is
     now a plain block on the same 1280 gutter as every other section. */
  .amen-card{position:relative;max-width:1280px;width:100%;margin:0 auto;
    padding:0 2.4rem 4.5rem;z-index:2}
  .amen-list{margin-top:1.8rem;columns:2;column-gap:3rem}
  .amen-list li{list-style:none;break-inside:avoid;padding:.7rem 0;border-bottom:1px solid var(--hair);
    font-size:.9rem;color:var(--fg-70)}
  .amen-list li b{color:var(--fg);font-weight:500}
  @media(max-width:700px){.amen-card{padding:0 1.2rem 3rem}.amen-list{columns:1}}'''

OLD_AGAL = '''  .agal{margin-top:3.2rem;padding-bottom:4rem}'''
NEW_AGAL = '''  .agal{margin-top:4.5rem;padding-bottom:3.4rem}'''


# --------------------------------------------------------------------------
#  Map (markup 18): the All chip needs to read as a reset, not a category.
# --------------------------------------------------------------------------

OLD_CHIP = '''  .chip span{color:var(--accent);margin-left:.45rem;font-variant-numeric:lining-nums}'''

NEW_CHIP = '''  .chip span{color:var(--accent);margin-left:.45rem;font-variant-numeric:lining-nums}
  /* markup 18: All is a reset, so it is drawn as an outline rather than as
     one more category chip. */
  .chip.all{border-color:rgba(var(--cream-rgb),.5)}
  .chip.all.on{background:transparent;border-color:var(--cream);color:var(--cream)}'''


# --------------------------------------------------------------------------
#  Footer and map marker: four digits, not three
# --------------------------------------------------------------------------

OLD_GIANT = '''  .foot-giant{font-family:var(--serif);font-weight:700;font-size:clamp(3.4rem,12vw,10rem);line-height:.82;
    color:transparent;-webkit-text-stroke:1px rgba(var(--cream-rgb),.16);text-align:center;letter-spacing:.04em;
    white-space:nowrap;user-select:none;margin-top:2rem;transform:translateY(18%)}'''

NEW_GIANT = '''  .foot-giant{font-family:var(--sans);font-weight:400;font-size:clamp(3.4rem,15vw,12rem);line-height:.82;
    color:transparent;-webkit-text-stroke:1px rgba(var(--cream-rgb),.18);text-align:center;letter-spacing:.14em;
    font-variant-numeric:lining-nums tabular-nums;
    white-space:nowrap;user-select:none;margin-top:2rem;transform:translateY(18%)}'''

OLD_MARKER = '''  .site-marker text{fill:var(--deep-2);font-family:var(--serif);font-size:17px;font-weight:700;text-anchor:middle;pointer-events:none}'''
NEW_MARKER = '''  .site-marker text{fill:var(--deep-2);font-family:var(--sans);font-size:13px;font-weight:600;
    letter-spacing:.5px;text-anchor:middle;pointer-events:none}'''


# --------------------------------------------------------------------------
#  Registration: the occupancy line next to the form (markup 2)
# --------------------------------------------------------------------------

NEW_CONTACT_CSS = '''  /* markup 2: Coming Soon Summer 2027, stated by the registration form as
     well as in the hero. */
  .soon-line{display:inline-flex;align-items:center;gap:.8rem;color:var(--accent);
    margin-top:1.4rem}
  .soon-line::before{content:"";flex:0 0 40px;height:1px;background:var(--accent)}
  .contact .soon-line{margin-bottom:.4rem}
'''


# markup 19: the sections put their 2.4rem gutter on the <section> and centre
# a 1280 .wrap inside it, so their content starts at gutter + (free space / 2).
# The full-bleed blocks below carry the gutter themselves inside a 1280 box, so
# their content used to start 2.4rem further right. Widening each box by exactly
# that gutter puts every block on one left edge, with the content still 1280.
GUTTER_CSS = """  .amen-card,.ahead,.agrid,.map-head,.map-filter,.map-note,.arrive .frame-caption{
    max-width:calc(1280px + 4.8rem)}"""


def run(h, sub, resub, cut_block):
    # ---- palette: two blues, default B ---------------------------------
    h = sub(h, OLD_PAL_NOTE, NEW_PAL_NOTE, 1, "palette note")
    h = sub(h, OLD_PAL_DEFAULT, NEW_PAL_DEFAULT, 1, "palette default to B")
    h = sub(h, OLD_PAL_HAIR, NEW_PAL_HAIR, 1, "palette hair")
    h = sub(h, OLD_PAL_SETS, NEW_PAL_SETS, 1, "palette sets A and B only")
    h = sub(h, OLD_PAL_DOTS, NEW_PAL_DOTS, 1, "palette switcher dots")

    # ---- wordmark -------------------------------------------------------
    h = sub(h, OLD_WORDMARK, NEW_WORDMARK, 1, "wordmark type")

    # ---- hero -----------------------------------------------------------
    h = sub(h, OLD_SCRIM, NEW_SCRIM, 1, "hero scrim, markup 14")
    h = sub(h, OLD_HERO_INNER, NEW_HERO_INNER, 1, "hero gutter, markup 19")
    h = sub(h, OLD_EYEBROW, NEW_EYEBROW, 1, "hero eyebrow out, markup 9")
    h = sub(h, OLD_H1, NEW_H1, 1, "hero h1 and stacked wordmark")
    h = sub(h, OLD_HERO_SUB, NEW_HERO_SUB, 1, "hero sub")
    h = sub(h, OLD_TAGLINE, NEW_TAGLINE, 1, "hero tagline, markup 11")
    h = sub(h, OLD_LOCKUPS, "", 1, "hero lockup css out, markups 12 and 13")

    # ---- offers out -----------------------------------------------------
    h = sub(h, OLD_INCENTIVE_CSS, "", 1, "offer band css out")
    h = sub(h, OLD_PERKBANNER_CSS, "", 1, "offer banner css out")
    h = cut_block(h, "  /* OFFER */", "  .offer-perks small{font-size:.8rem;color:var(--fg-70);line-height:1.5;display:block}\n",
                  "offer section css out")

    # ---- suites ---------------------------------------------------------
    h = sub(h, OLD_KICKER, "", 1, "suites kicker css out, markup 22")
    h = sub(h, OLD_PRICE, NEW_PRICE, 1, "pricing css, markup 20")

    # ---- amenities ------------------------------------------------------
    h = sub(h, OLD_AMEN_CARD, NEW_AMEN_CARD, 1, "amenity box css, markup 16")
    h = sub(h, OLD_AGAL, NEW_AGAL, 1, "amenity gallery spacing")

    # ---- map ------------------------------------------------------------
    h = sub(h, OLD_CHIP, NEW_CHIP, 1, "map All chip css, markup 18")
    h = sub(h, OLD_MARKER, NEW_MARKER, 1, "map site marker type")

    # ---- footer ---------------------------------------------------------
    h = sub(h, OLD_GIANT, NEW_GIANT, 1, "footer watermark type")

    # ---- registration ---------------------------------------------------
    h = sub(h, "  .map-note{", NEW_CONTACT_CSS + "  .map-note{", 1, "coming soon line css")

    # ---- one left gutter for the whole page (markup 19) ------------------
    # last in the sheet, so it wins over each block's own max-width
    h = sub(h, "\n</style>", "\n" + GUTTER_CSS + "\n</style>", 1,
            "shared gutter, markup 19")

    return h
