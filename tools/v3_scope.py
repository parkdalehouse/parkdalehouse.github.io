#!/usr/bin/env python3
"""Scope and accuracy layer of the v3 build. Imported by tools/apply_v3.py.

Correction pass of 15 September 2026, after the independent review of the
round-two package (Ventures/BSAR/Review-2026-09-15/REVIEW.md):

  leasing only   the Leasing Services Agreement, section 2.3, excludes property
                 management, rent collection, maintenance and emergency
                 response. Every line that described PMT as the manager of
                 1521, promised a repair or emergency line, or promised a
                 resident portal for rent and requests comes out.
  phone          the PMT main line is answered through an IVR and a
                 receptionist service, not by a dedicated 1521 leasing desk,
                 so no line on the page claims a person answers 24 hours a
                 day. The number stays, the coverage claim goes, until the
                 dedicated 1521 line exists with confirmed hours.
  markup 22      Claire asked for the 33 plan-type claim to go; the number
                 survived in the plan-set note under the filter. Out.
  consistency    one response standard (one business day), the locker and
                 partner-programme lines say the same thing top and bottom.
  honest form    the intake is a design preview and is not connected to a
                 lead destination. Submitting says so. Nothing pretends a
                 follow-up is coming.
"""

FORM_NOTE_CSS = '''  .form-note{font-size:.72rem;line-height:1.55;letter-spacing:.03em;
    color:var(--fg-70,rgba(28,26,23,.72));margin-top:.9rem;max-width:780px}
'''

OLD_DONE = ('<div class="form-done tone-deep" id="done"><b>Thank you.</b><br>'
            'The leasing team will follow up within one business day with floorplans and pre-leasing rates.</div>')
NEW_DONE = ('<div class="form-done tone-deep" id="done"><b>Preview only.</b><br>'
            'This form is not connected yet and nothing was sent. Registrations will be captured '
            'once the page is live at the final domain.</div>')

OLD_FORM_END = '''      <div class="full"><button class="btn btn-solid btn-mag" type="submit">Register Now</button></div>
    </form>'''
NEW_FORM_END = OLD_FORM_END + '''
    <p class="form-note">Design preview. Registrations are not yet being captured; the intake is connected to the leasing system and tested before launch.</p>'''


def run(h, sub, resub, cut_block):
    # ---- phone: number stays, coverage claim goes -----------------------
    h = sub(h, 'Or call <b>416.451.9499</b> &#183; answered live, 24/7</a>',
            'Or call <b>416.451.9499</b></a>', 1, "hero coverage claim out")
    h = sub(h, 'Prefer to talk? Call <a href="tel:+14164519499"><b>416.451.9499</b></a>. The line is answered live, 24 hours a day.',
            'Prefer to talk? Call <a href="tel:+14164519499"><b>416.451.9499</b></a>.',
            1, "contact coverage claim out")
    h = sub(h, '416.451.9499</a>, answered 24/7<br>', '416.451.9499</a><br>', 1,
            "footer coverage claim out")
    h = sub(h, '<span>Answered 24/7 by a <em>Person</em></span>',
            '<span>Register for <em>First Access</em></span>', 2, "marquee coverage claim out")
    h = sub(h, '<li><b>Leasing line answered</b> by a person, any hour</li>',
            '<li><b>Model suite</b> and leasing centre on site</li>', 1,
            "amenity list coverage claim out")

    # ---- leasing only ----------------------------------------------------
    h = sub(h, 'One institutional owner. One professional manager. Residents lease directly from the company that maintains the building, and a lease here renews for as long as you choose to stay.',
            'One institutional owner and one leasing team, from first enquiry to keys. A lease here renews for as long as you choose to stay.',
            1, "suites lede, leasing only")
    h = sub(h, '<p>When something breaks, you call one number and a person answers, at any hour. Every request is tracked in writing in the resident portal, where your lease, your rent and your receipts also live.</p>',
            '<p>Leasing at 1521 is handled by Property Management Toronto: one team from first enquiry to keys, with every registration answered in writing within one business day.</p>',
            1, "trust paragraph, leasing only")
    h = sub(h, '<b>24/7</b><small>Leasing and Emergency Line, Answered by a Person</small>',
            '<b>1 day</b><small>Business Day Response to Every Registration</small>',
            1, "trust stat 1")
    h = sub(h, '<b>One portal</b><small>Rent, Requests and Documents in One Place</small>',
            '<b>1,500+</b><small>Rental Homes Leased and Managed by PMT Across Toronto</small>',
            1, "trust stat 3")
    h = sub(h, '1521 is leased and managed by Property Management Toronto, managing rental homes across the city since 2011.',
            'Leasing at 1521 is by Property Management Toronto, leasing and managing rental homes across the city since 2011.',
            1, "trust fine line, leasing only")
    h = sub(h, 'Internet live before the first box is unpacked. The line answers 24/7.',
            'Internet live before the first box is unpacked.', 1, "concierge step 4")

    # ---- one response standard --------------------------------------------
    h = sub(h, '<p>Same-day response from the leasing team, seven days a week.</p>',
            '<p>A response from the leasing team within one business day.</p>', 1,
            "concierge step 1, one response standard")

    # ---- markup 22: the number goes everywhere ----------------------------
    h = sub(h, 'The final set of 33 plan types is under review with BS&#228;R.',
            'The final plan set is under review with BS&#228;R.', 1, "plan-set note, markup 22")

    # ---- locker and partner lines say one thing ---------------------------
    h = sub(h, 'granite countertops, and a private storage locker.',
            'granite countertops.', 1, "locker claim out of the lede")
    h = sub(h, 'Locker per suite to be confirmed.', 'Storage lockers to be confirmed.', 1,
            "locker note")
    h = sub(h, 'A resident program arranged with established partners, in place from the day you move in.',
            'A resident program proposed with established partners, to be in place from the day you move in. Partner agreements are pending.',
            1, "perks lede, proposed")
    h = sub(h, 'Every new resident at 1521 receives a pre-loaded PRESTO card',
            'Every new resident at 1521 is to receive a pre-loaded PRESTO card', 1,
            "presto line, proposed")

    # ---- honest form ------------------------------------------------------
    h = sub(h, OLD_DONE, NEW_DONE, 1, "form done, preview state")
    h = sub(h, OLD_FORM_END, NEW_FORM_END, 1, "form note")
    h = sub(h, "\n</style>", "\n" + FORM_NOTE_CSS + "</style>", 1, "form note css")
    return h
