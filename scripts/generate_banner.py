"""Generate the GitHub profile tech-stack banner (honeycomb + hills)."""

from __future__ import annotations

import math
import re
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ICONS_DIR = ROOT / "assets" / "_icons"
OUT_SVG = ROOT / "assets" / "stack-hills.svg"

WIDTH = 900
HEIGHT = 400
HEX_R = 50

# Flat-top hex packing
HEX_W = 2 * HEX_R
HEX_H = math.sqrt(3) * HEX_R
DX = 1.5 * HEX_R
DY = HEX_H

ROWS: list[list[str]] = [
    ["cs", "azure", "kafka", "docker"],
    ["dotnet", "kubernetes", "postgres", "redis"],
    ["java", "rabbitmq", "elasticsearch"],
]


def flat_hex_points(cx: float, cy: float, r: float) -> str:
    pts: list[str] = []
    for i in range(6):
        angle = math.radians(60 * i)
        pts.append(f"{cx + r * math.cos(angle):.2f},{cy + r * math.sin(angle):.2f}")
    return " ".join(pts)


def row_origins() -> list[tuple[float, float, str]]:
    row_widths = [len(row) * DX + HEX_R for row in ROWS]
    max_w = max(row_widths)
    cluster_h = (len(ROWS) - 1) * DY + HEX_H
    origin_x = (WIDTH - max_w) / 2 + HEX_R
    origin_y = 30 + HEX_H / 2

    placed: list[tuple[float, float, str]] = []
    for r_idx, row in enumerate(ROWS):
        row_w = len(row) * DX + HEX_R
        x0 = origin_x + (max_w - row_w) / 2
        y = origin_y + r_idx * DY
        for c_idx, name in enumerate(row):
            placed.append((x0 + c_idx * DX, y, name))
    return placed


def extract_icon_inner(name: str) -> tuple[str, str]:
    raw = (ICONS_DIR / f"{name}.png").read_text(encoding="utf-8")
    # Prefer the innermost svg (the actual 256x256 icon)
    matches = list(re.finditer(r"<svg\b[^>]*>(.*)</svg>", raw, flags=re.S))
    if not matches:
        raise RuntimeError(f"No svg in {name}")
    inner = matches[-1]
    svg_open = re.search(r"<svg\b[^>]*>", raw[inner.start() :]).group(0)
    body = inner.group(1)
    # Prefix gradient / clip ids so they stay unique across icons
    body = re.sub(r'id="([^"]+)"', rf'id="{name}-\1"', body)
    body = re.sub(r"url\(#([^)]+)\)", rf"url(#{name}-\1)", body)
    return svg_open, body


def build_svg() -> str:
    placed = row_origins()
    defs: list[str] = []
    hexes: list[str] = []

    for i, (cx, cy, name) in enumerate(placed):
        clip_id = f"hex-clip-{name}"
        defs.append(
            f'<clipPath id="{clip_id}"><polygon points="{flat_hex_points(cx, cy, HEX_R)}" /></clipPath>'
        )
        _, body = extract_icon_inner(name)
        scale = (HEX_R * 2) / 256
        x = cx - HEX_R
        y = cy - HEX_R
        hexes.append(
            f'<g clip-path="url(#{clip_id})">'
            f'<g transform="translate({x:.2f} {y:.2f}) scale({scale:.5f})">{body}</g>'
            f"</g>"
            f'<polygon points="{flat_hex_points(cx, cy, HEX_R)}" fill="none" '
            f'stroke="#000000" stroke-width="2.5" />'
        )

    hills = """
      <path d="M0,304 C70,286 130,322 210,296 C300,268 360,310 450,288 C540,266 620,306 710,280 C790,260 850,286 900,270 L900,400 L0,400 Z" fill="#8BCF7A"/>
      <path d="M0,332 C90,314 170,352 270,328 C370,302 460,346 560,322 C660,298 760,340 900,312 L900,400 L0,400 Z" fill="#A8DC9A"/>
      <path d="M0,358 C120,344 220,376 340,356 C470,334 580,378 700,356 C800,340 860,364 900,350 L900,400 L0,400 Z" fill="#C5EBB8"/>
    """

    label = (
        '<g transform="translate(20, 358)">'
        '<rect width="456" height="28" rx="2" fill="#111111"/>'
        '<text x="14" y="19" fill="#F5F5F5" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        'font-size="12">Istanbul  ·  distributed systems  ·  cloud-native architecture</text>'
        "</g>"
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="Tech stack">
  <rect width="{WIDTH}" height="{HEIGHT}" fill="#000000"/>
  <defs>
    {''.join(defs)}
  </defs>
  {''.join(hexes)}
  {hills}
  {label}
</svg>
"""


def main() -> None:
    OUT_SVG.parent.mkdir(parents=True, exist_ok=True)
    OUT_SVG.write_text(build_svg(), encoding="utf-8")
    print(f"Wrote {OUT_SVG}")


if __name__ == "__main__":
    main()
