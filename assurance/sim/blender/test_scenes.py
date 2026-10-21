#!/usr/bin/env python3
"""Checks of the hazard-scene catalogue (CI): every scene references a hazard and safety functions of
trace/items/hazards.yaml, its pose is within the assumed limits, the joint rig's reference geometry is consistent, and
the gallery README matches the catalogue. Needs PyYAML and numpy; no Blender."""
from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import arm_model  # noqa: E402
import export_scene  # noqa: E402
import gallery  # noqa: E402


class TestCatalogue(unittest.TestCase):
  def setUp(self):
    self.cat = export_scene.load_scenes(); self.items = export_scene.load_items()

  def test_every_scene_is_consistent(self):
    problems = [p for s in self.cat["scenes"] for p in export_scene.check(s, self.items, self.cat)]
    self.assertEqual(problems, [])

  def test_ids_are_unique_and_named_after_their_hazard(self):
    ids = [s["id"] for s in self.cat["scenes"]]
    self.assertEqual(len(ids), len(set(ids)))
    for s in self.cat["scenes"]:
      self.assertTrue(s["id"].startswith(s["hz"].lower() + "-"), s["id"])

  def test_iso_13854_gaps_are_ordered(self):
    lim = self.cat["iso_13854_mm"]
    self.assertLess(lim["finger"], lim["hand"]); self.assertLess(lim["hand"], lim["arm"]); self.assertLess(lim["arm"], lim["body"])

  def test_check_reports_a_bad_reference(self):
    bad = dict(self.cat["scenes"][0]); bad["hz"] = "HZ-ZZ99"; bad["sf"] = ["SF-99"]
    problems = export_scene.check(bad, self.items, self.cat)
    self.assertTrue(any("HZ-ZZ99" in p for p in problems)); self.assertTrue(any("SF-99" in p for p in problems))

  def test_gallery_readme_is_current(self):
    self.assertEqual(gallery.main(["--check"]), 0)


class TestArmModel(unittest.TestCase):
  def test_reference_pose_is_identity(self):
    p = (-260.0, 0.0, 195.0)
    self.assertEqual(tuple(arm_model.fk(p, [0] * 6)), p)

  def test_j1_turns_the_tip_about_z(self):
    t = arm_model.tcp([90, 0, 0, 0, 0, 0])
    self.assertAlmostEqual(t[2], 195.0, places=6)
    self.assertAlmostEqual(math.hypot(t[0], t[1]), 260.0, places=6)
    self.assertAlmostEqual(t[1], -260.0, places=6)

  def test_j2_raises_the_upper_arm(self):
    elbow = arm_model.joint_origin("J3", [0, 90, 0, 0, 0, 0])
    self.assertAlmostEqual(elbow[0], -20.0, places=6); self.assertAlmostEqual(elbow[2], 143.5 + 264.0, places=6)

  def test_j3_opens_the_elbow(self):
    wrist = arm_model.joint_origin("J4", [0, 0, 90, 0, 0, 0])
    self.assertGreater(wrist[2], 300.0)   # the forearm points up from the elbow

  def test_limits_are_checked(self):
    self.assertEqual(arm_model.check_pose([0] * 6), [])
    self.assertEqual(len(arm_model.check_pose([0, 0, -10, 0, 0, 0])), 1)

  def test_rotation_is_orthonormal(self):
    r = arm_model.rotation((1, 2, 3), 37.0)
    self.assertTrue((abs(r @ r.T - [[1, 0, 0], [0, 1, 0], [0, 0, 1]]) < 1e-12).all())


if __name__ == "__main__":
  unittest.main()
