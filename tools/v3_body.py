#!/usr/bin/env python3
"""Markup layer of the v3 build. Imported by tools/apply_v3.py.

Claire Bodrug's 22 markups, submitted 8 to 10 September 2026 through the v2
review tool, plus the two decisions from the meeting of 8 September (no offers
before pre-leasing) and the 10 September rename to 1521.

Markup numbers in the comments match the numbered list in
Landing-Page-v3/Landing_Page_v3_Change_Log_2026-09-15.md.
"""

# ==========================================================================
#  NAV (markups 8, 17)
# ==========================================================================

OLD_NAV_WM = '''<nav id="nav" class="tone-deep">
  <a class="wordmark" href="#top">The <em>501</em></a>'''
NEW_NAV_WM = '''<nav id="nav" class="tone-deep">
  <a class="wordmark" href="#top" aria-label="1521, Luxury Rentals on Queen West">1521</a>'''


# ==========================================================================
#  HERO (markups 9, 10, 11, 12, 13, 14, 19, plus Coming Soon Summer 2027)
# ==========================================================================

OLD_HERO = '''  <div class="hero-inner">
    <div class="label hero-eyebrow">Queen West</div>
    <h1>
      <span class="line"><span>The <em>501</em></span></span>
      <span class="line"><span class="tagline">Premium Rentals on Queen West</span></span>
    </h1>
    <p class="hero-sub">Landmark rental living on Queen West. Studio to three bedroom residences at 1521 Queen Street West. Steps from the 501 streetcar, Roncesvalles Village and the waterfront.</p>
    <div class="hero-ctas">
      <a class="btn btn-solid btn-mag" href="#contact">Register Now</a>
      <a class="hero-tel" href="tel:+14164519499">Or call <b>416.451.9499</b> &#183; answered live, 24/7</a>
    </div>
    <div class="hero-lockups">
      <div class="lockup"><small>A Development By</small><img src="{{DU_5}}" alt="BS&#228;R Group of Companies"></div>
      <div class="lockup-sep"></div>
      <div class="lockup"><small>Leasing Management By</small><img class="tall" src="{{DU_6}}" alt="PMT Property Management Toronto"></div>
    </div>
  </div>'''

NEW_HERO = '''  <div class="hero-inner">
    <div class="wrap">
      <h1>
        <span class="wm-stack" role="img" aria-label="1521">
          <span class="wm-d" aria-hidden="true"><span>15</span></span>
          <span class="wm-d" aria-hidden="true"><span>21</span></span>
          <span class="wm-rule" aria-hidden="true"></span>
        </span>
        <span class="line"><span class="tagline">Luxury Rentals on Queen West</span></span>
      </h1>
      <p class="label hero-soon">Coming Soon Summer 2027</p>
      <p class="hero-sub">Ninety-five purpose-built residences at 1521 Queen Street West. Studio to three bedroom, steps from the 501 streetcar, Roncesvalles Village and the waterfront.</p>
      <div class="hero-ctas">
        <a class="btn btn-solid btn-mag" href="#contact">Register Now</a>
        <a class="hero-tel" href="tel:+14164519499">Or call <b>416.451.9499</b> &#183; answered live, 24/7</a>
      </div>
    </div>
  </div>'''


# ==========================================================================
#  OFFER BAND (meeting of 8 September: no offers before pre-leasing)
# ==========================================================================

OLD_OFFER_BAND = '''<div class="incentive tone-deep" id="offer-band">
  <span class="label">Founding Resident Offer</span>
  <p class="big">Up to <span class="num">2</span> months free on select suites, plus a <span class="num">$500</span> move-in credit, for leases signed by October <span class="num">31, 2026</span>.</p>
  <p class="fine">Select suites, subject to availability. Conditions apply.</p>
</div>

'''


# ==========================================================================
#  SUITES (markups 20, 21, 22)
# ==========================================================================

OLD_KICKER_P = '''    <p class="suites-kicker reveal" style="--d:.12s">33 different types of floor plans.</p>
'''

PLAN_NAMES = [
    ("The Elm", "Studio A"),
    ("The Beaty", "1 Bed A"),
    ("The Melbourne", "1 Bed + Den A"),
    ("The Cowan", "2 Bed A"),
    ("The Tyndall", "2 Bed 2 Bath A"),
    ("The Sunnyside", "3 Bed A"),
]

# markup 21: the unit mix is being rebuilt around 33 plan types, so the demo
# suite counts come off the cards with the names.
PLAN_SPECS = [
    ("Studio &#183; 1 Bath &#183; 380 to 420 sf &#183; 27 suites",
     "Studio &#183; 1 Bath &#183; 380 to 420 sf"),
    ("1 Bed &#183; 1 Bath &#183; 500 to 550 sf &#183; 27 suites",
     "1 Bed &#183; 1 Bath &#183; 500 to 550 sf"),
    ("2 Bed &#183; 1 Bath &#183; 700 to 750 sf &#183; 31 suites",
     "2 Bed &#183; 1 Bath &#183; 700 to 750 sf"),
    ("3 Bed &#183; 2 Bath &#183; 950 to 1,050 sf &#183; 10 suites",
     "3 Bed &#183; 2 Bath &#183; 950 to 1,050 sf"),
]


# ==========================================================================
#  AMENITIES (markup 16): the label box moves below the images
# ==========================================================================

AMEN_CARD = '''  <div class="amen-card reveal">
    <div class="label sec-eyebrow">Amenities</div>
    <h2 style="font-size:clamp(1.5rem,2.8vw,2.2rem)">Everything, right at <em>home.</em></h2>
    <ul class="amen-list">
      <li><b>Rooftop terrace</b> with skyline views</li>
      <li><b>Multipurpose Fitness Studio</b></li>
      <li><b>Ground-floor retail</b> at your door</li>
      <li><b>Automated Parcel Delivery</b></li>
      <li><b>Secure bike room</b> with repair stand</li>
      <li><b>Leasing line answered</b> by a person, any hour</li>
    </ul>
  </div>
'''


# ==========================================================================
#  MAP (markup 18): an All chip that restores every category
# ==========================================================================

OLD_CHIPS = '''    <span class="label fl">Filter By</span>
    <button class="chip on" data-cat="food">Food &amp; Drink<span></span></button>'''

NEW_CHIPS = '''    <span class="label fl">Filter By</span>
    <button class="chip all on" data-cat="all" type="button">All<span></span></button>
    <button class="chip on" data-cat="food">Food &amp; Drink<span></span></button>'''


# ==========================================================================
#  PERKS BANNER (meeting of 8 September)
# ==========================================================================

OLD_PERK_BANNER = '''    <div class="perk-banner reveal">
      <p><b>Founding Resident offer.</b> Up to 2 months free on select suites and a $500 move-in credit.</p>
      <a href="#contact">Register Now</a>
    </div>
'''


# ==========================================================================
#  CONTACT (markups 1, 2, 6, 15)
# ==========================================================================

OLD_SELECT = '''        <select id="st">
          <option>The Elm (Studio)</option><option>The Beaty (1 Bed)</option><option>The Melbourne (1 Bed + Den)</option>
          <option>The Cowan (2 Bed)</option><option>The Tyndall (2 Bed, 2 Bath)</option><option>The Sunnyside (3 Bed)</option>
        </select>'''

NEW_SELECT = '''        <select id="st">
          <option>Studio</option><option>1 Bedroom</option><option>1 Bedroom + Den</option>
          <option>2 Bedroom</option><option>2 Bedroom, 2 Bath</option><option>3 Bedroom</option>
          <option>Not sure yet</option>
        </select>'''


# ==========================================================================
#  FOOTER (markups 4, 5, 7)
# ==========================================================================

OLD_FOOT_TOP = '''    <div>
      <a class="wordmark" href="#top">The <em>501</em></a>
      <p style="margin-top:1rem">1521 Queen Street West<br>Toronto, Ontario<br>Registration site to be confirmed</p>
    </div>
    <div>
      <span class="label foot-label">Leasing</span>
      <p><a href="tel:+14164519499">416.451.9499</a>, answered 24/7<br>
      <a href="#contact">Register Now</a><br><a href="#offer">Founding Resident Program</a></p>
    </div>'''

NEW_FOOT_TOP = '''    <div>
      <a class="wordmark" href="#top" aria-label="1521, Luxury Rentals on Queen West">1521</a>
      <p style="margin-top:1rem">1521 Queen Street West<br>Toronto, Ontario M6R 1A5<br>Coming Soon Summer 2027</p>
      <p style="margin-top:.9rem">1521queenwest.ca<br><span class="ph-cap">Domain to be confirmed</span></p>
    </div>
    <div>
      <span class="label foot-label">Leasing</span>
      <p><a href="tel:+14164519499">416.451.9499</a>, answered 24/7<br>
      <a href="https://www.propertymanagementto.com" target="_blank" rel="noopener noreferrer">Property Management Toronto</a><br>
      <a href="#contact">Register Now</a><br><a href="/register/">Phase 1 Registration Page</a></p>
    </div>'''

OLD_LEGAL = '''    Demonstration concept prepared by Property Management Toronto Inc. for BS&#228;R Group of Companies. "The 501" is a working
    name under review. Imagery is placeholder and concept rendering and does not represent final architecture, finishes or views.'''

NEW_LEGAL = '''    Demonstration concept prepared by Property Management Toronto Inc. for BS&#228;R Group of Companies.
    Imagery is placeholder and concept rendering and does not represent final architecture, finishes or views.'''

OLD_LEGAL_PRICE = '''The PRESTO program is provided through the City of Toronto and is subject to program terms. Pricing shown is PMT's recommended
    pre-leasing matrix and is subject to change. E.&amp;O.E.'''

NEW_LEGAL_PRICE = '''The PRESTO program is provided through the City of Toronto and is subject to program terms. Suite mix, floor plan
    types, rents and the occupancy date are not final and are subject to change. E.&amp;O.E.'''


# ==========================================================================
#  PALETTE SWITCHER: A and B only, default B
# ==========================================================================

OLD_PAL_BTNS = '''  <button type="button" data-pal="A" aria-pressed="false" title="A: Pantone Saratoga Signature Blue">A</button>
  <button type="button" data-pal="B" aria-pressed="false" title="B: Pantone Blue 072 C">B</button>
  <button type="button" data-pal="C" aria-pressed="true" title="C: Pantone Deep Purple 2617 C">C</button>
  <button type="button" data-pal="D" aria-pressed="false" title="D: Pantone Purple PMS 3555 C">D</button>'''

NEW_PAL_BTNS = '''  <button type="button" data-pal="A" aria-pressed="false" title="A: Pantone Saratoga Signature Blue">A</button>
  <button type="button" data-pal="B" aria-pressed="true" title="B: Pantone Blue 072 C">B</button>'''


def run(h, sub, resub, cut_block):
    # ---- nav ------------------------------------------------------------
    h = sub(h, OLD_NAV_WM, NEW_NAV_WM, 1, "nav wordmark, markup 8")

    # ---- hero -----------------------------------------------------------
    h = sub(h, OLD_HERO, NEW_HERO,
            1, "hero rebuilt, markups 9 to 14 and 19")
    h = sub(h,
            'alt="Placeholder image: a purpose-built rental at blue hour on Queen Street West with a passing streetcar"',
            'alt="Placeholder render: a purpose-built rental at blue hour on Queen Street West with a passing streetcar"',
            1, "hero alt")

    # ---- offer band out -------------------------------------------------
    h = sub(h, OLD_OFFER_BAND, "", 1, "offer band out")

    # ---- about ----------------------------------------------------------
    h = sub(h, "The 501 is an eight-storey purpose-built rental",
            "1521 is an eight-storey purpose-built rental", 1, "about lede")

    # ---- suites ---------------------------------------------------------
    h = sub(h, OLD_KICKER_P, "", 1, "33 floor plan types line out, markup 22")
    for old, new in PLAN_NAMES:
        h = sub(h, "<h3>%s</h3>" % old, "<h3>%s</h3>" % new, 1,
                "plan name %s, markup 21" % old)
    for old, new in PLAN_SPECS:
        h = sub(h, old, new, 1, "plan spec, markup 21")
    h = resub(h,
              r'<div class="price"><b>\$[0-9,]+<small>Starting From / Month</small></b>',
              '<div class="price"><b>Pricing to be announced</b>',
              6, "rents out, markup 20")
    h = sub(h, '<a class="avail" href="#contact">Check Availability</a>',
            '<a class="avail" href="#contact">Register for Updates</a>',
            6, "availability link, markup 20")
    h = sub(h, '<p class="bedcount" id="bedcount" role="status">Showing all 6 floor plan types</p>',
            '<p class="bedcount" id="bedcount" role="status">Showing all 6 floor plan types</p>\n'
            '    <p class="suites-foot reveal">Floor plan types shown are indicative. The final set of 33 plan types is under review with BS&#228;R.</p>',
            1, "plan set note, markup 21")

    # ---- amenities: label box below the images (markup 16) --------------
    h = sub(h, AMEN_CARD, "", 1, "amenity box lifted, markup 16")
    h = sub(h, '  <div class="amen-tail"></div>',
            AMEN_CARD + '  <div class="amen-tail"></div>', 1,
            "amenity box dropped below the images, markup 16")

    # ---- neighbourhood (markup 17) --------------------------------------
    h = sub(h, '<div class="label sec-eyebrow reveal">Neighbourhood</div>',
            '<div class="label sec-eyebrow reveal">The Neighbourhood</div>', 1,
            "neighbourhood label, markup 17")

    # ---- map (markup 18) ------------------------------------------------
    h = sub(h, OLD_CHIPS, NEW_CHIPS, 1, "All chip, markup 18")

    # ---- perks ----------------------------------------------------------
    h = sub(h, "Every new resident at The 501 receives",
            "Every new resident at 1521 receives", 1, "presto copy")
    h = sub(h, OLD_PERK_BANNER, "", 1, "offer banner out")
    h = sub(h, "The 501 is leased and managed by Property Management Toronto",
            "1521 is leased and managed by Property Management Toronto", 1,
            "trust line")

    # ---- marquee --------------------------------------------------------
    h = sub(h, "<span>Now <em>Leasing</em></span>",
            "<span>Coming Soon <em>Summer 2027</em></span>", 2, "marquee leasing")
    h = sub(h, "<span>From $1,925 a <em>Month</em></span>",
            "<span>Luxury Rentals on Queen <em>West</em></span>", 2,
            "marquee rent out, markup 20")

    # ---- offer section out ----------------------------------------------
    h = cut_block(h, '<section class="offer" id="offer">', "</section>\n\n",
                  "offer section out")

    # ---- contact (markups 1, 2) -----------------------------------------
    h = sub(h, OLD_SELECT, NEW_SELECT, 1, "bedroom types only, markup 1")
    h = sub(h, '<label for="st">Suite Type</label>',
            '<label for="st">Bedroom Type</label>', 1, "field label, markup 1")
    h = sub(h,
            '<h2 class="reveal mask" style="--d:.08s"><span class="ln"><span>Register</span></span><span class="ln"><span><em>Now.</em></span></span></h2>',
            '<h2 class="reveal mask" style="--d:.08s"><span class="ln"><span>Register</span></span><span class="ln"><span><em>Now.</em></span></span></h2>\n'
            '    <p class="label soon-line reveal" style="--d:.12s">Coming Soon Summer 2027</p>',
            1, "coming soon by the form, markup 2")
    h = sub(h,
            'Tell us what you are looking for and the leasing team will respond the same day.',
            'Register for Phase 1 and you will be first to see floor plans, finishes and rents when they are released.',
            1, "registration lede")

    # ---- footer (markups 4, 5, 7) ---------------------------------------
    h = sub(h, OLD_FOOT_TOP, NEW_FOOT_TOP, 1, "footer leasing block, markups 4 and 7")
    h = sub(h, OLD_LEGAL, NEW_LEGAL, 1, "working name notice out, markup 5")
    h = sub(h, OLD_LEGAL_PRICE, NEW_LEGAL_PRICE, 1, "pricing legal line, markup 20")
    h = sub(h, '<div class="foot-giant" aria-hidden="true">THE 501</div>',
            '<div class="foot-giant" aria-hidden="true">1521</div>', 1,
            "footer watermark, markup 8")

    # ---- palette switcher -----------------------------------------------
    h = sub(h, OLD_PAL_BTNS, NEW_PAL_BTNS, 1, "palette switcher A and B only")

    return h
