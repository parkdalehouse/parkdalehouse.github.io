"""Build switches for the v2 page.

One place so the body markup and the CSS can never disagree.
"""

# Nezam AI took the project marketing in Sept 2026 and a "Marketing By"
# footer credit was built and shipped for it. Ahmed switched it back off the
# same day, before BSaR saw it, pending the call on whether Nezam is named to
# BSaR at all. Everything for it is still here: the lockup in v2/brand/, the
# footer column in v2_body.py, the five-column grid in v2_css.py. Flip this to
# True and rerun tools/apply_v2.py then tools/inflate.py to put it back.
NEZAM_CREDIT = False
