#!/usr/bin/env python3
"""Checks of the standards tour: the figures are current and well formed, every stop has its page with its figures,
and the pages' previous and next links follow the order of TOUR in tour_figures.py."""
from __future__ import annotations

import re
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tour_figures as tf  # noqa: E402

WIKI = HERE.parents[1] / "wiki"
NAV = re.compile(r"^\[Standards tour\]\(Standards-tour\.md\) · stop (\d+) of (\d+) · ← \[[^\]]+\]\(([^)]+)\) · \[[^\]]+\]\(([^)]+)\) →$", re.M)


class TestFigures(unittest.TestCase):
  def test_committed_figures_are_current(self):
    self.assertEqual(tf.main(["--check"]), 0)

  def test_every_figure_is_well_formed_and_respects_reduced_motion(self):
    for name, svg in tf.render_all().items():
      root = ET.fromstring(svg)
      ns = "{http://www.w3.org/2000/svg}"
      self.assertTrue(root.find(f"{ns}title").text, name)
      self.assertTrue(root.find(f"{ns}desc").text, name)
      self.assertIn("prefers-reduced-motion:reduce", svg, name)

  def test_every_registered_figure_is_drawn(self):
    wanted = {f for s in tf.TOUR for f in s["figs"]} | set(tf.LANDING["figs"])
    self.assertEqual(wanted, set(tf.FIGS))

  def test_risk_graph_matches_the_package_ratings(self):
    for hz, r in tf.risk_ratings().items():
      self.assertEqual(tf.RISK_GRAPH[(r["s"], r["f"], r["p"])], r["plr"], hz)

  def test_ratings_and_gaps_are_read_from_the_record(self):
    self.assertIn("HZ-M01", tf.risk_ratings())
    self.assertEqual(tf.iso13854_gaps()["finger"], 25)


class TestPages(unittest.TestCase):
  def test_every_stop_has_its_page_figures_and_nav_in_order(self):
    n = len(tf.TOUR)
    for i, stop in enumerate(tf.TOUR):
      text = (WIKI / stop["page"]).read_text(encoding="utf-8")
      for fig in stop["figs"]:
        self.assertIn(f"../docs/assets/rebot/tour/{fig}.svg", text, stop["page"])
      navs = NAV.findall(text)
      self.assertEqual(len(navs), 2, f"{stop['page']}: expected the nav line at the top and the bottom")
      for num, total, prev, nxt in navs:
        self.assertEqual((int(num), int(total)), (i + 1, n), stop["page"])
        self.assertEqual(prev, tf.TOUR[i - 1]["page"] if i else "Standards-tour.md", stop["page"])
        self.assertEqual(nxt, tf.TOUR[i + 1]["page"] if i + 1 < n else "Standards-tour.md", stop["page"])
      self.assertIn("to be checked", text, f"{stop['page']}: clause references must be marked to be checked")
      self.assertIn("## What the project does not claim", text, stop["page"])

  def test_the_landing_page_lists_every_stop_and_its_figures(self):
    text = (WIKI / tf.LANDING["page"]).read_text(encoding="utf-8")
    for stop in tf.TOUR:
      self.assertIn(f"]({stop['page']})", text, stop["page"])
    for fig in tf.LANDING["figs"]:
      self.assertIn(f"../docs/assets/rebot/tour/{fig}.svg", text)


if __name__ == "__main__":
  unittest.main()
