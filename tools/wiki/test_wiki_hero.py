#!/usr/bin/env python3
"""Checks of the wiki's Home banner: it is current, well formed, embeds upstream's image of the arm, and credits it."""
from __future__ import annotations

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import wiki_hero as wh  # noqa: E402


class TestWikiHero(unittest.TestCase):
  def test_committed_banner_is_current(self):
    self.assertEqual(wh.main(["--check"]), 0)

  def test_banner_embeds_the_arm_and_credits_upstream(self):
    svg = wh.render()
    root = ET.fromstring(svg)
    ns = "{http://www.w3.org/2000/svg}"
    self.assertTrue(root.find(f"{ns}title").text)
    self.assertIn("Seeed Studio", root.find(f"{ns}desc").text)
    self.assertIsNotNone(root.find(f"{ns}image"))
    self.assertIn("not affiliated with or endorsed by Seeed Studio", svg)

  def test_home_page_uses_the_banner(self):
    home = (HERE.parents[1] / "wiki" / "Home.md").read_text(encoding="utf-8")
    self.assertTrue(home.startswith("![") and "docs/assets/rebot/wiki-hero.svg" in home.splitlines()[0])


if __name__ == "__main__":
  unittest.main()
