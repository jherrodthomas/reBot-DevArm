#!/usr/bin/env python3
"""Render the posed reBot Arm B601-DM v1.1 with Blender (bpy, Cycles on the CPU) for a scene of scenes.yaml.

  python3 render_scene.py out/<scene>            # every key frame of out/<scene>/scene.json, every camera -> stills/
  python3 render_scene.py out/<scene> --frames 3 --views main,scene --samples 24 --size 900x506
  python3 render_scene.py --pose 0,60,90,0,0,0 --opening 40 --view hero --out preview.png   # an ad-hoc pose

Geometry: upstream's STEP tessellated by step_to_obj.py (mesh/), posed by arm_model.py. Materials come from the part
names in the assembly tree (anodised aluminium, printed PLA and ABS, actuator housings, fasteners), matched by eye to
upstream's photographs. The bench, clamps, floor and lights are the scene's. The operator is the CC0 Quaternius figure
of library/people/, placed and posed by inverse kinematics on the hand. Pictures only: synthetic, no evidence credit.
Runs with Blender 4.2+ (blender -b -P render_scene.py -- ...) or `pip install bpy` (Python 3.11, bpy 5.0).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import bpy
import mathutils
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import arm_model  # noqa: E402

PEOPLE = HERE / "library" / "people"
VIEWS = {   # camera location, target (m, scene frame = STEP frame / 1000), lens mm
  "hero": {"loc": (0.72, -0.92, 0.40), "target": (0.0, 0.0, 0.13), "lens": 62},
  "elbow": {"loc": (-0.42, -0.55, 0.36), "target": (-0.18, 0.0, 0.17), "lens": 85},
  "top": {"loc": (-0.15, -0.2, 1.75), "target": (-0.15, -0.2, 0.1), "lens": 40},
  "front": {"loc": (-0.1, -1.3, 0.35), "target": (-0.15, 0.0, 0.25), "lens": 55},
  "scene": {"loc": (1.15, -1.55, 0.75), "target": (-0.1, 0.1, 0.25), "lens": 40},
  "hand": {"loc": (-0.5, -0.85, 0.5), "target": (-0.27, 0.0, 0.22), "lens": 70},
}
BENCH_TOP_Z = 0.0  # the base plate sits on the bench top at z = 0 (STEP z = 0)


def parse_args(argv):
  ap = argparse.ArgumentParser()
  ap.add_argument("scene_dir", nargs="?")
  ap.add_argument("--frames", type=int, default=0, help="render only this many key frames (0: all)")
  ap.add_argument("--views", default="", help="comma list of camera names (default: the scene's)")
  ap.add_argument("--samples", type=int, default=128)
  ap.add_argument("--size", default="1600x900")
  ap.add_argument("--pose", default="", help="ad hoc: six joint angles in degrees")
  ap.add_argument("--opening", type=float, default=0.0)
  ap.add_argument("--view", default="hero")
  ap.add_argument("--person", default="", help="ad hoc: male or female")
  ap.add_argument("--out", default="")
  ap.add_argument("--all-views", action="store_true", help="every camera at every key frame (default: side cameras only at the dashboard's frame)")
  ap.add_argument("--force", action="store_true", help="re-render stills that exist")
  if "--" in argv:
    argv = argv[argv.index("--") + 1:]
  return ap.parse_args(argv)


# ---------------------------------------------------------------- materials
def principled(name, base, metallic=0.0, rough=0.5, specular=0.5, coat=0.0, aniso=0.0):
  m = bpy.data.materials.new(name); m.use_nodes = True
  bsdf = m.node_tree.nodes["Principled BSDF"]
  bsdf.inputs["Base Color"].default_value = (*base, 1.0)
  bsdf.inputs["Metallic"].default_value = metallic
  bsdf.inputs["Roughness"].default_value = rough
  for key, val in (("Specular IOR Level", specular), ("Coat Weight", coat), ("Anisotropic", aniso)):
    if key in bsdf.inputs:
      bsdf.inputs[key].default_value = val
  return m


def materials():
  mats = {
    "alu": principled("anodised aluminium", (0.78, 0.79, 0.80), metallic=1.0, rough=0.32, aniso=0.4),
    "motor": principled("actuator black anodised", (0.012, 0.012, 0.013), metallic=0.6, rough=0.45),
    "green": principled("printed lime PLA", (0.55, 0.85, 0.05), rough=0.45, coat=0.1),
    "black": principled("printed black ABS", (0.010, 0.010, 0.011), rough=0.55, specular=0.3),
    "steel": principled("black-oxide steel", (0.09, 0.09, 0.10), metallic=0.9, rough=0.45),
    "rubber": principled("silicone", (0.25, 0.25, 0.26), rough=0.8),
    "bearing": principled("bearing steel", (0.55, 0.56, 0.57), metallic=1.0, rough=0.3),
    "payload": principled("payload cube", (0.85, 0.35, 0.12), rough=0.5),
    "hazard": principled("hazard marker", (0.84, 0.27, 0.21), rough=0.6),
  }
  return mats


GREEN_NAMES = ("Fuller", "Filler", "01_Finger", "01_Lower_Arm_Limit", "01_Rail_Bracket")


def material_for(path: str, mats):
  leaf = path.strip("/").split("/")[-1]
  if leaf.startswith("DM-J"):
    return mats["motor"]
  if "3D_Printed" in path:
    return mats["green"] if any(k in leaf for k in GREEN_NAMES) else mats["black"]
  if "Metal_Parts" in path:
    return mats["alu"]
  if "SILICONE" in leaf:
    return mats["rubber"]
  if leaf.endswith("ZZ") or leaf.startswith("AXK") or leaf in ("RAIL-170", "SLIDER", "GEAR-1M16C"):
    return mats["bearing"]
  return mats["steel"]


# ---------------------------------------------------------------- scene
def new_scene(samples, w, h):
  bpy.ops.wm.read_factory_settings(use_empty=True)
  sc = bpy.context.scene
  sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = samples
  sc.cycles.use_adaptive_sampling = True; sc.cycles.use_denoising = True; sc.cycles.denoiser = "OPENIMAGEDENOISE"
  sc.cycles.max_bounces = 6
  sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = w, h, 100
  sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
  sc.view_settings.exposure = -0.1
  sc.render.image_settings.file_format = "PNG"
  return sc


def build_arm(sc, parts, mats):
  """One Blender mesh per part in the reference pose; returns the objects in part order."""
  col = bpy.data.collections.new("arm"); sc.collection.children.link(col)
  obs = []
  for p in parts:
    me = bpy.data.meshes.new(p["file"][:60])
    me.from_pydata((p["verts"] * 0.001).tolist(), [], p["faces"].tolist())
    me.validate(clean_customdata=False); me.update()
    for poly in me.polygons:
      poly.use_smooth = True
    ob = bpy.data.objects.new(p["file"][:60], me)
    ob.data.materials.append(material_for(p["path"], mats))
    col.objects.link(ob)
    bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    try:
      bpy.ops.object.shade_smooth_by_angle(angle=math.radians(32))
    except Exception:
      pass
    ob.select_set(False)
    obs.append(ob)
  return obs


def set_pose(parts, obs, q, opening_mm):
  for p, ob in zip(parts, obs):
    v = arm_model.transform_points(p["verts"], p["gi"], p["side"], q, opening_mm) * 0.001
    ob.data.vertices.foreach_set("co", v.ravel())
    ob.data.update()


def cube(name, dims, loc, mat, rot=(0, 0, 0)):
  bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
  ob = bpy.context.active_object; ob.name = name; ob.scale = dims; ob.data.materials.append(mat)
  return ob


def plane(name, size, loc, mat, rot=(0, 0, 0)):
  bpy.ops.mesh.primitive_plane_add(size=size, location=loc, rotation=rot)
  ob = bpy.context.active_object; ob.name = name; ob.data.materials.append(mat)
  return ob


def bench_and_room(mats, fixtured=True):
  wood = bpy.data.materials.new("birch worktop"); wood.use_nodes = True
  nt = wood.node_tree; bsdf = nt.nodes["Principled BSDF"]
  tex = nt.nodes.new("ShaderNodeTexNoise"); tex.inputs["Scale"].default_value = 90; tex.inputs["Detail"].default_value = 6
  mapn = nt.nodes.new("ShaderNodeMapping"); mapn.inputs["Scale"].default_value = (1.0, 14.0, 1.0)
  coord = nt.nodes.new("ShaderNodeTexCoord"); ramp = nt.nodes.new("ShaderNodeValToRGB")
  ramp.color_ramp.elements[0].color = (0.62, 0.50, 0.34, 1); ramp.color_ramp.elements[1].color = (0.78, 0.66, 0.48, 1)
  nt.links.new(coord.outputs["Object"], mapn.inputs["Vector"]); nt.links.new(mapn.outputs["Vector"], tex.inputs["Vector"])
  nt.links.new(tex.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
  bsdf.inputs["Roughness"].default_value = 0.35
  if "Coat Weight" in bsdf.inputs:
    bsdf.inputs["Coat Weight"].default_value = 0.25
  cube("bench top", (1.6, 0.8, 0.04), (0.15, 0.0, -0.02), wood)
  for x, y in ((-0.55, -0.32), (0.85, -0.32), (-0.55, 0.32), (0.85, 0.32)):
    cube("bench leg", (0.05, 0.05, 0.86), (x, y, -0.47), mats["steel"])
  plane("floor", 12, (0, 0, -0.9), principled("floor concrete", (0.42, 0.42, 0.41), rough=0.85))
  plane("wall", 12, (0, 2.6, 2.0), principled("wall", (0.86, 0.86, 0.85), rough=0.9), rot=(math.radians(90), 0, 0))
  if fixtured:
    clamp = principled("clamp steel", (0.45, 0.46, 0.47), metallic=1.0, rough=0.4)
    for x in (-0.085, 0.085):
      cube("clamp", (0.03, 0.045, 0.02), (x, -0.07, 0.012), clamp)


def lights(sc):
  world = bpy.data.worlds.new("studio"); sc.world = world; world.use_nodes = True
  wn = world.node_tree; bg = wn.nodes["Background"]
  grad = wn.nodes.new("ShaderNodeTexGradient"); coord = wn.nodes.new("ShaderNodeTexCoord"); mp = wn.nodes.new("ShaderNodeMapping")
  mp.inputs["Rotation"].default_value = (0, math.radians(-90), 0)
  ramp = wn.nodes.new("ShaderNodeValToRGB")
  ramp.color_ramp.elements[0].position = 0.45; ramp.color_ramp.elements[0].color = (0.18, 0.19, 0.21, 1)
  ramp.color_ramp.elements[1].position = 0.75; ramp.color_ramp.elements[1].color = (0.62, 0.66, 0.72, 1)
  wn.links.new(coord.outputs["Generated"], mp.inputs["Vector"]); wn.links.new(mp.outputs["Vector"], grad.inputs["Vector"])
  wn.links.new(grad.outputs["Fac"], ramp.inputs["Fac"]); wn.links.new(ramp.outputs["Color"], bg.inputs["Color"])
  bg.inputs["Strength"].default_value = 0.55

  def area(name, loc, target, size, energy, color=(1, 1, 1)):
    bpy.ops.object.light_add(type="AREA", location=loc)
    l = bpy.context.active_object; l.name = name; l.data.energy = energy; l.data.size = size; l.data.color = color
    l.rotation_euler = (mathutils.Vector(target) - mathutils.Vector(loc)).to_track_quat("-Z", "Y").to_euler()
  area("key", (0.9, -1.1, 1.6), (0.05, 0.0, 0.1), 1.4, 260, (1.0, 0.97, 0.92))
  area("fill", (-1.3, -0.6, 0.9), (0.0, 0.0, 0.15), 2.2, 90, (0.92, 0.95, 1.0))
  area("rim", (-0.4, 1.4, 1.2), (0.0, 0.0, 0.15), 1.0, 180)


class Person:
  """The CC0 Quaternius figure: imported once, moved and IK-posed per frame."""

  def __init__(self, figure: str):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(PEOPLE / f"pedestrian_{figure}.glb"))
    self.obs = [o for o in bpy.data.objects if o not in before]
    self.rig = next(o for o in self.obs if o.type == "ARMATURE")
    for o in self.obs:
      if o.name.startswith("Icosphere"):
        o.hide_render = True; o.hide_viewport = True
    self.rig.animation_data_clear()
    self.rig.rotation_mode = "XYZ"
    bpy.ops.object.empty_add(location=(0, 0, 0)); self.target_r = bpy.context.active_object; self.target_r.name = "hand_r_target"
    bpy.ops.object.empty_add(location=(0, 0, 0)); self.target_l = bpy.context.active_object; self.target_l.name = "hand_l_target"
    bpy.ops.object.empty_add(location=(0, 0, 0)); self.pole = bpy.context.active_object; self.pole.name = "elbow_pole"
    bpy.context.view_layer.objects.active = self.rig
    bpy.ops.object.mode_set(mode="POSE")
    pb = self.rig.pose.bones
    for name in ("upperarm_l", "upperarm_r", "spine_02", "Head"):
      pb[name].rotation_mode = "XYZ"
    self.ik_r = pb["hand_r"].constraints.new("IK"); self.ik_r.target = self.target_r; self.ik_r.chain_count = 3
    self.ik_r.pole_target = self.pole; self.ik_r.pole_angle = math.radians(-90); self.ik_r.use_rotation = False
    self.ik_l = pb["hand_l"].constraints.new("IK"); self.ik_l.target = self.target_l; self.ik_l.chain_count = 3
    self.ik_l.use_rotation = False; self.ik_l.mute = True
    bpy.ops.object.mode_set(mode="OBJECT")

  def place(self, spec: dict):
    """spec: at [x,y,z] (feet, m), yaw (deg), pose: reach | stand | lean, hand_at [x,y,z], hand_l_at, lean (deg)."""
    px, py, pz = spec.get("at", (-0.30, 0.50, -0.90))
    self.rig.location = (px, py, pz); self.rig.rotation_euler = (0, 0, math.radians(spec.get("yaw", 0)))
    pose = spec.get("pose", "reach")
    pb = self.rig.pose.bones
    pb["spine_02"].rotation_euler = (math.radians(spec.get("lean", 14 if pose != "stand" else 2)), 0, 0)
    pb["Head"].rotation_euler = (math.radians(spec.get("head", 18 if pose != "stand" else 0)), 0, 0)
    self.pole.location = (px + 0.35, py + 0.30, pz + 1.05)
    if pose == "stand":
      self.ik_r.mute = True; self.ik_l.mute = True
      pb["upperarm_l"].rotation_euler = (0, 0, math.radians(-55)); pb["upperarm_r"].rotation_euler = (0, 0, math.radians(55))
    else:
      self.ik_r.mute = False; pb["upperarm_r"].rotation_euler = (0, 0, 0)
      self.target_r.location = spec.get("hand_at", (-0.27, 0.0, 0.22))
      if pose == "lean" and "hand_l_at" in spec:
        self.ik_l.mute = False; pb["upperarm_l"].rotation_euler = (0, 0, 0); self.target_l.location = spec["hand_l_at"]
      else:
        self.ik_l.mute = True; pb["upperarm_l"].rotation_euler = (0, 0, math.radians(-55))
    bpy.context.view_layer.update()


def camera(sc, view: dict):
  if sc.camera is None:
    bpy.ops.object.camera_add(); sc.camera = bpy.context.active_object; sc.camera.data.sensor_width = 36
  cam = sc.camera
  loc, target = mathutils.Vector(view["loc"]), mathutils.Vector(view["target"])
  cam.location = loc; cam.rotation_euler = (target - loc).to_track_quat("-Z", "Y").to_euler()
  cam.data.lens = view.get("lens", 62)
  cam.data.dof.use_dof = True; cam.data.dof.focus_distance = (target - loc).length; cam.data.dof.aperture_fstop = view.get("fstop", 5.6)


def render(sc, out: Path):
  out.parent.mkdir(parents=True, exist_ok=True)
  sc.render.filepath = str(out.resolve())
  bpy.ops.render.render(write_still=True)
  print("rendered", out)


def props(spec: dict, mats):
  """Scene props: payload cube in the gripper, a hazard marker, an unfixtured base (no clamps) are in the scene spec."""
  obs = {}
  if spec.get("payload"):
    p = spec["payload"]
    obs["payload"] = cube("payload", p.get("size", (0.05, 0.05, 0.05)), p.get("at", (-0.29, 0, 0.195)), mats["payload"])
  return obs


def main(argv):
  a = parse_args(argv)
  w, h = (int(x) for x in a.size.split("x"))
  sc = new_scene(a.samples, w, h)
  mats = materials()
  parts = arm_model.load_parts()
  obs = build_arm(sc, parts, mats)
  print(f"imported {len(obs)} parts")
  if a.scene_dir:
    sd = Path(a.scene_dir); spec = json.loads((sd / "scene.json").read_text())
    bench_and_room(mats, fixtured=spec.get("fixtured", True)); lights(sc)
    prop_obs = props(spec, mats)
    person = Person(spec["person"]["figure"]) if spec.get("person") else None
    views = [v for v in a.views.split(",") if v] or spec.get("views", ["hero"])
    cams = {**VIEWS, **spec.get("cameras", {})}
    frames = [f for f in spec["frames"] if f.get("key")] or spec["frames"]
    if a.frames:
      frames = frames[:a.frames]
    for f in frames:
      set_pose(parts, obs, f["q"], f.get("opening", 0.0))
      if person:
        person.place({**spec["person"], **f.get("person", {})})
      if "payload" in prop_obs and "payload_at" in f:
        prop_obs["payload"].location = f["payload_at"]
      for v in views:
        out = sd / "stills" / f"{f['i']:02d}-{v}.png"
        if v != spec.get("main", views[0]) and not f.get("now") and not a.all_views:
          continue                                   # the dashboard shows the side views only at its frame
        if out.exists() and not a.force:
          print("kept", out); continue
        camera(sc, cams[v])
        render(sc, out)
  else:
    q = [float(x) for x in a.pose.split(",")] if a.pose else [0.0] * 6
    bench_and_room(mats); lights(sc)
    set_pose(parts, obs, q, a.opening)
    if a.person:
      Person(a.person).place({})
    camera(sc, VIEWS[a.view])
    render(sc, Path(a.out or "preview.png"))
  return 0


if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
