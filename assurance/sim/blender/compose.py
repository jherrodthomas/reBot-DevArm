#!/usr/bin/env python3
"""Compose the review dashboard of a scene from out/<scene>/scene.json and its stills: one HTML page, screenshot to
dashboard.png with headless Chromium when one is found (CHROME=/path/to/chrome, or the usual locations).

  python3 assurance/sim/blender/compose.py out/hz-m01-elbow-pinch-teach [--t 1.6]

The layout is LionDriver's scene dashboard (assurance/sim/README.md §1.1 there): hazard card and arm state on the
left, the large view in the middle with a red band and the outcome tiles under it, the scene and top views, the
events on the right, a row of plots, the film strip of key frames, a footer saying what the picture is and is not.
Pictures only: synthetic, no evidence credit.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
W, H = 1600, 1100
CHROME_CANDIDATES = ["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "chromium", "chromium-browser", "google-chrome", "chrome"]


def chrome() -> str | None:
  c = os.environ.get("CHROME")
  if c and Path(c).exists():
    return c
  for cand in CHROME_CANDIDATES:
    if Path(cand).exists():
      return cand
    if shutil.which(cand):
      return shutil.which(cand)
  return None


def esc(s) -> str:
  return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def plot(title, right, xs, ys, ymin, ymax, t_now, window, limits=(), w=300, h=108, color="#4a9be8", note=""):
  x0, x1 = window
  px = lambda x: 36 + (x - x0) / (x1 - x0) * (w - 48)
  py = lambda y: 18 + (ymax - y) / (ymax - ymin) * (h - 42)
  pts = " ".join(f"{px(x):.1f},{py(min(ymax, max(ymin, y))):.1f}" for x, y in zip(xs, ys))
  lim = "".join(f'<line x1="{px(x0):.0f}" y1="{py(v):.0f}" x2="{px(x1):.0f}" y2="{py(v):.0f}" stroke="#F2A33A" stroke-dasharray="4 3"/>'
                f'<text x="{px(x1)-2:.0f}" y="{py(v)-3:.0f}" font-size="9" fill="#F2A33A" text-anchor="end">{esc(lab)}</text>' for v, lab in limits if ymin <= v <= ymax)
  ticks = "".join(f'<text x="{px(x):.0f}" y="{h-4}" font-size="9" fill="#8a9aa2" text-anchor="middle">{x:g}</text>' for x in range(int(x0), int(x1) + 1))
  body = f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="1.8"/>' if xs else f'<text x="{w/2:.0f}" y="{h/2+4:.0f}" font-size="11" fill="#8a9aa2" text-anchor="middle">{esc(note)}</text>'
  return f'''<svg width="{w}" height="{h}" style="background:#151c21;border-radius:8px">
  <text x="10" y="14" font-size="11.5" fill="#e6edf0" font-weight="600">{esc(title)}</text><text x="{w-10}" y="14" font-size="11.5" fill="#e6edf0" text-anchor="end">{esc(right)}</text>
  <text x="30" y="{py(ymax)+4:.0f}" font-size="9" fill="#8a9aa2" text-anchor="end">{ymax:g}</text><text x="30" y="{py(ymin)+4:.0f}" font-size="9" fill="#8a9aa2" text-anchor="end">{ymin:g}</text>
  {ticks}{lim}
  <line x1="{px(0):.0f}" y1="18" x2="{px(0):.0f}" y2="{h-24}" stroke="#d64535" stroke-dasharray="3 3"/>
  <line x1="{px(t_now):.0f}" y1="18" x2="{px(t_now):.0f}" y2="{h-24}" stroke="#ffffff" stroke-opacity="0.6"/>
  {body}</svg>'''


def nice_max(v: float) -> float:
  for m in (10, 20, 50, 80, 100, 150, 200, 300, 500, 800, 1000, 1500, 2000, 3000):
    if v <= m:
      return m
  return float(int(v / 1000 + 1) * 1000)


def html(sc: dict, sd: Path, t_now: float) -> str:
  rows = sc["rows"]; lim = sc["limits_mm"]; x0, x1 = sc["window"]
  now = min(rows, key=lambda r: abs(r["t"] - t_now))
  frames = sc["frames"]
  f_now = min(frames, key=lambda f: abs(f["t"] - t_now))
  main_v, side = sc["main"], [v for v in sc["views"] if v != sc["main"]][:2]
  still = lambda i, v: sd / "stills" / f"{i:02d}-{v}.png"
  img = lambda p, cls="": (f'<img class="{cls}" src="file://{p}">' if p.exists() else f'<div class="missing {cls}">render pending: {esc(p.name)}</div>')
  ts = [r["t"] for r in rows]
  plots = []
  if "gap_mm" in rows[0]:
    g = [r["gap_mm"] for r in rows]; top = nice_max(max(g) * 1.1)
    plots.append(plot(sc["gap_label"], f"{now['gap_mm']:.0f} mm", ts, g, 0, top, t_now, (x0, x1),
                      [(lim["finger"], f"ISO 13854 finger {lim['finger']} mm"), (lim["hand"], f"hand {lim['hand']} mm")]))
  if "dist_mm" in rows[0]:
    d = [r["dist_mm"] for r in rows]; top = nice_max(max(d) * 1.1)
    plots.append(plot(f"{sc['track']['point'].capitalize()} distance to the {'finger tips' if sc['track']['to'] == 'tcp' else sc['track']['to']}", f"{now['dist_mm']:.0f} mm", ts, d, 0, top, t_now, (x0, x1), [(100, "100 mm")]))
  kind = sc["motion"]["kind"]
  if kind == "joint_sweep":
    s = [r["joint_speed_dps"] for r in rows]
    plots.append(plot(f"{sc['motion']['joint']} speed", f"{now['joint_speed_dps']:.0f} °/s", ts, s, 0, nice_max(max(s) * 1.3 + 1), t_now, (x0, x1), [(sc["motion"]["rate_dps"], "assumed rate (DQ-016 open)")]))
  elif kind == "gripper_close":
    s = [r["jaw_speed_mms"] for r in rows]
    plots.append(plot("Jaw closing speed", f"{now['jaw_speed_mms']:.0f} mm/s", ts, s, 0, nice_max(max(s) * 1.3 + 1), t_now, (x0, x1), [(sc["motion"]["rate_mms"], "assumed rate (DQ-016 open)")]))
  elif kind == "drop":
    dz = [r["drop_mm"] for r in rows]
    plots.append(plot("Payload height above the bench", f"{now['drop_mm']:.0f} mm", ts, dz, 0, nice_max(max(dz) * 1.1), t_now, (x0, x1)))
  sp = [r["tcp_speed_mms"] for r in rows]
  if max(sp) > 0:
    plots.append(plot("Finger-tip speed", f"{now['tcp_speed_mms'] / 1000:.2f} m/s", ts, sp, 0, nice_max(max(sp) * 1.2), t_now, (x0, x1), [(250, "250 mm/s reduced-speed value (package OE-4)")]))
  for name in ("Actuator current", "Contact force", "Controller reaction"):
    if len(plots) < 5:
      plots.append(plot(name, "not modelled", [], [], 0, 1, t_now, (x0, x1), color="#8fd8d1", note="not modelled: kinematic scene"))
  plots = plots[:5]

  thumbs = "".join(f'<div class="thumb{" now" if f is f_now else ""}">{img(still(f["i"], main_v))}<div class="tl"><b>{f["t"]:+.1f} s</b> {esc(f["label"])}</div></div>' for f in frames[:6])
  kv = lambda pairs: '<div class="kv">' + "".join(f"<span>{esc(k)}</span><b class=\"{c}\">{esc(v)}</b>" for k, v, c in pairs) + "</div>"
  r = sc["rating"]
  state = [("Joints 1 to 6", " / ".join(f"{v:.0f}°" for v in now["q"]), ""), ("Gripper opening", f"{now['opening']:.0f} mm", "")]
  if "gap_mm" in now:
    state.append((sc["gap_label"], f"{now['gap_mm']:.0f} mm", "red" if now["gap_mm"] <= lim["finger"] else "amb" if now["gap_mm"] <= lim["hand"] else ""))
  if "dist_mm" in now:
    state.append((f"{sc['track']['point'].capitalize()} distance", f"{now['dist_mm']:.0f} mm", "red" if now["dist_mm"] <= 15 else ""))
  state += [("Finger-tip speed", f"{now['tcp_speed_mms'] / 1000:.2f} m/s", ""), ("Actuator current", "not modelled", ""), ("Contact force", "not modelled", "")]
  stops = "".join(f'<span class="{"ok" if "backstop" in s["state"] or "clamp" in s["state"] else "dot"}">●</span><span>{esc(s["sf"])} {esc(s["name"])}</span><b>{esc(s["state"])}</b>' for s in sc["stops"])
  events = "".join(f'<span class="{"red" if e.get("contact") or e.get("trigger") else ""}">● {e["t"]:+.2f} s</span><b class="{"red" if e.get("contact") else ""}">{esc(e["label"])}</b>' for e in sc["events"])
  contact = next((e for e in sc["events"] if e.get("contact")), None)
  crossed = next((e for e in sc["events"] if "finger gap" in e["label"] or "within 100 mm" in e["label"]), None)
  if "gap_mm" in rows[0]:
    mintile = ("Minimum gap", f"{min(x['gap_mm'] for x in rows):.0f} mm", "amb")
  elif "dist_mm" in rows[0]:
    mintile = ("Minimum distance", f"{min(x['dist_mm'] for x in rows):.0f} mm", "amb")
  elif kind == "drop":
    mintile = ("Impact speed", f"{max(x['drop_speed_mms'] for x in rows) / 1000:.1f} m/s", "amb")
  else:
    mintile = ("Measure", "static picture", "")
  tiles = [("Time from trigger", f"{t_now:+.1f} s", ""), mintile,
           ("Limit crossed", f"{crossed['t']:+.1f} s" if crossed else "no", "amb" if crossed else ""),
           ("Stop reaction", "none at BL-001" if not any(s["state"].startswith("exists") for s in sc["stops"]) else "see stops", ""),
           ("Contact", contact["label"].split(":")[0] if contact else "none", "red" if contact else "")]
  tiles_html = "".join(f'<div class="tile"><div class="l">{esc(l)}</div><div class="v {c}">{esc(v)}</div></div>' for l, v, c in tiles)
  callout = f"{sc['gap_label']} {now['gap_mm']:.0f} mm at {t_now:+.1f} s" if "gap_mm" in now else (f"{sc['track']['point']} at {now['dist_mm']:.0f} mm at {t_now:+.1f} s" if "dist_mm" in now else sc["motion_text"])
  band = "SYNTHETIC · UPSTREAM CAD POSED BY THE JOINT RIG · " + ("KINEMATIC MOTION" if kind != "static" else "STATIC POSE") + " · CC0 OPERATOR FIGURE · NO EVIDENCE CREDIT"
  overlay = f'''<svg class="ov" width="900" height="506" viewBox="0 0 900 506">
  <rect x="0" y="0" width="900" height="22" fill="#D64535"/><text x="450" y="15" text-anchor="middle" font-size="11.5" font-weight="700" fill="#fff" letter-spacing="1">{band}</text>
  <g font-family="Inter,Segoe UI,Helvetica,Arial" font-size="12.5" font-weight="600">
  <rect x="470" y="440" width="410" height="24" rx="5" fill="#D64535"/><text x="675" y="457" text-anchor="middle" fill="#101820">{esc(callout)}</text>
  </g>
  <text x="890" y="498" text-anchor="end" font-size="10" fill="#e6edf0" fill-opacity="0.8">camera: {esc(main_v)} · CFG-001 B601-DM v1.1 STEP · frame {f_now["i"]} at {f_now["t"]:+.1f} s</text>
</svg>'''
  return f'''<!doctype html><html><head><meta charset="utf-8"><title>Scene {esc(sc["id"])}</title>
<style>
body{{margin:0;background:#0d1114;color:#e6edf0;font-family:Inter,"Segoe UI",Helvetica,Arial,sans-serif;width:{W}px;height:{H}px;overflow:hidden}}
.hdr{{display:flex;justify-content:space-between;align-items:flex-start;padding:8px 10px 4px}}
.hdr h1{{font-size:17px;margin:0;font-weight:700}} .hdr .sub{{font-size:11.5px;color:#9fb0b8;max-width:1000px}}
.tag{{display:inline-block;background:#D64535;color:#fff;font-size:11px;font-weight:700;border-radius:4px;padding:2px 7px;margin-left:8px;vertical-align:middle}}
.meta{{display:flex;gap:22px;font-size:11px;color:#9fb0b8}} .meta b{{display:block;color:#e6edf0;font-size:12px;max-width:170px}}
.grid{{display:grid;grid-template-columns:300px 900px 340px;gap:8px;padding:0 10px}}
.card{{background:#151c21;border-radius:8px;padding:10px 12px;font-size:12px}}
.card h2{{font-size:14px;margin:0 0 6px;color:#f05a4e}} .card h3{{font-size:12.5px;margin:0 0 6px}}
.kv{{display:grid;grid-template-columns:auto 1fr;column-gap:10px;row-gap:5px;font-size:12px}} .kv b{{text-align:right}} .red{{color:#f05a4e}} .amb{{color:#F2A33A}}
.main{{position:relative;width:900px;height:506px;border-radius:8px;overflow:hidden;background:#151c21}} .main img{{width:900px;height:506px;display:block;object-fit:cover}} .ov{{position:absolute;left:0;top:0}}
.missing{{display:flex;align-items:center;justify-content:center;height:100%;color:#8a9aa2;font-size:12px;min-height:147px}}
.tiles{{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-top:8px}} .tile{{background:#151c21;border-radius:8px;padding:8px 12px}}
.tile .l{{font-size:11px;color:#9fb0b8}} .tile .v{{font-size:22px;font-weight:700;margin-top:2px;white-space:nowrap;overflow:hidden}}
.plots{{display:flex;gap:8px;padding:8px 10px 0}}
.thumbs{{display:flex;gap:8px;padding:8px 10px 0}} .thumb{{background:#151c21;border-radius:8px;overflow:hidden;width:262px}} .thumb img{{width:262px;height:147px;object-fit:contain;background:#0d1114;display:block}}
.tl{{font-size:10.5px;padding:4px 8px;color:#cfd8dc;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}} .thumb.now{{outline:2px solid #4a9be8}}
.foot{{font-size:10px;color:#7e949b;padding:6px 10px;display:flex;justify-content:space-between;gap:20px}}
.note{{font-size:10px;color:#7e949b;margin-top:6px}}
.sm img{{width:316px;height:178px;object-fit:cover;display:block;border-radius:6px}} .sm .missing{{height:178px}}
.sf{{display:grid;grid-template-columns:auto 1fr auto;column-gap:8px;row-gap:3px;font-size:11px;margin-top:6px}} .sf .dot{{color:#f05a4e}} .sf .ok{{color:#5fd38f}}
</style></head><body>
<div class="hdr"><div><h1>Scene {esc(sc["id"])} <span class="tag">{esc(sc["hz"])} · PLr {esc(r["plr"])} (package rating)</span></h1>
<div class="sub">{esc(sc["title"])}: {esc(sc["situation"])}</div></div>
<div class="meta"><div>Motion source<b>{esc(sc["motion_text"].split(",")[0].capitalize())}</b></div><div>Bench<b>{esc(sc["envelope"])}</b></div><div>Mode<b>{esc(sc["mode"])}</b></div><div>Time from trigger<b>{t_now:+.1f} s ({x0:g} to {x1:g})</b></div></div></div>
<div class="grid">
<div>
 <div class="card"><h2>Hazard {esc(sc["hz"])}</h2><div><b>{esc(sc["hz_title"])}</b></div>
 <div style="margin-top:6px;color:#cfd8dc">Effect: {esc(sc["effect"])}</div>
 {kv([("Severity", r["s"], ""), ("Exposure", r["f"], ""), ("Avoidance", r["p"], ""), ("PLr (risk graph)", r["plr"], "red"), ("Category target", r["cat"], ""), ("Envelopes", r["oe"], "")])}
 <div class="note">Ratings are the package's (WP-C-03 §5), to be re-rated for OE-1 (OI-1); not approved. Safety functions: {esc(", ".join(sc["sf"]) or "none allocated")}. Related: {esc(", ".join(sc["related"]) or "—")}.</div></div>
 <div class="card" style="margin-top:8px"><h3>Arm state ({esc(sc["motion_text"].split(" ")[0])})</h3>{kv(state)}
 <h3 style="margin-top:10px">Stop functions at BL-001</h3><div class="sf">{stops}</div></div>
</div>
<div><div class="main">{img(still(f_now["i"], main_v))}{overlay}</div><div class="tiles">{tiles_html}</div></div>
<div>
 <div class="card sm"><h3>Scene view ({esc(side[0] if side else "")})</h3>{img(still(f_now["i"], side[0])) if side else ""}</div>
 <div class="card sm" style="margin-top:8px"><h3>{esc(side[1].capitalize() if len(side) > 1 else "")} view</h3>{img(still(f_now["i"], side[1])) if len(side) > 1 else ""}</div>
 <div class="card" style="margin-top:8px"><h3>Events (kinematic)</h3><div class="kv">{events}</div>
 <div class="note">{esc(sc["change"])}</div></div>
</div>
</div>
<div class="plots">{"".join(plots)}</div>
<div class="thumbs">{thumbs}</div>
<div class="foot"><span>{esc(sc["caption"])} Upstream's v1.1 STEP meshed with OpenCascade, posed by the joint rig of arm_model.py and rendered in Blender/Cycles; the operator is a CC0 Quaternius figure posed by IK. Synthetic, no evidence credit.</span><span style="white-space:nowrap">reBot-DevArm assurance/sim/blender</span></div>
</body></html>'''


def main(argv) -> int:
  ap = argparse.ArgumentParser()
  ap.add_argument("scene_dir")
  ap.add_argument("--t", type=float, default=None, help="time shown in the large view (default: the contact or the last key frame)")
  a = ap.parse_args(argv)
  sd = Path(a.scene_dir).resolve()
  sc = json.loads((sd / "scene.json").read_text(encoding="utf-8"))
  t_now = a.t
  if t_now is None:
    contact = next((e for e in sc["events"] if e.get("contact")), None)
    t_now = contact["t"] if contact else sc["frames"][-1]["t"]
  page = sd / "dashboard.html"
  page.write_text(html(sc, sd, t_now), encoding="utf-8")
  c = chrome()
  if not c:
    print(f"wrote {page} (no Chromium found: set CHROME to screenshot it)")
    return 0
  png = sd / "dashboard.png"
  subprocess.run([c, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                  f"--window-size={W},{H}", f"--screenshot={png}", f"file://{page}"], check=True, capture_output=True)
  print(f"wrote {png}")
  return 0


if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
