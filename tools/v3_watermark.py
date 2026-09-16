"""Preview watermark layer for the v3 and register pages.

Nothing BSaR has seen is under a signed agreement yet, so every preview page
carries a faint, tiled, non-interactive text layer and a copyright meta tag.
Deliberately quiet: 5 percent grey on both cream and deep grounds, no border,
pointer-events none, printed as well as shown. Remove by deleting the two
edits in run() once the Marketing Services Agreement is executed.
"""

# One SVG tile, URL-encoded by hand so the page stays pure ASCII.
_TILE = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='560' height='360'%3E"
         "%3Ctext x='280' y='180' text-anchor='middle' transform='rotate(-24 280 180)' "
         "font-family='Helvetica,Arial,sans-serif' font-size='15' letter-spacing='4' "
         "fill='%23808080'%3EPROPERTY MANAGEMENT TORONTO  %C2%B7  PREVIEW%3C/text%3E%3C/svg%3E")

CSS = ('''
  /* ---- preview layer: PMT design preview, no agreement executed yet ---- */
  .pmt-preview{position:fixed;inset:0;z-index:9990;pointer-events:none;
    background:url("%s") repeat;background-size:560px 360px;opacity:.05;
    mix-blend-mode:normal}
  @media print{.pmt-preview{position:absolute;opacity:.08}}
''' % _TILE)

DIV = '<div class="pmt-preview" aria-hidden="true"></div>\n'

META = ('<meta name="copyright" content="Design and content copyright 2026 Property Management '
        'Toronto Inc. Preview for BSaR Group of Companies under proposal; not for reproduction.">\n')

ROBOTS = '<meta name="robots" content="noindex, nofollow, noarchive">\n'


def run(h, sub, resub, cut_block):
    h = sub(h, "\n</style>", "\n" + CSS + "</style>", 1, "preview layer css")
    h = sub(h, ROBOTS, ROBOTS + META, 1, "copyright meta")
    h = sub(h, '<nav id="nav" class="tone-deep">', DIV + '<nav id="nav" class="tone-deep">', 1, "preview layer div")
    return h
