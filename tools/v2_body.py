#!/usr/bin/env python3
"""Body/markup layer of the v2 build. Imported by tools/apply_v2.py.

Each block below is annotated with the Claire Bodrug markup number it answers.
"""

import re

from v2_flags import NEZAM_CREDIT


def run(h, sub, resub, cut_block):

    # ==================================================================
    # NAV  (markups 4, 5, 6, 7, 12, 23)
    # ==================================================================
    h = sub(h,
            '<nav id="nav">\n'
            '  <a class="wordmark" href="#top">Parkdale <em>House</em></a>\n'
            '  <div class="nav-links">\n'
            '    <a href="#suites">The Suites</a>\n'
            '    <a href="#amenities">The Amenities</a>\n'
            '    <a href="#neighbourhood">The Neighbourhood</a>\n'
            '    <a class="nav-tel" href="tel:+14164519499">416.451.9499</a>\n'
            '    <a class="nav-cta btn-mag" href="#contact">Book a Tour</a>\n'
            '  </div>\n'
            '</nav>',
            '<nav id="nav" class="tone-deep">\n'
            '  <a class="wordmark" href="#top">The <em>501</em></a>\n'
            '  <div class="nav-links">\n'
            '    <a href="#suites">Suites</a>\n'
            '    <a href="#amenities">Amenities</a>\n'
            '    <a href="#neighbourhood">Neighbourhood</a>\n'
            '    <a href="#perks">Residents</a>\n'
            '    <a class="nav-tel" href="tel:+14164519499">416.451.9499</a>\n'
            '    <a class="nav-cta btn-mag" href="#contact">Register Now</a>\n'
            '  </div>\n'
            '</nav>',
            1, "nav")

    # ==================================================================
    # HERO  (markups 12, 13, 14, 15, 16, 17, 23, 42)
    # ==================================================================
    h = sub(h, '<header class="hero" id="top">',
            '<header class="hero tone-deep" id="top">', 1, "hero tag")
    h = sub(h,
            'alt="Parkdale House at blue hour, seen from Queen and Lansdowne with a passing streetcar"',
            'alt="Placeholder image: a purpose-built rental at blue hour on Queen Street West with a passing streetcar"',
            1, "hero alt")
    h = sub(h,
            '    <div class="label hero-eyebrow">Now Leasing &#183; Queen &amp; Lansdowne</div>\n'
            '    <h1>\n'
            '      <span class="line"><span>Parkdale\'s</span></span>\n'
            '      <span class="line"><span><em>landmark</em> rental.</span></span>\n'
            '    </h1>\n'
            '    <p class="hero-sub">Ninety-five purpose-built residences at 1521 Queen Street West, from studios to three-bedroom suites. Steps from the 501 streetcar, Roncesvalles Village and the waterfront.</p>',
            '    <div class="label hero-eyebrow">Queen West</div>\n'
            '    <h1>\n'
            '      <span class="line"><span>The <em>501</em></span></span>\n'
            '      <span class="line"><span class="tagline">Premium Rentals on Queen West</span></span>\n'
            '    </h1>\n'
            '    <p class="hero-sub">Landmark rental living on Queen West. Studio to three bedroom residences at 1521 Queen Street West. Steps from the 501 streetcar, Roncesvalles Village and the waterfront.</p>',
            1, "hero copy")
    h = sub(h, '<a class="btn btn-solid btn-mag" href="#contact">Book a Tour</a>',
            '<a class="btn btn-solid btn-mag" href="#contact">Register Now</a>', 1, "hero cta")
    h = sub(h, '<div class="lockup"><small>Leased &amp; Managed By</small>',
            '<div class="lockup"><small>Leasing Management By</small>', 1, "hero lockup")
    h = sub(h,
            '  <div class="hero-coords">43.6389&#176; N &#183; 79.4426&#176; W &#183; Parkdale, Toronto</div>\n',
            '  <div class="ph-cap hero-ph">Placeholder. Hero photography to come.</div>\n',
            1, "hero coords out")

    # ==================================================================
    # INCENTIVE BAND  (renamed to match the Register Now CTA)
    # ==================================================================
    h = sub(h, '<div class="incentive" id="offer-band">',
            '<div class="incentive tone-deep" id="offer-band">', 1, "incentive tag")

    # ==================================================================
    # STATS BAND removed entirely  (markup 18)
    # ==================================================================
    h = cut_block(h, '<div class="stats">', '</div>\n\n<section id="about">',
                  "stats band")
    # that cut swallowed the opening tag of #about, so put it back
    h = sub(h, '</div>\n\n\n  <div class="wrap split">',
            '</div>\n\n<section id="about">\n  <div class="wrap split">',
            1, "about reopen")

    # ==================================================================
    # ABOUT  (markup 27: "The Building" becomes "The Suites")
    # ==================================================================
    h = sub(h, '      <div class="label sec-eyebrow reveal">The Building</div>',
            '      <div class="label sec-eyebrow reveal">The Suites</div>', 1, "about eyebrow")
    h = sub(h,
            '<h2 class="reveal mask" style="--d:.08s"><span class="ln"><span>A house for the</span></span><span class="ln"><span><em>neighbourhood.</em></span></span></h2>',
            '<h2 class="reveal mask" style="--d:.08s"><span class="ln"><span>Built for the long</span></span><span class="ln"><span><em>stay.</em></span></span></h2>',
            1, "about h2")
    h = sub(h,
            'Parkdale House is an eight-storey purpose-built rental at 1521 Queen Street West, designed as a rental from the first drawing.',
            'The 501 is an eight-storey purpose-built rental at 1521 Queen Street West, designed as a rental from the first drawing.',
            1, "about lede")
    h = sub(h,
            'alt="Two-bedroom suite living room with oak floors, walnut kitchen and the red brick church across the street"',
            'alt="Concept rendering: a two bedroom suite living room with oak floors, a walnut kitchen and the red brick church across the street"',
            1, "about img alt")

    # ==================================================================
    # SUITES  (markups 5, 19, 20, 31, 32, 33, 34, 35)
    # ==================================================================
    h = sub(h,
            '    <div class="label sec-eyebrow reveal">The Suites</div>\n'
            '    <h2 class="reveal mask" style="--d:.08s"><span class="ln"><span>Six floorplans, studios</span></span><span class="ln"><span>to <em>three bedrooms.</em></span></span></h2>\n'
            '    <p class="lede reveal" style="--d:.16s">Forty-three percent of Parkdale House is two- and three-bedroom suites, the inventory in shortest supply in the west end. Every residence includes in-suite laundry, four stainless appliances, stone countertops and oversized windows.</p>\n'
            '    <div class="plan-grid">',
            '    <div class="label sec-eyebrow reveal">Floor Plans</div>\n'
            '    <h2 class="reveal mask" style="--d:.08s"><span class="ln"><span>Elevated Living on</span></span><span class="ln"><span><em>Queen West.</em></span></span></h2>\n'
            '    <p class="suites-kicker reveal" style="--d:.12s">33 different types of floor plans.</p>\n'
            '    <p class="lede reveal" style="--d:.16s">Suites built for how you live. Every residence features in-suite laundry, stainless steel Whirlpool appliances, granite countertops, and a private storage locker.</p>\n'
            '    <p class="suites-foot reveal" style="--d:.2s">Locker per suite to be confirmed.</p>\n'
            '    <div class="bedfilter reveal" style="--d:.24s" role="group" aria-label="Filter floor plans by bedroom type">\n'
            '      <span class="label fl">Filter By</span>\n'
            '      <button class="bedbtn" type="button" data-bedfilter="all" aria-pressed="true">All</button>\n'
            '      <button class="bedbtn" type="button" data-bedfilter="studio" aria-pressed="false">Studio</button>\n'
            '      <button class="bedbtn" type="button" data-bedfilter="1" aria-pressed="false">1 Bed</button>\n'
            '      <button class="bedbtn" type="button" data-bedfilter="2" aria-pressed="false">2 Bed</button>\n'
            '      <button class="bedbtn" type="button" data-bedfilter="3" aria-pressed="false">3 Bed</button>\n'
            '    </div>\n'
            '    <p class="bedcount" id="bedcount" role="status">Showing all 6 floor plan types</p>\n'
            '    <div class="plan-grid" id="plangrid">',
            1, "suites head")

    # tag each plan card with its bedroom type, in DOM order
    beds = ["studio", "1", "1", "2", "2", "3"]
    seen = {"n": 0}

    def tag(m):
        b = beds[seen["n"]]
        seen["n"] += 1
        return '<div class="plan reveal" data-bed="%s" style="--d:%s">' % (b, m.group(1))

    h = resub(h, r'<div class="plan reveal" style="--d:([^"]+)">', tag, 6, "plan data-bed")

    # 3D suite tours placeholder (markup 19), and the pre-leasing note goes (34, 35)
    h = sub(h,
            '    <p class="suites-note reveal">Pre-leasing rates. Suite counts are combined within each plan family; 14 of the 95 suites are barrier-free. Floorplans and availability are released to the Priority Waitlist first.</p>\n',
            '    <div class="tours reveal">\n'
            '      <div class="tours-copy">\n'
            '        <h3>Walk every suite, <em>before it is built.</em></h3>\n'
            '        <p>3D suite tours coming soon. Matterport walkthroughs of each floor plan type will be published here as the model suites are completed.</p>\n'
            '      </div>\n'
            '      <div class="tours-frame">\n'
            '        <div>\n'
            '          <svg viewBox="0 0 48 48" aria-hidden="true">\n'
            '            <path d="M24 4 L42 14 L42 34 L24 44 L6 34 L6 14 Z"/>\n'
            '            <path d="M24 4 L24 24 M24 24 L42 14 M24 24 L6 14 M24 24 L24 44"/>\n'
            '          </svg>\n'
            '          <span class="ph-cap">3D suite tours coming soon</span>\n'
            '        </div>\n'
            '      </div>\n'
            '    </div>\n',
            1, "suite tours")

    # ==================================================================
    # AMENITIES  (markups 1, 6, 8, 9, 10, 11, 21, 36, 37)
    # ==================================================================
    h = sub(h, '<section class="amen" id="amenities">',
            '<section class="amen tone-deep" id="amenities">', 1, "amen tag")
    h = sub(h,
            '  <div class="amen-img" role="img" aria-label="Rooftop terrace at golden hour with lounge seating and the downtown skyline"></div>\n',
            '  <div class="amen-shot">\n'
            '    <div class="amen-img" role="img" aria-label="Placeholder render: rooftop terrace at golden hour with lounge seating and the downtown skyline"></div>\n'
            '    <div class="amen-imgcap"><span class="ph-cap">Placeholder render. Final rendering by Truong Ly.</span></div>\n'
            '  </div>\n',
            1, "amen render caption")
    h = sub(h,
            '    <div class="label sec-eyebrow">The Amenities</div>\n'
            '    <h2 style="font-size:clamp(1.7rem,3vw,2.4rem)">Beyond your <em>front door.</em></h2>\n'
            '    <ul class="amen-list">\n'
            '      <li><b>Rooftop terrace</b> with skyline views</li>\n'
            '      <li><b>Fitness studio</b> with strength and cardio zones</li>\n'
            '      <li><b>Co-working lounge</b> for residents</li>\n'
            '      <li><b>Ground-floor retail</b> at your door</li>\n'
            '      <li><b>Parcel and cold storage</b></li>\n'
            '      <li><b>Secure bike room</b> with repair stand</li>\n'
            '      <li><b>Pet wash station</b></li>\n'
            '      <li><b>Leasing line answered</b> by a person, any hour</li>\n'
            '    </ul>',
            '    <div class="label sec-eyebrow">Amenities</div>\n'
            '    <h2 style="font-size:clamp(1.5rem,2.8vw,2.2rem)">Everything, right at <em>home.</em></h2>\n'
            '    <ul class="amen-list">\n'
            '      <li><b>Rooftop terrace</b> with skyline views</li>\n'
            '      <li><b>Multipurpose Fitness Studio</b></li>\n'
            '      <li><b>Ground-floor retail</b> at your door</li>\n'
            '      <li><b>Automated Parcel Delivery</b></li>\n'
            '      <li><b>Secure bike room</b> with repair stand</li>\n'
            '      <li><b>Leasing line answered</b> by a person, any hour</li>\n'
            '    </ul>',
            1, "amen list")

    # pinned horizontal scene becomes a flat grid; the co-working card goes (markup 11)
    h = sub(h,
            '  <div class="hscene" id="hscene">\n'
            '    <div class="hsticky">\n'
            '      <div class="hhead">\n'
            '        <div class="label sec-eyebrow reveal">The Amenity Floor</div>\n'
            '        <h2 class="reveal" style="--d:.08s;font-size:clamp(1.7rem,3vw,2.4rem)">Toured like a <em>hotel.</em></h2>\n'
            '      </div>\n'
            '      <div class="htrack" id="htrack">\n'
            '        <div class="hcard">\n'
            '          <div class="frame" data-cursor="View"><img src="{{DU_8}}" alt="Boutique lobby with limestone feature wall, wood slat ceiling and brass mailboxes"></div>\n'
            '          <div class="frame-caption"><span>Lobby &#183; Ground Floor</span><span>Concept Rendering</span></div>\n'
            '        </div>\n'
            '        <div class="hcard">\n'
            '          <div class="frame" data-cursor="View"><img src="{{DU_9}}" alt="Fitness studio with pine-green feature wall, brass dumbbell rack and glass wall"></div>\n'
            '          <div class="frame-caption"><span>Fitness Studio &#183; Level 2</span><span>Concept Rendering</span></div>\n'
            '        </div>\n'
            '        <div class="hcard">\n'
            '          <div class="frame" data-cursor="View"><img src="{{DU_10}}" alt="Co-working lounge with long oak table, linen chairs and brass library lamps"></div>\n'
            '          <div class="frame-caption"><span>Co-Working Lounge &#183; Level 2</span><span>Concept Rendering</span></div>\n'
            '        </div>\n'
            '        <div class="hcard">\n'
            '          <div class="frame" data-cursor="View"><img src="{{DU_11}}" alt="Secure bike room with two-tier brass-railed racks and repair bench"></div>\n'
            '          <div class="frame-caption"><span>Bike Room &#183; Level P1</span><span>Concept Rendering</span></div>\n'
            '        </div>\n'
            '      </div>\n'
            '    </div>\n'
            '  </div>',
            '  <div class="agal">\n'
            '    <div class="ahead">\n'
            '      <div class="label sec-eyebrow reveal">The Amenities</div>\n'
            '      <h2 class="reveal" style="--d:.08s;font-size:clamp(1.5rem,2.8vw,2.2rem)">Amenity space you use, <em>every week.</em></h2>\n'
            '    </div>\n'
            '    <div class="agrid">\n'
            '      <div class="acard reveal-img">\n'
            '        <div class="frame"><img src="{{DU_8}}" alt="Concept rendering: boutique lobby with a limestone feature wall, wood slat ceiling and mailboxes"></div>\n'
            '        <div class="frame-caption"><span>Lobby &#183; Ground Floor</span><span>Concept Rendering</span></div>\n'
            '      </div>\n'
            '      <div class="acard reveal-img" style="--d:.08s">\n'
            '        <div class="frame"><img src="{{DU_9}}" alt="Concept rendering: multipurpose fitness studio with a feature wall, dumbbell rack and glass wall"></div>\n'
            '        <div class="frame-caption"><span>Fitness Studio &#183; Level 2</span><span>Concept Rendering</span></div>\n'
            '      </div>\n'
            '      <div class="acard reveal-img" style="--d:.16s">\n'
            '        <div class="frame"><img src="{{DU_11}}" alt="Concept rendering: secure bike room with two-tier racks and a repair bench"></div>\n'
            '        <div class="frame-caption"><span>Bike Room &#183; Level P1</span><span>Concept Rendering</span></div>\n'
            '      </div>\n'
            '    </div>\n'
            '  </div>',
            1, "amenity gallery")

    # ==================================================================
    # NEIGHBOURHOOD  (markups 2, 7, 22, 38, 39, 43)
    # ==================================================================
    h = sub(h, '    <div class="label sec-eyebrow reveal">The Neighbourhood</div>',
            '    <div class="label sec-eyebrow reveal">Neighbourhood</div>', 1, "hood eyebrow")
    h = sub(h,
            '    <p class="hood-quote reveal" style="--d:.1s">Parkdale keeps the scale, the storefronts and the daily rhythm of the <em>old city.</em></p>',
            '    <p class="hood-quote reveal" style="--d:.1s"><span data-copy-review>Queen West sets the pace at street level: independent storefronts, the streetcar at the curb, the lake fifteen minutes <em>south.</em></span><span class="copy-flag">Copy under review</span></p>',
            1, "hood quote copy")
    # streetcar card title (markup 22)
    h = sub(h, '<div class="hood-txt"><b>501 Queen streetcar</b><span class="walk">At the door</span>',
            '<div class="hood-txt"><b>Your stop on Queen West</b><span class="walk">At the door</span>',
            1, "streetcar card")
    # the card Claire flagged for replacement (markup 2)
    h = sub(h,
            '      <div class="hood-card reveal-img" style="--d:.1s">\n'
            '        <div class="hood-shot"><img src="{{DU_19}}" alt="Illustrative image: a low-rise main street of independent shopfronts, awnings and street trees"></div>\n'
            '        <div class="hood-txt"><b>Roncesvalles Village</b><span class="walk">12 min walk</span><p>Cafes, bakeries and the Revue Cinema, one streetcar stop west.</p></div>\n'
            '      </div>\n',
            '      <div class="hood-card is-ph reveal-img" style="--d:.1s">\n'
            '        <div class="hood-shot"><span>Neighbourhood photography to come</span></div>\n'
            '        <div class="hood-txt"><b>Neighbourhood photography to come</b><span class="walk">To be confirmed</span><p>Card to be replaced with a neighbourhood amenity of BSaR\'s choosing, using the captured photography.</p></div>\n'
            '      </div>\n',
            1, "placeholder hood card")
    # Queen West Retail (markups 38, 39)
    h = sub(h,
            '<div class="hood-txt"><b>Queen West at street level</b><span class="walk">Out the door</span><p>Parkdale\'s independent restaurants, galleries and shops line the block.</p></div>',
            '<div class="hood-txt"><b>Queen West Retail</b><span class="walk">Out the door</span></div>',
            1, "queen west retail")
    h = sub(h,
            'alt="Illustrative image: a west-end street at eye level, independent storefronts and low-rise brick facades"',
            'alt="Illustrative image: a Queen West street at eye level, independent storefronts and low-rise brick facades"',
            1, "hood alt 6")

    # ==================================================================
    # MAP  (markup 40)
    # ==================================================================
    h = sub(h, '<section class="mapsec" id="map">',
            '<section class="mapsec tone-deep" id="map">', 1, "map tag")
    h = sub(h,
            '<h2 class="reveal mask" style="--d:.08s"><span class="ln"><span>The neighbourhood,</span></span><span class="ln"><span><em>mapped.</em></span></span></h2>',
            '<h2 class="reveal" style="--d:.08s"><span data-copy-review>Queen West, <em>mapped.</em></span><span class="copy-flag">Copy under review</span></h2>',
            1, "map h2")
    h = sub(h,
            'aria-label="Interactive neighbourhood map of Parkdale around 1521 Queen Street West"',
            'aria-label="Interactive neighbourhood map of Queen West around 1521 Queen Street West"',
            1, "map aria")
    h = sub(h, "el('text', {y:7}, sm).textContent = 'PH';",
            "el('text', {y:6}, sm).textContent = '501';", 1, "map site marker")

    # ==================================================================
    # MOVE Neighbourhood + Map above Resident Perks  (markups 3 and 30)
    # ==================================================================
    start = h.find('<section class="hood" id="neighbourhood">')
    end = h.find('<section class="offer" id="offer">')
    if start == -1 or end == -1 or end < start:
        raise SystemExit("apply_v2: cannot locate the neighbourhood block to move")
    block = h[start:end]
    h = h[:start] + h[end:]
    anchor = '<section id="perks">'
    if h.count(anchor) != 1:
        raise SystemExit("apply_v2: #perks anchor is not unique")
    h = h.replace(anchor, block + anchor, 1)

    # ==================================================================
    # RESIDENT PERKS -> RESIDENTS  (markups 4, 24, 25, 30)
    # ==================================================================
    h = sub(h, '    <div class="label sec-eyebrow reveal">Resident Perks</div>',
            '    <div class="label sec-eyebrow reveal">Residents</div>', 1, "perks eyebrow")
    h = sub(h,
            '        <h3>Three months of transit, <em>included.</em></h3>\n'
            '        <p>Every new Parkdale House resident receives a 3-month PRESTO pass, provided through the City of Toronto\'s new-resident transit program. The 501 streetcar stops at the corner; King Street, the Financial District and the waterfront are a direct ride.</p>',
            '        <h3>Transit, <em>included.</em></h3>\n'
            '        <p>Every new resident at The 501 receives a pre-loaded PRESTO card, value to be confirmed, provided through the City of Toronto\'s new-resident transit program. The 501 streetcar stops at the corner; King Street, the Financial District and the waterfront are a direct ride.</p>',
            1, "presto copy")
    h = sub(h, 'alt="TTC streetcar passing the front of Parkdale House on Queen Street at dusk"',
            'alt="Illustrative image: a TTC streetcar passing the front of the building on Queen Street at dusk"',
            1, "presto img alt")
    h = sub(h, '          <small>3-Month PRESTO Pass<br>Every New Resident</small>',
            '          <small>Pre-Loaded PRESTO Card<br>Every New Resident</small>', 1, "presto card label")
    # PRESTO card artwork now follows the palette
    h = sub(h,
            '            <rect x="4" y="4" width="332" height="208" rx="18" fill="var(--deep-2)" fill-opacity=".55" stroke="var(--accent)" stroke-width="2.5"/>\n'
            '            <rect x="30" y="86" width="52" height="40" rx="7" fill="none" stroke="var(--accent)" stroke-width="2"/>\n'
            '            <path d="M46 86 L46 126 M66 86 L66 126 M30 106 L82 106" stroke="var(--accent)" stroke-width="1.2" opacity=".7"/>\n'
            '            <path d="M266 46 A26 26 0 0 1 292 72" fill="none" stroke="var(--accent)" stroke-width="2.2" opacity=".9"/>\n'
            '            <path d="M256 56 A16 16 0 0 1 272 72" fill="none" stroke="var(--accent)" stroke-width="2.2" opacity=".65"/>\n'
            '            <path d="M246 66 A6 6 0 0 1 252 72" fill="none" stroke="var(--accent)" stroke-width="2.2" opacity=".4"/>\n'
            '            <path d="M30 156 L118 156 M30 172 L94 172" stroke="var(--accent)" stroke-width="3" opacity=".55" stroke-linecap="round"/>\n'
            '            <path d="M232 176 L310 176" stroke="var(--accent)" stroke-width="3" opacity=".8" stroke-linecap="round"/>',
            '            <rect class="pc-bg" x="4" y="4" width="332" height="208" rx="18" stroke-width="2.5"/>\n'
            '            <rect class="pc-ln" x="30" y="86" width="52" height="40" rx="7" stroke-width="2"/>\n'
            '            <path class="pc-ln" d="M46 86 L46 126 M66 86 L66 126 M30 106 L82 106" stroke-width="1.2" opacity=".7"/>\n'
            '            <path class="pc-ln" d="M266 46 A26 26 0 0 1 292 72" stroke-width="2.2" opacity=".9"/>\n'
            '            <path class="pc-ln" d="M256 56 A16 16 0 0 1 272 72" stroke-width="2.2" opacity=".65"/>\n'
            '            <path class="pc-ln" d="M246 66 A6 6 0 0 1 252 72" stroke-width="2.2" opacity=".4"/>\n'
            '            <path class="pc-ln" d="M30 156 L118 156 M30 172 L94 172" stroke-width="3" opacity=".55" stroke-linecap="round"/>\n'
            '            <path class="pc-ln" d="M232 176 L310 176" stroke-width="3" opacity=".8" stroke-linecap="round"/>',
            1, "presto card art")
    # remove the "professional management" perk (markup 25)
    h = sub(h,
            '      <div class="perk reveal" style="--d:.15s">\n'
            '        <h3>Professional management, <em>around the clock.</em></h3>\n'
            '        <p>Report a leak at midnight and a person picks up, not a voicemail box. Every request is logged in writing and tracked to close, and rent, documents and receipts live in the same resident portal.</p>\n'
            '        <div class="perk-logos"><span class="logo-chip tall"><img src="{{DU_16}}" alt="PMT Property Management Toronto"></span></div>\n'
            '      </div>\n',
            '',
            1, "remove management perk")
    h = sub(h, '      <a href="#offer">Founding Resident Program</a>',
            '      <a href="#contact">Register Now</a>', 1, "perk banner link")

    # ==================================================================
    # TRUST STRIP  (markups 26 and 42)
    # ==================================================================
    h = sub(h, '<section class="trust">', '<section class="trust tone-deep">', 1, "trust tag")
    h = sub(h,
            '      <span class="label foot-label" style="color:var(--accent)">Leased &amp; Managed By</span>',
            '      <span class="label foot-label" style="color:var(--accent)">Leasing Management By</span>',
            1, "trust lockup")
    h = sub(h,
            'Parkdale House is leased and managed by Property Management Toronto, managing rental homes across the city since 2011.',
            'The 501 is leased and managed by Property Management Toronto, managing rental homes across the city since 2011.',
            1, "trust fine")

    # ==================================================================
    # MARQUEE  (pet wash removed with markup 36, name and corner updated)
    # ==================================================================
    old_marq = ('<span>Now <em>Leasing</em></span><span>Queen &amp; Lansdowne</span>'
                '<span>501 Streetcar at the <em>Door</em></span><span>Studios to 3 Bedrooms</span>'
                '<span>Answered 24/7 by a <em>Person</em></span><span>Pet Wash Station</span>'
                '<span>From $1,925 a <em>Month</em></span>')
    new_marq = ('<span>Now <em>Leasing</em></span><span>Queen West</span>'
                '<span>501 Streetcar at the <em>Door</em></span><span>Studio to 3 Bedroom</span>'
                '<span>Answered 24/7 by a <em>Person</em></span><span>Automated Parcel Delivery</span>'
                '<span>From $1,925 a <em>Month</em></span>')
    h = sub(h, old_marq, new_marq, 2, "marquee")
    h = sub(h, '<div class="marq" aria-hidden="true">',
            '<div class="marq tone-deep" aria-hidden="true">', 1, "marq tag")

    # ==================================================================
    # OFFER SECTION  (CTA wording, markup 23)
    # ==================================================================
    h = sub(h, '<a class="btn btn-solid btn-mag reveal" href="#contact">Book a Tour</a>',
            '<a class="btn btn-solid btn-mag reveal" href="#contact">Register Now</a>', 1, "offer cta")
    h = sub(h, 'Join the Priority Waitlist before public launch. Founding Residents receive first access to floorplans, view suites and pre-leasing rates.',
            'Register before public launch. Founding Residents receive first access to floor plans, view suites and pre-leasing rates.',
            1, "offer lede")
    h = sub(h, '<small>Floorplans, view suites and pre-leasing rates are released to the waitlist before public launch.</small>',
            '<small>Floor plans, view suites and pre-leasing rates are released to registrants before public launch.</small>',
            1, "offer perk 1")
    h = sub(h, 'alt="The wood-canopied entrance of Parkdale House at evening, with the 1521 address plate"',
            'alt="Concept rendering: the wood-canopied entrance at evening, with the 1521 address plate"',
            1, "arrive alt")

    # ==================================================================
    # CONTACT  (markups 23 and 41)
    # ==================================================================
    h = sub(h,
            '    <div class="label sec-eyebrow reveal">Book a Tour</div>\n'
            '    <h2 class="reveal mask" style="--d:.08s"><span class="ln"><span>See the corner</span></span><span class="ln"><span>for <em>yourself.</em></span></span></h2>',
            '    <div class="label sec-eyebrow reveal">Registration</div>\n'
            '    <h2 class="reveal mask" style="--d:.08s"><span class="ln"><span>Register</span></span><span class="ln"><span><em>Now.</em></span></span></h2>',
            1, "contact head")
    h = sub(h, '<div class="full"><button class="btn btn-mag" style="border-color:var(--ink);color:var(--ink)" type="submit">Book a Tour</button></div>',
            '<div class="full"><button class="btn btn-solid btn-mag" type="submit">Register Now</button></div>',
            1, "contact submit")
    h = sub(h, '<div class="form-done" id="done">',
            '<div class="form-done tone-deep" id="done">', 1, "form done tag")

    # ==================================================================
    # FOOTER  (markups 12, 26, 28, 29, 42)
    # ==================================================================
    h = sub(h, '<footer>', '<footer class="tone-deep">', 1, "footer tag")
    h = sub(h,
            '      <a class="wordmark" href="#top">Parkdale <em>House</em></a>\n'
            '      <p style="margin-top:1rem">1521 Queen Street West<br>Toronto, Ontario<br>parkdalehouse.ca</p>',
            '      <a class="wordmark" href="#top">The <em>501</em></a>\n'
            '      <p style="margin-top:1rem">1521 Queen Street West<br>Toronto, Ontario<br>Registration site to be confirmed</p>',
            1, "footer wordmark")
    h = sub(h,
            '      <p><a href="tel:+14164519499">416.451.9499</a>, answered 24/7<br>\n'
            '      <a href="#contact">Book a Tour</a><br><a href="#offer">Founding Resident Program</a></p>',
            '      <p><a href="tel:+14164519499">416.451.9499</a>, answered 24/7<br>\n'
            '      <a href="#contact">Register Now</a><br><a href="#offer">Founding Resident Program</a></p>',
            1, "footer leasing")
    h = sub(h,
            '      <span class="label foot-label">A Development By</span>\n'
            '      <img class="bsar" src="{{DU_25}}" alt="BS&#228;R Group of Companies">\n'
            '      <p style="margin-top:.6rem;font-size:.75rem">BS&#228;R Group of Companies</p>',
            '      <span class="label foot-label">A Development By</span>\n'
            '      <a href="https://www.bsargroup.com" target="_blank" rel="noopener noreferrer">\n'
            '        <img class="bsar" src="{{DU_25}}" alt="BS&#228;R Group of Companies"></a>\n'
            '      <p style="margin-top:.6rem;font-size:.75rem"><a href="https://www.bsargroup.com" target="_blank" rel="noopener noreferrer">BS&#228;R Group of Companies</a></p>',
            1, "footer bsar link")
    h = sub(h,
            '      <span class="label foot-label">Leased &amp; Managed By</span>\n'
            '      <img src="{{DU_26}}" alt="PMT Property Management Toronto">\n'
            '      <p style="margin-top:.6rem;font-size:.75rem">Property Management Toronto Inc.<br>PMT Realty Inc., Brokerage</p>',
            '      <span class="label foot-label">Leasing Management By</span>\n'
            '      <a href="https://www.propertymanagementto.com" target="_blank" rel="noopener noreferrer">\n'
            '        <img src="{{DU_26}}" alt="PMT Property Management Toronto"></a>\n'
            '      <p style="margin-top:.6rem;font-size:.75rem"><a href="https://www.propertymanagementto.com" target="_blank" rel="noopener noreferrer">Property Management Toronto Inc.</a><br>PMT Realty Inc., Brokerage</p>',
            1, "footer pmt link")

    # Nezam AI took the project marketing over in Sept 2026, so it carries a
    # partner credit beside the developer and the manager. Placeholder wording
    # until the scope line is settled. Off by Ahmed's call on 2026-09-07; see
    # tools/v2_flags.py.
    if NEZAM_CREDIT:
        h = sub(h,
                '      <p style="margin-top:.6rem;font-size:.75rem"><a href="https://www.propertymanagementto.com" '
                'target="_blank" rel="noopener noreferrer">Property Management Toronto Inc.</a><br>'
                'PMT Realty Inc., Brokerage</p>\n'
                '    </div>\n',
                '      <p style="margin-top:.6rem;font-size:.75rem"><a href="https://www.propertymanagementto.com" '
                'target="_blank" rel="noopener noreferrer">Property Management Toronto Inc.</a><br>'
                'PMT Realty Inc., Brokerage</p>\n'
                '    </div>\n'
                '    <div class="foot-lockup">\n'
                '      <span class="label foot-label">Marketing By</span>\n'
                '      <a href="https://nezamai.com" target="_blank" rel="noopener noreferrer">\n'
                '        <img class="nezam" src="{{NEZAM_LOCKUP}}" alt="Nezam AI"></a>\n'
                '      <p style="margin-top:.6rem;font-size:.75rem">'
                '<a href="https://nezamai.com" target="_blank" rel="noopener noreferrer">Nezam AI Consulting</a></p>\n'
                '    </div>\n',
                1, "footer nezam credit")
    h = sub(h,
            '    Demonstration concept prepared by Property Management Toronto Inc. for BS&#228;R Group of Companies. "Parkdale House" is a working\n'
            '    name for demonstration purposes. Imagery is concept rendering and does not represent final architecture, finishes or views.',
            '    Demonstration concept prepared by Property Management Toronto Inc. for BS&#228;R Group of Companies. "The 501" is a working\n'
            '    name under review. Imagery is placeholder and concept rendering and does not represent final architecture, finishes or views.',
            1, "footer legal")
    h = sub(h, '  <div class="foot-giant" aria-hidden="true">PARKDALE HOUSE</div>',
            '  <div class="foot-giant" aria-hidden="true">THE 501</div>', 1, "foot giant")

    # ==================================================================
    # PALETTE SWITCHER markup
    # ==================================================================
    h = sub(h, '</footer>\n',
            '</footer>\n\n'
            '<div class="pal" role="group" aria-label="Brand palette preview">\n'
            '  <span class="pal-lbl">Palette</span>\n'
            '  <button type="button" data-pal="A" aria-pressed="false" '
            'title="A: Pantone Saratoga Signature Blue">A</button>\n'
            '  <button type="button" data-pal="B" aria-pressed="false" '
            'title="B: Pantone Blue 072 C">B</button>\n'
            '  <button type="button" data-pal="C" aria-pressed="true" '
            'title="C: Pantone Deep Purple 2617 C">C</button>\n'
            '  <button type="button" data-pal="D" aria-pressed="false" '
            'title="D: Pantone Purple PMS 3555 C">D</button>\n'
            '</div>\n',
            1, "palette switcher")

    return h
