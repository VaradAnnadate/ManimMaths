"""Shared helpers and 3Blue1Brown-inspired styling for the Eigenvalues & Eigenvectors video."""

from __future__ import annotations

import hashlib
import os
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    Line,
    RoundedRectangle,
    SVGMobject,
    Text,
    VGroup,
)

# 3Blue1Brown-inspired color palette
BG_COLOR = "#000000"          # Pure black background
GRID_COLOR = "#1F3B5C"        # Subtle blue grid lines
AXIS_COLOR = "#8BA3C7"        # Soft steel-blue axes
PRIMARY_TEXT = "#F4F6FA"      # Crisp off-white text
MUTED_TEXT = "#9BA8BD"        # Muted slate for captions/credits
ACCENT_BLUE = "#58C4DD"       # 3b1b signature cyan-blue
ACCENT_GOLD = "#F4D35E"       # Warm gold for highlights / lambda
ACCENT_GREEN = "#83C167"      # Soft green for v1 / i-hat
ACCENT_CORAL = "#FC6255"      # Coral-red for v2 / non-eigenvector
ACCENT_PURPLE = "#B189C6"     # Soft purple for general vectors / spans

SVG_CACHE_DIR = Path(__file__).resolve().parent / ".svg_cache"
SVG_CACHE_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["font.family"] = "serif"


def math_svg(
    tex: str,
    color: str = PRIMARY_TEXT,
    font_size: int = 28,
    height: float | None = None,
) -> SVGMobject:
    """Render a TeX math string to a crisp Computer Modern SVG using matplotlib mathtext.

    Caches the generated SVG by content hash so repeated renders are instant.
    """
    key = hashlib.sha256(f"{tex}|{color}|{font_size}".encode("utf-8")).hexdigest()[:16]
    svg_path = SVG_CACHE_DIR / f"math_{key}.svg"

    if not svg_path.exists():
        fig = plt.figure(figsize=(0.01, 0.01), dpi=300)
        fig.patch.set_alpha(0.0)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")
        ax.text(
            0.5,
            0.5,
            f"${tex}$",
            color=color,
            fontsize=font_size,
            ha="center",
            va="center",
        )
        fig.savefig(
            svg_path,
            format="svg",
            bbox_inches="tight",
            pad_inches=0.04,
            transparent=True,
        )
        plt.close(fig)

        # Sanitize SVG: remove any <path> without a non-empty 'd' attribute
        # (e.g., space glyphs emitted by matplotlib that crash svgelements)
        tree = ET.parse(svg_path)
        root = tree.getroot()
        for parent in root.iter():
            for child in list(parent):
                if child.tag.endswith("path") and not (child.attrib.get("d") or "").strip():
                    parent.remove(child)
        tree.write(svg_path, encoding="utf-8", xml_declaration=True)

    # Read native SVG height in points so all expressions keep true typographic scale
    tree = ET.parse(svg_path)
    svg_h_attr = tree.getroot().attrib.get("height", "24pt")
    svg_h_pt = float(svg_h_attr.replace("pt", "").replace("px", ""))

    mob = SVGMobject(str(svg_path))
    mob.set_color(color)
    if height is not None:
        mob.scale_to_fit_height(height)
    else:
        mob.scale_to_fit_height(svg_h_pt * 0.014)
    return mob


def make_matrix(
    rows: list[list[str]],
    color: str = PRIMARY_TEXT,
    entry_colors: list[list[str]] | None = None,
    font_size: int = 30,
    bracket_buff: float = 0.16,
    row_buff: float = 0.48,
    col_buff: float = 0.58,
) -> VGroup:
    """Create a clean vector-graphics matrix with square brackets."""
    n_rows = len(rows)
    n_cols = len(rows[0]) if rows else 0
    entries = VGroup()
    grid: list[list[SVGMobject]] = []

    for r in range(n_rows):
        row_mobs = []
        for c in range(n_cols):
            c_col = entry_colors[r][c] if entry_colors else color
            m = math_svg(rows[r][c], color=c_col, font_size=font_size)
            row_mobs.append(m)
            entries.add(m)
        grid.append(row_mobs)

    # Arrange in a uniform grid
    for r in range(n_rows):
        for c in range(n_cols):
            grid[r][c].move_to([c * col_buff, -r * row_buff, 0])
    entries.center()

    h = entries.height + 0.22
    w = entries.width + 2 * bracket_buff
    top_y = entries.get_top()[1] + 0.11
    bot_y = entries.get_bottom()[1] - 0.11
    left_x = entries.get_left()[0] - bracket_buff
    right_x = entries.get_right()[0] + bracket_buff
    tick = 0.11

    left_bracket = VGroup(
        Line([left_x + tick, top_y, 0], [left_x, top_y, 0], color=color, stroke_width=2.6),
        Line([left_x, top_y, 0], [left_x, bot_y, 0], color=color, stroke_width=2.6),
        Line([left_x, bot_y, 0], [left_x + tick, bot_y, 0], color=color, stroke_width=2.6),
    )
    right_bracket = VGroup(
        Line([right_x - tick, top_y, 0], [right_x, top_y, 0], color=color, stroke_width=2.6),
        Line([right_x, top_y, 0], [right_x, bot_y, 0], color=color, stroke_width=2.6),
        Line([right_x, bot_y, 0], [right_x - tick, bot_y, 0], color=color, stroke_width=2.6),
    )
    return VGroup(left_bracket, entries, right_bracket)


def make_det(
    rows: list[list[str]],
    color: str = PRIMARY_TEXT,
    font_size: int = 30,
    bar_buff: float = 0.18,
    row_buff: float = 0.52,
    col_buff: float = 0.85,
) -> VGroup:
    """Create a determinant |...| with vertical bars."""
    n_rows = len(rows)
    n_cols = len(rows[0]) if rows else 0
    entries = VGroup()
    grid: list[list[SVGMobject]] = []

    for r in range(n_rows):
        row_mobs = []
        for c in range(n_cols):
            m = math_svg(rows[r][c], color=color, font_size=font_size)
            row_mobs.append(m)
            entries.add(m)
        grid.append(row_mobs)

    for r in range(n_rows):
        for c in range(n_cols):
            grid[r][c].move_to([c * col_buff, -r * row_buff, 0])
    entries.center()

    top_y = entries.get_top()[1] + 0.12
    bot_y = entries.get_bottom()[1] - 0.12
    left_x = entries.get_left()[0] - bar_buff
    right_x = entries.get_right()[0] + bar_buff

    left_bar = Line([left_x, top_y, 0], [left_x, bot_y, 0], color=color, stroke_width=2.6)
    right_bar = Line([right_x, top_y, 0], [right_x, bot_y, 0], color=color, stroke_width=2.6)
    return VGroup(left_bar, entries, right_bar)


def make_badge(text_str: str, accent: str = ACCENT_BLUE) -> VGroup:
    """Create a subtle pill/section badge for the top-left corner."""
    label = Text(text_str, font="Helvetica Neue", font_size=20, color=accent, weight="BOLD")
    box = RoundedRectangle(
        corner_radius=0.12,
        width=label.width + 0.42,
        height=label.height + 0.22,
        stroke_color=accent,
        stroke_width=1.5,
        fill_color=BG_COLOR,
        fill_opacity=0.85,
    )
    label.move_to(box.get_center())
    return VGroup(box, label)


def make_info_card(
    title: str,
    body_lines: list[str],
    accent: str = ACCENT_BLUE,
    width: float = 5.4,
) -> VGroup:
    """Create a dark translucent card for overlays over grids."""
    title_mob = Text(title, font="Helvetica Neue", font_size=24, color=accent, weight="BOLD")
    body_mobs = VGroup(
        *[Text(line, font="Helvetica Neue", font_size=19, color=PRIMARY_TEXT) for line in body_lines]
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    content = VGroup(title_mob, body_mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    box = RoundedRectangle(
        corner_radius=0.16,
        width=max(width, content.width + 0.55),
        height=content.height + 0.5,
        stroke_color=accent,
        stroke_width=1.6,
        fill_color="#000000",
        fill_opacity=0.90,
    )
    content.move_to(box.get_center())
    return VGroup(box, content)
