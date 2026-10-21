#!/usr/bin/env python3
"""Resolve the scenes of scenes.yaml into out/<scene>/scene.json: the pose over time, the gripper opening, the gap or
distance series against the ISO 13854 minimum gaps, the events, the key frames to render and the hazard card.

  python3 assurance/sim/blender/export_scene.py                 # every scene (gap series take about a minute each)
  python3 assurance/sim/blender/export_scene.py hz-m01-elbow-pinch-teach --dt 0.1

Every motion is kinematic: a joint or the gripper moves at the assumed rate named in the scene, and nothing stops it
(the scene freezes at the first contact and says so). No actuator, controller or person is modelled. Pictures only:
synthetic, no evidence credit (../README.md §4).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import arm_model  # noqa: E402

ASSURANCE = HERE.parents[1]
SCENES = HERE / "scenes.yaml"
OUT = HERE / "out"
HAZARDS = ASSURANCE / "trace" / "items" / "hazards.yaml"
G_MM = 9810.0
MOTIONS = ("joint_sweep", "gripper_close", "drop", "static")


def load_scenes(path: Path = SCENES) -> dict:
  return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_items() -> dict:
  return {it["id"]: it for it in yaml.safe_load(HAZARDS.read_text(encoding="utf-8"))}


def check(scene: dict, items: dict, cat: dict) -> list[str]:
  """Reference and schema problems of one catalogue entry (empty when fine)."""
  p = []
  sid = scene.get("id", "?")
  for key in ("id", "hz", "title", "situation", "effect", "rating", "pose", "motion", "views", "main", "window", "caption", "status"):
    if key not in scene:
      p.append(f"{sid}: missing `{key}`")
  hz = scene.get("hz")
  if hz not in items or items[hz].get("kind") != "hazard":
    p.append(f"{sid}: hz {hz} is not a hazard of trace/items/hazards.yaml")
  for r in scene.get("related", []):
    if r not in items:
      p.append(f"{sid}: related {r} is not in hazards.yaml")
  for sf in scene.get("sf", []):
    if sf not in items or items[sf].get("kind") != "safety-function":
      p.append(f"{sid}: sf {sf} is not a safety function of hazards.yaml")
  if scene.get("motion", {}).get("kind") not in MOTIONS:
    p.append(f"{sid}: motion.kind must be one of {MOTIONS}")
  if len(scene.get("pose", [])) != 6:
    p.append(f"{sid}: pose needs six joint angles")
  for msg in arm_model.check_pose(scene.get("pose", [0] * 6)):
    if not (scene["id"] == "hz-m06-tip-over-unfixtured" and msg.startswith("J3")):   # drawn past the limit on purpose
      p.append(f"{sid}: {msg}")
  if scene.get("main") not in scene.get("views", []):
    p.append(f"{sid}: main view is not in views")
  if scene.get("status") not in ("rendered", "catalogued"):
    p.append(f"{sid}: status must be rendered or catalogued")
  jid = scene.get("motion", {}).get("joint")
  if jid and jid not in {j["id"] for j in arm_model.JOINTS}:
    p.append(f"{sid}: motion.joint {jid} unknown")
  return p


# ---------------------------------------------------------------- kinematics
def pose_at(scene: dict, t: float) -> tuple[list[float], float]:
  """Joint angles (deg) and gripper opening (mm) at time t, with no stop."""
  q = list(scene["pose"]); opening = float(scene.get("opening", 0.0)); m = scene["motion"]
  t0 = float(m.get("t0", 0.0))
  if m["kind"] == "joint_sweep" and t > t0:
    ji = [j["id"] for j in arm_model.JOINTS].index(m["joint"])
    span = m["to"] - m["from"]; dur = abs(span) / m["rate_dps"]
    q[ji] = m["from"] + span * min(1.0, (t - t0) / dur)
  elif m["kind"] == "gripper_close" and t > t0:
    span = m["to"] - m["from"]; dur = abs(span) / m["rate_mms"]
    opening = m["from"] + span * min(1.0, (t - t0) / dur)
  return q, opening


def resolve_point(spec, q, opening, scene) -> list[float]:
  """A point given as [x, y, z] (m), 'tcp' or 'joint:Jn', plus an offset (m) -> scene metres."""
  if isinstance(spec, dict):
    at, off = spec.get("at", "tcp"), spec.get("offset", [0, 0, 0])
  else:
    at, off = spec, [0, 0, 0]
  if isinstance(at, (list, tuple)):
    base = np.asarray(at, dtype=float)
  elif at == "tcp":
    base = arm_model.tcp(q) * 0.001
  elif isinstance(at, str) and at.startswith("joint:"):
    base = arm_model.joint_origin(at[6:], q) * 0.001
  else:
    raise ValueError(f"unknown point {at!r}")
  return [round(float(v), 4) for v in base + np.asarray(off, dtype=float)]


class Geometry:
  """Subsampled reference points per group, posed on demand (the full meshes are only needed to render)."""

  def __init__(self, every: int = 24):
    self.parts = arm_model.load_parts()
    self.groups = {}
    for g in arm_model.GROUPS:
      pts = [p["verts"][::every] for p in self.parts if p["group"] == g and p["side"] == 0]
      self.groups[g] = (np.vstack(pts), arm_model.GROUPS.index(g))
    self.fingers = [(p["verts"][::every], p["side"]) for p in self.parts if p["side"]]

  def posed(self, g: str, q, opening=0.0) -> np.ndarray:
    pts, gi = self.groups[g]
    out = [arm_model.transform_points(pts, gi, 0, q, opening)]
    if g == "Gripper":
      out += [arm_model.transform_points(v, gi, side, q, opening) for v, side in self.fingers]
    return np.vstack(out)

  def link_gap(self, q, jid: str, radius_mm: float = 45.0) -> float:
    j = next(j for j in arm_model.JOINTS if j["id"] == jid)
    ci = arm_model.GROUPS.index(j["child"])
    o = arm_model.joint_origin(jid, q); a = arm_model.rotation_of_axis(jid, q); a = a / np.linalg.norm(a)

    def away(pts):
      rel = pts - o
      radial = np.linalg.norm(rel - np.outer(rel @ a, a), axis=1)
      return pts[radial > radius_mm]
    pa, pb = away(self.posed(arm_model.GROUPS[ci - 1], q)), away(self.posed(arm_model.GROUPS[ci], q))
    return arm_model.min_distance(pa, pb) if len(pa) and len(pb) else float("nan")

  def height_above(self, q, opening, g: str, plane_z: float) -> float:
    return float(self.posed(g, q, opening)[:, 2].min() - plane_z)

  def distance_to(self, point_mm, q, opening, to: str) -> float:
    if to == "tcp":
      return float(np.linalg.norm(arm_model.tcp(q) - point_mm))
    return float(np.linalg.norm(self.posed(to, q, opening) - point_mm, axis=1).min())


# ---------------------------------------------------------------- the scene
def build(scene: dict, cat: dict, items: dict, geo: Geometry, dt: float) -> dict:
  lim = cat["iso_13854_mm"]
  t0, t1 = scene["window"]
  ts = [round(t0 + i * dt, 3) for i in range(int(round((t1 - t0) / dt)) + 1)]
  m = scene["motion"]; kind = m["kind"]; tm = float(m.get("t0", 0.0))
  person = scene.get("person")
  track = scene.get("track")
  head_mm = hand_mm = None
  if person and person.get("head"):
    head_mm = np.asarray(resolve_point(person["head"], scene["pose"], scene.get("opening", 0.0), scene)) * 1000
  if person and person.get("hand"):
    hand_mm = np.asarray(resolve_point(person["hand"], scene["pose"], scene.get("opening", 0.0), scene)) * 1000

  rows, events, frozen_at = [], [], None
  q_prev = opening_prev = None; tcp_prev = None; peak_speed = 0.0
  crossed = set()
  for t in ts:
    if frozen_at is not None:
      q, opening = frozen_q, frozen_opening
    else:
      q, opening = pose_at(scene, t)
    row = {"t": t, "q": [round(v, 2) for v in q], "opening": round(opening, 2)}
    tcp = arm_model.tcp(q)
    row["tcp_mm"] = [round(float(v), 1) for v in tcp]
    row["tcp_speed_mms"] = round(float(np.linalg.norm(tcp - tcp_prev)) / dt, 1) if tcp_prev is not None else 0.0
    peak_speed = max(peak_speed, row["tcp_speed_mms"])
    if q_prev is not None:
      ji = [j["id"] for j in arm_model.JOINTS].index(m["joint"]) if kind == "joint_sweep" else None
      row["joint_speed_dps"] = round(abs(q[ji] - q_prev[ji]) / dt, 1) if ji is not None else 0.0
      row["jaw_speed_mms"] = round(abs(opening - opening_prev) / dt, 1)
    else:
      row["joint_speed_dps"] = 0.0; row["jaw_speed_mms"] = 0.0
    if kind == "gripper_close":
      row["gap_mm"] = round(opening, 1)
    elif scene.get("gap"):
      row["gap_mm"] = round(geo.link_gap(q, scene["gap"]), 1)
    elif scene.get("surface"):
      s = scene["surface"]; row["gap_mm"] = round(geo.height_above(q, opening, s["group"], s["plane_z_mm"]), 1)
    if track:
      point = head_mm if track["point"] == "head" else hand_mm
      row["dist_mm"] = round(geo.distance_to(point, q, opening, track["to"]), 1)
    if kind == "drop":
      z0 = float(arm_model.tcp(scene["pose"])[2]); fall = 0.0 if t < tm else 0.5 * G_MM * (t - tm) ** 2
      h = z0 - 25.0  # the cube's half-size: it rests on the bench when its centre is 25 mm up
      row["drop_mm"] = round(max(0.0, h - fall), 1)
      row["drop_speed_mms"] = round(0.0 if t < tm or fall >= h else G_MM * (t - tm), 1)
      if fall >= h and "impact" not in crossed:
        crossed.add("impact"); events.append({"t": t, "label": f"payload hits the bench at {math.sqrt(2 * h / G_MM) * G_MM / 1000:.1f} m/s"})
    # events
    if frozen_at is None and abs(t - tm) < dt / 2 and kind != "static":
      label = (f"{m['joint']} starts: {m['from']:g}° to {m['to']:g}° at {m['rate_dps']:g} °/s" if kind == "joint_sweep" else
               f"close command: {m['from']:g} mm to {m['to']:g} mm at {m['rate_mms']:g} mm/s" if kind == "gripper_close" else
               "motor power removed; gripper releases")
      events.append({"t": t, "label": label, "trigger": True})
    g = row.get("gap_mm")
    if g is not None and frozen_at is None:
      g_prev = rows[-1]["gap_mm"] if rows else g
      for name in ("arm", "hand", "finger"):
        if g <= lim[name] < g_prev and name not in crossed and name in scene.get("gap_limits", ["finger", "hand", "arm"]):
          crossed.add(name); events.append({"t": t, "label": f"gap {g:.0f} mm: ISO 13854 {name} gap ({lim[name]} mm) crossed"})
      if g <= lim["finger"] and kind in ("gripper_close", "joint_sweep") and (person or kind == "gripper_close") and "contact" not in crossed:
        crossed.add("contact"); frozen_at = t; frozen_q, frozen_opening = q, opening
        events.append({"t": t, "label": "finger caught in the gap: scene frozen (contact not modelled)", "contact": True})
    d = row.get("dist_mm")
    if d is not None and frozen_at is None:
      if d <= 100 and "near" not in crossed:
        crossed.add("near"); events.append({"t": t, "label": f"{track['point']} within 100 mm of the {'finger tips' if track['to'] == 'tcp' else track['to']}"})
      if d <= 15 and "contact" not in crossed:
        crossed.add("contact"); frozen_at = t; frozen_q, frozen_opening = q, opening
        events.append({"t": t, "label": f"{track['point']} struck at {peak_speed / 1000:.2f} m/s (peak finger-tip speed): scene frozen (contact not modelled)", "contact": True})
    if m.get("intended_stop_deg") is not None and kind == "joint_sweep" and "intended" not in crossed:
      ji = [j["id"] for j in arm_model.JOINTS].index(m["joint"])
      if (m["to"] - m["from"]) * (q[ji] - m["intended_stop_deg"]) >= 0:
        crossed.add("intended"); events.append({"t": t, "label": f"intended stop angle {m['intended_stop_deg']:g}° passed: no watchdog at BL-001"})
    if kind == "joint_sweep" and frozen_at is None and "end" not in crossed and t > tm:
      ji = [j["id"] for j in arm_model.JOINTS].index(m["joint"])
      if abs(q[ji] - m["to"]) < 1e-6:
        crossed.add("end"); events.append({"t": t, "label": f"{m['joint']} reaches {m['to']:g}°" + (" (modelled end-stop)" if m["to"] == 0 and m["joint"] == "J3" else "")})
    if kind == "gripper_close" and frozen_at is None and "end" not in crossed and t > tm and abs(opening - m["to"]) < 1e-6:
      crossed.add("end"); events.append({"t": t, "label": f"jaws at {m['to']:g} mm"})
    rows.append(row); q_prev, opening_prev, tcp_prev = q, opening, tcp
  if m.get("intended_stop_deg") is not None:
    events.append({"t": round(tm + 0.25, 2), "label": "where SF-08 (250 ms watchdog) would have stopped it", "marker": True})
  events.sort(key=lambda e: e["t"])

  # key frames: window start, trigger, events, the closest approach, end, filled to six
  measure = "gap_mm" if "gap_mm" in rows[0] else "dist_mm" if "dist_mm" in rows[0] else None
  t_closest = min(rows, key=lambda r: (r[measure], r["t"]))["t"] if measure else None
  want = sorted({ts[0], ts[-1]} | {e["t"] for e in events if not e.get("marker")} | ({t_closest} if t_closest is not None else set()))
  if len(want) < 6:
    extra = [round(t0 + k * (t1 - t0) / 5, 2) for k in range(6)]
    for e in extra:
      if len(want) >= 6:
        break
      if all(abs(e - w) > dt * 1.5 for w in want):
        want.append(e)
  want = sorted(want)[:8]
  by_t = {r["t"]: r for r in rows}

  def nearest(t):
    return min(rows, key=lambda r: abs(r["t"] - t))
  frames = []
  for i, t in enumerate(want):
    r = nearest(t)
    measured = r.get("gap_mm", r.get("dist_mm"))
    label = next((e["label"] for e in events if abs(e["t"] - t) < dt / 2), None) or ("start" if i == 0 else "end" if t == want[-1] else f"{measured} mm" if measured is not None else f"{r['tcp_speed_mms'] / 1000:.2f} m/s" if r["tcp_speed_mms"] else "")
    f = {"i": i, "t": r["t"], "label": label, "q": r["q"], "opening": r["opening"], "key": True}
    if person:
      pp = {}
      if person.get("hand"):
        pp["hand_at"] = resolve_point(person["hand"], r["q"], r["opening"], scene)
      if person.get("hand_l"):
        pp["hand_l_at"] = resolve_point(person["hand_l"], r["q"], r["opening"], scene)
      f["person"] = pp
    if kind == "drop":
      f["payload_at"] = [round(v, 4) for v in (np.asarray(r["tcp_mm"]) * 0.001 + np.array([0.0, 0.0, 0.0]) - np.array([0.0, 0.0, (arm_model.tcp(scene["pose"])[2] - 25.0 - r["drop_mm"]) * 0.001]))]
    frames.append(f)

  contact_t = next((e["t"] for e in events if e.get("contact")), None)
  t_show = contact_t if contact_t is not None else t_closest if t_closest is not None else frames[-1]["t"]
  f_now = min(frames, key=lambda f: abs(f["t"] - t_show))
  f_now["now"] = True                      # the frame the dashboard's large and side views show
  cams = {}
  for name, c in scene.get("cameras", {}).items():
    cams[name] = {"loc": c["loc"], "target": resolve_point(c["target"], scene["pose"], scene.get("opening", 0.0), scene), "lens": c.get("lens", 62)}
  hz = items[scene["hz"]]
  gaps = [r["gap_mm"] for r in rows if "gap_mm" in r]
  dists = [r["dist_mm"] for r in rows if "dist_mm" in r]
  contact = next((e for e in events if e.get("contact")), None)
  outcome = ("**contact**: " + contact["label"].split(":")[0] + f" at {contact['t']:+.2f} s") if contact else \
            (f"no contact; minimum gap {min(gaps):.0f} mm" if gaps else f"no contact; minimum distance {min(dists):.0f} mm" if dists else
             next((e["label"] for e in events if "hits" in e["label"]), f"peak finger-tip speed {peak_speed / 1000:.2f} m/s" if peak_speed > 0 else "static picture"))
  return {
    "id": scene["id"], "hz": scene["hz"], "hz_title": hz["title"], "title": scene["title"], "related": scene.get("related", []),
    "situation": scene["situation"], "effect": scene["effect"], "rating": scene["rating"], "mode": scene.get("mode", ""),
    "envelope": scene.get("envelope", ""), "sf": scene.get("sf", []), "stops": scene.get("stops", []),
    "motion": m, "motion_text": motion_text(scene), "pose": scene["pose"], "opening": scene.get("opening", 0.0),
    "fixtured": scene.get("fixtured", True), "payload": scene.get("payload"), "props": scene.get("props", {}), "person": person, "head_mm": None if head_mm is None else head_mm.tolist(),
    "views": scene["views"], "main": scene["main"], "cameras": cams, "window": scene["window"], "dt": dt,
    "limits_mm": lim, "gap_label": gap_label(scene), "track": track, "rows": rows, "events": events, "frames": frames,
    "outcome": outcome, "caption": scene["caption"], "change": scene.get("change", ""), "status": scene["status"],
  }


def motion_text(scene: dict) -> str:
  m = scene["motion"]
  return {"joint_sweep": f"kinematic {m.get('joint')} sweep, {m.get('from', 0):g}° to {m.get('to', 0):g}° at {m.get('rate_dps', 0):g} °/s (assumed)",
          "gripper_close": f"kinematic jaw closing, {m.get('from', 0):g} mm to {m.get('to', 0):g} mm at {m.get('rate_mms', 0):g} mm/s (assumed)",
          "drop": "kinematic free fall of the payload from t = 0", "static": "static pose"}[m["kind"]]


def gap_label(scene: dict) -> str:
  if scene["motion"]["kind"] == "gripper_close":
    return "Jaw opening"
  if scene.get("gap"):
    j = next(j for j in arm_model.JOINTS if j["id"] == scene["gap"])
    return f"{j['name'].capitalize()} link gap ({scene['gap']})"
  if scene.get("surface"):
    return scene["surface"]["label"].capitalize()
  return ""


def main(argv) -> int:
  ap = argparse.ArgumentParser()
  ap.add_argument("ids", nargs="*")
  ap.add_argument("--dt", type=float, default=0.1)
  ap.add_argument("--check", action="store_true", help="only check the catalogue")
  a = ap.parse_args(argv)
  cat = load_scenes(); items = load_items()
  problems = [p for s in cat["scenes"] for p in check(s, items, cat)]
  ids = [s["id"] for s in cat["scenes"]]
  if len(set(ids)) != len(ids):
    problems.append("duplicate scene IDs")
  for p in problems:
    print(p)
  if problems:
    return 1
  if a.check:
    print(f"{len(ids)} scenes, catalogue consistent")
    return 0
  geo = Geometry()
  for s in cat["scenes"]:
    if a.ids and s["id"] not in a.ids:
      continue
    sc = build(s, cat, items, geo, a.dt)
    d = OUT / s["id"]; d.mkdir(parents=True, exist_ok=True)
    (d / "scene.json").write_text(json.dumps(sc, indent=1), encoding="utf-8")
    print(f"{s['id']}: {len(sc['rows'])} steps, {len(sc['events'])} events, {len(sc['frames'])} frames; {sc['outcome']}")
  return 0


if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
