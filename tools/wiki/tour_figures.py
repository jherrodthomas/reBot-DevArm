#!/usr/bin/env python3
"""Animated figures of the wiki's standards tour, one or two per standard page.

Each figure explains one idea of a standard (the risk reduction loop of ISO 12100, the risk graph of ISO 13849-1, the
stop categories of EN 60204-1, ...) as a short looping animation in plain SVG with CSS keyframes, so it plays inside a
GitHub image. Every figure is drawn in its finished, fully labelled state: a viewer that does not animate, or a reader
who asks for reduced motion, sees the whole picture at once; the animation only reveals it step by step.

Where a figure shows something about the arm, the value is read from the record when the figure is generated (the
package's risk-graph ratings from WP-C-03 §5, the ISO 13854 gaps the hazard scenes use from
assurance/sim/blender/scenes.yaml, the tour itself from TOUR below), never typed here. Everything else is the
standard's own idea drawn generically. The figures explain; they claim nothing about the arm, and the clause
references on the pages are to be checked against a licensed copy.

  python3 tools/wiki/tour_figures.py           # write docs/assets/rebot/tour/*.svg
  python3 tools/wiki/tour_figures.py --check   # CI: fail if a committed figure differs from a fresh render
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "docs" / "assets" / "rebot" / "tour"
WP_C03 = ROOT / "assurance" / "02-concept" / "WP-C-03-risk-assessment.md"
SCENES = ROOT / "assurance" / "sim" / "blender" / "scenes.yaml"

FONT = "'Source Sans 3', 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
C = {
  "bg": "#FFFFFF", "panel": "#F4F3EF", "ink": "#122026", "muted": "#4E6A73", "line": "#C9D6DB", "navy": "#1E4752",
  "mid": "#5F8F99", "light": "#B9CFD4", "pale": "#E8F0F2", "gold": "#F2A33A", "gold_text": "#8A5A0B",
  "cream": "#FBF3E3", "teal": "#0E8C83", "red": "#D64535", "red_pale": "#FBE3E0", "green": "#2E8B57",
  "green_pale": "#E3F3EA", "white": "#FFFFFF",
}
W = 960
FOOT = "Explains the standard's idea, not a claim about the arm · clause references to be checked · tools/wiki/tour_figures.py"

# The tour: the order a newcomer meets the standards, following the arm through its lifecycle. The wiki pages carry
# the same order in their "previous / next" lines; test_tour_figures.py checks that they agree.
CHAPTERS = [
  ("1", "Find the risk"), ("2", "Make the stop reliable"), ("3", "Wire it and stop it"),
  ("4", "Keep people out of harm's way"), ("5", "Check the design"), ("6", "New kinds of risk"),
  ("7", "Argue it and run it"), ("8", "The law"),
]
TOUR = [
  {"page": "ISO-12100-risk-assessment.md", "name": "ISO 12100", "topic": "risk assessment and risk reduction", "chapter": "1", "figs": ["iso-12100"]},
  {"page": "ISO-10218-industrial-robots.md", "name": "ISO 10218-1 and -2", "topic": "industrial robots and robot applications", "chapter": "1", "figs": ["iso-10218"]},
  {"page": "ISO-13849-control-system-reliability.md", "name": "ISO 13849-1 and -2", "topic": "safety-related parts of control systems", "chapter": "2", "figs": ["iso-13849-risk-graph", "iso-13849-category-3"]},
  {"page": "IEC-62061-machinery-SIL.md", "name": "IEC 62061", "topic": "functional safety of machinery control systems", "chapter": "2", "figs": ["iec-62061"]},
  {"page": "IEC-61508-functional-safety.md", "name": "IEC 61508", "topic": "the functional safety umbrella", "chapter": "2", "figs": ["iec-61508"]},
  {"page": "EN-60204-electrical-equipment.md", "name": "EN 60204-1", "topic": "electrical equipment of machines", "chapter": "3", "figs": ["en-60204"]},
  {"page": "ISO-13850-emergency-stop.md", "name": "ISO 13850", "topic": "the emergency stop function", "chapter": "3", "figs": ["iso-13850"]},
  {"page": "ISO-13854-minimum-gaps.md", "name": "ISO 13854", "topic": "minimum gaps to avoid crushing", "chapter": "4", "figs": ["iso-13854"]},
  {"page": "ISO-13857-reach-distances.md", "name": "ISO 13857", "topic": "safety distances against reaching", "chapter": "4", "figs": ["iso-13857"]},
  {"page": "ISO-13855-separation-distance.md", "name": "ISO 13855", "topic": "positioning safeguards: approach speed and stopping time", "chapter": "4", "figs": ["iso-13855"]},
  {"page": "ISO-TS-15066-collaborative-robots.md", "name": "ISO/TS 15066", "topic": "collaborative robots", "chapter": "4", "figs": ["iso-ts-15066"]},
  {"page": "IEC-60812-FMEA.md", "name": "IEC 60812", "topic": "failure modes and effects analysis", "chapter": "5", "figs": ["iec-60812"]},
  {"page": "IEC-61025-fault-tree-analysis.md", "name": "IEC 61025", "topic": "fault tree analysis", "chapter": "5", "figs": ["iec-61025"]},
  {"page": "ISO-21448-performance-limits.md", "name": "ISO 21448", "topic": "hazards without a failure (used as a method)", "chapter": "5", "figs": ["iso-21448"]},
  {"page": "IEC-62443-cybersecurity.md", "name": "IEC 62443", "topic": "industrial cybersecurity", "chapter": "6", "figs": ["iec-62443"]},
  {"page": "ISO-IEC-TR-5469-AI-and-safety.md", "name": "ISO/IEC TR 5469", "topic": "artificial intelligence and functional safety", "chapter": "6", "figs": ["iso-iec-tr-5469"]},
  {"page": "UL-4600-safety-case.md", "name": "UL 4600", "topic": "the safety case", "chapter": "7", "figs": ["ul-4600"]},
  {"page": "Automotive-SPICE-process-capability.md", "name": "Automotive SPICE", "topic": "process capability", "chapter": "7", "figs": ["aspice"]},
  {"page": "Machinery-Regulation.md", "name": "Machinery Regulation", "topic": "Regulation (EU) 2023/1230", "chapter": "8", "figs": ["machinery-regulation"]},
  {"page": "AI-Act.md", "name": "AI Act", "topic": "Regulation (EU) 2024/1689", "chapter": "8", "figs": ["ai-act"]},
]
LANDING = {"page": "Standards-tour.md", "figs": ["tour-map", "tour-pyramid"]}


# ================================================================ animation

class Anim:
  """CSS keyframes on one loop. Every element keeps its finished state as its base style, so with the animation off
  (reduced motion, a viewer that does not animate) the figure shows everything; the keyframes hide it until its time
  and fade it out at the end of the loop, which then starts again."""

  def __init__(self, cycle: float):
    self.cycle = cycle
    self.reset = cycle - 0.8
    self.rules: list[str] = []
    self.n = 0

  def p(self, t: float) -> str:
    return f"{max(0.0, min(100.0, 100.0 * t / self.cycle)):.2f}%"

  def _name(self) -> str:
    self.n += 1
    return f"a{self.n}"

  def _rule(self, name: str, frames: str, base: str = "") -> str:
    self.rules.append(f"@keyframes {name}{{{frames}}}")
    self.rules.append(f".{name}{{animation:{name} {self.cycle:g}s linear infinite;{base}}}")
    return name

  def show(self, t: float, until: float | None = None, fade: float = 0.35, static: bool = True) -> str:
    """Hidden until t, visible from t + fade until `until` (default: the end of the loop)."""
    end = self.reset if until is None else until
    frames = (f"0%,{self.p(t)}{{opacity:0}}{self.p(t + fade)},{self.p(end)}{{opacity:1}}"
              f"{self.p(end + fade)},100%{{opacity:0}}")
    return self._rule(self._name(), frames, "" if static else "opacity:0;")

  def vis(self, windows: list[tuple[float, float | None]], static: bool = True, fade: float = 0.25) -> str:
    """Visible only inside the (start, end) windows; a window from 0 is visible as the loop starts, and an end of
    None keeps it visible through the end of the loop (so an element shown at both ends never blinks)."""
    pts: list[tuple[float, int]] = []
    for s0, s1 in windows:
      if s0 <= 0:
        pts.append((0.0, 1))
      else:
        pts += [(s0, 0), (s0 + fade, 1)]
      if s1 is None:
        pts.append((self.cycle, 1))
      else:
        pts += [(s1, 1), (s1 + fade, 0)]
    if pts[0][0] > 0:
      pts.insert(0, (0.0, 0))
    if pts[-1][0] < self.cycle:
      pts.append((self.cycle, 0))
    frames = "".join(f"{self.p(t)}{{opacity:{o}}}" for t, o in pts)
    return self._rule(self._name(), frames, "" if static else "opacity:0;")

  def draw(self, t: float, dur: float, length: float, until: float | None = None) -> str:
    """A stroke drawn from its start between t and t + dur (stroke-dasharray trick)."""
    end = self.reset if until is None else until
    L = f"{length:.0f}"
    frames = (f"0%,{self.p(t)}{{stroke-dashoffset:{L}}}{self.p(t + dur)},{self.p(end)}{{stroke-dashoffset:0}}"
              f"{self.p(end + 0.3)},100%{{stroke-dashoffset:{L}}}")
    return self._rule(self._name(), frames, f"stroke-dasharray:{L};stroke-dashoffset:0;")

  def move(self, pts: list[tuple[float, float, float]], static: tuple[float, float] | None = None) -> str:
    """Translate along (t, x, y) points, piecewise linear; holds the last point until the end of the loop."""
    sx, sy = static if static else pts[-1][1:]
    frames = [f"0%{{transform:translate({pts[0][1]:.1f}px,{pts[0][2]:.1f}px)}}"]
    frames += [f"{self.p(t)}{{transform:translate({x:.1f}px,{y:.1f}px)}}" for t, x, y in pts]
    frames.append(f"100%{{transform:translate({pts[-1][1]:.1f}px,{pts[-1][2]:.1f}px)}}")
    return self._rule(self._name(), "".join(frames), f"transform:translate({sx:.1f}px,{sy:.1f}px);")

  def turn(self, pts: list[tuple[float, float]], origin: tuple[float, float], static: float | None = None) -> str:
    """Rotate about origin through (t, degrees) points, piecewise linear; holds the last angle."""
    ox, oy = origin
    sa = pts[-1][1] if static is None else static
    frames = [f"0%{{transform:rotate({pts[0][1]:.1f}deg)}}"]
    frames += [f"{self.p(t)}{{transform:rotate({d:.1f}deg)}}" for t, d in pts]
    frames.append(f"100%{{transform:rotate({pts[-1][1]:.1f}deg)}}")
    return self._rule(self._name(), "".join(frames), f"transform-origin:{ox:.1f}px {oy:.1f}px;transform:rotate({sa:.1f}deg);")

  def style(self) -> str:
    return ("<style>" + "".join(self.rules) +
            "@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>")


# ================================================================ drawing

def esc(s: str) -> str:
  return escape(str(s), {'"': "&quot;"})


def cls(c: str) -> str:
  return f' class="{c}"' if c else ""


def text(x: float, y: float, s: str, size: float = 20, fill: str = C["ink"], weight: int = 400, anchor: str = "start",
         c: str = "", italic: bool = False, spacing: float = 0) -> str:
  extra = (' font-style="italic"' if italic else "") + (f' letter-spacing="{spacing}"' if spacing else "")
  return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
          f'text-anchor="{anchor}"{extra}{cls(c)}>{esc(s)}</text>')


def wrap(s: str, width: float, size: float) -> list[str]:
  per = max(4, int(width / (size * 0.52)))
  lines, cur = [], ""
  for w in s.split():
    if cur and len(cur) + 1 + len(w) > per:
      lines.append(cur)
      cur = w
    else:
      cur = f"{cur} {w}".strip()
  if cur:
    lines.append(cur)
  return lines


def para(x: float, y: float, s: str, size: float, width: float, fill: str = C["ink"], weight: int = 400,
         anchor: str = "start", c: str = "", lh: float = 1.25) -> str:
  return "".join(text(x, y + i * size * lh, ln, size, fill, weight, anchor, c) for i, ln in enumerate(wrap(s, width, size)))


def rect(x: float, y: float, w: float, h: float, fill: str, r: float = 10, stroke: str = "", sw: float = 2,
         c: str = "", dash: str = "") -> str:
  st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
  da = f' stroke-dasharray="{dash}"' if dash else ""
  return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}"{st}{da}{cls(c)}/>'


def line(x1: float, y1: float, x2: float, y2: float, stroke: str = C["muted"], sw: float = 2.5, arrow: bool = False,
         c: str = "", dash: str = "") -> str:
  m = ' marker-end="url(#ah)"' if arrow else ""
  da = f' stroke-dasharray="{dash}"' if dash else ""
  return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" '
          f'stroke-linecap="round"{da}{m}{cls(c)}/>')


def path(d: str, stroke: str = C["muted"], sw: float = 2.5, fill: str = "none", arrow: bool = False, c: str = "",
         dash: str = "") -> str:
  m = ' marker-end="url(#ah)"' if arrow else ""
  da = f' stroke-dasharray="{dash}"' if dash else ""
  return (f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}" stroke-linecap="round" '
          f'stroke-linejoin="round"{da}{m}{cls(c)}/>')


def circle(x: float, y: float, r: float, fill: str, stroke: str = "", sw: float = 2, c: str = "") -> str:
  st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
  return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"{st}{cls(c)}/>'


def g(inner: str, c: str = "", transform: str = "") -> str:
  tr = f' transform="{transform}"' if transform else ""
  return f"<g{cls(c)}{tr}>{inner}</g>"


def poly_len(pts: list[tuple[float, float]]) -> float:
  return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def poly_d(pts: list[tuple[float, float]]) -> str:
  return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def token(a: Anim, pts: list[tuple[float, float, float]], color: str = C["gold"], r: float = 11, t_hide: float | None = None) -> str:
  """A dot that travels along timed points; hidden in the finished picture."""
  mv = a.move(pts)
  sh = a.show(pts[0][0] - 0.2, t_hide if t_hide is not None else pts[-1][0] + 0.4, static=False)
  return g(g(circle(0, 0, r, color, C["white"], 3), mv), sh)


def chip(x: float, y: float, s: str, fill: str = C["pale"], ink: str = C["navy"], size: float = 15, c: str = "") -> str:
  w = len(s) * size * 0.56 + 16
  return g(rect(x, y - size - 3, w, size + 10, fill, r=6) + text(x + 8, y, s, size, ink, 600), c)


def arm_glyph(x: float, y: float, s: float = 1.0, a1: float = -60, a2: float = 70, color: str = C["navy"], turn: str = "") -> str:
  """A six-axis desktop arm in profile: base, upper arm, forearm, gripper. Angles in degrees from horizontal. `turn`
  is an Anim.turn class about the shoulder (x, y - 34 * s): it moves the links and leaves the base where it is."""
  r1, r2 = 70 * s, 62 * s
  sx, sy = x, y - 34 * s
  ex, ey = sx + r1 * math.cos(math.radians(a1)), sy + r1 * math.sin(math.radians(a1))
  wx, wy = ex + r2 * math.cos(math.radians(a2 + a1)), ey + r2 * math.sin(math.radians(a2 + a1))
  base = rect(x - 30 * s, y - 10 * s, 60 * s, 10 * s, C["navy"], r=3) + rect(x - 16 * s, y - 34 * s, 32 * s, 26 * s, color, r=5)
  links = (line(sx, sy, ex, ey, C["light"], 13 * s) + line(ex, ey, wx, wy, C["light"], 11 * s) + circle(ex, ey, 8 * s, color) +
           line(wx, wy, wx + 10 * s, wy + 12 * s, C["gold"], 5 * s) + line(wx, wy, wx + 14 * s, wy - 4 * s, C["gold"], 5 * s) +
           circle(wx, wy, 6 * s, color))
  return base + (g(links, turn) if turn else links) + circle(sx, sy, 9 * s, color)


def person_glyph(x: float, y: float, s: float = 1.0, color: str = C["mid"], c: str = "") -> str:
  """A standing person, feet at (x, y)."""
  return g(circle(x, y - 150 * s, 15 * s, color) +
           path(f"M{x:.1f},{y - 132 * s:.1f} L{x:.1f},{y - 70 * s:.1f} M{x - 26 * s:.1f},{y - 112 * s:.1f} L{x + 26 * s:.1f},{y - 112 * s:.1f} "
                f"M{x:.1f},{y - 70 * s:.1f} L{x - 18 * s:.1f},{y:.1f} M{x:.1f},{y - 70 * s:.1f} L{x + 18 * s:.1f},{y:.1f}", color, 9 * s), c)


def svg(slug: str, label: str, title: str, desc: str, body: list[str], h: int, a: Anim) -> str:
  head = (text(28, 34, label.upper(), 14, C["muted"], 700, spacing=1.2) + text(28, 66, title, 26, C["ink"], 700))
  foot = text(W / 2, h - 14, FOOT, 12.5, C["muted"], 400, "middle")
  return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" '
          f'aria-labelledby="t-{slug} d-{slug}" font-family="{FONT}">'
          f'<title id="t-{slug}">{esc(title)}</title><desc id="d-{slug}">{esc(desc)}</desc>'
          f'<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
          f'<path d="M0,0 L10,5 L0,10 z" fill="{C["muted"]}"/></marker></defs>'
          + a.style() + rect(0, 0, W, h, C["bg"], r=0) + head + "".join(body) + foot + "</svg>\n")


FIGS: dict[str, callable] = {}


def figure(slug: str):
  def deco(fn):
    FIGS[slug] = fn
    return fn
  return deco


# ================================================================ record data

def risk_ratings(path: Path = WP_C03) -> dict[str, dict]:
  """Package ratings from the WP-C-03 §5 table: hazard -> {scenario, s, f, p, plr}."""
  out = {}
  row = re.compile(r"^\| (HZ-[A-Z]\d\d) \| [^|]+ \| ([^|]+?) \| (S[12]) \| (F[12]) \| (P[12]) \| ([a-e]) \|")
  for ln in path.read_text(encoding="utf-8").splitlines():
    m = row.match(ln)
    if m:
      out[m.group(1)] = {"scenario": m.group(2).strip(), "s": m.group(3), "f": m.group(4), "p": m.group(5), "plr": m.group(6)}
  return out


def iso13854_gaps(path: Path = SCENES) -> dict[str, int]:
  """The ISO 13854 minimum gaps the hazard scenes use (scenes.yaml, iso_13854_mm)."""
  m = re.search(r"^iso_13854_mm:\s*\{([^}]*)\}", path.read_text(encoding="utf-8"), re.M)
  if not m:
    raise SystemExit("scenes.yaml has no iso_13854_mm line")
  return {k.strip(): int(v) for k, v in (kv.split(":") for kv in m.group(1).split(","))}


RISK_GRAPH = {("S1", "F1", "P1"): "a", ("S1", "F1", "P2"): "b", ("S1", "F2", "P1"): "b", ("S1", "F2", "P2"): "c",
              ("S2", "F1", "P1"): "c", ("S2", "F1", "P2"): "d", ("S2", "F2", "P1"): "d", ("S2", "F2", "P2"): "e"}


# ================================================================ figures

@figure("tour-map")
def tour_map() -> str:
  a = Anim(17)
  h = 650
  cw, gap, x0 = 219, 12, 24
  ys = (92, 346)
  ch_h = 236
  step = 1.6
  body = []
  for i, (num, name) in enumerate(CHAPTERS):
    col, row = i % 4, i // 4
    x, y = x0 + col * (cw + gap), ys[row]
    t = 0.3 + i * step
    stops = [s for s in TOUR if s["chapter"] == num]
    card = rect(x, y, cw, ch_h, C["panel"], r=14)
    card += circle(x + 26, y + 30, 17, C["navy"]) + text(x + 26, y + 37, num, 19, C["white"], 700, "middle")
    for k, ln in enumerate(wrap(name, cw - 66, 18)):
      card += text(x + 52, y + 28 + k * 21, ln, 18, C["ink"], 700)
    inner = ""
    for k, s in enumerate(stops):
      yy = y + 118 + k * 32
      inner += g(circle(x + 22, yy - 6, 6, C["gold"]) + text(x + 36, yy, s["name"], 17, C["ink"], 600),
                 a.show(t + 0.35 + 0.25 * k))
    hi = rect(x - 3, y - 3, cw + 6, ch_h + 6, "none", r=16, stroke=C["gold"], sw=4, c=a.show(t, t + step, static=False))
    body.append(g(card, a.show(t)) + inner + hi)
  n_pages, n_ch = len(TOUR), len(CHAPTERS)
  body.append(text(W / 2, 612, f"{n_pages} stops in {n_ch} chapters, read left to right, top to bottom", 17, C["muted"], 400, "middle"))
  return svg("tour-map", "Standards tour", "The route: from finding the risk to the law", (
    f"The {n_pages} stops of the standards tour in {n_ch} chapters, revealed chapter by chapter: " +
    "; ".join(f"{n} {name}: " + ", ".join(s['name'] for s in TOUR if s['chapter'] == n) for n, name in CHAPTERS) + "."),
    body, h, a)


@figure("tour-pyramid")
def tour_pyramid() -> str:
  a = Anim(14)
  h = 580
  cx, base_y = 320, 520
  tiers = [  # (label, standards, bottom width, fill, ink)
    ("Type A · basic concepts", "ISO 12100: every machine", 600, C["navy"], C["white"]),
    ("Type B · aspects and safeguards", "ISO 13849-1/-2 · EN 60204-1 · ISO 13850 · ISO 13854 · ISO 13855 · ISO 13857", 480, C["mid"], C["white"]),
    ("Type C · one kind of machine", "ISO 10218-1/-2, industrial robots, with ISO/TS 15066", 360, C["gold"], C["ink"]),
  ]
  th = 124
  body = [g(text(cx, 112, "Where a type C standard differs from A or B, type C governs (to be checked)", 15.5, C["muted"], 400, "middle"), a.show(9.4))]
  for i, (lab, stds, w, fill, ink) in enumerate(tiers):
    y = base_y - (i + 1) * th
    top_w = w - 120
    d = f"M{cx - w / 2:.0f},{y + th:.0f} L{cx + w / 2:.0f},{y + th:.0f} L{cx + top_w / 2:.0f},{y + 6:.0f} L{cx - top_w / 2:.0f},{y + 6:.0f} Z"
    tier = path(d, "none", 0, fill) + text(cx, y + 42, lab, 19, ink, 700, "middle")
    tier += para(cx, y + 70, stds, 16, top_w - 30, ink, 400, "middle")
    body.append(g(tier, a.show(0.4 + i * 1.6)))
  ax = 648
  body.append(g(line(ax, base_y - 20, ax, base_y - 3 * th + 20, C["muted"], 2.5, arrow=True) +
                f'<text x="{ax - 12}" y="{base_y - 1.5 * th:.0f}" font-size="16" fill="{C["muted"]}" font-weight="700" text-anchor="middle" '
                f'transform="rotate(-90 {ax - 12} {base_y - 1.5 * th:.0f})">more specific</text>', a.show(5.4)))
  side_x, side_w = 676, 272
  side = [("Functional safety", "IEC 61508 · IEC 62061"), ("Analysis methods", "IEC 60812 · IEC 61025 · ISO 21448"),
          ("New kinds of risk", "IEC 62443 · ISO/IEC TR 5469"), ("Argument and process", "UL 4600 · Automotive SPICE"),
          ("Law, not a standard", "Machinery Regulation · AI Act")]
  body.append(g(text(side_x, 150, "Beside the pyramid", 18, C["ink"], 700), a.show(6.4)))
  for k, (lab, stds) in enumerate(side):
    y = 172 + k * 68
    body.append(g(rect(side_x, y, side_w, 58, C["panel"], r=10) + text(side_x + 12, y + 24, lab, 16, C["muted"], 700) +
                  text(side_x + 12, y + 47, stds, 15, C["ink"], 600), a.show(6.8 + 0.45 * k)))
  return svg("tour-pyramid", "Standards tour", "How machinery standards stack: types A, B and C", (
    "A pyramid built from the bottom: type A, ISO 12100, basic concepts for every machine; type B, one safety aspect or "
    "one kind of safeguard (ISO 13849-1 and -2, EN 60204-1, ISO 13850, ISO 13854, ISO 13855, ISO 13857); type C, one "
    "kind of machine, ISO 10218-1 and -2 for industrial robots with ISO/TS 15066. An arrow marks the tiers as more "
    "specific towards the top; where a type C standard differs from A or B, type C governs. Beside it the standards "
    "outside the pyramid: functional safety, analysis methods, cybersecurity and AI, the safety case and process "
    "capability, and the law."), body, h, a)


@figure("iso-12100")
def iso_12100() -> str:
  a = Anim(17)
  h = 700
  lx, lw, bh = 40, 330, 54
  left = [("Limits of the machine", "WP-C-01"), ("Identify hazards", "WP-C-03"), ("Estimate the risk", "WP-C-03"), ("Evaluate the risk", "WP-C-03")]
  ys = [124, 202, 280, 358]
  body = [g(text(lx, 110, "RISK ASSESSMENT", 14, C["muted"], 700, spacing=1.2), a.show(0.2))]
  for i, ((lab, wp), y) in enumerate(zip(left, ys)):
    blk = rect(lx, y, lw, bh, C["pale"], r=10) + text(lx + 16, y + 35, f"{i + 1}  {lab}", 20, C["ink"], 700) + chip(lx + lw - 92, y + 33, wp)
    body.append(g(blk, a.show(0.3 + 0.5 * i)))
    if i:
      body.append(g(line(lx + lw / 2, ys[i - 1] + bh, lx + lw / 2, y - 4, arrow=True), a.show(0.3 + 0.5 * i)))
  dx, dy = lx + lw / 2, 490
  dia = path(f"M{dx},{dy - 46} L{dx + 110},{dy} L{dx},{dy + 46} L{dx - 110},{dy} Z", C["gold"], 2.5, C["cream"]) + text(dx, dy + 7, "Reduced enough?", 19, C["ink"], 700, "middle")
  body.append(g(line(dx, ys[-1] + bh, dx, dy - 50, arrow=True) + dia, a.show(2.3)))
  doc_y = 580
  body.append(g(line(dx, dy + 46, dx, doc_y - 4, arrow=True) + text(dx + 10, dy + 72, "yes", 17, C["green"], 700) +
                rect(lx, doc_y, lw, bh, C["green_pale"], r=10) + text(lx + 16, doc_y + 35, "Document it, then stop", 20, C["ink"], 700) +
                chip(lx + lw - 92, doc_y + 33, "WP-K-02"), a.show(12.2)))
  rx, rw = 520, 400
  body.append(g(text(rx, 110, "RISK REDUCTION, IN THIS ORDER", 14, C["muted"], 700, spacing=1.2), a.show(5.0)))
  steps = [("Step 1", "Inherently safe design", "WP-C-05"), ("Step 2", "Safeguarding and complementary protective measures", "WP-S-03"),
           ("Step 3", "Information for use", "WP-O-03")]
  sy = [140, 272, 404]
  sh = 104
  for i, ((n, lab, wp), y) in enumerate(zip(steps, sy)):
    t = 5.9 + 0.9 * i
    blk = rect(rx, y, rw, sh, C["panel"], r=12) + text(rx + 18, y + 32, n, 16, C["muted"], 700) + para(rx + 18, y + 62, lab, 20, rw - 36, C["ink"], 700, lh=1.15) + chip(rx + rw - 92, y + 32, wp)
    hi = rect(rx - 3, y - 3, rw + 6, sh + 6, "none", r=14, stroke=C["gold"], sw=4, c=a.show(t, t + 0.9, static=False))
    body.append(g(blk, a.show(t)) + hi)
    if i:
      body.append(g(line(rx + rw / 2, sy[i - 1] + sh, rx + rw / 2, y - 4, arrow=True), a.show(t)))
  no = path(f"M{dx + 110},{dy} L{rx - 40},{dy} L{rx - 40},{sy[0] + 52} L{rx - 6},{sy[0] + 52}", C["red"], 2.5, arrow=True)
  body.append(g(no + text(dx + 124, dy - 10, "no", 17, C["red"], 700), a.show(5.3)))
  ret_y = 548
  back = path(f"M{rx + rw / 2},{sy[-1] + sh} L{rx + rw / 2},{ret_y} L{465},{ret_y} L{465},{ys[1] + bh / 2} L{lx + lw + 6},{ys[1] + bh / 2}", C["mid"], 2.5, arrow=True)
  body.append(g(back + text(rx - 30, ret_y + 32, "A measure can bring new hazards: go round again.", 16, C["muted"], 600), a.show(8.6)))
  cxl = lx + lw / 2
  pts = [(2.8, cxl, ys[0] + 27), (3.4, cxl, ys[1] + 27), (3.9, cxl, ys[2] + 27), (4.4, cxl, ys[3] + 27), (4.9, cxl, dy),
         (5.6, rx - 40, dy), (6.0, rx - 40, sy[0] + 52), (6.3, rx + rw / 2, sy[0] + 52), (7.2, rx + rw / 2, sy[1] + 52),
         (8.1, rx + rw / 2, sy[2] + 52), (8.9, rx + rw / 2, ret_y), (9.5, 465, ret_y), (10.2, 465, ys[1] + 27), (10.6, cxl, ys[1] + 27),
         (11.0, cxl, ys[2] + 27), (11.3, cxl, ys[3] + 27), (11.7, cxl, dy), (12.3, cxl, doc_y + 27)]
  body.append(token(a, pts, t_hide=12.8))
  return svg("iso-12100", "ISO 12100 · risk assessment and risk reduction", "The loop: assess, reduce in three steps, assess again", (
    "Left, the four steps of risk assessment: determine the limits of the machine, identify hazards, estimate the risk, "
    "evaluate it, then ask whether the risk is reduced enough. If not, right, the three-step method in its fixed order: "
    "inherently safe design, then safeguarding and complementary protective measures, then information for use. A "
    "measure can bring new hazards, so the loop goes back to hazard identification; when the risk is reduced enough, "
    "the result is documented. Chips name the record's work product for each step."), body, h, a)


@figure("iso-13849-risk-graph")
def iso_13849_risk_graph() -> str:
  a = Anim(16)
  h = 660
  ratings = risk_ratings()
  for hz in ("HZ-M01", "HZ-M02"):
    r = ratings[hz]
    if RISK_GRAPH[(r["s"], r["f"], r["p"])] != r["plr"]:
      raise SystemExit(f"{hz}: WP-C-03 rates {r['s']} {r['f']} {r['p']} -> PL {r['plr']}, the risk graph gives {RISK_GRAPH[(r['s'], r['f'], r['p'])]}")
  leaves = list(RISK_GRAPH.items())
  ly = [150 + i * 62 for i in range(8)]
  x_s, x_f, x_p, x_l = 60, 210, 380, 580
  p_y = [(ly[2 * i] + ly[2 * i + 1]) / 2 for i in range(4)]
  f_y = [(p_y[2 * i] + p_y[2 * i + 1]) / 2 for i in range(2)]
  s_y = (f_y[0] + f_y[1]) / 2
  tree, labels = "", ""

  def edge(x1, y1, x2, y2, label, upper):
    nonlocal tree, labels
    tree += line(x1, y1, x2, y2, C["light"], 3)
    labels += text(x2 - 8, y2 - 12 if upper else y2 + 24, label, 15, C["muted"], 600, "end")
  for i, fy in enumerate(f_y):
    edge(x_s, s_y, x_f, fy, "S1 slight" if i == 0 else "S2 serious", i == 0)
  for i, py in enumerate(p_y):
    edge(x_f, f_y[i // 2], x_p, py, "F1 seldom, short" if i % 2 == 0 else "F2 often, long", i % 2 == 0)
  for i, y in enumerate(ly):
    edge(x_p, p_y[i // 2], x_l, y, "P1 possible" if i % 2 == 0 else "P2 scarcely", i % 2 == 0)
  for x, lab in ((x_s, "Severity"), (x_f, "Frequency, exposure"), (x_p, "Avoidance")):
    tree += text(x + (0 if x == x_s else 0), 112, lab, 15, C["navy"], 700, "start" if x == x_s else "middle")
  tree += circle(x_s, s_y, 9, C["navy"]) + text(x_s, s_y + 30, "start", 15, C["muted"], 700, "middle")
  for x in (x_f, x_p):
    for y in (f_y if x == x_f else p_y):
      tree += circle(x, y, 5, C["mid"])
  pl_fill = {"a": "#E3F3EA", "b": "#EAF2D9", "c": "#FBF3E3", "d": "#FBE6CF", "e": "#FBE3E0"}
  for (k, pl), y in zip(leaves, ly):
    tree += rect(x_l + 6, y - 20, 46, 38, pl_fill[pl], r=8, stroke=C["line"], sw=1.5) + text(x_l + 29, y + 7, pl, 22, C["ink"], 700, "middle")
  tree += text(x_l + 29, 112, "PLr", 15, C["navy"], 700, "middle")
  body = [g(tree + labels, a.show(0.2))]
  for hz, col, t0, box_y in (("HZ-M01", C["gold"], 1.2, 150), ("HZ-M02", C["teal"], 6.6, 330)):
    r = ratings[hz]
    si = 0 if r["s"] == "S1" else 1
    fi = si * 2 + (0 if r["f"] == "F1" else 1)
    li = list(RISK_GRAPH).index((r["s"], r["f"], r["p"]))
    pts = [(x_s, s_y), (x_f, f_y[si]), (x_p, p_y[fi]), (x_l, ly[li])]
    body.append(path(poly_d(pts), col, 7, c=a.draw(t0, 2.4, poly_len(pts))))
    card = (rect(672, box_y, 262, 154, C["panel"], r=12, stroke=col, sw=3) + text(688, box_y + 30, hz, 20, C["ink"], 700) +
            para(688, box_y + 56, r["scenario"], 16, 236, C["ink"]) +
            text(688, box_y + 132, f"{r['s']} · {r['f']} · {r['p']}  →  PLr {r['plr']}", 18, C["ink"], 700))
    body.append(g(card, a.show(t0 + 2.6)))
    body.append(g(rect(x_l + 3, ly[li] - 23, 52, 44, "none", r=9, stroke=col, sw=4), a.show(t0 + 2.4)))
  body.append(g(para(672, 520, "Ratings are the concept-phase package's, carried in the record's risk assessment (WP-C-03 §5); not yet re-rated for the bench envelope.", 14.5, 262, C["muted"]), a.show(9.8)))
  return svg("iso-13849-risk-graph", "ISO 13849-1 · how good must a safety function be", "The risk graph: three questions give the required PL", (
    "The risk graph of ISO 13849-1 as a tree from a start point: severity S1 slight or S2 serious, then frequency or "
    "duration of exposure F1 or F2, then possibility of avoiding the hazard P1 or P2, ending in a required Performance "
    "Level from a (lowest) to e (highest). Two paths are traced with ratings read from the record's risk assessment: " +
    "; ".join(f"{hz} {ratings[hz]['scenario']}, {ratings[hz]['s']} {ratings[hz]['f']} {ratings[hz]['p']} gives PLr {ratings[hz]['plr']}" for hz in ("HZ-M01", "HZ-M02")) +
    ". The ratings are the package's, not yet re-rated."), body, h, a)


@figure("iso-13849-category-3")
def iso_13849_category_3() -> str:
  a = Anim(18)
  h = 640
  y1, y2 = 210, 390
  xs = [("I", 210), ("L", 390), ("O", 570)]
  names = {"I": "Input", "L": "Logic", "O": "Output"}
  body = [g(rect(30, 220, 120, 160, C["panel"], r=14) + circle(90, 272, 34, C["red"], C["gold"], 8) +
            text(90, 340, "E-stop", 18, C["ink"], 700, "middle") + text(90, 364, "two contacts", 15, C["muted"], 400, "middle"), a.show(0.2))]
  bw = 120
  for ch, y in ((1, y1), (2, y2)):
    blocks = line(150, y + 30 if ch == 1 else y - 30, xs[0][1] - 4, y, C["muted"], 2.5)
    for k, (nm, x) in enumerate(xs):
      blocks += rect(x, y - 34, bw, 68, C["pale"], r=10) + text(x + bw / 2, y - 4, f"{nm}{ch}", 22, C["ink"], 700, "middle") + text(x + bw / 2, y + 20, names[nm], 15, C["muted"], 400, "middle")
      if k:
        blocks += line(xs[k - 1][1] + bw, y, x - 4, y, C["muted"], 2.5, arrow=True)
    body.append(g(text(xs[0][1], y - 48, f"CHANNEL {ch}", 14, C["muted"], 700, spacing=1.2) + blocks, a.show(0.5 + 0.4 * ch)))
  body.append(g(line(xs[1][1] + bw / 2, y1 + 36, xs[1][1] + bw / 2, y2 - 36, C["mid"], 2.5, dash="7 6") +
                text(xs[1][1] + bw / 2 + 12, (y1 + y2) / 2 + 6, "cross-monitoring", 16, C["mid"], 700), a.show(1.6)))
  # two contactors whose contacts sit in series on one motor supply line
  kx, bus = 740, 880
  rail = (line(bus, 128, bus, y1 - 18, C["navy"], 4) + line(bus, y1 + 18, bus, y2 - 18, C["navy"], 4) + line(bus, y2 + 18, bus, 470, C["navy"], 4) +
          text(bus, 116, "24 V motor supply", 15, C["navy"], 700, "middle") + circle(bus, 494, 24, C["navy"]) + text(bus, 501, "M", 20, C["white"], 700, "middle"))
  for ch, y in ((1, y1), (2, y2)):
    rail += (line(xs[2][1] + bw, y, kx - 4, y, C["muted"], 2.5, arrow=True) + rect(kx, y - 30, 70, 60, C["panel"], r=10) +
             text(kx + 35, y + 7, f"K{ch}", 20, C["ink"], 700, "middle") + line(kx + 70, y, bus - 14, y, C["mid"], 2, dash="4 5"))
  body.append(g(rail, a.show(1.2)))
  # contact states: closed (the motor can run), open (power removed)
  stop1, reset1, fault, stop2 = 5.4, 8.2, 8.4, 12.4
  for ch, y in ((1, y1), (2, y2)):
    closed = line(bus, y - 18, bus, y + 18, C["navy"], 4)
    opened = line(bus, y - 18, bus + 20, y + 14, C["red"], 4)
    if ch == 1:   # opens at the first demand; stuck closed after the fault
      body.append(g(closed, a.vis([(0, stop1), (reset1, None)])))
      body.append(g(opened, a.vis([(stop1, reset1)], static=False)))
    else:         # opens at both demands
      body.append(g(closed, a.vis([(0, stop1), (reset1, stop2)], static=False)))
      body.append(g(opened, a.vis([(stop1, reset1), (stop2, a.reset)])))
  for ch, y in ((1, y1), (2, y2)):
    pts = [(2.6, 150, y), (3.4, xs[0][1] + bw / 2, y), (4.1, xs[1][1] + bw / 2, y), (4.8, xs[2][1] + bw / 2, y), (5.4, kx + 35, y)]
    body.append(token(a, pts, C["red"], 9, t_hide=5.8))
  body.append(g(rect(190, 476, 470, 46, C["green_pale"], r=10) + text(425, 506, "Stop demand: both contacts open, power off", 19, C["ink"], 700, "middle"), a.show(5.5, 8.2, static=False)))
  body.append(g(rect(xs[2][1] - 4, y1 - 38, bw + 8, 76, "none", r=12, stroke=C["red"], sw=4) +
                text(xs[2][1] + bw / 2, y1 - 48, "fault: output stuck on", 15, C["red"], 700, "middle"), a.show(fault)))
  pts = [(9.6, 150, y2), (10.4, xs[0][1] + bw / 2, y2), (11.1, xs[1][1] + bw / 2, y2), (11.8, xs[2][1] + bw / 2, y2), (12.4, kx + 35, y2)]
  body.append(token(a, pts, C["red"], 9, t_hide=12.8))
  pts = [(9.6, 150, y1), (10.4, xs[0][1] + bw / 2, y1), (11.1, xs[1][1] + bw / 2, y1)]
  body.append(token(a, pts, C["red"], 9, t_hide=11.4))
  body.append(g(rect(190, 476, 470, 46, C["cream"], r=10) + text(425, 506, "One fault: K2 still removes power", 19, C["ink"], 700, "middle"), a.show(12.6)))
  body.append(g(rect(190, 534, 470, 42, C["panel"], r=10) + text(425, 561, "The fault is detected: no restart until it is repaired", 17, C["ink"], 600, "middle"), a.show(13.6)))
  return svg("iso-13849-category-3", "ISO 13849-1 · designated architecture, category 3", "Two channels: one fault does not lose the stop", (
    "An emergency-stop device with two contacts feeds two channels, each an input, a logic and an output, with "
    "cross-monitoring between the logic blocks. Each channel drives a contactor, K1 and K2, whose contacts sit in series "
    "on the 24 V motor supply. A stop demand travels down both channels and both contacts open. Then a fault sticks the "
    "output of channel 1 on, so K1 stays closed; at the next demand K2 still opens and removes power, and the "
    "monitoring detects the fault so the machine cannot restart until it is repaired. This is the shape of category 3, "
    "the architecture most often used to reach PL d."), body, h, a)


@figure("iso-10218")
def iso_10218() -> str:
  a = Anim(15)
  h = 620
  body = []
  # the application: bench, arm, person, marked area
  app = rect(28, 104, 540, 470, "none", r=18, stroke=C["mid"], sw=3, dash="10 8")
  app += text(48, 136, "Part 2 · the robot application", 19, C["mid"], 700)
  app += rect(70, 420, 380, 18, "#D9C7A6", r=4) + rect(90, 438, 14, 110, C["muted"], r=2) + rect(416, 438, 14, 110, C["muted"], r=2)
  app += line(70, 552, 540, 552, C["light"], 3) + path("M466,552 L466,420", C["gold"], 3, dash="8 7") + text(458, 410, "marked area", 15, C["gold_text"], 700, "end")
  app += person_glyph(510, 552, 1.0, C["mid"])
  body.append(g(app, a.show(5.2)))
  robot = rect(100, 178, 290, 236, "none", r=16, stroke=C["navy"], sw=3.5) + text(116, 206, "Part 1 · the robot", 19, C["navy"], 700)
  robot += arm_glyph(200, 420, 1.45, -55, 85)
  body.append(g(robot, a.show(0.4)))
  part1 = ["Emergency stop and protective stop", "Speed, force, axis and space limits", "Enabling device in manual mode",
           "Operating modes and mode selection", "Safety-related control at a required PL",
           "Features for collaborative applications"]
  part2 = ["Risk assessment of the whole cell", "Layout, clearances and safeguarding", "Integration of the stops and modes",
           "Information for use and training", "Verification and validation on site"]
  x0 = 596
  body.append(g(text(x0, 120, "PART 1 ASKS THE ROBOT FOR", 14, C["navy"], 700, spacing=1.2), a.show(0.9)))
  for k, s_ in enumerate(part1):
    body.append(g(circle(x0 + 8, 148 + k * 34 - 6, 6, C["navy"]) + text(x0 + 24, 148 + k * 34, s_, 17, C["ink"], 600), a.show(1.2 + 0.5 * k)))
  body.append(g(text(x0, 376, "PART 2 ASKS THE APPLICATION FOR", 14, C["mid"], 700, spacing=1.2), a.show(5.6)))
  for k, s_ in enumerate(part2):
    body.append(g(circle(x0 + 8, 404 + k * 34 - 6, 6, C["mid"]) + text(x0 + 24, 404 + k * 34, s_, 17, C["ink"], 600), a.show(6.0 + 0.5 * k)))
  body.append(rect(97, 175, 296, 242, "none", r=18, stroke=C["gold"], sw=5, c=a.show(0.9, 4.6, static=False)))
  body.append(rect(25, 101, 546, 476, "none", r=20, stroke=C["gold"], sw=5, c=a.show(5.6, 9.2, static=False)))
  return svg("iso-10218", "ISO 10218-1 and -2 · industrial robots", "Part 1 is the robot; Part 2 is everything around it", (
    "A desktop arm on a bench inside two boundaries. The inner one is Part 1, the robot, which must provide an "
    "emergency stop and a protective stop, speed, force, axis and space limits, an enabling device in manual mode, "
    "operating modes, safety-related control at a required Performance Level and features for collaborative "
    "applications. The outer one is Part 2, the robot application: the bench, the marked area and the person, which "
    "need a risk assessment of the whole cell, layout and safeguarding, integration of the stops and modes, "
    "information for use and training, and verification and validation on site."), body, h, a)


@figure("iec-62061")
def iec_62061() -> str:
  a = Anim(14)
  h = 620
  top, dec = 150, 92

  def y(log_v: float) -> float:
    return top + (-4 - log_v) * dec
  body = []
  ax = 210
  axis = line(ax, y(-4), ax, y(-8), C["muted"], 2.5)
  for e in range(4, 9):
    axis += line(ax - 8, y(-e), ax, y(-e), C["muted"], 2.5) + text(ax - 14, y(-e) + 6, f"10⁻{'⁴⁵⁶⁷⁸'[e - 4]}", 17, C["muted"], 600, "end")
  axis += text(ax - 14, y(-4) - 24, "PFHD per hour", 15, C["muted"], 700, "end")
  body.append(g(axis, a.show(0.2)))
  lg = math.log10
  pl = [("a", -4, -5), ("b", -5, lg(3e-6)), ("c", lg(3e-6), -6), ("d", -6, -7), ("e", -7, -8)]
  sil = [("SIL 1", -5, -6), ("SIL 2", -6, -7), ("SIL 3", -7, -8)]
  plx, silx, bw = 260, 540, 150
  fills = {"a": "#E3F3EA", "b": "#EAF2D9", "c": "#FBF3E3", "d": "#FBE6CF", "e": "#FBE3E0"}
  body.append(g(text(plx + bw / 2, 118, "ISO 13849-1: PL", 18, C["navy"], 700, "middle"), a.show(0.4)))
  for k, (n, hi, lo) in enumerate(pl):
    body.append(g(rect(plx, y(hi) + 2, bw, y(lo) - y(hi) - 4, fills[n], r=8, stroke=C["line"], sw=1.5) +
                  text(plx + bw / 2, (y(hi) + y(lo)) / 2 + 8, f"PL {n}", 21, C["ink"], 700, "middle"), a.show(0.6 + 0.4 * k)))
  body.append(g(text(silx + bw / 2, 118, "IEC 62061: SIL", 18, C["navy"], 700, "middle"), a.show(3.0)))
  for k, (n, hi, lo) in enumerate(sil):
    body.append(g(rect(silx, y(hi) + 2, bw, y(lo) - y(hi) - 4, C["pale"], r=8, stroke=C["line"], sw=1.5) +
                  text(silx + bw / 2, (y(hi) + y(lo)) / 2 + 8, n, 21, C["ink"], 700, "middle"), a.show(3.2 + 0.4 * k)))
  body.append(g(text(silx + bw / 2, (y(-4) + y(-5)) / 2 + 6, "no SIL", 17, C["muted"], 600, "middle"), a.show(4.4)))
  pairs = [((y(-4) + y(-5)) / 2, (y(-4) + y(-5)) / 2), ((y(-5) + y(lg(3e-6))) / 2, (y(-5) + y(-6)) / 2),
           ((y(lg(3e-6)) + y(-6)) / 2, (y(-5) + y(-6)) / 2), ((y(-6) + y(-7)) / 2, (y(-6) + y(-7)) / 2), ((y(-7) + y(-8)) / 2, (y(-7) + y(-8)) / 2)]
  for k, (ya, yb) in enumerate(pairs):
    L = math.dist((plx + bw, ya), (silx, yb))
    body.append(line(plx + bw + 4, ya, silx - 6, yb, C["mid"], 2.5, dash="", c=a.draw(5.0 + 0.4 * k, 0.5, L)))
  d_hi, d_lo = y(-6), y(-7)
  body.append(rect(plx - 4, d_hi - 2, silx + bw - plx + 8, d_lo - d_hi + 4, "none", r=10, stroke=C["gold"], sw=4, c=a.show(7.4)))
  px = 730
  body.append(g(rect(px, 150, 210, 160, C["panel"], r=12) + text(px + 14, 178, "PFHD", 18, C["ink"], 700) +
                para(px + 14, 204, "the average probability of a dangerous failure per hour of the safety function", 15.5, 186, C["ink"]), a.show(1.6)))
  body.append(g(rect(px, 330, 210, 190, C["cream"], r=12) + text(px + 14, 358, "Same scale, two names", 18, C["ink"], 700) +
                para(px + 14, 384, "A function rated PL d sits in the band of SIL 2. Machinery stops at SIL 3; IEC 61508 goes to SIL 4.", 15.5, 186, C["ink"]), a.show(7.6)))
  return svg("iec-62061", "IEC 62061 · functional safety of machinery control", "PL and SIL: two names for one scale of failure rates", (
    "A logarithmic axis of the average probability of a dangerous failure per hour, PFHD, from 10 to the minus 4 at "
    "the top to 10 to the minus 8 at the bottom. Left, the Performance Levels of ISO 13849-1, PL a to PL e; right, the "
    "Safety Integrity Levels of IEC 62061, SIL 1 to SIL 3, with no SIL beside PL a. Lines join the bands that share a "
    "range: PL b and c with SIL 1, PL d with SIL 2, PL e with SIL 3. The PL d and SIL 2 band is outlined: a function "
    "rated PL d sits in the band of SIL 2."), body, h, a)


@figure("iec-61508")
def iec_61508() -> str:
  a = Anim(16)
  h = 680
  phases = ["Concept and scope", "Hazard and risk analysis", "Safety requirements and allocation",
            "Realisation: hardware and software", "Installation and commissioning", "Overall safety validation",
            "Operation, maintenance, modification", "Decommissioning"]
  x0, bw, bh, gy = 150, 380, 52, 64
  ys = [104 + k * gy for k in range(len(phases))]
  body = []
  for k, (ph, yy) in enumerate(zip(phases, ys)):
    t = 0.4 + 0.45 * k
    blk = rect(x0, yy, bw, bh, C["pale"] if k not in (3,) else C["cream"], r=10) + text(x0 + 16, yy + 33, f"{k + 1}  {ph}", 18.5, C["ink"], 700)
    if k:
      blk += line(x0 + bw / 2, ys[k - 1] + bh, x0 + bw / 2, yy - 3, C["muted"], 2.5, arrow=True)
    body.append(g(blk, a.show(t)))
  # management and assessment run alongside every phase
  for k, (lab, col, xx) in enumerate((("Management of functional safety", C["navy"], 40), ("Verification of each phase", C["mid"], 92))):
    bar = rect(xx, 104, 40, ys[-1] + bh - 104, col, r=10)
    cy = (104 + ys[-1] + bh) / 2
    bar += (f'<text x="{xx + 26}" y="{cy:.0f}" font-size="16" fill="{C["white"]}" font-weight="700" text-anchor="middle" '
            f'transform="rotate(-90 {xx + 26} {cy:.0f})">{esc(lab)}</text>')
    body.append(g(bar, a.show(4.4 + 0.5 * k)))
  ax = x0 + bw + 30
  body.append(g(line(ax, 104, ax, ys[-1] + bh, C["gold"], 4) + text(ax + 14, 98, "Functional safety assessment", 16, C["gold_text"], 700), a.show(5.6)))
  for k in (2, 5, 6):
    body.append(g(circle(ax, ys[k] + bh / 2, 11, C["gold"], C["white"], 3) + line(x0 + bw + 4, ys[k] + bh / 2, ax - 12, ys[k] + bh / 2, C["gold"], 2.5, dash="4 5"), a.show(6.0 + 0.4 * [2, 5, 6].index(k))))
  pts = [(7.6 + 0.55 * k, x0 + bw - 26, yy + bh / 2) for k, yy in enumerate(ys)]
  body.append(token(a, pts, t_hide=pts[-1][0] + 0.6))
  cx = 730
  cards = [("SIL 1 to SIL 4", "the integrity a safety function must reach; machinery uses up to SIL 3 (IEC 62061)"),
           ("Independence grows with SIL", "the higher the integrity, the more independent the assessor must be"),
           ("Tool classes T1, T2, T3", "how far a software tool can put an error into the result, and what that requires")]
  for k, (t1, t2) in enumerate(cards):
    yy = 150 + k * 160
    n1 = len(wrap(t1, 186, 18))
    body.append(g(rect(cx, yy, 210, 144, C["panel"], r=12) + para(cx + 14, yy + 28, t1, 18, 186, C["ink"], 700) +
                  para(cx + 14, yy + 34 + 22 * n1, t2, 15, 186, C["ink"]), a.show(12.4 + 0.5 * k)))
  return svg("iec-61508", "IEC 61508 · the functional safety umbrella", "One lifecycle, managed, verified and assessed throughout", (
    "The overall safety lifecycle of IEC 61508 as eight phases from concept and scope, hazard and risk analysis and "
    "safety requirements, through realisation in hardware and software, installation, validation and operation, to "
    "decommissioning. Beside every phase run management of functional safety and verification; a functional safety "
    "assessment checks the requirements, the validation and changes in operation. Cards explain the safety integrity "
    "levels SIL 1 to 4, that the assessor's independence grows with SIL, and the tool classes T1 to T3."), body, h, a)


@figure("en-60204")
def en_60204() -> str:
  a = Anim(15)
  h = 640
  gx0, gx1, t_stop = 270, 640, 340
  rows = [("Category 0", "Power removed at once: the motors coast to a stop", "uncontrolled"),
          ("Category 1", "A controlled stop, then power removed", "controlled, then off"),
          ("Category 2", "A controlled stop, power left on", "controlled, held")]
  body = []
  body.append(g(line(t_stop, 108, t_stop, 538, C["red"], 2.5, dash="6 6") + text(t_stop, 100, "stop demand", 15, C["red"], 700, "middle"), a.show(0.3)))
  for k, (cat, desc, kind) in enumerate(rows):
    y0 = 118 + k * 142
    t = 0.6 + 2.8 * k
    run, zero = y0 + 26, y0 + 92
    base = text(30, y0 + 40, cat, 21, C["ink"], 700) + para(30, y0 + 66, desc, 15.5, 220, C["muted"])
    base += line(gx0, zero, gx1, zero, C["light"], 2) + line(gx0, run - 12, gx0, zero, C["light"], 2) + text(gx0 - 6, run + 4, "speed", 13, C["muted"], 600, "end")
    body.append(g(base, a.show(t)))
    if k == 0:
      d = f"M{gx0},{run} L{t_stop},{run} C{t_stop + 70},{run} {t_stop + 140},{zero - 6} {gx1 - 20},{zero}"
      off_at = t_stop
    else:
      d = f"M{gx0},{run} L{t_stop},{run} L{t_stop + 110},{zero}"
      off_at = t_stop + 110 if k == 1 else None
    body.append(path(d, C["navy"], 4, c=a.draw(t + 0.3, 1.6, 520)))
    py = zero + 18
    strip = rect(gx0, py, (off_at or gx1) - gx0, 14, C["green"], r=3) + text(gx0 + 6, py + 34, "power", 13, C["muted"], 600)
    if off_at:
      strip += rect(off_at, py, gx1 - off_at, 14, C["red"], r=3) + text(off_at + 6, py + 34, "off", 13, C["red"], 700)
    else:
      strip += text(gx1 - 4, py + 34, "on, standstill monitored", 13, C["green"], 700, "end")
    body.append(g(strip, a.show(t + 1.2)))
  rx = 664
  items = ["Supply disconnecting device", "Overcurrent protection", "Protection against electric shock", "Protective bonding",
           "Control circuits and functions", "Verification tests (§18)"]
  body.append(g(text(rx, 124, "ALSO IN EN 60204-1", 14, C["muted"], 700, spacing=1.2), a.show(9.0)))
  for k, s_ in enumerate(items):
    body.append(g(rect(rx, 140 + k * 54, 272, 44, C["panel"], r=8) + text(rx + 12, 168 + k * 54, s_, 15.5, C["ink"], 600), a.show(9.3 + 0.35 * k)))
  body.append(g(rect(rx, 476, 272, 64, C["cream"], r=8) + para(rx + 12, 500, "An emergency stop is category 0 or 1 (ISO 13850)", 15.5, 248, C["ink"], 700), a.show(11.6)))
  return svg("en-60204", "EN 60204-1 · electrical equipment of machines", "Three ways to stop: the stop categories", (
    "Three speed-against-time graphs share one stop demand. Category 0: power is removed at once and the motors coast "
    "to a stop, uncontrolled. Category 1: a controlled stop with power available, then power removed at standstill. "
    "Category 2: a controlled stop with power left on and standstill monitored. Beside them, other topics of EN 60204-1: "
    "the supply disconnecting device, overcurrent protection, protection against electric shock, protective bonding, "
    "control circuits and functions, and verification tests; an emergency stop is category 0 or 1."), body, h, a)


@figure("iso-13850")
def iso_13850() -> str:
  a = Anim(16)
  h = 640
  steps = [("Press", "Anyone, one action, a device in easy reach"), ("Stop", "Overrides every other function; stop category 0 or 1"),
           ("Stay stopped", "The device latches until it is reset by hand"), ("Reset the device", "Resetting does not start the machine"),
           ("Restart", "Only a separate, deliberate start command")]
  times = [1.0, 3.0, 5.0, 7.2, 9.6]
  body = []
  # the device: yellow background, red mushroom head, raised or pressed
  dev = circle(170, 240, 92, "#F7D046") + circle(170, 240, 70, C["white"], C["line"], 2)
  body.append(g(dev, a.show(0.2)))
  body.append(g(circle(170, 240, 56, C["red"], "#A3281C", 4) + circle(158, 226, 18, "#E8776B"), a.vis([(0, times[0]), (times[3], None)])))
  body.append(g(circle(170, 244, 50, "#B8362A", "#7E1F16", 4), a.vis([(times[0], times[3])], static=False)))
  body.append(g(rect(118, 344, 104, 34, C["red_pale"], r=8) + text(170, 367, "latched", 17, C["red"], 700, "middle"), a.show(times[2], times[3], static=False)))
  # the arm: moving, stopped, still after reset, moving again after the start command
  arm_y = 560
  turn = a.turn([(0.0, 0), (0.6, -14), (1.2, 0), (times[1], 0), (times[4] + 0.4, 0), (times[4] + 1.2, -14), (times[4] + 2.0, 0), (times[4] + 2.8, -14)], (170, arm_y - 34), static=0)
  body.append(g(rect(60, arm_y, 220, 12, "#D9C7A6", r=3) + arm_glyph(170, arm_y, 1.0, -60, 80, turn=turn), a.show(0.2)))
  body.append(g(text(170, arm_y + 40, "moving", 16, C["green"], 700, "middle"), a.vis([(0, times[1]), (times[4] + 0.3, a.reset)], static=False)))
  body.append(g(text(170, arm_y + 40, "stopped", 16, C["red"], 700, "middle"), a.vis([(times[1], times[4] + 0.3)], static=False)))
  x0 = 380
  for k, ((t1, t2), t) in enumerate(zip(steps, times)):
    yy = 106 + k * 98
    blk = rect(x0, yy, 550, 84, C["panel"], r=12) + circle(x0 + 34, yy + 42, 18, C["navy"]) + text(x0 + 34, yy + 49, str(k + 1), 19, C["white"], 700, "middle")
    blk += text(x0 + 66, yy + 36, t1, 21, C["ink"], 700) + text(x0 + 66, yy + 64, t2, 16.5, C["ink"])
    body.append(g(blk, a.show(t - 0.4)))
    body.append(rect(x0 - 3, yy - 3, 556, 90, "none", r=14, stroke=C["gold"], sw=4, c=a.show(t - 0.4, t + 1.6, static=False)))
  return svg("iso-13850", "ISO 13850 · the emergency stop function", "Press, stop, stay stopped, reset, then restart on purpose", (
    "An emergency-stop device, a red mushroom head on a yellow background, beside a desktop arm, and five steps. "
    "1 Press: anyone, one action, a device in easy reach. 2 Stop: it overrides every other function, as a stop of "
    "category 0 or 1. 3 Stay stopped: the device latches until it is reset by hand. 4 Reset the device: resetting does "
    "not start the machine. 5 Restart: only a separate, deliberate start command moves it again. The animation presses "
    "the head, the arm stops and stays stopped through the reset, and moves again only after the start command."), body, h, a)


@figure("iso-13854")
def iso_13854() -> str:
  a = Anim(14)
  h = 600
  gaps = iso13854_gaps()
  order = sorted(gaps.items(), key=lambda kv: -kv[1])
  body = []
  lx0, lx1, top, bot = 60, 210, 170, 360
  body.append(g(rect(lx0, top, lx1 - lx0, bot - top, C["navy"], r=10) + text((lx0 + lx1) / 2, bot + 30, "fixed part", 15, C["muted"], 600, "middle"), a.show(0.2)))
  start_x, travel = 560, 320
  mv = a.move([(0.8, 0, 0), (2.6, -120, 0), (4.6, -200, 0), (6.4, -240, 0), (8.4, -300, 0), (10.0, -330, 0)], static=(-160, 0))
  body.append(g(rect(start_x, top, 150, bot - top, C["mid"], r=10) + text(start_x + 75, bot + 30, "moving part", 15, C["muted"], 600, "middle"), mv))
  body.append(g(text(310, 140, "the gap", 17, C["ink"], 700, "middle") + text(310, 410, "not to scale", 14, C["muted"], 400, "middle"), a.show(0.4)))
  cross_t = [2.6, 4.6, 6.4, 9.6][:len(order)]
  rx = 700
  body.append(g(text(rx, 124, "A GAP OF AT LEAST", 14, C["muted"], 700, spacing=1.2), a.show(0.4)))
  for k, ((part, mm), t) in enumerate(zip(order, cross_t)):
    yy = 150 + k * 92
    row = rect(rx, yy, 236, 80, C["panel"], r=12) + text(rx + 16, yy + 34, f"{mm} mm", 24, C["ink"], 700) + text(rx + 16, yy + 62, f"avoids crushing the {part}", 16, C["ink"])
    body.append(g(row, a.show(0.6 + 0.3 * k)))
    body.append(g(text(rx + 212, yy + 36, "✓", 26, C["green"], 700, "middle"), a.vis([(0.9 + 0.3 * k, t)], static=False)))
    body.append(g(rect(rx, yy, 236, 80, "none", r=12, stroke=C["red"], sw=3.5) + text(rx + 212, yy + 36, "✕", 26, C["red"], 700, "middle"),
                  a.vis([(t, a.reset)], static=False)))
    body.append(g(rect(250, 452, 400, 44, C["red_pale"], r=10) + text(450, 481, f"gap below {mm} mm: the {part} can be crushed", 18, C["ink"], 700, "middle"),
                  a.vis([(t, (cross_t[k + 1] if k + 1 < len(cross_t) else a.reset))], static=False)))
  body.append(g(para(60, 530, "Values as the record's hazard scenes use them (scenes.yaml); the standard lists more body parts.", 15, 600, C["muted"]), a.show(0.6)))
  return svg("iso-13854", "ISO 13854 · minimum gaps to avoid crushing", "Leave room for the body part, or none at all", (
    "A fixed part and a moving part close the gap between them. Beside them, the minimum gaps the record's hazard "
    "scenes use: " + ", ".join(f"{mm} mm avoids crushing the {part}" for part, mm in order) + ". As the gap closes "
    "past each value the row turns from safe to can be crushed. Values are read from the record's scenes.yaml; the "
    "standard lists more body parts."), body, h, a)


@figure("iso-13857")
def iso_13857() -> str:
  a = Anim(15)
  h = 620
  body = []
  # left panel: reaching over a protective structure
  fy = 520
  left = line(30, fy, 470, fy, C["muted"], 3) + text(40, 124, "REACHING OVER A STRUCTURE", 14, C["muted"], 700, spacing=1.2)
  left += rect(380, 330, 80, fy - 330, C["red_pale"], r=6, stroke=C["red"], sw=2) + text(420, 322, "hazard", 15, C["red"], 700, "middle")
  left += rect(250, 300, 16, fy - 300, C["navy"], r=3) + text(274, 500, "structure", 15, C["navy"], 700)
  left += person_glyph(140, fy, 1.15, C["mid"])
  left += line(285, fy + 0, 285, fy - 0, C["muted"])
  dims = line(258, fy + 30, 380, fy + 30, C["ink"], 2) + text(319, fy + 52, "c", 19, C["ink"], 700, "middle")
  dims += line(220, fy, 220, 300, C["ink"], 2) + text(206, 410, "b", 19, C["ink"], 700, "end")
  dims += line(476, fy, 476, 330, C["ink"], 2) + text(486, 430, "a", 19, C["ink"], 700)
  body.append(g(left, a.show(0.2)))
  body.append(g(dims, a.show(1.0)))
  reach = path("M156,366 C210,300 250,270 300,300 C330,318 345,345 352,370", C["mid"], 9)
  body.append(g(reach, a.show(2.0)))
  body.append(g(circle(352, 372, 9, C["green"]) + text(323, 440, "stops short", 15, C["green"], 700, "middle"), a.show(3.4)))
  body.append(g(para(40, 160, "a: height of the hazard · b: height of the structure · c: horizontal distance to the hazard", 15.5, 420, C["ink"]), a.show(4.2)))
  # right panel: reaching through an opening
  rx = 510
  right = text(rx + 10, 124, "REACHING THROUGH AN OPENING", 14, C["muted"], 700, spacing=1.2)
  right += rect(rx + 150, 210, 18, 300, C["navy"], r=3) + rect(rx + 146, 336, 26, 44, C["white"], r=2)
  right += rect(rx + 330, 300, 80, 116, C["red_pale"], r=6, stroke=C["red"], sw=2) + text(rx + 370, 292, "hazard", 15, C["red"], 700, "middle")
  right += text(rx + 159, 202, "guard with an opening e", 15, C["navy"], 700, "middle")
  body.append(g(right, a.show(6.0)))
  hand = path(f"M{rx + 20},358 L{rx + 140},358", C["mid"], 18) + path(f"M{rx + 140},358 L{rx + 230},358", C["mid"], 8)
  body.append(g(g(hand, a.move([(6.6, -80, 0), (8.2, 0, 0)], static=(0, 0))), a.show(6.4)))
  body.append(g(line(rx + 168, 450, rx + 330, 450, C["ink"], 2) + text(rx + 249, 474, "sr", 19, C["ink"], 700, "middle") +
                circle(rx + 230, 358, 7, C["green"]), a.show(8.6)))
  body.append(g(para(rx + 10, 160, "The smaller the opening, the less fits through it and the shorter the safety distance sr behind it.", 15.5, 420, C["ink"]), a.show(9.4)))
  body.append(g(rect(rx + 10, 528, 420, 44, C["cream"], r=10) + text(rx + 220, 556, "The standard's tables give a, b, c and sr by risk", 16.5, C["ink"], 700, "middle"), a.show(10.6)))
  return svg("iso-13857", "ISO 13857 · safety distances", "Keep the hazard out of reach: over a structure or through an opening", (
    "Left, side view of a person reaching over a protective structure towards a hazard: a is the height of the "
    "hazard, b the height of the structure, c the horizontal distance from the structure to the hazard; the reach "
    "curves over the structure and stops short of the hazard. Right, a hand reaching through an opening e in a guard: "
    "the smaller the opening, the less fits through it and the shorter the safety distance sr behind it. The "
    "standard's tables give a, b, c and sr by risk."), body, h, a)


@figure("iso-13855")
def iso_13855() -> str:
  a = Anim(15)
  h = 640
  body = []
  floor = rect(30, 110, 900, 330, C["panel"], r=14)
  hz_x, hz_r = 760, 110
  floor += circle(hz_x, 275, hz_r, C["red_pale"], C["red"], 2) + text(hz_x, 410, "hazard zone (the arm's reach)", 15, C["red"], 700, "middle")
  det_x = 470
  floor += line(det_x, 128, det_x, 424, C["navy"], 4, dash="10 8")
  body.append(g(floor + text(det_x, 104, "detection line", 15, C["navy"], 700, "middle"), a.show(0.2)))
  arm = g(circle(hz_x, 275, 16, C["navy"]) + line(hz_x, 275, hz_x - 70, 235, C["mid"], 12) + circle(hz_x - 70, 235, 8, C["navy"]), a.turn([(0, 0), (0.8, 40), (1.6, 0), (2.4, 40), (3.2, 0), (4.0, 40), (4.6, 20), (5.2, 0)], (hz_x, 275), static=0))
  body.append(g(arm, a.show(0.2)))
  # the person: approaches at K, crosses the line, keeps going while the arm stops
  py = 275
  mv = a.move([(0.6, 0, 0), (3.0, 260, 0), (5.2, 400, 0)], static=(400, 0))
  person = circle(110, py, 26, C["mid"]) + circle(110, py, 10, C["white"])
  body.append(g(person, mv))
  body.append(g(path(f"M140,{py - 46} L230,{py - 46}", C["mid"], 3, arrow=True) + text(140, py - 56, "K: approach speed", 16, C["mid"], 700), a.show(0.8)))
  body.append(g(rect(det_x - 6, 128, 12, 296, C["gold"], r=4), a.show(3.0, 3.6, static=False)))
  # S, C, T dimensions
  s_y = 470
  body.append(g(line(det_x, s_y, hz_x - hz_r, s_y, C["ink"], 2.5) + line(det_x, s_y - 10, det_x, s_y + 10, C["ink"], 2.5) +
                line(hz_x - hz_r, s_y - 10, hz_x - hz_r, s_y + 10, C["ink"], 2.5) + text((det_x + hz_x - hz_r) / 2, s_y + 28, "S: minimum distance", 17, C["ink"], 700, "middle"), a.show(5.8)))
  body.append(g(f'<rect x="{det_x}" y="132" width="90" height="288" fill="{C["gold"]}" fill-opacity="0.25"/>', a.show(6.6)))
  body.append(g(text(det_x + 45, 440 + 0, "C", 18, C["gold_text"], 700, "middle"), a.show(6.6)))
  # the timer: T, from detection to standstill
  tx0, tx1, ty = 120, 420, 520
  body.append(g(text(tx0, ty - 12, "T: time from detection to standstill", 16, C["ink"], 700) + rect(tx0, ty, tx1 - tx0, 18, C["pale"], r=4), a.show(3.0)))
  grow = a._rule(a._name(), f"0%,{a.p(3.0)}{{transform:scaleX(0)}}{a.p(5.2)},{a.p(a.reset)}{{transform:scaleX(1)}}{a.p(a.reset + 0.3)},100%{{transform:scaleX(0)}}",
                 f"transform-origin:{tx0}px {ty}px;transform:scaleX(1);")
  body.append(rect(tx0, ty, tx1 - tx0, 18, C["navy"], r=4, c=grow))
  body.append(g(rect(480, 500, 450, 84, C["cream"], r=12) + text(705, 536, "S = K × T + C", 30, C["ink"], 700, "middle") +
                text(705, 568, "speed of approach × time to stop + intrusion allowance", 15.5, C["ink"], 400, "middle"), a.show(7.6)))
  return svg("iso-13855", "ISO 13855 · positioning safeguards", "How far away must the detection be? S = K × T + C", (
    "Top view: a person approaches at speed K towards a detection line in front of the arm's hazard zone. When the "
    "person crosses the line, a timer T runs from detection to standstill while the person keeps moving; the arm stops "
    "before the person arrives. The minimum distance S from the detection line to the hazard zone is K times T plus "
    "C, an intrusion allowance for how far a hand reaches past the detection before it is detected."), body, h, a)


@figure("iso-ts-15066")
def iso_ts_15066() -> str:
  a = Anim(16)
  h = 660
  panels = [("Safety-rated monitored stop", "Nobody moves the arm while a person is inside; it resumes when they leave"),
            ("Hand guiding", "The operator moves the arm by hand, holding an enabling device"),
            ("Speed and separation monitoring", "The closer the person, the slower the arm; at the limit it stops"),
            ("Power and force limiting", "Contact is allowed, below the limit for that body region")]
  pw, ph = 440, 252
  pos = [(30, 100), (490, 100), (30, 368), (490, 368)]
  body = []
  for k, ((title_, note), (x, y)) in enumerate(zip(panels, pos)):
    t = 0.4 + 3.6 * k
    base = rect(x, y, pw, ph, C["panel"], r=14) + text(x + 18, y + 32, f"{k + 1}  {title_}", 19, C["ink"], 700) + para(x + 18, y + 58, note, 15, pw - 36, C["muted"])
    base += rect(x + 30, y + 214, 200, 10, "#D9C7A6", r=3)
    body.append(g(base, a.show(0.2)))
    body.append(rect(x - 3, y - 3, pw + 6, ph + 6, "none", r=16, stroke=C["gold"], sw=4, c=a.show(t, t + 3.4, static=False)))
    ax, ay = x + 110, y + 214
    if k == 0:
      zone = rect(x + 40, y + 96, 250, 118, "none", r=8, stroke=C["red"], sw=2, dash="7 6")
      arm = arm_glyph(ax, ay, 0.85, -60, 80, turn=a.turn([(t, 0), (t + 0.5, -12), (t + 1.0, 0), (t + 3.0, 0), (t + 3.4, -12)], (ax, ay - 29), static=0))
      ppl = g(person_glyph(x + 390, y + 238, 0.75, C["mid"]), a.move([(t, 0, 0), (t + 1.0, -150, 0), (t + 2.6, -150, 0), (t + 3.2, 0, 0)], static=(0, 0)))
      stop = g(rect(x + 52, y + 104, 120, 34, C["red"], r=8) + text(x + 112, y + 127, "STOPPED", 16, C["white"], 700, "middle"), a.show(t + 1.0, t + 2.7, static=False))
      body.append(g(zone + arm + ppl + stop, ""))
    elif k == 1:
      arm = arm_glyph(ax, ay, 0.85, -60, 80, turn=a.turn([(t, 0), (t + 1.2, 18), (t + 2.4, -10), (t + 3.2, 0)], (ax, ay - 29), static=0))
      ppl = person_glyph(x + 330, y + 238, 0.75, C["mid"]) + rect(x + 300, y + 150, 26, 16, C["gold"], r=4) + text(x + 350, y + 140, "enabling device", 13, C["gold_text"], 700)
      body.append(arm + ppl)
    elif k == 2:
      arm = arm_glyph(ax, ay, 0.85, -60, 80, turn=a.turn([(t, 0), (t + 0.4, -14), (t + 0.8, 0), (t + 1.6, -8), (t + 2.4, 0), (t + 3.2, 0)], (ax, ay - 29), static=0))
      ppl = g(person_glyph(x + 400, y + 238, 0.75, C["mid"]), a.move([(t, 0, 0), (t + 2.4, -120, 0), (t + 3.4, -120, 0)], static=(-60, 0)))
      sep = line(x + 200, y + 200, x + 380, y + 200, C["ink"], 2) + text(x + 290, y + 192, "separation", 13, C["ink"], 700, "middle")
      bar = rect(x + 330, y + 96, 90, 14, C["pale"], r=4) + text(x + 330, y + 90, "arm speed", 13, C["muted"], 700)
      shrink = a._rule(a._name(), f"0%,{a.p(t)}{{transform:scaleX(1)}}{a.p(t + 2.4)},{a.p(a.reset)}{{transform:scaleX(0.08)}}{a.p(a.reset + 0.3)},100%{{transform:scaleX(1)}}",
                       f"transform-origin:{x + 330}px {y + 96}px;transform:scaleX(0.5);")
      bar += rect(x + 330, y + 96, 90, 14, C["green"], r=4, c=shrink)
      body.append(arm + ppl + g(sep, a.show(t)) + bar)
    else:
      arm = arm_glyph(ax, ay, 0.85, -60, 80, turn=a.turn([(t, 0), (t + 1.0, 14), (t + 2.6, 14), (t + 3.2, 0)], (ax, ay - 29), static=14))
      hand = rect(x + 204, y + 166, 40, 20, "#E9B48F", r=8)
      meter = rect(x + 330, y + 100, 26, 110, C["pale"], r=4) + line(x + 322, y + 126, x + 364, y + 126, C["red"], 2.5)
      meter += text(x + 370, y + 124, "limit for", 13, C["red"], 700) + text(x + 370, y + 140, "the region", 13, C["red"], 700)
      rise = a._rule(a._name(), f"0%,{a.p(t + 1.0)}{{transform:scaleY(0)}}{a.p(t + 1.8)},{a.p(a.reset)}{{transform:scaleY(1)}}{a.p(a.reset + 0.3)},100%{{transform:scaleY(0)}}",
                     f"transform-origin:{x + 343}px {y + 210}px;transform:scaleY(1);")
      meter += rect(x + 330, y + 140, 26, 70, C["gold"], r=4, c=rise) + text(x + 343, y + 230, "force", 13, C["muted"], 700, "middle")
      body.append(arm + hand + meter)
  return svg("iso-ts-15066", "ISO/TS 15066 · collaborative robots", "Four ways a person and a robot can share space", (
    "Four panels, one per collaborative operating mode. 1 Safety-rated monitored stop: the arm stops and stays stopped "
    "while a person is inside its zone, and resumes when they leave. 2 Hand guiding: the operator moves the arm by "
    "hand while holding an enabling device. 3 Speed and separation monitoring: the closer the person, the slower the "
    "arm, until it stops at the limit. 4 Power and force limiting: contact is allowed, with the force kept below the "
    "limit for that body region."), body, h, a)


@figure("iec-60812")
def iec_60812() -> str:
  a = Anim(16)
  h = 640

  def card(x, y, w, hh, head, body_, fill, t, c_=None):
    return g(rect(x, y, w, hh, fill, r=12) + text(x + 14, y + 28, head.upper(), 13.5, C["muted"], 700, spacing=1.1) +
             para(x + 14, y + 56, body_, 17.5, w - 28, C["ink"], 600), a.show(t))

  def rating(x, y, letter, word, t):
    return g(circle(x, y, 26, C["navy"]) + text(x, y + 9, letter, 24, C["white"], 700, "middle") +
             text(x, y + 50, word, 14.5, C["muted"], 700, "middle"), a.show(t))
  body = [g(text(30, 104, "ONE ROW OF THE WORKSHEET, AN ILLUSTRATION OF THE METHOD", 13.5, C["muted"], 700, spacing=1.1), a.show(0.2))]
  r1, r2 = 120, 300
  body.append(card(30, r1, 210, 130, "Function", "Remove motor power when the E-stop is pressed", C["pale"], 0.5))
  body.append(g(line(242, r1 + 65, 266, r1 + 65, C["muted"], 2.5, arrow=True), a.show(1.4)))
  body.append(card(270, r1, 210, 130, "Failure mode", "A contactor welds closed", C["red_pale"], 1.4))
  body.append(g(line(482, r1 + 65, 506, r1 + 65, C["muted"], 2.5, arrow=True), a.show(2.3)))
  body.append(card(510, r1, 230, 130, "Effect", "Power stays on: the arm can keep moving", C["red_pale"], 2.3))
  body.append(rating(830, r1 + 50, "S", "severity", 3.2))
  body.append(g(line(375, r2 - 4, 375, r1 + 134, C["muted"], 2.5, arrow=True), a.show(4.1)))
  body.append(card(270, r2, 210, 120, "Cause", "Overload, or the end of its life", C["panel"], 4.1))
  body.append(g(line(242, r2 + 50, 268, r2 + 50, C["muted"], 2, dash="4 5"), a.show(5.0)))
  body.append(rating(150, r2 + 50, "O", "occurrence", 5.0))
  body.append(card(510, r2, 230, 120, "Current control", "Its mirror contact is checked before each start", C["green_pale"], 5.9))
  body.append(rating(830, r2 + 50, "D", "detection", 6.8))
  pr = rect(510, 470, 420, 70, C["cream"], r=12) + text(530, 500, "S, O and D give the priority", 18, C["ink"], 700)
  pr += text(530, 526, "a risk priority number, or another scheme (2018 edition)", 14.5, C["muted"], 400)
  body.append(g(pr, a.show(7.8)))
  body.append(g(rect(30, 470, 450, 70, C["navy"], r=12) + text(50, 500, "Action, then rate the row again", 18, C["white"], 700) +
                text(50, 526, "e.g. a second contactor in series, a monitored output", 14.5, C["light"], 400), a.show(8.8)))
  body.append(g(line(508, 505, 484, 505, C["muted"], 2.5, arrow=True), a.show(8.8)))
  body.append(g(para(30, 572, "Every function, every failure mode, every cause: the worksheet is the analysis, rated before and after each action.", 15.5, 900, C["muted"]), a.show(9.8)))
  return svg("iec-60812", "IEC 60812 · failure modes and effects analysis", "FMEA: how can it fail, what happens, what catches it", (
    "One row of an FMEA worksheet built step by step, as an illustration of the method: the function, remove motor "
    "power when the E-stop is pressed; the failure mode, a contactor welds closed; the effect, power stays on and the "
    "arm can keep moving, rated for severity S; the cause, overload or end of life, rated for occurrence O; the current "
    "control, its mirror contact checked before each start, rated for detection D. S, O and D give the priority, by a "
    "risk priority number or another scheme the 2018 edition allows; an action follows and the row is rated again."), body, h, a)


@figure("iec-61025")
def iec_61025() -> str:
  a = Anim(18)
  h = 660

  def ev_box(x, y, w, s_, c_=""):
    return rect(x - w / 2, y, w, 52, C["pale"], r=10) + para(x, y + 22, s_, 15.5, w - 16, C["ink"], 700, "middle", lh=1.15)

  def or_gate(x, y, fill=C["white"]):
    return path(f"M{x - 20},{y + 26} Q{x},{y + 16} {x + 20},{y + 26} Q{x + 18},{y - 2} {x},{y - 14} Q{x - 18},{y - 2} {x - 20},{y + 26} Z", C["navy"], 2.5, fill) + text(x, y + 50, "OR", 12, C["muted"], 700, "middle")

  def and_gate(x, y, fill=C["white"]):
    return path(f"M{x - 20},{y + 26} L{x - 20},{y} A20,20 0 0,1 {x + 20},{y} L{x + 20},{y + 26} Z", C["navy"], 2.5, fill) + text(x, y + 50, "AND", 12, C["muted"], 700, "middle")

  def basic(x, y, s_):
    return circle(x, y, 22, C["white"], C["navy"], 2.5) + para(x, y + 42, s_, 14, 110, C["ink"], 600, "middle", lh=1.1)
  top_x = 380
  tree = rect(top_x - 220, 96, 440, 54, C["red_pale"], r=10, stroke=C["red"], sw=2) + text(top_x, 129, "Motor power stays on after an E-stop demand", 17, C["ink"], 700, "middle")
  tree += line(top_x, 150, top_x, 178, C["navy"], 2.5) + or_gate(top_x, 192)
  ax, cx_ = 230, 560
  tree += path(f"M{top_x},{218} L{top_x},{226} L{ax},{226} L{ax},{240}", C["navy"], 2.5) + path(f"M{top_x},{226} L{cx_},{226} L{cx_},{258}", C["navy"], 2.5)
  tree += ev_box(ax, 240, 200, "Both channels fail") + line(ax, 292, ax, 304, C["navy"], 2.5) + and_gate(ax, 318)
  c1, c2 = 120, 340
  tree += path(f"M{ax},{344} L{ax},{354} L{c1},{354} L{c1},{366}", C["navy"], 2.5) + path(f"M{ax},{354} L{c2},{354} L{c2},{366}", C["navy"], 2.5)
  for cx2, lab in ((c1, "Channel 1 fails"), (c2, "Channel 2 fails")):
    tree += ev_box(cx2, 366, 180, lab) + line(cx2, 418, cx2, 430, C["navy"], 2.5) + or_gate(cx2, 444)
    tree += path(f"M{cx2},{470} L{cx2},{480} L{cx2 - 55},{480} L{cx2 - 55},{492}", C["navy"], 2.5) + path(f"M{cx2},{480} L{cx2 + 55},{480} L{cx2 + 55},{492}", C["navy"], 2.5)
  tree += basic(c1 - 55, 514, "K1 welded") + basic(c1 + 55, 514, "Logic 1 fault") + basic(c2 - 55, 514, "K2 welded") + basic(c2 + 55, 514, "Logic 2 fault")
  tree += basic(cx_, 280, "Common cause: one event fails both")
  body = [g(tree, a.show(0.2))]
  # lit states
  lit = lambda x, y: circle(x, y, 22, C["red"], C["navy"], 2.5)
  box_lit = lambda x, y, w: rect(x - w / 2, y, w, 52, "none", r=10, stroke=C["red"], sw=4)
  top_lit = rect(top_x - 223, 93, 446, 60, "none", r=12, stroke=C["red"], sw=5)
  body.append(g(lit(c1 - 55, 514), a.vis([(1.6, 10.0)], static=False)))
  body.append(g(box_lit(c1, 366, 180), a.vis([(2.3, 10.0)], static=False)))
  body.append(g(rect(560, 400, 370, 60, C["green_pale"], r=10) + text(745, 436, "One channel down: the stop still works", 17, C["ink"], 700, "middle"), a.show(3.0, 5.4, static=False)))
  body.append(g(lit(c2 - 55, 514), a.vis([(5.6, 10.0)], static=False)))
  body.append(g(box_lit(c2, 366, 180), a.vis([(6.3, 10.0)], static=False)))
  body.append(g(box_lit(ax, 240, 200), a.vis([(7.0, 10.0)], static=False)))
  body.append(g(top_lit, a.vis([(7.7, 10.0), (12.4, 15.6)], static=False)))
  body.append(g(rect(560, 400, 370, 60, C["red_pale"], r=10) + text(745, 436, "Both down: the top event happens", 17, C["ink"], 700, "middle"), a.show(7.9, 10.0, static=False)))
  body.append(g(lit(cx_, 280), a.vis([(11.0, 15.6)], static=False)))
  body.append(g(rect(560, 400, 370, 60, C["red_pale"], r=10) + text(745, 436, "A common cause skips the redundancy", 17, C["ink"], 700, "middle"), a.show(12.6, 15.6, static=False)))
  mcs = rect(660, 96, 270, 270, C["panel"], r=12) + text(676, 124, "MINIMAL CUT SETS", 13.5, C["muted"], 700, spacing=1.1)
  for k, s_ in enumerate(["K1 welded + K2 welded", "K1 welded + Logic 2 fault", "Logic 1 fault + K2 welded", "Logic 1 fault + Logic 2 fault", "Common cause, alone"]):
    mcs += text(676, 158 + k * 34, s_, 16, C["ink"], 600 if k < 4 else 700)
  mcs += para(676, 336, "The smallest sets of events that cause the top event", 14, 240, C["muted"])
  body.append(g(mcs, a.show(14.0)))
  return svg("iec-61025", "IEC 61025 · fault tree analysis", "Fault trees: which combinations cause the top event", (
    "A fault tree, as an illustration of the method, for the top event 'motor power stays on after an E-stop demand'. "
    "An OR gate joins two branches: both channels fail, an AND gate over channel 1 fails and channel 2 fails, each an "
    "OR gate over a welded contactor or a logic fault; and a common cause that fails both channels at once. The "
    "animation lights one basic event (the stop still works), then the second channel (the top event happens), then "
    "the common cause alone (it skips the redundancy). The minimal cut sets are listed: each pair of one fault per "
    "channel, and the common cause alone."), body, h, a)


@figure("iso-21448")
def iso_21448() -> str:
  a = Anim(15)
  h = 620
  gx, gy, cw, rh = 70, 130, 270, 190
  body = []
  heads = text(gx + cw / 2, gy - 12, "Known", 18, C["navy"], 700, "middle") + text(gx + cw * 1.5, gy - 12, "Unknown", 18, C["navy"], 700, "middle")
  heads += (f'<text x="{gx - 18}" y="{gy + rh / 2:.0f}" font-size="18" fill="{C["navy"]}" font-weight="700" text-anchor="middle" transform="rotate(-90 {gx - 18} {gy + rh / 2:.0f})">Unsafe</text>'
            f'<text x="{gx - 18}" y="{gy + rh * 1.5:.0f}" font-size="18" fill="{C["navy"]}" font-weight="700" text-anchor="middle" transform="rotate(-90 {gx - 18} {gy + rh * 1.5:.0f})">Safe</text>')
  cells = [(gx, gy, "2  Known and unsafe", C["cream"], "e.g. a contact too light for the torque estimate to sense"),
           (gx + cw, gy, "3  Unknown and unsafe", C["red_pale"], "the scenes nobody has thought of yet"),
           (gx, gy + rh, "1  Known and safe", C["green_pale"], "handled by a measure or a limit"),
           (gx + cw, gy + rh, "4  Unknown and safe", C["panel"], "harmless whether found or not")]
  grid = heads
  for x, y, lab, fill, ex in cells:
    grid += rect(x + 4, y + 4, cw - 8, rh - 8, fill, r=12) + text(x + 20, y + 34, lab, 18, C["ink"], 700) + para(x + 20, y + 62, ex, 15, cw - 40, C["muted"])
  body.append(g(grid, a.show(0.2)))
  # area 3 shrinks as it is explored; area 2 shrinks as measures land
  shrink3 = a._rule(a._name(), f"0%,{a.p(2.0)}{{transform:scale(1)}}{a.p(4.4)},{a.p(a.reset)}{{transform:scale(0.45)}}{a.p(a.reset + 0.3)},100%{{transform:scale(1)}}",
                    f"transform-origin:{gx + 2 * cw - 10}px {gy + rh - 10}px;transform:scale(0.45);")
  body.append(rect(gx + cw + 30, gy + 96, cw - 60, rh - 110, C["red"], r=10, c=shrink3).replace("<rect", '<rect fill-opacity="0.35"', 1))
  shrink2 = a._rule(a._name(), f"0%,{a.p(6.0)}{{transform:scale(1)}}{a.p(8.4)},{a.p(a.reset)}{{transform:scale(0.5)}}{a.p(a.reset + 0.3)},100%{{transform:scale(1)}}",
                    f"transform-origin:{gx + 10}px {gy + rh - 10}px;transform:scale(0.5);")
  body.append(rect(gx + 30, gy + 110, cw - 60, rh - 124, C["gold"], r=10, c=shrink2).replace("<rect", '<rect fill-opacity="0.45"', 1))
  body.append(path(f"M{gx + cw + 40},{gy + 150} C{gx + cw},{gy + 170} {gx + cw - 20},{gy + 170} {gx + cw - 50},{gy + 150}", C["navy"], 3, arrow=True, c=a.draw(2.4, 1.4, 120)))
  body.append(path(f"M{gx + cw - 44},{gy + rh - 14} L{gx + cw - 44},{gy + rh + 40}", C["navy"], 3, arrow=True, c=a.draw(6.4, 1.2, 60)))
  steps = [("Find the triggering conditions", "analysis, tests, field data: move area 3 into area 2"),
           ("Add measures or limit the envelope", "move area 2 into area 1"),
           ("Argue what is left", "the residual risk of areas 2 and 3 is acceptable")]
  rx = 650
  for k, (t1, t2) in enumerate(steps):
    yy = 130 + k * 130
    body.append(g(rect(rx, yy, 280, 112, C["panel"], r=12) + circle(rx + 26, yy + 30, 15, C["navy"]) + text(rx + 26, yy + 36, str(k + 1), 16, C["white"], 700, "middle") +
                  para(rx + 50, yy + 34, t1, 17, 216, C["ink"], 700) + para(rx + 18, yy + 82, t2, 15, 250, C["muted"]), a.show(2.2 + 4.0 * k)))
  return svg("iso-21448", "ISO 21448 · hazards without a failure (used as a method)", "Shrink the unknown and the unsafe", (
    "A two-by-two grid: known or unknown, safe or unsafe. Area 1 known and safe, handled by a measure or a limit; area "
    "2 known and unsafe, for example a contact too light for a torque estimate to sense; area 3 unknown and unsafe, the "
    "scenes nobody has thought of yet; area 4 unknown and safe. The animation shrinks area 3 as triggering conditions "
    "are found through analysis, tests and field data, moving them into area 2, then shrinks area 2 as measures or "
    "envelope limits move it into area 1; what is left is argued as acceptable residual risk."), body, h, a)


@figure("iec-62443")
def iec_62443() -> str:
  a = Anim(17)
  h = 660
  zones = [("Network, laptops", 30, 190), ("Host PC: ROS 2, SDK, policy", 252, 230), ("Motor bus: CAN", 514, 170), ("Safety chain: relay, contactor", 760, 172)]
  zy, zh = 116, 150
  body = []
  for k, (lab, x, w) in enumerate(zones):
    fill = C["cream"] if k == 3 else C["pale"]
    body.append(g(rect(x, zy, w, zh, fill, r=14, stroke=C["navy"] if k < 3 else C["gold"], sw=2.5, dash="" if k == 3 else "9 7") +
                  text(x + 14, zy + 28, "ZONE", 13, C["muted"], 700, spacing=1.2) + para(x + 14, zy + 56, lab, 18, w - 28, C["ink"], 700), a.show(0.3 + 0.4 * k)))
  yc = zy + 104
  for k, (x1, x2) in enumerate(((220, 252), (482, 514))):
    body.append(g(rect(x1 - 6, yc - 14, x2 - x1 + 12, 28, C["navy"], r=6) + circle((x1 + x2) / 2, yc, 9, C["gold"]), a.show(1.9 + 0.3 * k)))
  body.append(g(text(722, yc - 4, "no", 15, C["red"], 700, "middle") + text(722, yc + 14, "conduit", 15, C["red"], 700, "middle"), a.show(2.6)))
  body.append(g(rect(30, zy + zh + 12, 30, 20, C["navy"], r=5) + circle(45, zy + zh + 22, 6, C["gold"]) +
                text(70, zy + zh + 28, "conduit: a controlled, authenticated path between two zones", 15, C["ink"], 600), a.show(2.2)))
  # an attack that the first conduit refuses, then one that gets in and still cannot reach the chain
  ay = yc
  body.append(token(a, [(3.2, 60, ay), (4.4, 214, ay), (4.9, 150, ay - 40)], C["red"], 10, t_hide=5.2))
  body.append(g(rect(30, zy + zh + 44, 300, 40, C["green_pale"], r=8) + text(180, zy + zh + 70, "refused: not authenticated", 16, C["ink"], 700, "middle"), a.show(4.4, 6.0, static=False)))
  body.append(token(a, [(6.4, 60, ay), (7.4, 236, ay), (8.4, 400, ay), (9.2, 498, ay), (10.0, 620, ay), (10.8, 700, ay), (11.2, 680, ay - 40)], C["red"], 10, t_hide=11.5))
  body.append(g(rect(514, zy + zh + 44, 418, 40, C["cream"], r=8) + text(723, zy + zh + 70, "still out of reach: the chain has no network path", 16, C["ink"], 700, "middle"), a.show(10.8, 13.2, static=False)))
  # IEC 62443-4-1 practices and 4-2 component requirements
  prac = [("SM", "security management"), ("SR", "security requirements"), ("SD", "secure by design"), ("SI", "secure implementation"),
          ("SVV", "verification, validation"), ("DM", "security issues"), ("SUM", "update management"), ("SG", "security guidelines")]
  body.append(g(text(30, 384, "IEC 62443-4-1: THE EIGHT PRACTICES OF A SECURE DEVELOPMENT LIFECYCLE", 13.5, C["muted"], 700, spacing=1.1), a.show(12.0)))
  for k, (code, name) in enumerate(prac):
    x = 30 + (k % 4) * 228
    y = 400 + (k // 4) * 70
    body.append(g(rect(x, y, 216, 58, C["panel"], r=10) + text(x + 14, y + 26, code, 18, C["navy"], 700) + text(x + 14, y + 47, name, 14.5, C["ink"]), a.show(12.2 + 0.2 * k)))
  body.append(g(rect(30, 548, 900, 50, C["pale"], r=10) + text(48, 579, "IEC 62443-4-2: component requirements under seven foundational requirements, each at a security level SL 1 to 4", 15.5, C["ink"], 600), a.show(14.0)))
  return svg("iec-62443", "IEC 62443 · industrial cybersecurity", "Zones, conduits, and a safety chain no network can reach", (
    "Four zones from left to right: the network and laptops, the host PC with ROS 2, the SDK and the policy, the CAN "
    "motor bus, and the hardwired safety chain. Conduits join the first three; there is no conduit to the safety chain. "
    "A first attack is refused at the first conduit because it is not authenticated; a second gets through to the motor "
    "bus and still cannot reach the chain, which has no network path. Below, the eight practices of IEC 62443-4-1: "
    "security management, requirements, secure by design, secure implementation, verification and validation, security "
    "issue management, update management and guidelines; and IEC 62443-4-2's component requirements under seven "
    "foundational requirements, each at a security level 1 to 4."), body, h, a)


@figure("iso-iec-tr-5469")
def iso_iec_tr_5469() -> str:
  a = Anim(16)
  h = 620
  stages = [("Learned component", "proposes a motion", C["cream"], 30), ("Clamp", "joint, speed and torque limits", C["pale"], 270),
            ("Safety layer", "watchdog, modes, plausibility", C["pale"], 500), ("Motors", "", C["panel"], 740)]
  sy, sh = 140, 120
  body = []
  for k, (t1, t2, fill, x) in enumerate(stages):
    w = 190 if k < 3 else 190
    body.append(g(rect(x, sy, w, sh, fill, r=14) + text(x + 16, sy + 40, t1, 20, C["ink"], 700) + para(x + 16, sy + 70, t2, 15.5, w - 32, C["muted"]), a.show(0.3 + 0.4 * k)))
    if k:
      body.append(g(line(stages[k - 1][3] + 194, sy + sh / 2, x - 6, sy + sh / 2, C["muted"], 2.5, arrow=True), a.show(0.3 + 0.4 * k)))
  chain = rect(270, 340, 660, 70, C["navy"], r=14) + text(290, 384, "Hardwired safety chain: cuts motor power whatever the software does", 18, C["white"], 700)
  chain += path("M835,340 L835,266", C["gold"], 3.5, arrow=True)
  body.append(g(chain, a.show(1.9)))
  my = sy + sh - 16
  # a normal command passes; a too-fast one is clipped; a wild one is stopped by the safety layer
  body.append(token(a, [(2.8, 120, my), (3.6, 365, my), (4.4, 595, my), (5.2, 835, my)], C["green"], 11, t_hide=5.5))
  body.append(g(text(480, 116, "an ordinary command passes", 16, C["green"], 700, "middle"), a.show(2.8, 5.6, static=False)))
  body.append(token(a, [(6.0, 120, my), (6.8, 330, my)], C["gold"], 15, t_hide=7.0))
  body.append(token(a, [(7.0, 365, my), (7.8, 595, my), (8.6, 835, my)], C["green"], 9, t_hide=8.9))
  body.append(g(text(480, 116, "a too-fast command leaves the clamp inside the limits", 16, C["gold_text"], 700, "middle"), a.show(6.0, 9.0, static=False)))
  body.append(token(a, [(9.4, 120, my), (10.2, 365, my), (10.9, 560, my)], C["red"], 11, t_hide=11.3))
  body.append(g(rect(500, sy - 4, 194, sh + 8, "none", r=16, stroke=C["red"], sw=4) + text(480, 116, "a command that breaks a rule stops the arm", 16, C["red"], 700, "middle"), a.show(10.9, 13.0, static=False)))
  q = [("Technology class", "can the component be built and checked with existing safety methods?"),
       ("Usage level", "is it part of a safety function, or outside it with no say over safety?")]
  for k, (t1, t2) in enumerate(q):
    x = 30 + k * 460
    body.append(g(rect(x, 448, 440, 116, C["panel"], r=12) + text(x + 16, 480, t1, 18, C["ink"], 700) + para(x + 16, 508, t2, 15.5, 408, C["muted"]), a.show(13.2 + 0.5 * k)))
  return svg("iso-iec-tr-5469", "ISO/IEC TR 5469 · artificial intelligence and functional safety", "Keep the learned part outside the safety function", (
    "A pipeline from a learned component that proposes a motion, through a clamp of joint, speed and torque limits and "
    "a safety layer with watchdog, modes and plausibility checks, to the motors; below, a hardwired safety chain that "
    "cuts motor power whatever the software does. An ordinary command passes; a too-fast command leaves the clamp "
    "inside the limits; a command that breaks a rule is stopped by the safety layer. Below, the two questions the "
    "report uses to classify an AI component: its technology class and its usage level."), body, h, a)


@figure("ul-4600")
def ul_4600() -> str:
  a = Anim(16)
  h = 660
  body = []
  top = rect(260, 100, 440, 62, C["navy"], r=12) + text(480, 128, "CLAIM", 13, C["light"], 700, "middle", spacing=1.2) + text(480, 151, "The arm is acceptably safe in its envelope", 18, C["white"], 700, "middle")
  body.append(g(top, a.show(0.3)))
  body.append(g(line(480, 162, 480, 192, C["navy"], 2.5) + path("M270,192 L690,192 L670,236 L250,236 Z", C["navy"], 2, C["pale"]) +
                text(470, 220, "ARGUMENT: over each hazard and safety function", 15, C["navy"], 700, "middle"), a.show(1.1)))
  subs = [("Every hazard is identified and rated", 160), ("Each safety function reaches its PL", 480), ("The assumptions hold in use", 790)]
  for k, (s_, x) in enumerate(subs):
    t = 1.9 + 0.5 * k
    body.append(g(line(470, 236, x, 270, C["navy"], 2) + rect(x - 125, 270, 250, 62, C["white"], r=12, stroke=C["navy"], sw=2.5) +
                  para(x, 296, s_, 16, 220, C["ink"], 700, "middle", lh=1.15), a.show(t)))
  for k, (x, parent) in enumerate(((110, 160), (210, 160), (410, 480), (500, 480), (790, 790))):
    t = 3.8 + 0.4 * k
    body.append(g(line(x, 380, parent, 334, C["green"], 2) +
                  circle(x, 404, 24, C["green_pale"], C["green"], 2.5) + text(x, 411, "E", 18, C["green"], 700, "middle"), a.show(t)))
  body.append(g(text(30, 456, "EVIDENCE with its review state", 14, C["green"], 700, spacing=1), a.show(4.2)))
  dfx = 580
  body.append(g(path(f"M{dfx + 20},{382} L{570},{338}", C["red"], 2.5, arrow=True) + rect(dfx, 382, 160, 48, C["red_pale"], r=10, stroke=C["red"], sw=2.5) +
                text(dfx + 80, 413, "DEFEATER", 16, C["red"], 700, "middle"), a.show(6.4)))
  body.append(g(rect(352, 266, 256, 70, "none", r=14, stroke=C["gold"], sw=5) + text(480, 456, "the claim stays open until the defeater is closed", 15, C["gold_text"], 700, "middle"), a.show(7.2)))
  body.append(g(para(dfx, 452 + 30, "a reason to doubt the claim, published, never hidden", 14.5, 170, C["red"]), a.show(6.8)))
  loop = path("M930,420 C960,300 960,180 704,131", C["mid"], 3, arrow=True)
  body.append(g(loop + text(948, 470, "field data:", 14.5, C["mid"], 700, "end") + text(948, 488, "safety performance", 14.5, C["mid"], 700, "end") + text(948, 506, "indicators", 14.5, C["mid"], 700, "end"), a.show(9.0)))
  body.append(g(rect(30, 540, 900, 66, C["panel"], r=12) + para(48, 568, "UL 4600 asks for the argument itself: claims, arguments, evidence, the defeaters you found, and the indicators that would tell you the claim has stopped being true.", 16, 864, C["ink"]), a.show(10.4)))
  return svg("ul-4600", "UL 4600 · the safety case", "Claims, arguments, evidence, and the reasons to doubt them", (
    "A safety case as a tree: the top claim that the arm is acceptably safe in its envelope, an argument over each hazard "
    "and safety function, and three sub-claims: every hazard is identified and rated, each safety function reaches its "
    "PL, the assumptions hold in use. Evidence items, each with its review state, attach under the sub-claims. A "
    "defeater, a reason to doubt a claim, attaches to the second sub-claim, which stays open until the defeater is "
    "closed. Field data return as safety performance indicators to the top claim."), body, h, a)


@figure("aspice")
def aspice() -> str:
  a = Anim(15)
  h = 660
  levels = [("0", "Incomplete", "the process does not achieve its purpose"), ("1", "Performed", "the outcomes are achieved"),
            ("2", "Managed", "planned, monitored, work products controlled"), ("3", "Established", "a defined standard process is used"),
            ("4", "Predictable", "measured and controlled in numbers"), ("5", "Innovating", "improved continuously")]
  x0, base, sw, sh = 40, 604, 148, 60
  body = []
  for k, (n, name, what) in enumerate(levels):
    x, y = x0 + k * sw, base - (k + 1) * sh
    t = 0.4 + 1.6 * k
    step = rect(x, y, sw - 6, base - y, C["pale"] if k < 3 else C["panel"], r=8)
    step += text(x + 12, y + 28, f"CL{n}", 20, C["navy"], 700) + text(x + 12, y + 50, name, 16, C["ink"], 700)
    body.append(g(step, a.show(t)))
    n = len(wrap(what, sw - 16, 14))
    body.append(g(para(x + 12, y - 10 - 17.5 * (n - 1), what, 14, sw - 16, C["muted"]), a.show(t + 0.3)))
  pts = [(0.8 + 1.6 * k, x0 + k * sw + 118, base - (k + 1) * sh + 24) for k in range(6)]
  body.append(token(a, pts, t_hide=pts[-1][0] + 1.0))
  body.append(g(rect(40, 100, 420, 84, C["cream"], r=12) + para(56, 128, "Each level adds process attributes, rated N, P, L or F: not, partly, largely or fully achieved.", 15.5, 390, C["ink"], 600), a.show(10.4)))
  return svg("aspice", "Automotive SPICE · process capability", "Six capability levels, each built on the one below", (
    "A staircase of the six capability levels: CL0 incomplete, the process does not achieve its purpose; CL1 performed, "
    "the outcomes are achieved; CL2 managed, planned, monitored and with work products controlled; CL3 established, a "
    "defined standard process is used; CL4 predictable, measured and controlled in numbers; CL5 innovating, improved "
    "continuously. Each level adds process attributes, rated not, partly, largely or fully achieved."), body, h, a)


@figure("machinery-regulation")
def machinery_regulation() -> str:
  a = Anim(17)
  h = 660
  body = []
  ty = 132
  tl = line(60, ty, 900, ty, C["light"], 6)
  for x, d1, d2 in ((90, "19 July 2023", "in force"), (520, "20 January 2027", "applies; the Machinery Directive is repealed")):
    tl += circle(x, ty, 11, C["navy"]) + text(x, ty - 22, d1, 17, C["ink"], 700, "middle" if x > 100 else "start") + text(x, ty + 34, d2, 15, C["muted"], 600, "middle" if x > 100 else "start")
  body.append(g(tl, a.show(0.3)))
  flow = [("Annex III", "Essential health and safety requirements"), ("Risk assessment", "the manufacturer's, documented"),
          ("Annex IV", "Technical documentation"), ("Conformity assessment", "internal control, or a notified body"),
          ("Annex V", "EU declaration of conformity"), ("CE marking", "then it may be placed on the market")]
  fy, fw, fh = 214, 290, 96
  pos = [(30, fy), (335, fy), (640, fy), (640, fy + 128), (335, fy + 128), (30, fy + 128)]
  for k, ((t1, t2), (x, y)) in enumerate(zip(flow, pos)):
    t = 1.2 + 0.9 * k
    fill = C["cream"] if k == 3 else C["pale"]
    body.append(g(rect(x, y, fw, fh, fill, r=12) + text(x + 16, y + 32, t1, 19, C["ink"], 700) + para(x + 16, y + 60, t2, 15.5, fw - 32, C["muted"]), a.show(t)))
  arrows = [(320, fy + 48, 333, fy + 48), (625, fy + 48, 638, fy + 48), (785, fy + 98, 785, fy + 126), (638, fy + 176, 627, fy + 176), (333, fy + 176, 322, fy + 176)]
  for k, (x1, y1, x2, y2) in enumerate(arrows):
    body.append(g(line(x1, y1, x2, y2, C["muted"], 3, arrow=True), a.show(1.6 + 0.9 * k)))
  pts = [(6.8, 175, fy + 48), (7.4, 480, fy + 48), (8.0, 785, fy + 48), (8.6, 785, fy + 176), (9.2, 480, fy + 176), (9.8, 175, fy + 176)]
  body.append(token(a, pts, t_hide=10.4))
  route = rect(30, 474, 900, 128, C["panel"], r=12) + text(48, 504, "TWO ROUTES THROUGH CONFORMITY ASSESSMENT", 13.5, C["muted"], 700, spacing=1.1)
  route += text(48, 536, "Internal control (Module A):", 17, C["ink"], 700) + text(300, 536, "the manufacturer checks and declares, applying harmonised standards", 15.5, C["ink"])
  route += text(48, 568, "A notified body:", 17, C["ink"], 700) + text(300, 568, "required for the machinery listed in Annex I Part A, which includes", 15.5, C["ink"])
  route += text(300, 590, "safety functions with self-evolving behaviour from machine learning", 15.5, C["ink"])
  body.append(g(route, a.show(10.8)))
  return svg("machinery-regulation", "Regulation (EU) 2023/1230 · the Machinery Regulation", "From essential requirements to the CE mark", (
    "A timeline: in force on 19 July 2023, applies from 20 January 2027 when the Machinery Directive is repealed. Then "
    "the route a manufacturer follows: the essential health and safety requirements of Annex III, a documented risk "
    "assessment, the technical documentation of Annex IV, conformity assessment, the EU declaration of conformity of "
    "Annex V, and CE marking before the machine is placed on the market. Two routes through conformity assessment: "
    "internal control, Module A, applying harmonised standards; or a notified body, required for the machinery listed "
    "in Annex I Part A, which includes safety functions with self-evolving behaviour from machine learning."), body, h, a)


@figure("ai-act")
def ai_act() -> str:
  a = Anim(17)
  h = 660
  qs = [("Is there an AI system in the product?", 104), ("Is it a safety component of the product?", 224),
        ("Is the product under Annex I law, such as the Machinery Regulation, and does it need third-party conformity assessment?", 344)]
  qx, qw = 40, 470
  body = []
  for k, (q, y) in enumerate(qs):
    hh = 84 if k == 2 else 64
    body.append(g(rect(qx, y, qw, hh, C["pale"], r=12) + text(qx + 16, y + 26, f"Q{k + 1}", 14, C["muted"], 700) + para(qx + 56, y + 27, q, 17, qw - 72, C["ink"], 700), a.show(0.3 + 0.5 * k)))
    if k:
      body.append(g(line(qx + qw / 2, qs[k - 1][1] + 64, qx + qw / 2, y - 4, C["green"], 3, arrow=True) + text(qx + qw / 2 + 10, y - 22, "yes", 15, C["green"], 700), a.show(0.3 + 0.5 * k)))
  hr_y = 480
  body.append(g(line(qx + qw / 2, 428, qx + qw / 2, hr_y - 4, C["green"], 3, arrow=True) + text(qx + qw / 2 + 10, hr_y - 22, "yes", 15, C["green"], 700) +
                rect(qx, hr_y, qw, 128, C["red_pale"], r=12, stroke=C["red"], sw=2.5) + text(qx + 16, hr_y + 32, "High-risk AI system, Article 6(1)", 19, C["ink"], 700) +
                para(qx + 16, hr_y + 60, "risk management, data governance, logging, transparency, human oversight, accuracy, robustness, cybersecurity, conformity assessment", 15, qw - 32, C["ink"]), a.show(1.8)))
  nx = 590
  body.append(g(rect(nx, 224, 340, 168, C["green_pale"], r=12) + text(nx + 16, 256, "Not high-risk by this route", 19, C["ink"], 700) +
                para(nx + 16, 284, "e.g. a learned component outside every safety function, its output clamped. Other duties of the Act may still apply.", 15.5, 308, C["ink"]), a.show(2.2)))
  body.append(g(path(f"M{qx + qw},{256} L{nx - 6},{256}", C["red"], 3, arrow=True) + text(qx + qw + 14, 246, "no", 15, C["red"], 700), a.show(2.2)))
  # path A: yes, yes, yes; path B: yes, then no
  xa = qx + qw - 40
  body.append(token(a, [(3.2, xa, 136), (4.0, xa, 256), (4.8, xa, 386), (5.6, xa, 540)], C["red"], 12, t_hide=7.4))
  body.append(token(a, [(8.6, xa, 136), (9.4, xa, 256), (10.4, nx + 40, 256), (11.0, nx + 40, 300)], C["green"], 12, t_hide=13.4))
  body.append(g(rect(nx, 430, 340, 104, C["panel"], r=12) + para(nx + 16, 460, "The Act applies in stages; which dates bind a high-risk system of this kind is to be checked against the current text.", 15, 308, C["muted"]), a.show(12.2)))
  return svg("ai-act", "Regulation (EU) 2024/1689 · the AI Act", "When does an AI component make a product high-risk?", (
    "A decision path. Q1: is there an AI system in the product? Q2: is it a safety component of the product? Q3: is "
    "the product under the Union law listed in Annex I, such as the Machinery Regulation, and does it need third-party "
    "conformity assessment? Yes to all three makes it a high-risk AI system under Article 6(1), with duties for risk "
    "management, data governance, logging, transparency, human oversight, accuracy, robustness, cybersecurity and "
    "conformity assessment. No at Q2, for example a learned component outside every safety function with its output "
    "clamped, means it is not high-risk by this route; other duties may still apply. The Act applies in stages."), body, h, a)


# ---- end of figures ----


def render_all() -> dict[str, str]:
  return {f"{slug}.svg": fn() for slug, fn in FIGS.items()}


def main(argv: list[str]) -> int:
  files = render_all()
  if "--check" in argv:
    problems = []
    for name, text_ in files.items():
      p = OUT / name
      if not p.exists() or p.read_text(encoding="utf-8") != text_:
        problems.append(f"docs/assets/rebot/tour/{name}: stale or missing; run tools/wiki/tour_figures.py")
    extra = sorted(p.name for p in OUT.glob("*.svg") if p.name not in files) if OUT.exists() else []
    problems += [f"docs/assets/rebot/tour/{n}: not produced by the generator; remove it" for n in extra]
    for p in problems:
      print(p)
    if problems:
      return 1
    print(f"tour figures current: {len(files)}")
    return 0
  OUT.mkdir(parents=True, exist_ok=True)
  for name, text_ in files.items():
    (OUT / name).write_text(text_, encoding="utf-8")
  print(f"wrote {len(files)} figures to {OUT.relative_to(ROOT)}")
  return 0


if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
