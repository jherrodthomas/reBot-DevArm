#!/usr/bin/env python3
"""Hero strip of the hazard scenes for the README and the wiki: the 3D view of three dashboards side by side, each
with its hazard ID, cut from the committed gallery JPEGs (assurance/sim/blender/dashboards). Pictures only: synthetic,
no evidence credit; the red band of each view stays in the crop.

  python3 assurance/sim/figures/fig_sim_hero.py           # write sim-hero-dashboards.jpg
  python3 assurance/sim/figures/fig_sim_hero.py --check   # CI: fail if stale
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
GAL = HERE.parent / "blender" / "dashboards"
OUT = HERE / "sim-hero-dashboards.jpg"
SCENES = [("hz-m01-elbow-pinch-teach", "HZ-M01 elbow pinch, TEACH"), ("hz-p03-wrist-against-bench", "HZ-P03 hand under the gripper"),
          ("hz-m04-sweep-strike-run", "HZ-M04 sweep past a head, RUN")]
VIEW = (318, 62, 1218, 568)   # the large view in the 1600 px dashboard
TILE_W, GAP = 600, 6


def font(size):
  for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
    if Path(f).exists():
      return ImageFont.truetype(f, size)
  return ImageFont.load_default()


def render() -> bytes:
  tile_h = round(TILE_W * (VIEW[3] - VIEW[1]) / (VIEW[2] - VIEW[0]))
  strip = Image.new("RGB", (TILE_W * 3 + GAP * 2, tile_h + 30), (13, 17, 20))
  d = ImageDraw.Draw(strip); f = font(16)
  for k, (sid, label) in enumerate(SCENES):
    src = Image.open(GAL / f"{sid}.jpg").convert("RGB")
    top = next((y for y in range(40, 140) if src.getpixel((768, y))[0] > 180 and src.getpixel((768, y))[1] < 110), VIEW[1])  # the red band
    im = src.crop((VIEW[0], top, VIEW[2], top + VIEW[3] - VIEW[1])).resize((TILE_W, tile_h), Image.LANCZOS)
    x = k * (TILE_W + GAP); strip.paste(im, (x, 0))
    d.text((x + 10, tile_h + 15), label, fill=(230, 237, 240), font=f, anchor="lm")
  d.text((strip.width - 10, tile_h + 15), "synthetic · no evidence credit", fill=(242, 163, 58), font=f, anchor="rm")
  buf = io.BytesIO(); strip.save(buf, "JPEG", quality=80, optimize=True); return buf.getvalue()


def main(argv) -> int:
  data = render()
  if "--check" in argv:
    if not OUT.exists() or OUT.read_bytes() != data:
      print(f"{OUT.relative_to(HERE.parents[2])} is stale; run fig_sim_hero.py"); return 1
    print("sim hero strip current"); return 0
  OUT.write_bytes(data); print("wrote", OUT); return 0


if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
