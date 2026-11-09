#!/usr/bin/env python3
"""
Stage the public registration site for https://1521queenwest.ca.

The preview repository (parkdalehouse.github.io) also carries v2, v3, the
mortgages preview and a robots.txt that blocks everything, so the live page
gets its own folder, ../1521-live-site, meant for its own GitHub Pages
repository with the custom domain set. This script fills that folder:

    index.html        tools/inflate.py --target live (no review tool)
    photos/, renders/ only the files the page uses, with their 960 px copies
    CNAME             1521queenwest.ca
    robots.txt, sitemap.xml, 404.html, favicon.ico, .nojekyll
    .gitignore        keeps NOT_READY.txt (and any runbook) out of the repository

and, BESIDE the folder so it is never published:

    ../1521-live-site_GO_LIVE.md   the DNS records and the launch checklist

It refuses while any of the five Truong Ly renders is missing, because Claire
made them the condition for going live ("Once we have the final images we can
go live with the Registration Page", 2 November 2026). --allow-missing-renders
stages a dry run and marks the folder NOT READY.

Nothing here pushes, creates a repository or touches DNS.

    python3 tools/apply_v3.py && python3 tools/apply_register.py \\
      && python3 tools/inflate.py --target live && python3 tools/build_live.py
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_register import ENDPOINT, LIVE_URL, ROOT, SLIDES, missing_renders, small_of  # noqa: E402
from inflate import LIVE_DIR  # noqa: E402

DOMAIN = "1521queenwest.ca"
RUNBOOK = LIVE_DIR.parent / "1521-live-site_GO_LIVE.md"
ICON = ROOT / "brand" / "1521_icon_orange_180.png"
GITHUB_PAGES_A = ["185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153"]
GITHUB_PAGES_AAAA = ["2606:50c0:8000::153", "2606:50c0:8001::153",
                     "2606:50c0:8002::153", "2606:50c0:8003::153"]

NOT_FOUND = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>1521 | Page not found</title>
<style>
  body{margin:0;min-height:100vh;display:grid;place-items:center;background:#FCF6ED;color:#1C1A17;
    font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;text-align:center;padding:1.5rem}
  h1{font-weight:400;color:#10069F;margin:0 0 .6rem;font-size:1.6rem}
  a{color:#10069F}
</style>
</head>
<body>
<main>
  <h1>Page not found</h1>
  <p><a href="/">Register for 1521 Queen West</a></p>
</main>
</body>
</html>
"""


def go_live_md(ready: bool, missing: list[str]) -> str:
    state = ("READY to publish once BSaR signs off the proof."
             if ready else "NOT READY. Missing renders: " + ", ".join(Path(m).name for m in missing)
             + ". Get them from BSaR, run tools/prep_images.py --renders DIR --crop co-working=L,T,R,B,"
             " then rebuild.")
    a = "\n".join("| A | @ | %s |" % ip for ip in GITHUB_PAGES_A)
    aaaa = "\n".join("| AAAA | @ | %s |" % ip for ip in GITHUB_PAGES_AAAA)
    return f"""# 1521queenwest.ca go-live

State: {state}

Internal runbook. It lives BESIDE the publish folder `1521-live-site/` on
purpose: nothing in this file may be published. The folder is built by
`tools/build_live.py` in `Ventures/BSAR/parkdalehouse-site/`; never edit the
files in it by hand.

## 0. Sign-off first

Nothing here starts until BSaR (Claire) has signed off the proof in writing,
including both consent boxes and the privacy notice, and the five renders are
in. The intake workflow `YoFu9Qj59hJqcP3z` is built and tested but switched
OFF until then.

## 0a. Timing and people

- Do DNS and HTTPS at least two business days before the hoarding goes up
  (mid-December) and before Tarek releases the press release. A scan before
  the certificate exists shows a security warning; a scan before DNS shows a
  Namecheap parking page.
- Name, before starting: who at BSaR has the Namecheap login (the domains are
  registered to Claire Bodrug personally), who at PMT runs these steps, and who
  at PMT owns the leads.
- If the renders are late, ask BSaR in writing whether to launch without them.

## 1. Repository (PMT, with Ahmed's yes)

1. Create a new public GitHub repository under the `parkdalehouse` account,
   for example `parkdalehouse/1521queenwest`.
2. From `1521-live-site/`: `git add -A && git commit`, add the remote, push
   `main`. Its `.gitignore` keeps `NOT_READY.txt` out; never push while that
   file exists.
3. Settings, Pages: deploy from branch `main`, folder `/ (root)`.
4. GitHub account settings, Pages, Verified domains: add `{DOMAIN}` and copy
   the TXT record it gives (host `_github-pages-challenge-parkdalehouse`).
5. Settings, Pages, Custom domain: `{DOMAIN}`. Save. (The CNAME file already says so.)

## 2. DNS (registrant: Claire Bodrug personally, at Namecheap)

Whois (8 Nov 2026): 1521queenwest.ca and 1521queen.ca are registered to Claire
Bodrug as an individual; all four names expire 21 September 2027. The
Marketing Services Agreement s. 11.3 says campaign domains are registered in
the Owner's name: ask BSaR to turn on auto-renew for all four and to move them
to BSAR (Queen) LP.

In Namecheap, Domain List, `{DOMAIN}`, Advanced DNS:

1. Leave Mail Settings and the email forwarding records alone (MX
   eforward1-3.registrar-servers.com and the SPF TXT record). Change Host
   Records only.
2. Add the GitHub verification TXT record from step 1.4 first.
3. Delete the parking records (the URL Redirect and the CNAME `www` to
   parkingpage.namecheap.com), then add:

| Type | Host | Value |
|---|---|---|
{a}
{aaaa}
| CNAME | www | parkdalehouse.github.io. |

The other three names BSaR holds (1521queenwest.com, 1521queen.ca,
1521queen.com) each get a Namecheap URL Redirect record, Host `@` and `www`,
Permanent (301), to `https://{DOMAIN}/`. That redirect answers plain http
only: Namecheap holds no certificate for those names, so someone typing
`https://1521queen.ca` gets a browser warning. Every printed piece, the
hoarding QR and the press release use {DOMAIN} itself, so this is acceptable
at launch. If the alternates ever get printed, give each its own tiny GitHub
Pages repository (CNAME plus an index that redirects), which gets its own
certificate.

## 3. HTTPS

When GitHub Pages shows the DNS check passing (minutes to a few hours), tick
Enforce HTTPS. The certificate is issued by GitHub automatically.

## 4. Launch checks (all must pass before anyone is told it is live)

0. Switch the intake on: `python3 build_intake.py --deploy --activate` in
   `Ventures/BSAR/Registration-Intake/` (or Activate in n8n).

1. `https://{DOMAIN}/` and `https://www.{DOMAIN}/` load the page with a padlock.
2. `http://` redirects to `https://`; the three other names redirect here.
3. Scan the printed hoarding QR (it encodes `https://{DOMAIN}/?src=hoarding`)
   on one iPhone and one Android phone: the page loads.
4. On one of them, register for real with autofill. It must show the thank
   you, arrive in Ahmed's Slack DM WITHOUT the [TEST] tag, and appear as a row
   in the n8n data table `bsar_1521_registrations_v2` with site `live` and
   source `hoarding`. Delete the test row afterwards.
5. Failure path: deactivate workflow `YoFu9Qj59hJqcP3z`, submit, see "We could
   not confirm your registration" with the leasing number, reactivate.
6. Call 416-725-9222 in and out of business hours: it rings where expected,
   voicemail works, and whoever answers knows how to log a removal request.
7. View source: `index, follow`, canonical `{LIVE_URL}`, no review tool.
   `https://{DOMAIN}/GO_LIVE.md` and `/NOT_READY.txt` must return 404.
8. Paste the URL into Slack or iMessage: the share card shows the approved
   description and the exterior image.
9. Note the n8n execution count before launch; check it again the next morning.

## 5. After launch

- Retire the preview: remove `https://parkdalehouse.github.io` from the
  intake's allowed origins (`build_intake.py`, PREVIEW_ORIGINS, redeploy) and
  point the preview `/register/` at {DOMAIN}. Review any preview rows before
  the first export; a real person may have used it.
- Kill switch: deactivating workflow `YoFu9Qj59hJqcP3z` stops intake at once;
  the page then tells people to call the leasing line.

## Registrations after launch

- Each one is a row in the n8n data table `bsar_1521_registrations_v2` (n8n,
  Overview, Data tables) and a Slack DM to Ahmed. Export the table as CSV
  from n8n for BSaR (the Owner controls the list, MSA s. 14.2) or for an email
  tool. Decide who at PMT owns the leads and whether they also go to a shared
  channel.
- `consent` is the 1521 updates box (required). `consent_pmt` is the separate,
  optional PMT box (MSA s. 14.2): only people with `yes` there may stay on
  PMT's own list after the agreement ends.
- Rows with status `check: sent fast` were sent within 2.5 seconds of the
  page opening: possibly a bot, possibly autofill. Check before contacting.
- Unsubscribe and removal requests (by email reply or the leasing line) must be
  acted on within 10 business days (CASL): delete or mark the row and remove
  the person from any list built from an export. Choose the email platform,
  with working unsubscribe links, before the first email goes out.
- Accepted risk: the webhook is public. A script that forges an allowed
  Origin header can add rows and spends one n8n execution per post. The
  intake sends one Slack alert when 50 bot posts are dropped in a day; watch
  the execution count in the first weeks; a bot challenge in front of n8n is
  the fix if abuse shows up.

## How registrations flow

The form posts to `{ENDPOINT}` (n8n workflow "BSaR 1521 Queen West
Registration Intake", source in `Ventures/BSAR/Registration-Intake/`). Each
registration is saved to the data table, answered, then announced in Slack.
Only these origins are accepted: https://{DOMAIN}, https://www.{DOMAIN} and
the preview at https://parkdalehouse.github.io (marked [TEST]).
"""


def page_paths(html: str) -> set[str]:
    paths = set(re.findall(r'(?:src|data-src)="((?:photos|renders)/[^"]+)"', html))
    for group in re.findall(r'(?:srcset|data-srcset)="([^"]+)"', html):
        for part in group.split(","):
            p = part.strip().split(" ")[0]
            if p.startswith(("photos/", "renders/")):
                paths.add(p)
    return paths


def main() -> int:
    ap = argparse.ArgumentParser(description="Stage the 1521queenwest.ca site")
    ap.add_argument("--allow-missing-renders", action="store_true",
                    help="stage a dry run without the Truong Ly renders, marked NOT READY")
    args = ap.parse_args()

    missing = missing_renders()
    if missing and not args.allow_missing_renders:
        raise SystemExit("build_live: refusing, %d render(s) missing: %s"
                         % (len(missing), ", ".join(Path(m).name for m in missing)))

    index = LIVE_DIR / "index.html"
    if not index.exists():
        raise SystemExit("build_live: %s missing. Run tools/inflate.py --target live" % index)
    html = index.read_text(encoding="utf-8")

    # ---- what the page must and must not be --------------------------------
    for bad, why in (("noindex", "the live page must be indexable"),
                     ("../", "a path climbs above the site root"),
                     ("client markup tool", "the review tool"),
                     ("parkdalehouse", "a preview address"),
                     ("Truong Ly rendering goes here", "a proof placeholder")):
        if bad in html:
            raise SystemExit("build_live: %s (%r found)" % (why, bad))
    for need in ('<link rel="canonical" href="%s">' % LIVE_URL, ENDPOINT, 'content="index, follow"'):
        if need not in html:
            raise SystemExit("build_live: %s is missing from the page" % need)

    # ---- assets: exactly the files the page names -------------------------
    wanted = page_paths(html)
    expected = set()
    for s in SLIDES:
        if (ROOT / s.file).exists():
            expected.add(s.file)
            if (ROOT / small_of(s.file)).exists():
                expected.add(small_of(s.file))
    if wanted != expected:
        raise SystemExit("build_live: page and slide list disagree: %s"
                         % sorted(wanted.symmetric_difference(expected)))
    for sub in ("photos", "renders"):
        shutil.rmtree(LIVE_DIR / sub, ignore_errors=True)
    for rel in sorted(wanted):
        src = ROOT / rel
        if not src.exists():
            raise SystemExit("build_live: %s is named by the page but missing" % rel)
        dst = LIVE_DIR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    # ---- the small files ---------------------------------------------------
    (LIVE_DIR / "CNAME").write_text(DOMAIN + "\n")
    (LIVE_DIR / ".nojekyll").write_text("")
    (LIVE_DIR / "robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n"
                                         % LIVE_URL)
    (LIVE_DIR / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "  <url><loc>%s</loc></url>\n</urlset>\n" % LIVE_URL)
    (LIVE_DIR / "404.html").write_text(NOT_FOUND)
    from PIL import Image
    with Image.open(ICON) as im:
        im.convert("RGBA").save(LIVE_DIR / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    ready = not missing
    # the runbook sits beside the publish folder, never inside it
    (LIVE_DIR / "GO_LIVE.md").unlink(missing_ok=True)
    RUNBOOK.write_text(go_live_md(ready, missing))
    (LIVE_DIR / ".gitignore").write_text("NOT_READY.txt\nGO_LIVE.md\n.DS_Store\n")
    marker = LIVE_DIR / "NOT_READY.txt"
    if ready:
        marker.unlink(missing_ok=True)
    else:
        marker.write_text("Staged without the Truong Ly renders. Do not publish.\n")

    # ---- non-ASCII and dashes in what we wrote -----------------------------
    for f in LIVE_DIR.rglob("*"):
        if f.is_file() and f.suffix in (".html", ".md", ".txt", ".xml") and ".git" not in f.parts:
            text = f.read_text(encoding="utf-8")
            if any(ord(c) > 127 for c in text):
                raise SystemExit("build_live: non-ASCII text in %s" % f.name)

    if not (LIVE_DIR / ".git").exists():
        subprocess.run(["git", "init", "-q", "-b", "main", str(LIVE_DIR)], check=True)

    size = sum(f.stat().st_size for f in LIVE_DIR.rglob("*") if f.is_file() and ".git" not in f.parts)
    print("build_live: staged %s, %d files, %.1f MB, %s"
          % (LIVE_DIR.name, sum(1 for f in LIVE_DIR.rglob("*") if f.is_file() and ".git" not in f.parts),
             size / 1048576, "READY" if ready else "NOT READY (renders missing)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
