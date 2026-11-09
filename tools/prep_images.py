#!/usr/bin/env python3
"""
Prepare the registration page images.

1. Every carousel photo gets a 960 px copy beside it (name-960.jpg) for
   phones. The EXIF block (Jacob Cote's embedded copyright), the colour
   profile and any XMP are carried over, as his credit guidelines ask.

2. --renders DIR imports BSaR's Truong Ly renders (Claire, 2 and 3 November
   2026) into renders/ as a 1800 px and a 960 px JPEG each. Files are matched
   by name, so the WeTransfer names work as they arrive:

       SUITE UNIT 805.png               -> renders/1521-suite-interior.jpg
       CO-WORKING LOUNGE.png            -> renders/1521-co-working-lounge.jpg
       PARTY ROOM.png                   -> renders/1521-party-room.jpg
       GYM 1.png                        -> renders/1521-fitness-studio.jpg
       OUTDOOR LOUNGE - TERRACE.png     -> renders/1521-terrace.jpg

   Claire asked for the co-working lounge to be cropped "to remove the red
   chair from view". The import refuses that render until a crop is given:
   open the source, find the chair, then pass the box that leaves it out as
   fractions of the width and height, left,top,right,bottom:

       python3 tools/prep_images.py --renders DIR --crop co-working=0,0,0.78,1

   --check-crop writes the cropped frame to the temp folder only, to look at first.
   Each import is logged in renders/SOURCES.md with the crop it used.

Run from anywhere:
    python3 tools/prep_images.py                      phone copies only
    python3 tools/prep_images.py --renders DIR --crop co-working=L,T,R,B
"""

from __future__ import annotations

import argparse
import io
import tempfile
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_register import ROOT, SLIDES, small_of  # noqa: E402

RENDERS = ROOT / "renders"
SMALL = 960
LARGE = 1800

# slug -> (patterns that identify the source file, target name, crop required)
RENDER_MAP = {
    "suite": ((r"suite",), "1521-suite-interior.jpg", False),
    "co-working": ((r"co.?working",), "1521-co-working-lounge.jpg", True),
    "party": ((r"party",), "1521-party-room.jpg", False),
    "gym": ((r"gym", r"fitness"), "1521-fitness-studio.jpg", False),
    "terrace": ((r"terrace",), "1521-terrace.jpg", False),
}


def small_copies() -> int:
    made = 0
    for s in SLIDES:
        src = ROOT / s.file
        dst = ROOT / small_of(s.file)
        if not src.exists() or (dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime):
            continue
        from PIL import Image
        with Image.open(src) as im:
            meta = {k: im.info[k] for k in ("exif", "icc_profile", "xmp") if im.info.get(k)}
            out = im.convert("RGB")
            out.thumbnail((SMALL, SMALL), Image.LANCZOS)
        out.save(dst, "JPEG", quality=78, optimize=True, progressive=True, **meta)
        made += 1
        print("prep_images: %s (%d KB)" % (dst.relative_to(ROOT), dst.stat().st_size // 1024))
    return made


def parse_crop(text: str) -> tuple[str, tuple[float, float, float, float]]:
    slug, _, box = text.partition("=")
    parts = [float(x) for x in box.split(",")]
    if slug not in RENDER_MAP or len(parts) != 4:
        raise SystemExit("prep_images: --crop wants SLUG=left,top,right,bottom, slug one of %s"
                         % ", ".join(RENDER_MAP))
    left, top, right, bottom = parts
    if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
        raise SystemExit("prep_images: crop box %s is not inside 0..1" % box)
    return slug, (left, top, right, bottom)


def find_source(folder: Path, patterns: tuple[str, ...]) -> Path | None:
    hits = [p for p in sorted(folder.iterdir())
            if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".tif", ".tiff")
            and any(re.search(pat, p.stem, re.I) for pat in patterns)]
    if len(hits) > 1:
        raise SystemExit("prep_images: more than one file matches %s: %s"
                         % (patterns, ", ".join(h.name for h in hits)))
    return hits[0] if hits else None


def to_rgb(img):
    """Upright, flattened RGB. A CMYK or other non-RGB file is converted
    through its own profile to sRGB, or refused when it has none."""
    from PIL import Image, ImageCms, ImageOps
    img = ImageOps.exif_transpose(img)
    if img.mode in ("L", "LA") and img.info.get("icc_profile"):
        src = ImageCms.ImageCmsProfile(io.BytesIO(img.info["icc_profile"]))
        return ImageCms.profileToProfile(img.convert("L"), src, ImageCms.createProfile("sRGB"),
                                         outputMode="RGB")
    if img.mode not in ("RGB", "RGBA", "LA", "P", "L"):
        icc = img.info.get("icc_profile")
        if not icc:
            raise SystemExit("prep_images: a %s image with no colour profile; ask for an RGB export"
                             % img.mode)
        src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
        return ImageCms.profileToProfile(img, src, ImageCms.createProfile("sRGB"), outputMode="RGB")
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[-1])
        return bg
    return img.convert("RGB")


def save_pair(img, target: Path, icc: bytes | None) -> None:
    from PIL import Image
    for edge, path, q in ((LARGE, target, 84), (SMALL, ROOT / small_of(str(target.relative_to(ROOT))), 80)):
        out = img.copy()
        out.thumbnail((edge, edge), Image.LANCZOS)
        kw = {"quality": q, "optimize": True, "progressive": True}
        if icc:
            kw["icc_profile"] = icc
        out.save(path, "JPEG", **kw)
        print("prep_images: %s %dx%d (%d KB)" % (path.relative_to(ROOT), out.width, out.height,
                                                path.stat().st_size // 1024))


def import_renders(folder: Path, crops: dict, check_only: bool) -> None:
    from PIL import Image
    if not folder.is_dir():
        raise SystemExit("prep_images: %s is not a folder" % folder)
    RENDERS.mkdir(exist_ok=True)
    log = []
    for slug, (patterns, name, needs_crop) in RENDER_MAP.items():
        src = find_source(folder, patterns)
        if src is None:
            print("prep_images: no %s render in %s, skipped" % (slug, folder))
            continue
        box = crops.get(slug)
        if needs_crop and box is None:
            raise SystemExit("prep_images: the co-working lounge needs --crop co-working=L,T,R,B "
                             "(Claire: crop to remove the red chair from view)")
        with Image.open(src) as im:
            # keep the source profile only for RGB sources; to_rgb() makes the rest sRGB
            # keep a profile only when it is an RGB one; grey and CMYK become sRGB in to_rgb()
            icc = im.info.get("icc_profile") if im.mode in ("RGB", "RGBA") else None
            img = to_rgb(im)
        if box:
            w, h = img.size
            img = img.crop((round(box[0] * w), round(box[1] * h),
                            round(box[2] * w), round(box[3] * h)))
        if check_only:
            tmp = Path(tempfile.gettempdir()) / ("1521-crop-check-" + name)
            img.copy().resize((img.width // 3, img.height // 3)).save(tmp, "JPEG", quality=80)
            print("prep_images: crop check written to %s" % tmp)
            continue
        save_pair(img, RENDERS / name, icc)
        log.append("| %s | %s | %s | %s |" % (date.today().isoformat(), src.name, name,
                                              ",".join("%g" % v for v in box) if box else "none"))
    if log and not check_only:
        sources = RENDERS / "SOURCES.md"
        head = ("# Renders on the registration page\n\nTruong Ly Design Inc. renders supplied by "
                "BSaR (Claire Bodrug, 2 and 3 November 2026). Imported by tools/prep_images.py.\n\n"
                "| Imported | Source file | Page file | Crop (l,t,r,b) |\n|---|---|---|---|\n")
        old = sources.read_text().split("|---|---|---|---|\n", 1)[1] if sources.exists() else ""
        sources.write_text(head + old + "\n".join(log) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="Prepare 1521 registration page images")
    ap.add_argument("--renders", type=Path, help="folder holding BSaR's render files")
    ap.add_argument("--crop", action="append", default=[], help="SLUG=left,top,right,bottom")
    ap.add_argument("--check-crop", action="store_true", help="write cropped frames to /tmp only")
    args = ap.parse_args()
    crops = dict(parse_crop(c) for c in args.crop)
    if args.renders:
        import_renders(args.renders.expanduser().resolve(), crops, args.check_crop)
    if not args.check_crop:
        made = small_copies()
        print("prep_images: %d phone copies made" % made)
    return 0


if __name__ == "__main__":
    sys.exit(main())
