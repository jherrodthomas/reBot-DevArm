# Hazard scenes in Blender

| Field | Value |
|---|---|
| Scope | A 3D scene and a review dashboard for every hazard of [WP-C-03](../../02-concept/WP-C-03-risk-assessment.md) that a picture helps (fifteen of 34 so far), on upstream's CAD posed by the joint rig; part of [WP-P-12](../README.md) |
| Version | 0.2 (2026-10-21): fifteen scenes, open hands, a cable prop. 0.1 (2026-10-21): the pipeline, twelve scenes, the gallery |
| Status | Draft. AI-drafted (Claude, AI assistant; I0 under WP-M-02 §3.3); not reviewed. **Pictures only: synthetic, no evidence credit** ([method §4](../README.md#4-what-the-pictures-are-and-are-not)) |

**Gallery: [dashboards/README.md](dashboards/README.md)**, one dashboard per scene with its outcome.

## 1. Pipeline

| Step | Script | Runs in | Writes |
|---|---|---|---|
| 0 (once) | [`step_to_obj.py`](step_to_obj.py) | Python with `cadquery-ocp` | `mesh/` (git-ignored): one OBJ per part and `index.json` with each part's path in the assembly tree; a parsed cache on first use |
| 1 | [`export_scene.py`](export_scene.py) | Python with PyYAML and numpy | `out/<scene>/scene.json` (git-ignored): the hazard card, the pose at every 0.1 s, the gap or distance series, the events, the key frames, the cameras |
| 2 | [`render_scene.py`](render_scene.py) | Blender 4.2+ (`blender -b -P render_scene.py -- out/<scene>`) or Python 3.11 with `bpy` | `out/<scene>/stills/<frame>-<camera>.png` |
| 3 | [`compose.py`](compose.py) | Python; headless Chromium for the PNG (`CHROME=`) | `out/<scene>/dashboard.html` and `dashboard.png` |
| 4 | [`gallery.py`](gallery.py) | Python with Pillow | [`dashboards/`](dashboards/README.md) (committed: the JPEG, a small JSON with the outcome and events, the README) |

```sh
python3 assurance/sim/blender/export_scene.py --check     # the catalogue only (CI, with test_scenes.py)
python3 assurance/sim/blender/export_scene.py hz-m02-gripper-finger-teach
python3 assurance/sim/blender/render_scene.py assurance/sim/blender/out/hz-m02-gripper-finger-teach --samples 48 --size 900x506
python3 assurance/sim/blender/compose.py assurance/sim/blender/out/hz-m02-gripper-finger-teach
python3 assurance/sim/blender/gallery.py
python3 assurance/sim/blender/render_scene.py --pose 0,60,90,0,0,0 --opening 40 --view scene --out preview.png   # an ad-hoc pose
```

## 2. A scene

Every entry of [`scenes.yaml`](scenes.yaml) names the hazard, carries the package's rating and the stop functions at
BL-001, and gives a pose, one kinematic motion (a joint sweep, the gripper closing, a payload falling, or a static
pose), what to measure (a link gap, a height above the bench, or the distance from a head or hand point to the finger
tips), where the person stands and any prop (the supply cable). The exporter checks every reference against `trace/items/hazards.yaml`, moves the
geometry through the motion at an assumed rate, records when the measure crosses the ISO 13854 gaps or reaches the
person, freezes the scene at the first contact (contact is not modelled) and picks the key frames: the start, the
trigger, every event, the end.

The dashboard is LionDriver's layout: hazard card and arm state on the left; the large view with the red band, the
outcome tiles and the callout in the middle; the scene and top views and the event list on the right; a row of plots
(the measure against its limits, the joint or jaw speed against the assumed rate, the finger-tip speed against the
package's 250 mm/s value, and "not modelled" where a current or a force would be); the film strip of key frames; a
footer that says what the picture is and is not.

## 3. Assets

The arm is upstream's CAD (`hardware/`, CC BY-NC-SA 4.0, never edited here; the OBJs are regenerated, not committed).
The operator is one of the two CC0 Quaternius figures in [`library/people/`](library/people/README.md), copied from
LionDriver's library, reset to the rig's rest pose with a relaxed curl of the fingers, so a hand in a gap shows its fingers there.
The bench, clamps, floor and lights are procedural. No HDRI or texture is fetched.
