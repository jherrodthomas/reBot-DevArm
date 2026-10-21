# WP-P-12 Hazard scenes and simulation pictures

| Field | Value |
|---|---|
| Work product | WP-P-12 |
| Title | Hazard scenes and simulation pictures: the hazards of WP-C-03 drawn on upstream's CAD |
| Standard reference | ISO 12100:2010 §5.4 (an aid to hazard identification and to the risk-graph inputs of ISO 13849-1 Annex A); ISO 21448 §6 as an informative method for scenario-based review. Clause numbers are to be checked against licensed copies |
| Version | 0.2 (2026-10-21): the figure's hands open (rest pose with a relaxed curl) so the hand-guiding scenes show fingers in the gap; all twelve scenes re-rendered. 0.1 (2026-10-21): the joint rig built from upstream's STEP, a catalogue of twelve hazard scenes, the kinematic exporter, the Blender renderer, the dashboard composer and the gallery |
| Status | Draft. AI-drafted (Claude, AI assistant; I0 under [WP-M-02 §3.3](../01-management/WP-M-02-safety-plan.md#33-ai-assisted-authoring)); not reviewed. **Pictures only: synthetic, no evidence credit** ([§4](#4-what-the-pictures-are-and-are-not)) |
| Owner | Safety manager (role, WP-M-02 §3.1); drafted by the Claude session |
| Configuration | CFG-001, reBot Arm B601-DM v1.1 (WP-C-01 §2); the STEP of BL-001 (`206ebda`) |
| Feeds | Review of [WP-C-03](../02-concept/WP-C-03-risk-assessment.md) (the ratings, OI-1 re-rating for OE-1), [WP-C-04](../02-concept/WP-C-04-safety-functions-and-plr.md) (what each safety function would change), [WP-C-06](../02-concept/WP-C-06-human-robot-interaction-and-misuse.md) (the interaction situations), the mechanical analysis of joint gaps (WP-H-10, GAP-01); figures for the wiki. Nothing in the safety case |

![Dashboard of hz-m01-elbow-pinch-teach: the elbow closing on the operator's fingers while hand-guiding in TEACH; the large view shows the elbow gap at 25 mm with the operator's arm reaching in, the plots the gap against the ISO 13854 limits, the events and the stop functions that do not exist at BL-001](blender/dashboards/hz-m01-elbow-pinch-teach.jpg)

*The elbow pinch of HZ-M01 at the moment the link gap passes the ISO 13854 finger gap; all twelve are in the
[gallery](blender/dashboards/README.md). A red band on every picture says what it is: synthetic, no evidence credit.*

## 1. Purpose

The risk assessment of the arm ([WP-C-03](../02-concept/WP-C-03-risk-assessment.md)) rates 34 hazards from the
concept-phase package, most of them on a desktop arm nobody in the project has yet seen move under the fork's rules.
The pictures here put each hazard that a picture helps in front of a reviewer: the real geometry of upstream's CAD,
posed by a joint rig at the moment the hazard occurs, with a person where the interaction situations of WP-C-06
put them, and with the numbers the geometry gives (a link gap against the ISO 13854 minimum gaps, a distance, a
speed) alongside the package's rating and the stop functions that do or do not exist at BL-001.

They are a review aid, the same as LionDriver's hazardous-event scenes (`assurance/sim/blender/` there): they help the
lead and a reviewer see what a rating means and what a safety function would change. They are not evidence of
anything, and the first safety case claims nothing from them (§4).

## 2. Where things are

| Path | Content |
|---|---|
| [`blender/scenes.yaml`](blender/scenes.yaml) | The catalogue: one entry per hazard scene with the hazard, the package's rating, the safety functions, the stop functions at BL-001, the pose, the kinematic motion and its assumed rate, the person, the cameras and the caption |
| [`blender/arm_model.py`](blender/arm_model.py) | The joint rig: the link groups of upstream's assembly tree, six joint axes read off the actuator housings, the gripper's rail, forward kinematics, link gaps and surface heights (numpy only) |
| [`blender/step_to_obj.py`](blender/step_to_obj.py) | Tessellates upstream's STEP into one OBJ per part with OpenCascade (`mesh/`, git-ignored; regenerate) |
| [`blender/export_scene.py`](blender/export_scene.py) | Resolves a catalogue entry into `out/<scene>/scene.json`: the pose over time, the gap or distance series, the events, the key frames to render |
| [`blender/render_scene.py`](blender/render_scene.py) | Poses the CAD at each key frame and renders the cameras with Blender (bpy, Cycles on the CPU); places and IK-poses the CC0 operator figure |
| [`blender/compose.py`](blender/compose.py) | The review dashboard of a scene (one HTML page, screenshot to PNG with headless Chromium) |
| [`blender/gallery.py`](blender/gallery.py) | The gallery [`blender/dashboards/README.md`](blender/dashboards/README.md) and the committed JPEGs (generated; CI checks it) |
| [`blender/test_scenes.py`](blender/test_scenes.py) | CI: every scene references a hazard and safety functions of `trace/items/hazards.yaml`, the poses are within the assumed limits, the rig's reference geometry holds, the gallery is current |
| [`blender/library/people/`](blender/library/people/README.md) | The two CC0 Quaternius figures, copied from LionDriver's library |
| [`requirements.txt`](requirements.txt) | Pinned packages; only PyYAML and numpy for the checks |

```sh
python3 assurance/sim/blender/step_to_obj.py hardware/reBot_B601_DM/reBot_B601_DM_v1.1_20260425.step assurance/sim/blender/mesh   # once, 25 s
python3 assurance/sim/blender/export_scene.py                       # every scene, about 10 s
python3 assurance/sim/blender/render_scene.py assurance/sim/blender/out/hz-m01-elbow-pinch-teach --samples 48 --size 900x506
python3 assurance/sim/blender/compose.py assurance/sim/blender/out/hz-m01-elbow-pinch-teach
python3 assurance/sim/blender/gallery.py
python3 assurance/sim/blender/test_scenes.py                        # CI
```

Rendering is Cycles on the CPU: about 20 s per still at 900 by 506 pixels and 48 samples (the dashboard shows the
large view at that size), so a scene with six key frames and three cameras takes about seven minutes on four cores.

## 3. The joint rig

Upstream's STEP assembly groups its 326 parts by link (Base, Link1 to Link6, Gripper), so a joint is the rotation of
every group from its child onward about one axis. The six axes were read off the actuator housings (the centre of
each DM-J4340P or DM-J4310 bounding box, the axis along its short side) and checked against the spacer that bolts
each child link to the output flange. The as-modelled pose is the reference `q = 0`: upper arm horizontal, forearm
folded back over it, wrist up, gripper pointing away from the base along -X. The gripper is a rack-and-pinion slide
on a 170 mm rail: its opening moves the two fingers, sliders, extensions and racks apart along the rail.

| Joint | Actuator | Axis at `q = 0` (mm, STEP frame) | Positive direction | Assumed limit (deg) |
|---|---|---|---|---|
| J1 base yaw | DM-J4340P | through (0, 0, 52.5), +Z | right-hand about +Z | ±170 |
| J2 shoulder pitch | DM-J4340P | through (-20, -3.4, 143.5), Y | raises the upper arm | -10 to 100 |
| J3 elbow pitch | DM-J4340P | through (244, -3.4, 143.5), Y | opens the elbow (0 = folded, as modelled) | 0 to 170 |
| J4 wrist pitch | DM-J4310 | through (1.4, -3, 197.5), Y | opens the wrist | ±100 |
| J5 wrist roll | DM-J4310 | through (-76.9, 0, 260), Z | right-hand | ±180 |
| J6 tool roll | DM-J4310 | through (-77.6, 0, 195), X | right-hand | continuous |
| Gripper | DM-J4310 | fingers along Y, closed at 0 mm | opening | 0 to 80 mm (assumed) |

The link lengths from the axes: upper arm 264 mm, forearm 249 mm, wrist 100 mm, J6 to the finger tips 182 mm; the
finger tips reach about 750 mm from the base axis over the assumed J2 and J3 ranges (the package says 650 mm, the
difference is the assumed limits). **Upstream declares no joint limits or speeds** (GAP-10218-03): every limit and
every rate in the catalogue is an assumption named in the scene's caption, and the speed caps per mode are an open
decision (DQ-016). The rig moves the geometry; it has no dynamics, no actuator model, no controller and no contact.

Link gaps are the smallest distance between the posed points of the two links a joint connects, leaving out the
points within 45 mm of the joint axis (the actuator housing itself, where the gap is always zero). The points are
every 24th vertex of the tessellation, so a gap is right to a few millimetres, and the "surface" scenes measure the
lowest point of a link group above the bench plane.

## 4. What the pictures are, and are not

| | Is | Is not |
|---|---|---|
| Geometry | Upstream's v1.1 CAD, tessellated and posed by the rig of §3 | A measurement of a built arm; the printed parts and covers as fitted |
| Motion | One joint or the gripper moving at an assumed rate, nothing stopping it; the scene freezes at the first contact and says so | A run of the controller, the SDK or a policy; a plant; any dynamics |
| Numbers | Gaps, heights, distances and finger-tip speeds from the kinematics, against the ISO 13854 gaps (25, 100, 120, 500 mm, to be checked) and the package's 250 mm/s reduced-speed value | Forces, pressures, currents, temperatures: every dashboard says "not modelled" where it would show one |
| Person | A CC0 figure placed where WP-C-06 puts the person, hands posed by inverse kinematics with relaxed open fingers; the head or hand *point* the distance is measured to is the scene's | A body model; a hand whose fingers are measured (only the point is); a human response |
| Rating | The package's S, F, P, PLr and category as WP-C-03 §5 carries them, with the note that OE-1 re-rating is open (OI-1) | A rating this record has accepted |
| Stops | The stop functions WP-C-04 allocates, with their state at BL-001 (most do not exist) | A claim that any of them works |

A red band on every render reads *synthetic, no evidence credit*. No scene is referenced from a claim or an evidence
record in `case/`, and `test_scenes.py` does not check anything about the arm, only about the catalogue.

## 5. The scenes

Twelve scenes, one per hazard of WP-C-03 that a picture helps ([gallery with the outcomes](blender/dashboards/README.md)):
the hand-guiding pinches (HZ-M01 at the elbow, HZ-M02 in the gripper, HZ-P03 against the bench), the RUN strikes and
contacts (HZ-M04 sweep into a head, HZ-P02 a hand reaching in, HZ-P01 the forehead), tip-over (HZ-M06) and payload
drop (HZ-M07), restart with the operator in reach (HZ-P04), the control hazards that end in the elbow gap (HZ-C05
limit overshoot, HZ-C01 last-command hold) and entanglement at the tool roll (HZ-M05). Each dashboard says what would
change the outcome, in WP-C-04 and WP-C-06 terms.

What the first twelve already show the reviewer: the elbow and wrist gaps of the as-modelled covers close through the
finger gap well before the modelled end-stop (HZ-M01, HZ-C05, HZ-C01: a joint-gap design measure, DM-02, is not
optional, GAP-01); a person at the bench edge is inside the sweep of the gripper at every pose that reaches the near
side (HZ-M04, HZ-P04: the marked area of WP-C-02 §6 has to be at the far side of the bench or the base turned); and
the package's rates for TEACH and RUN are the numbers every outcome turns on (DQ-016).

## 6. Open items

| ID | Item | Owner | Gate |
|---|---|---|---|
| OI-1 | Replace the assumed joint limits, rates and gripper opening with upstream's declared values once they exist (GAP-10218-03) or the lead's (DQ-016); re-export every scene | Systems engineer | G1 |
| OI-2 | Condition variants per operating envelope (OE-2 classroom with a second person, OE-3 cell) once the envelopes are decided (DQ-003) | Safety manager | G1 |
| OI-3 | When the controller safety layer exists (DQ-020), a plant layer that runs its stop functions against these motions, as LionDriver's layer 1 does; until then every scene is kinematic | Software safety engineer | G3 |
