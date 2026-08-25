# PMT Mortgages — landing page (preview)

Served at https://parkdalehouse.github.io/mortgages/

One page, two audience tracks (landlords and first-time buyers), switched by the
on-page toggle or by `?for=buyers`. Use the `?for=buyers` deep link in any tenant
campaign so renters land on their own content.

This lives here only because it needed a host that is not the `nezamai` account.
It is unrelated to the Parkdale House / BSAR site at the repo root and is not
linked from it. **Do not touch anything outside this folder.** The root
`index.html` is the live BSAR landing page plus its client markup tool.

## Not indexable, twice over

- The repo root `robots.txt` disallows the entire domain.
- This page also carries `<meta name="robots" content="noindex, nofollow">`.

## Before this goes on propertymanagementto.com

1. **Delete the `noindex` meta tag** in `index.html`, or the live page will never be indexed.
2. Jerome's written FSRA/RECO sign-off must be in hand. This page is regulated advertising.
3. Legal review of the tenant conflict-of-interest disclosure in the buyer FAQ.
4. Re-verify the rate sheet. Rates here are a static copy and do not auto-update.

Source of truth for edits: `PMT/Mortgages/Website/` in the PMT workspace.
