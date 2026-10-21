# Operator figures

Two figures for the operator and bystander of the hazard scenes, copied unchanged from LionDriver's library (`assurance/sim/blender/library/people/` there, where `build_people.py` rebuilds them). They are built by
[`build_people.py`](build_people.py) from two free Quaternius packs, both **CC0 1.0** (public domain dedication; no
attribution required), so the built files are committed here rather than fetched. Pictures only: synthetic,
no evidence credit.

| File | Figure | Built from |
|---|---|---|
| `pedestrian_male.glb` | Male base character, short parted hair; 1.78 m | Universal Base Characters [Standard]: `Superhero_Male_FullBody`, `Hair_SimpleParted` |
| `pedestrian_female.glb` | Female base character, hair in buns; 1.66 m | Universal Base Characters [Standard]: `Superhero_Female_FullBody`, `Hair_Buns` |

Both files carry the pack's 65-bone rig and the `Walk_Loop` animation of the Universal Animation Library [Standard].
Their textures are cut to 1024 px JPEG, and the grey hair textures are tinted brown. Clothes are assigned from the bone each polygon follows: a long-sleeved shirt, trousers and shoes. The head and hands keep the skin texture. The packs ship only base bodies, and
their outfits are in the paid versions.

**In a scene:**
- `render_scene.py` imports one figure per scene, stands it where the catalogue entry puts it, facing the bench, and
  poses the hands by inverse kinematics on the hand points the exporter computed (`reach`: one hand at a point;
  `lean`: both hands on the arm; `stand`: arms down, with a lean of the spine for a bystander looking in).
- The pack's base pose has closed hands, so a figure shows where a hand is, not the fingers (WP-P-12 OI-2).
- A scene picks the figure with `person: {figure: male | female}` in [`../../scenes.yaml`](../../scenes.yaml).

**Sources** (downloaded 2026-10-19):
- Universal Base Characters: [quaternius.com](https://quaternius.com/packs/universalbasecharacters.html), [itch.io](https://quaternius.itch.io/universal-base-characters).
- Universal Animation Library: [quaternius.com](https://quaternius.com/packs/universalanimationlibrary.html), [itch.io](https://quaternius.itch.io/universal-animation-library).

Both packs' `License.txt` give CC0 1.0. To rebuild, download the two "Standard" zips and run:

```sh
python3 assurance/sim/blender/library/people/build_people.py "Universal Base Characters[Standard].zip" "Universal Animation Library[Standard].zip"
```
