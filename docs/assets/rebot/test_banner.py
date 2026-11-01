#!/usr/bin/env python3
"""Checks of the README and wiki banner: it is current, well formed, embeds upstream's image of the arm, and credits it."""
from __future__ import annotations

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import banner as wh  # noqa: E402


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
    home = (HERE.parents[2] / "wiki" / "Home.md").read_text(encoding="utf-8")
    self.assertTrue(home.startswith("![") and "docs/assets/rebot/banner.svg" in home.splitlines()[0])

  def test_readme_assurance_section_opens_with_the_banner(self):
    readme = (HERE.parents[2] / "README.md").read_text(encoding="utf-8")
    section = readme.split("## The assurance record", 1)[1]
    first_image = section[section.index("<img"):].split(">", 1)[0]
    self.assertIn("docs/assets/rebot/banner.svg", first_image)


if __name__ == "__main__":
  unittest.main()
