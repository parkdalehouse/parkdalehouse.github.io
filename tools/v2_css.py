#!/usr/bin/env python3
"""CSS layer of the v2 build. Imported by tools/apply_v2.py."""

from v2_flags import NEZAM_CREDIT


def run(h, sub, resub, cut_block):

    # ------------------------------------------------------------------
    # 1. Context-free token renames.
    #    --line-dark must go before --line so the longer name wins.
    # ------------------------------------------------------------------
    for old, new, n, label in [
        ("var(--line-dark)", "var(--hair)", 3, "line-dark"),
        ("var(--line)", "var(--hair)", 23, "line"),
        ("var(--linen-70)", "var(--fg-70)", 13, "linen-70"),
        ("var(--linen-45)", "var(--fg-45)", 12, "linen-45"),
        ("var(--pine-70)", "var(--fg-70)", 6, "pine-70"),
        ("var(--brass)", "var(--accent)", 60, "brass"),
        ("rgba(251,248,241,", "rgba(var(--cream-rgb),", 8, "linen rgba"),
        ("rgba(20,32,27,", "rgba(var(--deep-2-rgb),", 17, "ink rgba"),
        ("rgba(30,58,47,", "rgba(var(--deep-rgb),", 1, "pine rgba"),
        ("rgba(196,166,52,", "rgba(var(--orange-rgb),", 1, "brass rgba"),
        ("#14201B", "var(--deep-2)", 3, "ink hex"),
        ("#C4A634", "var(--accent)", 8, "brass hex"),
    ]:
        h = sub(h, old, new, n, label)

    # ------------------------------------------------------------------
    # 2. Base surface. Cream page, deep bands.
    # ------------------------------------------------------------------
    h = sub(h,
            "body{background:var(--pine);color:var(--linen);font-family:var(--sans);",
            "body{background:var(--bg);color:var(--fg);font-family:var(--sans);",
            1, "body surface")
    h = sub(h,
            "::selection{background:var(--accent);color:var(--ink)}",
            "::selection{background:var(--accent);color:var(--cream)}",
            1, "selection")
    h = sub(h,
            "body::after{content:\"\";position:fixed;inset:0;pointer-events:none;z-index:99;opacity:.05;",
            "body::after{content:\"\";position:fixed;inset:0;pointer-events:none;z-index:99;opacity:.045;",
            1, "grain")

    # Libre Baskerville only ships 400 and 700, so the old optical-size hints go.
    h = sub(h,
            "h1,h2,h3{font-family:var(--serif);font-optical-sizing:auto;font-weight:360;text-wrap:balance}",
            "h1,h2,h3{font-family:var(--serif);font-weight:400;letter-spacing:-.012em;text-wrap:balance}",
            1, "heading face")

    # ------------------------------------------------------------------
    # 3. Buttons
    # ------------------------------------------------------------------
    h = sub(h, ".btn:hover{color:var(--ink)}",
            ".btn:hover{color:var(--btn-on-accent)}", 1, "btn hover")
    h = sub(h, ".btn-solid{background:var(--accent);color:var(--ink)}",
            ".btn-solid{background:var(--accent);color:var(--btn-on-accent);border-color:var(--accent)}",
            1, "btn solid")
    h = sub(h, ".btn-solid::before{background:var(--linen)}",
            ".btn-solid::before{background:var(--btn-hover-bg)}", 1, "btn solid before")
    h = sub(h, ".btn-solid:hover{color:var(--ink)}",
            ".btn-solid:hover{color:var(--btn-hover-fg)}", 1, "btn solid hover")

    # ------------------------------------------------------------------
    # 4. Nav. Always sits over the dark hero, so it is pinned to cream text.
    # ------------------------------------------------------------------
    h = sub(h,
            "    background:linear-gradient(180deg,rgba(var(--deep-2-rgb),.72),transparent)}",
            "    background:linear-gradient(180deg,rgba(var(--deep-2-rgb),.78),transparent)}",
            1, "nav gradient")
    h = sub(h, "nav.scrolled{background:rgba(var(--deep-2-rgb),.96)",
            "nav.scrolled{background:rgba(var(--deep-2-rgb),.97)", 1, "nav scrolled")
    h = sub(h,
            "  .wordmark{font-family:var(--serif);font-weight:420;color:var(--linen);font-size:1.12rem;\n"
            "    letter-spacing:.26em;text-transform:uppercase;text-decoration:none;white-space:nowrap}\n"
            "  .wordmark em{font-style:italic;color:var(--accent)}",
            "  .wordmark{font-family:var(--serif);font-weight:400;color:var(--cream);font-size:1.06rem;\n"
            "    letter-spacing:.24em;text-transform:uppercase;text-decoration:none;white-space:nowrap}\n"
            "  .wordmark em{font-style:normal;font-weight:700;color:var(--accent);letter-spacing:.16em}",
            1, "wordmark")
    h = sub(h, "  .nav-links a{color:var(--linen);text-decoration:none;",
            "  .nav-links a{color:var(--cream);text-decoration:none;", 1, "nav links")
    h = sub(h, ".nav-cta:hover{background:var(--accent);color:var(--ink)!important}",
            ".nav-cta:hover{background:var(--accent);color:var(--deep-2)!important}", 1, "nav cta hover")
    # a fifth nav item needs a little more room before the links collapse
    h = sub(h, "@media(max-width:960px){.nav-links a:not(.nav-cta):not(.nav-tel){display:none}}",
            "@media(max-width:1080px){.nav-links a:not(.nav-cta):not(.nav-tel){display:none}}",
            1, "nav breakpoint")
    h = sub(h, "  .nav-links{display:flex;gap:2rem;align-items:center}",
            "  .nav-links{display:flex;gap:1.7rem;align-items:center}", 1, "nav gap")

    # the palette switcher is pinned bottom left, so the hero lockups need room
    h = sub(h, "    padding:7.5rem 2.4rem 2.6rem}",
            "    padding:7.5rem 2.4rem 4.4rem}", 1, "hero inner padding")

    # ------------------------------------------------------------------
    # 5. Hero
    # ------------------------------------------------------------------
    h = sub(h, "    overflow:hidden;background:var(--ink)}",
            "    overflow:hidden;background:var(--deep-2)}", 1, "hero bg")
    h = sub(h, "  .hero h1{color:var(--linen);font-size:clamp(2.7rem,6.6vw,5.6rem);line-height:1.02;letter-spacing:-.01em;max-width:15ch;",
            "  .hero h1{color:var(--cream);font-size:clamp(2.9rem,8vw,6.4rem);line-height:1.0;letter-spacing:-.02em;max-width:16ch;",
            1, "hero h1")
    h = sub(h, "  .hero h1 em{font-style:italic;font-weight:340;color:var(--accent)}",
            "  .hero h1 em{font-style:normal;font-weight:700;color:var(--accent);letter-spacing:-.01em}",
            1, "hero h1 em")
    h = sub(h, "  .hero-tel b{font-weight:600;color:var(--linen);",
            "  .hero-tel b{font-weight:600;color:var(--cream);", 1, "hero tel")
    h = sub(h, "  .hero-sub{color:var(--fg-70);max-width:52ch;margin:1.5rem 0 2.1rem;font-size:1.02rem;",
            "  .hero-sub{color:rgba(var(--cream-rgb),.84);max-width:54ch;margin:1.3rem 0 2.1rem;font-size:1.02rem;",
            1, "hero sub")
    # the coordinate line is removed (markup 17), so its rules go with it
    h = sub(h,
            "  .hero-coords{position:absolute;right:2.4rem;bottom:5rem;z-index:3;writing-mode:vertical-rl;\n"
            "    font-size:.62rem;letter-spacing:.3em;color:var(--fg-45);text-transform:uppercase;\n"
            "    opacity:0;animation:fadeIn 1.2s 1.6s forwards}\n"
            "  @media(max-width:700px){.hero-coords{display:none}}\n",
            "  /* hero tagline line inside the H1 (markups 13 and 16) */\n"
            "  .hero h1 .tagline{display:block;font-size:clamp(.98rem,2.05vw,1.5rem);line-height:1.25;\n"
            "    letter-spacing:.01em;color:rgba(var(--cream-rgb),.92);margin-top:.55rem;max-width:24ch}\n"
            "  /* discreet placeholder captions for artwork still to come */\n"
            "  .ph-cap{font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;\n"
            "    color:var(--fg-45);font-weight:500}\n"
            "  .hero-ph{position:absolute;right:2.4rem;bottom:1.5rem;z-index:3;\n"
            "    color:rgba(var(--cream-rgb),.62);opacity:0;animation:fadeIn 1.2s 1.7s forwards}\n"
            "  @media(max-width:700px){.hero-ph{right:1.2rem;bottom:.85rem;font-size:.5rem;\n"
            "    letter-spacing:.14em}}\n",
            1, "hero coords out, tagline and placeholder in")

    # ------------------------------------------------------------------
    # 6. Incentive band
    # ------------------------------------------------------------------
    h = sub(h, "  .incentive{position:relative;background:var(--ink);",
            "  .incentive{position:relative;background:var(--deep-2);", 1, "incentive bg")
    h = sub(h, "    line-height:1.3;color:var(--linen);max-width:44ch;margin:0 auto}",
            "    line-height:1.32;color:var(--cream);max-width:44ch;margin:0 auto}", 1, "incentive big")

    # ------------------------------------------------------------------
    # 7. Stats band removed entirely (markup 18)
    # ------------------------------------------------------------------
    h = cut_block(h, "  /* STATS */", "  /* SECTIONS */", "stats css")
    h = h.replace("section{padding:6.5rem 2.4rem;position:relative}",
                  "  /* SECTIONS */\n  section{padding:6.5rem 2.4rem;position:relative}", 1)

    # ------------------------------------------------------------------
    # 8. Shared section type
    # ------------------------------------------------------------------
    h = sub(h, "  h2{font-size:clamp(2rem,4vw,3.2rem);line-height:1.1;color:var(--linen)}",
            "  h2{font-size:clamp(1.75rem,3.5vw,2.85rem);line-height:1.14;color:var(--fg)}",
            1, "h2")
    h = sub(h, "  h2 em{font-style:italic;color:var(--accent);font-weight:340}",
            "  h2 em{font-style:italic;color:var(--em);font-weight:400}", 1, "h2 em")

    # ------------------------------------------------------------------
    # 9. Suites. The old light-section overrides are now the page default.
    # ------------------------------------------------------------------
    h = sub(h,
            "  /* SUITES (light section) */\n"
            "  .suites{background:var(--linen);color:var(--ink)}\n"
            "  .suites h2{color:var(--ink)}\n"
            "  .suites h2 em{color:var(--pine);font-style:italic}\n"
            "  .suites .lede{color:var(--fg-70)}\n"
            "  .suites .sec-eyebrow{color:var(--pine)}\n"
            "  .suites .sec-eyebrow::after{background:var(--accent);opacity:1}\n",
            "  /* SUITES */\n"
            "  .suites .sec-eyebrow::after{opacity:1}\n"
            "  .suites-kicker{font-family:var(--serif);font-size:clamp(1.05rem,2vw,1.35rem);\n"
            "    color:var(--em);margin-top:1.1rem}\n"
            "  .suites-foot{margin-top:1.6rem;font-size:.72rem;color:var(--fg-45);letter-spacing:.02em}\n"
            "  /* bedroom filter (markup 20) */\n"
            "  .bedfilter{display:flex;align-items:center;gap:.55rem;flex-wrap:wrap;margin-top:2.6rem}\n"
            "  .bedfilter .fl{color:var(--fg-45);margin-right:.5rem}\n"
            "  .bedbtn{border:1px solid var(--hair);background:transparent;color:var(--fg);\n"
            "    padding:.55rem 1.05rem;cursor:pointer;font-family:var(--sans);font-size:.66rem;\n"
            "    text-transform:uppercase;letter-spacing:.16em;font-weight:600;transition:all .25s}\n"
            "  .bedbtn:hover{border-color:var(--accent);color:var(--accent)}\n"
            "  .bedbtn[aria-pressed=\"true\"]{background:var(--accent);border-color:var(--accent);\n"
            "    color:var(--btn-on-accent)}\n"
            "  .plan[hidden]{display:none}\n"
            "  .bedcount{margin-top:1.1rem;font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;\n"
            "    color:var(--fg-45)}\n"
            "  /* 3D suite tours placeholder (markup 19) */\n"
            "  .tours{margin-top:3.4rem;border:1px solid var(--hair);background:rgba(255,255,255,.5);\n"
            "    display:grid;grid-template-columns:1.1fr 1fr;gap:0;align-items:stretch;overflow:hidden}\n"
            "  @media(max-width:860px){.tours{grid-template-columns:1fr}}\n"
            "  .tours-copy{padding:2.4rem 2.6rem}\n"
            "  @media(max-width:860px){.tours-copy{padding:2rem}}\n"
            "  .tours-copy h3{font-size:clamp(1.35rem,2.4vw,1.85rem);font-weight:400}\n"
            "  .tours-copy h3 em{font-style:italic;color:var(--em)}\n"
            "  .tours-copy p{font-size:.9rem;color:var(--fg-70);margin-top:.9rem;max-width:44ch}\n"
            "  .tours-frame{position:relative;min-height:250px;border-left:1px solid var(--hair);\n"
            "    display:grid;place-items:center;padding:2rem;\n"
            "    background:repeating-linear-gradient(135deg,rgba(var(--deep-rgb),.05) 0 12px,transparent 12px 24px)}\n"
            "  @media(max-width:860px){.tours-frame{border-left:none;border-top:1px solid var(--hair);min-height:200px}}\n"
            "  .tours-frame div{text-align:center}\n"
            "  .tours-frame svg{width:56px;height:56px;margin:0 auto .9rem;display:block;\n"
            "    stroke:var(--em);fill:none;stroke-width:1.2;opacity:.8}\n",
            1, "suites css")
    h = sub(h, "  .plan{border:1px solid var(--hair);background:var(--linen);",
            "  .plan{border:1px solid var(--hair);background:rgba(255,255,255,.55);", 1, "plan bg")
    for old, new, label in [
        (".fp-wall{fill:none;stroke:var(--pine);", ".fp-wall{fill:none;stroke:var(--deep);", "fp wall"),
        (".fp-in{fill:none;stroke:var(--pine);", ".fp-in{fill:none;stroke:var(--deep);", "fp in"),
        (".fp-lite{fill:none;stroke:var(--pine);", ".fp-lite{fill:none;stroke:var(--deep);", "fp lite"),
        (".fp-arc{fill:none;stroke:var(--pine);", ".fp-arc{fill:none;stroke:var(--deep);", "fp arc"),
    ]:
        h = sub(h, old, new, 1, label)
    h = sub(h, "  .plan h3{font-size:1.5rem;font-weight:400;color:var(--ink)}",
            "  .plan h3{font-size:1.32rem;font-weight:400;color:var(--fg)}", 1, "plan h3")
    h = sub(h, "font-size:1.25rem;color:var(--ink);",
            "font-size:1.25rem;color:var(--fg);", 1, "plan price")
    h = sub(h, "    color:var(--pine);text-decoration:none;white-space:nowrap;border-bottom:1px solid var(--accent);",
            "    color:var(--deep);text-decoration:none;white-space:nowrap;border-bottom:1px solid var(--accent);",
            1, "plan avail")
    h = sub(h, "  .suites-note{margin-top:2rem;font-size:.78rem;color:var(--fg-70)}\n", "",
            1, "suites note css")

    # ------------------------------------------------------------------
    # 10. Amenities. The pinned horizontal scroll scene becomes a plain grid.
    # ------------------------------------------------------------------
    h = sub(h, "  .amen{padding:0;position:relative;background:var(--pine)}",
            "  .amen{padding:0;position:relative;background:var(--deep)}", 1, "amen bg")
    h = sub(h, "  .amen-card{position:relative;max-width:600px;background:var(--pine);border:1px solid var(--hair);",
            "  .amen-card{position:relative;max-width:600px;background:var(--deep);border:1px solid var(--hair);",
            1, "amen card bg")
    h = sub(h, "  .amen-list li b{color:var(--linen);font-weight:500}",
            "  .amen-list li b{color:var(--fg);font-weight:500}", 1, "amen list b")
    h = sub(h,
            "  /* HORIZONTAL AMENITY GALLERY (pinned scene) */\n"
            "  .hscene{height:300vh;position:relative;margin-top:4rem}\n"
            "  .hsticky{position:sticky;top:0;height:100vh;overflow:hidden;display:flex;flex-direction:column;justify-content:center}\n"
            "  .hhead{max-width:1280px;width:100%;margin:0 auto;padding:0 2.4rem 2.2rem}\n"
            "  .htrack{display:flex;gap:2.2rem;padding:0 2.4rem;will-change:transform}\n"
            "  .hcard{flex:0 0 auto;width:min(62vw,860px)}\n"
            "  .hcard .frame img{min-height:0;aspect-ratio:2.18/1;width:100%}\n"
            "  .hscene.flat{height:auto;margin-top:3rem}\n"
            "  .hscene.flat .hsticky{position:static;height:auto;overflow:visible;display:block}\n"
            "  .hscene.flat .hhead{padding-bottom:1.6rem}\n"
            "  .hscene.flat .htrack{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:1fr;gap:2.4rem;transform:none!important;padding-bottom:4rem}\n"
            "  .hscene.flat .hcard{width:100%}\n",
            "  /* AMENITY GALLERY (flat grid; the pinned scroll scene was removed) */\n"
            "  .agal{margin-top:3.2rem;padding-bottom:4rem}\n"
            "  .ahead{max-width:1280px;width:100%;margin:0 auto;padding:0 2.4rem 1.8rem}\n"
            "  .agrid{max-width:1280px;margin:0 auto;padding:0 2.4rem;display:grid;\n"
            "    grid-template-columns:repeat(3,1fr);gap:2rem 1.6rem}\n"
            "  @media(max-width:1000px){.agrid{grid-template-columns:repeat(2,1fr)}}\n"
            "  @media(max-width:640px){.agrid{grid-template-columns:1fr}}\n"
            "  .acard .frame img{min-height:0;aspect-ratio:3/2;width:100%}\n",
            1, "gallery css")
    # caption strip under the full-bleed amenity render (markup 8)
    h = sub(h, "  @media(max-width:700px){.amen-card{margin:-8rem 1.2rem 0;padding:2rem}.amen-list{columns:1}}",
            "  @media(max-width:700px){.amen-card{margin:-8rem 1.2rem 0;padding:2rem}.amen-list{columns:1}}\n"
            "  .amen-shot{position:relative}\n"
            "  .amen-imgcap{position:absolute;left:2.4rem;bottom:1.1rem;z-index:3;max-width:60%}\n"
            "  .amen-imgcap .ph-cap{color:rgba(var(--cream-rgb),.9);\n"
            "    text-shadow:0 1px 10px rgba(var(--deep-2-rgb),.85)}\n"
            "  @media(max-width:700px){.amen-imgcap{left:1.2rem;bottom:.8rem;max-width:80%}}",
            1, "amen img caption")

    # ------------------------------------------------------------------
    # 11. Perks. Two cards now instead of three (markup 25).
    # ------------------------------------------------------------------
    h = sub(h, "  .presto h3{font-size:clamp(1.5rem,2.6vw,2.1rem);font-weight:380;color:var(--linen)}",
            "  .presto h3{font-size:clamp(1.35rem,2.35vw,1.9rem);font-weight:400;color:var(--fg)}",
            1, "presto h3")
    h = sub(h, "  .presto h3 em{font-style:italic;color:var(--accent)}",
            "  .presto h3 em{font-style:italic;color:var(--em)}", 1, "presto h3 em")
    h = sub(h, "  .perk-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4rem;margin-top:1.4rem}",
            "  .perk-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1.4rem;margin-top:1.4rem}",
            1, "perk grid")
    h = sub(h, "    background:linear-gradient(160deg,rgba(var(--cream-rgb),.035),transparent 55%);",
            "    background:rgba(255,255,255,.5);", 1, "perk bg")
    h = sub(h, "  .perk h3{font-size:1.4rem;font-weight:380}",
            "  .perk h3{font-size:1.28rem;font-weight:400}", 1, "perk h3")
    h = sub(h, "  .perk h3 em{font-style:italic;color:var(--accent)}",
            "  .perk h3 em{font-style:italic;color:var(--em)}", 1, "perk h3 em")
    h = sub(h, "  .logo-chip{background:var(--linen);padding:.55rem .9rem;display:inline-flex;align-items:center}",
            "  .logo-chip{background:#FFFFFF;border:1px solid var(--hair);padding:.55rem .9rem;\n"
            "    display:inline-flex;align-items:center}", 1, "logo chip")
    h = sub(h, "  .concierge-head h3{font-size:1.4rem;font-weight:380}",
            "  .concierge-head h3{font-size:1.28rem;font-weight:400}", 1, "concierge h3")
    h = sub(h, "  .concierge-head h3 em{font-style:italic;color:var(--accent)}",
            "  .concierge-head h3 em{font-style:italic;color:var(--em)}", 1, "concierge h3 em")
    h = sub(h, "  .step b{display:block;font-family:var(--serif);font-weight:420;font-size:1.05rem;margin-bottom:.3rem}",
            "  .step b{display:block;font-family:var(--serif);font-weight:700;font-size:.98rem;margin-bottom:.3rem}",
            1, "step b")
    h = sub(h, "  .perk-banner p{font-size:.95rem;color:var(--linen)}",
            "  .perk-banner p{font-size:.95rem;color:var(--fg)}", 1, "perk banner p")
    h = sub(h, "  .perk-banner p b{font-family:var(--serif);font-weight:420;color:var(--accent)}",
            "  .perk-banner p b{font-family:var(--serif);font-weight:700;color:var(--accent)}",
            1, "perk banner b")
    h = sub(h, "    color:var(--linen);text-decoration:none;border-bottom:1px solid var(--accent);padding-bottom:.2rem;white-space:nowrap}",
            "    color:var(--fg);text-decoration:none;border-bottom:1px solid var(--accent);padding-bottom:.2rem;white-space:nowrap}",
            1, "perk banner a")
    h = sub(h, "  .presto-cardbox small{font-size:.56rem;letter-spacing:.2em;text-transform:uppercase;color:var(--linen);font-weight:600;",
            "  .presto-cardbox small{font-size:.56rem;letter-spacing:.2em;text-transform:uppercase;color:var(--cream);font-weight:600;",
            1, "presto cardbox small")
    # the PRESTO card artwork follows the palette
    h = sub(h, "  .presto-card{width:150px;",
            "  .presto-card .pc-bg{fill:var(--deep-2);fill-opacity:.92}\n"
            "  .presto-card .pc-ln{stroke:var(--orange);fill:none}\n"
            "  .presto-card{width:150px;", 1, "presto card art")

    # ------------------------------------------------------------------
    # 12. Trust strip and marquee
    # ------------------------------------------------------------------
    h = sub(h, "  .trust{background:var(--ink);border-top:1px solid var(--hair)}",
            "  .trust{background:var(--deep-2);border-top:1px solid var(--hair)}", 1, "trust bg")
    h = sub(h, "    color:var(--linen);line-height:1.05;letter-spacing:-.005em;",
            "    color:var(--fg);line-height:1.05;letter-spacing:-.005em;", 1, "trust stats b")
    h = sub(h, "  .marq{overflow:hidden;background:var(--ink);",
            "  .marq{overflow:hidden;background:var(--deep);", 1, "marq bg")
    h = sub(h, "  .marq span em{font-family:var(--serif);font-style:italic;font-weight:380;text-transform:none;",
            "  .marq span em{font-family:var(--serif);font-style:italic;font-weight:400;text-transform:none;",
            1, "marq em")

    # ------------------------------------------------------------------
    # 13. Neighbourhood
    # ------------------------------------------------------------------
    h = sub(h,
            "  .hood{background:var(--linen);color:var(--ink)}\n"
            "  .hood .sec-eyebrow{color:var(--pine)}\n",
            "  /* copy the client still has open (markups 40 and 43) */\n"
            "  [data-copy-review]{position:relative;display:inline}\n"
            "  .copy-flag{display:inline-block;vertical-align:super;margin-left:.5rem;\n"
            "    font-family:var(--sans);font-size:.5rem;letter-spacing:.16em;text-transform:uppercase;\n"
            "    font-weight:600;color:var(--accent);border:1px solid var(--accent);\n"
            "    padding:.18rem .42rem;border-radius:2px;white-space:nowrap;line-height:1}\n",
            1, "hood overrides out")
    h = sub(h, "    line-height:1.28;max-width:26ch;color:var(--ink)}",
            "    line-height:1.3;max-width:30ch;color:var(--fg)}", 1, "hood quote")
    h = sub(h, "  .hood-quote em{font-style:italic;color:var(--pine)}",
            "  .hood-quote em{font-style:italic;color:var(--em)}", 1, "hood quote em")
    h = sub(h, "  .hood-quote{font-family:var(--serif);font-weight:340;font-size:clamp(1.7rem,3.6vw,2.9rem);",
            "  .hood-quote{font-family:var(--serif);font-weight:400;font-size:clamp(1.45rem,3vw,2.35rem);",
            1, "hood quote size")
    h = sub(h, "  .hood-card b{font-family:var(--serif);font-size:1.15rem;font-weight:420;display:block;margin-bottom:.6rem}",
            "  .hood-card b{font-family:var(--serif);font-size:1.05rem;font-weight:700;display:block;margin-bottom:.6rem}",
            1, "hood card b")
    h = sub(h, "    text-transform:uppercase;color:var(--pine);white-space:nowrap;font-variant-numeric:lining-nums;",
            "    text-transform:uppercase;color:var(--deep);white-space:nowrap;font-variant-numeric:lining-nums;",
            1, "walk")
    h = sub(h, "    .hood-card:hover .walk{background:var(--accent);color:var(--ink)}",
            "    .hood-card:hover .walk{background:var(--accent);color:var(--cream)}", 1, "walk hover")
    # placeholder neighbourhood card (markup 2)
    h = sub(h, "  .hood-txt{border-top:2px solid var(--accent);padding-top:1.1rem}",
            "  .hood-txt{border-top:2px solid var(--accent);padding-top:1.1rem}\n"
            "  .hood-card.is-ph .hood-shot{display:grid;place-items:center;min-height:0;aspect-ratio:3/2;\n"
            "    background:repeating-linear-gradient(135deg,rgba(var(--deep-rgb),.06) 0 12px,transparent 12px 24px);\n"
            "    border:1px solid var(--hair)}\n"
            "  .hood-card.is-ph .hood-txt{border-top-color:var(--hair)}\n"
            "  .hood-card.is-ph .hood-shot span{font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;\n"
            "    color:var(--fg-45);font-weight:600;text-align:center;padding:0 1.2rem}",
            1, "placeholder hood card")

    # ------------------------------------------------------------------
    # 14. Map
    # ------------------------------------------------------------------
    h = sub(h, "  .mapsec{padding:0;background:var(--pine)}",
            "  .mapsec{padding:0;background:var(--deep)}", 1, "mapsec bg")
    h = sub(h, "    border-top:1px solid var(--hair);border-bottom:1px solid var(--hair);overflow:hidden;background:var(--ink)}",
            "    border-top:1px solid var(--hair);border-bottom:1px solid var(--hair);overflow:hidden;background:var(--deep-2)}",
            1, "map shell bg")
    h = sub(h, "  .map-park{fill:#24463A;stroke:rgba(var(--cream-rgb),.06)}",
            "  .map-park{fill:rgba(var(--cream-rgb),.075);stroke:rgba(var(--cream-rgb),.06)}",
            1, "map park")
    h = sub(h, "  .poi:hover circle{fill:var(--linen)}",
            "  .poi:hover circle{fill:var(--cream)}", 1, "poi hover")
    h = sub(h, "  .site-marker text{fill:var(--ink);font-family:var(--serif);font-size:20px;font-weight:600;",
            "  .site-marker text{fill:var(--deep-2);font-family:var(--serif);font-size:17px;font-weight:700;",
            1, "site marker text")
    h = sub(h, "  .map-ctrl button:hover{background:var(--accent);color:var(--ink)}",
            "  .map-ctrl button:hover{background:var(--accent);color:var(--deep-2)}", 1, "map ctrl hover")
    h = sub(h, "  .map-card b{font-family:var(--serif);font-weight:420;font-size:1.1rem;color:var(--linen);",
            "  .map-card b{font-family:var(--serif);font-weight:700;font-size:1.02rem;color:var(--fg);",
            1, "map card b")
    h = sub(h, "  .chip{border:1px solid var(--hair);background:transparent;color:var(--linen);",
            "  .chip{border:1px solid var(--hair);background:transparent;color:var(--fg);", 1, "chip")
    h = sub(h, "  .chip.on{background:var(--accent);border-color:var(--accent);color:var(--ink)}\n"
               "  .chip.on span{color:var(--ink)}",
            "  .chip.on{background:var(--accent);border-color:var(--accent);color:var(--deep-2)}\n"
            "  .chip.on span{color:var(--deep-2)}", 1, "chip on")

    # ------------------------------------------------------------------
    # 15. Offer, form, footer
    # ------------------------------------------------------------------
    h = sub(h, "  .offer{text-align:center;border-top:1px solid var(--hair)}",
            "  .offer{text-align:center;border-top:1px solid var(--hair)}\n"
            "  .offer h2 em{color:var(--em)}", 1, "offer")
    h = sub(h,
            "  /* FORM */\n"
            "  .contact{background:var(--linen);color:var(--ink)}\n"
            "  .contact h2{color:var(--ink)}\n"
            "  .contact .sec-eyebrow{color:var(--pine)}\n"
            "  .contact .lede{color:var(--fg-70)}\n"
            "  .contact a{color:var(--ink)}\n",
            "  /* FORM */\n"
            "  .contact a{color:var(--fg)}\n",
            1, "contact overrides out")
    h = sub(h, "    color:var(--ink);margin-bottom:.45rem}",
            "    color:var(--fg);margin-bottom:.45rem}", 1, "label")
    h = sub(h, "    font-family:var(--sans);font-size:.95rem;color:var(--ink);transition:border-color .25s}",
            "    font-family:var(--sans);font-size:.95rem;color:var(--fg);transition:border-color .25s}",
            1, "input")
    h = sub(h, "  .form-done{display:none;background:var(--pine);color:var(--linen);",
            "  .form-done{display:none;background:var(--deep);color:var(--cream);", 1, "form done")
    h = sub(h, "  .form-done b{color:var(--accent);font-family:var(--serif);font-weight:400;font-size:1.2rem}",
            "  .form-done b{color:var(--orange);font-family:var(--serif);font-weight:700;font-size:1.15rem}",
            1, "form done b")
    # the body used to supply the dark ground; the footer must carry its own now
    h = sub(h, "  footer{position:relative;padding:4.5rem 2.4rem 0;overflow:hidden;border-top:1px solid var(--hair)}",
            "  footer{position:relative;padding:4.5rem 2.4rem 0;overflow:hidden;\n"
            "    background:var(--deep-2);border-top:1px solid var(--hair)}", 1, "footer bg")
    # The Nezam AI marketing credit, see tools/v2_flags.py.
    if NEZAM_CREDIT:
        # A fourth partner column (Nezam AI, marketing) makes the grid five wide.
        # The track ratios are tuned so no partner legal name wraps at 1280: the
        # PMT and BSaR columns get the extra room, the two text columns give it up.
        h = sub(h, "  .foot-grid{max-width:1280px;margin:0 auto;display:grid;"
                   "grid-template-columns:1.3fr 1fr 1fr 1fr;gap:2.5rem}",
                "  .foot-grid{max-width:1280px;margin:0 auto;display:grid;"
                "grid-template-columns:1.05fr 1.05fr .92fr 1.16fr .97fr;gap:2rem}", 1, "foot grid cols")
        # three marks of three different aspect ratios: centre them in a shared
        # box so they sit on one optical line instead of hanging from the label
        h = sub(h, "  .foot-lockup img{width:150px;margin-top:.7rem}\n"
                   "  .foot-lockup img.bsar{width:120px}",
                "  .foot-lockup>a{display:flex;align-items:center;min-height:58px;margin-top:.5rem}\n"
                "  .foot-lockup img{width:150px}\n"
                "  .foot-lockup img.bsar{width:120px}\n"
                "  .foot-lockup img.nezam{width:162px}", 1, "foot lockup marks")
        h = sub(h, "  @media(max-width:1000px){.foot-grid{grid-template-columns:1fr 1fr}}",
                "  @media(max-width:1180px){.foot-grid{grid-template-columns:repeat(3,1fr)}}\n"
                "  @media(max-width:820px){.foot-grid{grid-template-columns:1fr 1fr}}", 1, "foot grid mq")

    h = sub(h, "  .foot-giant{font-family:var(--serif);font-weight:380;font-size:clamp(4rem,13vw,11rem);line-height:.78;",
            "  .foot-giant{font-family:var(--serif);font-weight:700;font-size:clamp(3.4rem,12vw,10rem);line-height:.82;",
            1, "foot giant")

    # ------------------------------------------------------------------
    # 16. Palette switcher, print rules, reduced-motion cleanup
    # ------------------------------------------------------------------
    # the coordinate line is gone; the placeholder caption takes its place in
    # the reduced-motion opt-out so it is never left invisible
    h = sub(h, "    .hero-eyebrow,.hero-sub,.hero-ctas,.hero-coords,.hero-lockups{opacity:1}",
            "    .hero-eyebrow,.hero-sub,.hero-ctas,.hero-ph,.hero-lockups{opacity:1}",
            1, "reduced motion hero")
    h = sub(h, "    #hcv{display:none}\n    .hero-fallback{transform:none}\n    .hscene{height:auto}\n  }",
            "    #hcv{display:none}\n    .hero-fallback{transform:none}\n  }\n" + SWITCHER_CSS,
            1, "switcher css")

    return h


SWITCHER_CSS = '''
  /* ---- palette switcher (BSaR review aid, not a public control) ---- */
  .pal{position:fixed;left:1rem;bottom:1rem;z-index:70;display:flex;align-items:center;gap:.45rem;
    padding:.5rem .65rem;background:rgba(var(--deep-2-rgb),.86);border:1px solid rgba(var(--cream-rgb),.20);
    border-radius:999px;backdrop-filter:blur(8px);box-shadow:0 8px 26px rgba(0,0,0,.28)}
  .pal-lbl{font-family:var(--sans);font-size:.5rem;letter-spacing:.18em;text-transform:uppercase;
    font-weight:600;color:rgba(var(--cream-rgb),.62);margin-right:.15rem}
  .pal button{width:20px;height:20px;padding:0;border-radius:50%;cursor:pointer;
    border:1px solid rgba(var(--cream-rgb),.35);font:600 8px/1 var(--sans);color:transparent;
    transition:transform .2s var(--ease),box-shadow .2s var(--ease)}
  .pal button:hover{transform:scale(1.16)}
  .pal button[aria-pressed="true"]{box-shadow:0 0 0 2px rgba(var(--cream-rgb),.9);transform:scale(1.1)}
  .pal button[data-pal="A"]{background:#0032AD}
  .pal button[data-pal="B"]{background:#10069F}
  .pal button[data-pal="C"]{background:#480B6A}
  .pal button[data-pal="D"]{background:#512079}
  @media(max-width:560px){.pal{left:.6rem;bottom:.6rem;padding:.42rem .5rem;gap:.35rem}
    .pal button{width:17px;height:17px}
    .pal-lbl{display:none}}
  @media print{.pal{display:none}}
'''
