#!/usr/bin/env python3
"""The wiki's header banner: upstream's own image of the reBot Arm B601-DM v1.1 beside the project's title.

The image is Seeed Studio's render of the arm, media/v1.1_2.png in upstream's record (CC BY-NC-SA 4.0), credited on
the banner. It is cut to the arm and saved once as a web-sized JPEG next to the banner; the banner is an SVG that
embeds that JPEG, so it renders as one image on GitHub and in the wiki.

  python3 tools/wiki/wiki_hero.py --photo   # re-cut docs/assets/rebot/wiki-hero-arm.jpg from media/v1.1_2.png (needs Pillow)
  python3 tools/wiki/wiki_hero.py           # write docs/assets/rebot/wiki-hero.svg from the committed JPEG
  python3 tools/wiki/wiki_hero.py --check   # CI: fail if the banner differs from a fresh render
"""
from __future__ import annotations

import base64
import sys
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "media" / "v1.1_2.png"
PHOTO = ROOT / "docs" / "assets" / "rebot" / "wiki-hero-arm.jpg"
OUT = ROOT / "docs" / "assets" / "rebot" / "wiki-hero.svg"
FONT = "'Source Sans 3', 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
W, H = 1280, 520
PHOTO_H = 470
CREDIT = "Image: Seeed Studio, reBot Arm B601-DM v1.1 (upstream media/v1.1_2.png), CC BY-NC-SA 4.0. The fork is not affiliated with or endorsed by Seeed Studio."


def cut_photo() -> None:
  from PIL import Image
  im = Image.open(SOURCE).convert("RGBA")
  flat = Image.new("RGB", im.size, (255, 255, 255))
  flat.paste(im, mask=im.split()[-1])
  grey = flat.convert("L").point(lambda v: 255 if v < 244 else 0)   # everything that is not near-white: the arm and its shadow
  box = grey.getbbox()
  pad = 60
  box = (max(0, box[0] - pad), max(0, box[1] - pad), min(flat.width, box[2] + pad), min(flat.height, box[3] + pad))
  arm = flat.crop(box)
  arm = arm.resize((round(arm.width * PHOTO_H * 2 / arm.height), PHOTO_H * 2), Image.LANCZOS)   # twice the banner size for sharp screens
  arm.save(PHOTO, "JPEG", quality=82, optimize=True, progressive=True)
  print(f"wrote {PHOTO.relative_to(ROOT)} {arm.size}")


def jpeg_size(data: bytes) -> tuple[int, int]:
  """Width and height from a JPEG's SOF marker (no Pillow needed in CI)."""
  i = 2
  while i < len(data):
    if data[i] != 0xFF:
      i += 1
      continue
    marker = data[i + 1]
    seg = int.from_bytes(data[i + 2:i + 4], "big")
    if marker in (0xC0, 0xC1, 0xC2):
      return int.from_bytes(data[i + 7:i + 9], "big"), int.from_bytes(data[i + 5:i + 7], "big")
    i += 2 + seg
  raise SystemExit("no JPEG size marker")


def render() -> str:
  data = PHOTO.read_bytes()
  pw, ph = jpeg_size(data)
  w = round(pw * PHOTO_H / ph)
  x = W - w - 24
  y = (H - PHOTO_H) / 2 - 8
  b64 = base64.b64encode(data).decode("ascii")
  t = lambda x_, y_, s, size, fill, weight=400: (f'<text x="{x_}" y="{y_}" font-size="{size}" fill="{fill}" font-weight="{weight}">{escape(s)}</text>')
  lines = [
    t(56, 168, "reBot-DevArm assurance", 54, "#122026", 700),
    t(58, 216, "The safety-assurance record for a fork of", 26, "#4E6A73"),
    t(58, 250, "Seeed Studio's open desktop robot arm", 26, "#4E6A73"),
    f'<rect x="58" y="292" width="64" height="5" rx="2" fill="#F2A33A"/>',
    t(58, 336, "ISO 12100 · ISO 10218-1/-2 · ISO/TS 15066", 21, "#1E4752", 600),
    t(58, 368, "ISO 13849-1 · EN 60204-1 · IEC 62443", 21, "#1E4752", 600),
    t(58, 400, "ISO/IEC TR 5469 · the Machinery Regulation", 21, "#1E4752", 600),
    t(58, 470, "Standards-informed; no compliance is claimed.", 17, "#4E6A73"),
  ]
  return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
          f'role="img" aria-labelledby="wh-t wh-d" font-family="{FONT}">'
          f'<title id="wh-t">reBot-DevArm assurance</title>'
          f'<desc id="wh-d">The reBot Arm B601-DM v1.1, Seeed Studio\'s desktop robot arm, with its gripper raised, beside the '
          f'title reBot-DevArm assurance: the safety-assurance record for a fork of the arm, following ISO 12100, ISO 10218-1 '
          f'and -2, ISO/TS 15066, ISO 13849-1, EN 60204-1, IEC 62443, ISO/IEC TR 5469 and the Machinery Regulation. {escape(CREDIT)}</desc>'
          f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>'
          f'<image x="{x}" y="{y:.0f}" width="{w}" height="{PHOTO_H}" href="data:image/jpeg;base64,{b64}" xlink:href="data:image/jpeg;base64,{b64}"/>'
          + "".join(lines) +
          f'<text x="{W - 24}" y="{H - 14}" font-size="12.5" fill="#4E6A73" text-anchor="end">{escape(CREDIT)}</text></svg>\n')


def main(argv: list[str]) -> int:
  if "--photo" in argv:
    cut_photo()
  svg = render()
  if "--check" in argv:
    if not OUT.exists() or OUT.read_text(encoding="utf-8") != svg:
      print("docs/assets/rebot/wiki-hero.svg is stale; run tools/wiki/wiki_hero.py")
      return 1
    print("wiki banner current")
    return 0
  OUT.write_text(svg, encoding="utf-8")
  print(f"wrote {OUT.relative_to(ROOT)} ({len(svg) // 1024} KB)")
  return 0


if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
