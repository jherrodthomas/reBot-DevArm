#!/usr/bin/env python3
"""Kinematic model of the reBot Arm B601-DM v1.1 (CFG-001) built from upstream's STEP assembly.

The STEP file (hardware/reBot_B601_DM/reBot_B601_DM_v1.1_20260425.step, upstream's record) is tessellated by
step_to_obj.py into one OBJ per part under mesh/ (git-ignored; regenerate). Its assembly tree groups the parts by link
(Base, Link1 .. Link6, Gripper), so a joint rig is the rotation of every group from a joint's child onward about that
joint's axis. The axes were read off the actuator housings and their spacers in the as-modelled pose, which is the
reference pose q = 0 (upper arm horizontal along +X, forearm folded back over it, wrist up, gripper pointing -X).
Upstream declares no joint limits (GAP-10218-03): the limits here are assumptions for pictures, named as such.

Everything is in millimetres and degrees, Z up, STEP coordinates. No bpy: usable from any Python with numpy.
Pictures only: synthetic, no evidence credit (README.md §4).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
MESH = HERE / "mesh"
STEP = HERE.parents[2] / "hardware" / "reBot_B601_DM" / "reBot_B601_DM_v1.1_20260425.step"

GROUPS = ["Base", "Link1", "Link2", "Link3", "Link4", "Link5", "Link6", "Gripper"]

# Joint axes in the reference pose: origin = centre of the actuator housing that drives the joint (bounding box of its
# mesh), axis = the housing's short side, checked against the spacer that bolts the child link to the output flange.
# `child` is the first group that moves with the joint. A positive angle turns the child by the right-hand rule about
# `axis`; the axis signs are chosen so that positive J2 raises the upper arm and positive J3 and J4 open the elbow and
# wrist. `limit` is an assumption (deg, from the reference pose); upstream declares none.
JOINTS = [
  {"id": "J1", "name": "base yaw", "origin": (0.0, 0.0, 52.5), "axis": (0, 0, 1), "child": "Link1", "motor": "DM-J4340P", "limit": (-170, 170)},
  {"id": "J2", "name": "shoulder pitch", "origin": (-20.0, -3.4, 143.5), "axis": (0, -1, 0), "child": "Link2", "motor": "DM-J4340P", "limit": (-10, 100)},
  {"id": "J3", "name": "elbow pitch", "origin": (244.0, -3.4, 143.5), "axis": (0, 1, 0), "child": "Link3", "motor": "DM-J4340P", "limit": (0, 170)},
  {"id": "J4", "name": "wrist pitch", "origin": (1.4, -3.0, 197.5), "axis": (0, 1, 0), "child": "Link4", "motor": "DM-J4310", "limit": (-100, 100)},
  {"id": "J5", "name": "wrist roll", "origin": (-76.9, 0.0, 260.0), "axis": (0, 0, 1), "child": "Link5", "motor": "DM-J4310", "limit": (-180, 180)},
  {"id": "J6", "name": "tool roll", "origin": (-77.6, 0.0, 195.0), "axis": (1, 0, 0), "child": "Link6", "motor": "DM-J4310", "limit": (-180, 360)},
]
# The gripper: a DM-J4310 in Link6 drives a pinion (GEAR-1M16C) on two racks; each finger rides a slider on a 170 mm
# rail along Y. Reference pose: closed (the finger faces meet at y = 0). Opening = distance between the finger faces.
GRIPPER = {"motor": "DM-J4310", "axis": (0, 1, 0), "opening_ref_mm": 0.0, "opening_max_mm": 80.0,  # max: assumption
           "tcp_ref": (-260.0, 0.0, 195.0)}                                                          # finger tips, closed
SIDE_PARTS = ("01_Finger", "SLIDER", "02_Slider_Extension", "02_Rack")  # the parts that travel with a finger

# Link lengths read from the joint origins (mm), for the text and the reach envelope.
LINKS = {
  "upper arm (J2 to J3)": 264.0,
  "forearm (J3 to J4)": round(math.dist((244.0, 143.5), (1.4, 197.5)), 1),
  "wrist (J4 to J5)": round(math.dist((1.4, 197.5), (-76.9, 260.0)), 1),
  "J5 to J6": 65.0,
  "J6 to finger tips": round(260.0 - 77.6, 1),
}


def load_parts(mesh_dir: Path = MESH, every: int = 1) -> list[dict]:
  """The tessellated parts: name, path, group, vertices (N×3 mm), faces (M×3), side (+1/-1 finger side or 0)."""
  index = json.loads((mesh_dir / "index.json").read_text())
  cache = mesh_dir / "cache.npz"                      # parsed once; the OBJ text takes 15 s to read, the cache 1 s
  arrays = dict(np.load(cache)) if cache.exists() else {}
  parts = []
  for p in index:
    key = p["file"]
    if key + ":v" in arrays:
      v, fa = arrays[key + ":v"], arrays[key + ":f"]
    else:
      verts, faces = [], []
      with open(mesh_dir / key) as f:
        for line in f:
          if line.startswith("v "):
            verts.append([float(x) for x in line.split()[1:4]])
          elif line.startswith("f "):
            faces.append([int(i) - 1 for i in line.split()[1:4]])
      v, fa = np.asarray(verts, dtype=float), np.asarray(faces, dtype=np.int64)
      arrays[key + ":v"], arrays[key + ":f"] = v, fa
    group = p["path"].strip("/").split("/")[0].split(":")[0]
    leaf = p["path"].split("/")[-1]
    side = 0
    if group == "Gripper" and leaf in SIDE_PARTS:
      c = (v.min(0) + v.max(0)) / 2
      side = 1 if (c[2] > 195.0 if leaf == "02_Rack" else c[1] > 0) else -1
    parts.append({"file": p["file"], "path": p["path"], "leaf": leaf, "group": group, "gi": GROUPS.index(group),
                  "verts": v[::every] if every > 1 else v, "faces": fa, "side": side})
  if not cache.exists():
    np.savez(cache, **arrays)
  return parts


def rotation(axis, deg: float) -> np.ndarray:
  a = np.asarray(axis, dtype=float); a /= np.linalg.norm(a)
  t = math.radians(deg); c, s = math.cos(t), math.sin(t)
  x, y, z = a
  return np.array([[c + x * x * (1 - c), x * y * (1 - c) - z * s, x * z * (1 - c) + y * s],
                   [y * x * (1 - c) + z * s, c + y * y * (1 - c), y * z * (1 - c) - x * s],
                   [z * x * (1 - c) - y * s, z * y * (1 - c) + x * s, c + z * z * (1 - c)]])


def check_pose(q) -> list[str]:
  """Joint angles outside the assumed limits (empty when fine)."""
  out = []
  for j, qi in zip(JOINTS, q):
    lo, hi = j["limit"]
    if not lo <= qi <= hi:
      out.append(f"{j['id']} = {qi:g}° outside the assumed limit [{lo}, {hi}]")
  return out


def transform_points(pts: np.ndarray, gi: int, side: int, q, opening_mm: float) -> np.ndarray:
  """Points of a part in group index `gi` (finger side `side`) moved to joint angles q (deg, 6) and gripper opening."""
  v = np.asarray(pts, dtype=float).copy()
  if side:
    v[:, 1] += side * (opening_mm - GRIPPER["opening_ref_mm"]) / 2.0
  for j, qi in reversed(list(zip(JOINTS, q))):          # distal joints first, all axes in the reference frame
    if gi >= GROUPS.index(j["child"]) and qi:
      o = np.asarray(j["origin"])
      v = (v - o) @ rotation(j["axis"], qi).T + o
  return v


def pose(parts: list[dict], q, opening_mm: float = 0.0) -> list[np.ndarray]:
  """Posed vertices of every part."""
  return [transform_points(p["verts"], p["gi"], p["side"], q, opening_mm) for p in parts]


def fk(point, q, group: str = "Gripper") -> np.ndarray:
  """A point attached to `group` (reference pose, mm) at joint angles q."""
  return transform_points(np.asarray([point], dtype=float), GROUPS.index(group), 0, q, 0.0)[0]


def tcp(q) -> np.ndarray:
  return fk(GRIPPER["tcp_ref"], q)


def joint_origin(jid: str, q) -> np.ndarray:
  """Where a joint's axis origin sits at joint angles q (it moves with the joint's parent)."""
  j = next(j for j in JOINTS if j["id"] == jid)
  return fk(j["origin"], q, GROUPS[GROUPS.index(j["child"]) - 1])


def min_distance(a: np.ndarray, b: np.ndarray, chunk: int = 400) -> float:
  """Smallest distance between two point sets (mm); exact for the points given, so the answer is as fine as the
  subsampling of the tessellation (a few millimetres at most on flat faces)."""
  a = np.asarray(a, dtype=np.float32); b = np.asarray(b, dtype=np.float32)
  bb = (b * b).sum(1)
  best = np.inf
  for i in range(0, len(a), chunk):
    ai = a[i:i + chunk]
    d2 = (ai * ai).sum(1)[:, None] + bb[None, :] - 2.0 * ai @ b.T
    best = min(best, float(d2.min()))
  return math.sqrt(max(best, 0.0))


def group_points(parts, posed, group: str, every: int = 12, exclude_near=None, radius_mm: float = 0.0) -> np.ndarray:
  """Subsampled posed points of a group; optionally without those within radius_mm of a line (origin, axis)."""
  pts = [v[::every] for p, v in zip(parts, posed) if p["group"] == group]
  pts = np.vstack(pts) if pts else np.zeros((0, 3))
  if exclude_near is not None and len(pts):
    o, a = (np.asarray(exclude_near[0], dtype=float), np.asarray(exclude_near[1], dtype=float))
    a = a / np.linalg.norm(a)
    rel = pts - o
    radial = np.linalg.norm(rel - np.outer(rel @ a, a), axis=1)
    pts = pts[radial > radius_mm]
  return pts


def link_gap(parts, q, jid: str, every: int = 12, radius_mm: float = 45.0) -> float:
  """Smallest gap (mm) between the two links a joint connects, away from the actuator housing itself (points within
  radius_mm of the joint axis are left out, or the answer would always be zero at the motor)."""
  j = next(j for j in JOINTS if j["id"] == jid)
  ci = GROUPS.index(j["child"])
  posed = pose(parts, q)
  axis_now = (joint_origin(jid, q), rotation_of_axis(jid, q))
  a = group_points(parts, posed, GROUPS[ci - 1], every, axis_now, radius_mm)
  b = group_points(parts, posed, GROUPS[ci], every, axis_now, radius_mm)
  return min_distance(a, b) if len(a) and len(b) else float("nan")


def rotation_of_axis(jid: str, q) -> np.ndarray:
  """The joint's axis direction at joint angles q."""
  j = next(j for j in JOINTS if j["id"] == jid)
  parent = GROUPS[GROUPS.index(j["child"]) - 1]
  o = np.asarray(j["origin"], dtype=float); a = np.asarray(j["axis"], dtype=float)
  return fk(o + a, q, parent) - fk(o, q, parent)


def surface_gap(parts, q, group: str, plane_z: float, every: int = 12) -> float:
  """Smallest height (mm) of a group's points above a horizontal surface at plane_z (negative: through it)."""
  posed = pose(parts, q)
  pts = group_points(parts, posed, group, every)
  return float(pts[:, 2].min() - plane_z) if len(pts) else float("nan")


def reach_mm(samples: int = 25) -> float:
  """Largest horizontal distance of the finger tips from the J1 axis over the assumed J2 and J3 ranges (J4 = 0)."""
  best = 0.0
  for q2 in np.linspace(*JOINTS[1]["limit"], samples):
    for q3 in np.linspace(*JOINTS[2]["limit"], samples):
      t = tcp([0, q2, q3, 0, 0, 0])
      best = max(best, float(math.hypot(t[0], t[1])))
  return best


if __name__ == "__main__":
  parts = load_parts()
  print(f"{len(parts)} parts, groups:", {g: sum(p['group'] == g for p in parts) for g in GROUPS})
  print("TCP reference", tcp([0] * 6), "reach over the assumed range (mm)", round(reach_mm(), 0))
  for jid in ("J2", "J3", "J4"):
    print(jid, "gap at reference pose", round(link_gap(parts, [0] * 6, jid), 1), "mm")
