#!/usr/bin/env python3
"""Cut a scene's clip from its rendered frames (render_scene.py --video) with ffmpeg: a red band and the time on each
frame, then an H.264 mp4 at the exporter's step rate. Pictures only: synthetic, no evidence credit.

  python3 assurance/sim/blender/clip.py out/<scene> [--fps 10] [--out dashboards/clips/<scene>.mp4]
  python3 assurance/sim/blender/clip.py --reel dashboards/clips/*.mp4 --out dashboards/clips/reel.mp4
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent


def font(size):
  for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
    if Path(f).exists():
      return ImageFont.truetype(f, size)
  return ImageFont.load_default()


def annotate(sc: dict, frames: list[Path], step: int, tmp: Path) -> list[Path]:
  out = []
  f_big, f_small = font(15), font(13)
  band = "SYNTHETIC · KINEMATIC SCENE ON UPSTREAM'S CAD · NO EVIDENCE CREDIT"
  for k, fp in enumerate(frames):
    im = Image.open(fp).convert("RGB"); d = ImageDraw.Draw(im); w, h = im.size
    d.rectangle([0, 0, w, 22], fill=(214, 69, 53)); d.text((w / 2, 11), band, fill="white", font=f_small, anchor="mm")
    r = sc["rows"][min(k * step, len(sc["rows"]) - 1)]
    label = f"{sc['hz']} · {sc['id']} · t = {r['t']:+.1f} s"
    m = r.get("gap_mm", r.get("dist_mm"))
    if m is not None:
      label += f" · {sc['gap_label'] or sc['track']['point'] + ' distance'}: {m:.0f} mm"
    d.rectangle([0, h - 26, w, h], fill=(16, 24, 32)); d.text((10, h - 13), label, fill="white", font=f_big, anchor="lm")
    ev = [e["label"] for e in sc["events"] if e["t"] <= r["t"] + 1e-6 and not e.get("marker")]
    if ev:
      d.text((w - 10, h - 13), ev[-1][:60], fill=(242, 163, 58), font=f_small, anchor="rm")
    p = tmp / f"{k:04d}.png"; im.save(p); out.append(p)
  return out


def main(argv) -> int:
  ap = argparse.ArgumentParser()
  ap.add_argument("scene_dir", nargs="?")
  ap.add_argument("--fps", type=float, default=10.0)
  ap.add_argument("--step", type=int, default=1, help="the --step the frames were rendered with")
  ap.add_argument("--out", default="")
  ap.add_argument("--reel", nargs="*", help="concatenate these clips instead")
  a = ap.parse_args(argv)
  if a.reel:
    lst = Path(tempfile.mkdtemp()) / "list.txt"
    lst.write_text("".join(f"file '{Path(c).resolve()}'\n" for c in a.reel))
    out = a.out or str(HERE / "dashboards" / "clips" / "reel.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", out], check=True)
    print("wrote", out); return 0
  sd = Path(a.scene_dir).resolve(); sc = json.loads((sd / "scene.json").read_text())
  frames = sorted((sd / "frames").glob("*.png"))
  if not frames:
    print("no frames: run render_scene.py --video first"); return 1
  tmp = Path(tempfile.mkdtemp())
  annotate(sc, frames, a.step, tmp)
  out = a.out or str(HERE / "dashboards" / "clips" / f"{sc['id']}.mp4")
  Path(out).parent.mkdir(parents=True, exist_ok=True)
  subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(a.fps), "-i", str(tmp / "%04d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                  "-crf", "26", "-movflags", "+faststart", "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", out], check=True)
  print("wrote", out, f"({len(frames)} frames at {a.fps:g} fps)"); return 0


if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
