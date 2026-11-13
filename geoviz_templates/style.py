"""
geoviz_templates.style
======================
A compact design system for publication-quality geoscience figures.

Original palettes and helpers; no third-party branding.

Usage
-----
>>> from geoviz_templates.style import use_style, PALETTE
>>> use_style()
"""

from __future__ import annotations

import matplotlib as mpl
from cycler import cycler

# --------------------------------------------------------------------------
# Original palette (hand-tuned, print-friendly)
# --------------------------------------------------------------------------
PALETTE = {
    "deep":   "#0B4F4A",   # deep teal    - primary series
    "coral":  "#E76F51",   # coral        - events / emphasis
    "teal":   "#14919B",   # teal         - secondary series
    "sand":   "#D9C58F",   # sand         - background series
    "moss":   "#7A8B5C",   # moss green   - recovery / positive
    "navy":   "#22384F",   # navy         - text emphasis
    "slate":  "#5B6B73",   # slate gray   - grid / axes
    "paper":  "#FCFCF9",   # paper white  - figure background
    "aqua":   "#5FD0C7",   # light aqua   - fills
    "plum":   "#7D5BA6",   # plum         - extra categorical
}

SERIES_CYCLER = cycler(color=[
    PALETTE["deep"], PALETTE["coral"], PALETTE["teal"],
    PALETTE["sand"], PALETTE["moss"], PALETTE["plum"], PALETTE["navy"],
])

# Sequential ramp: month/grade style (cold -> warm)
GRADE_CMAP = mpl.colors.LinearSegmentedColormap.from_list(
    "gvt_grade",
    ["#22384F", "#14919B", "#7AC7C4", "#E7D8B1", "#E9A178", "#E76F51", "#9C3D2E"],
)

# Diverging ramp: centered on 0 (anomalies, correlations)
DIVERGE_CMAP = mpl.colors.LinearSegmentedColormap.from_list(
    "gvt_diverge",
    ["#9C3D2E", "#E9A178", "#F5F1E3", "#7AC7C4", "#0B4F4A"],
)

# Continuous ramp: density / intensity
CONT_CMAP = mpl.colors.LinearSegmentedColormap.from_list(
    "gvt_cont",
    ["#F5F1E3", "#BFE0D9", "#5FD0C7", "#14919B", "#0B4F4A"],
)


def use_style(font_family: str = "Microsoft YaHei", base_size: float = 10.5) -> None:
    """Apply the geoviz_templates matplotlib style globally."""
    mpl.rcParams.update({
        # figure
        "figure.facecolor": PALETTE["paper"],
        "axes.facecolor": PALETTE["paper"],
        "savefig.facecolor": PALETTE["paper"],
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.12,
        # fonts (CJK-capable, graceful fallback)
        "font.family": ["sans-serif"],
        "font.sans-serif": [font_family, "DejaVu Sans", "Arial"],
        "axes.unicode_minus": False,
        "font.size": base_size,
        "axes.titlesize": base_size + 2,
        "axes.labelsize": base_size,
        "xtick.labelsize": base_size - 1,
        "ytick.labelsize": base_size - 1,
        "legend.fontsize": base_size - 1,
        # axes
        "axes.edgecolor": PALETTE["slate"],
        "axes.linewidth": 0.9,
        "axes.labelcolor": PALETTE["navy"],
        "axes.prop_cycle": SERIES_CYCLER,
        "axes.grid": True,
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        # grid & ticks
        "grid.color": PALETTE["slate"],
        "grid.alpha": 0.22,
        "grid.linewidth": 0.6,
        "xtick.color": PALETTE["navy"],
        "ytick.color": PALETTE["navy"],
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        # lines & legend
        "lines.linewidth": 1.8,
        "lines.markersize": 4.5,
        "legend.frameon": False,
        "legend.handlelength": 1.6,
    })


def panel_label(ax, letter: str, dx: float = -0.08, dy: float = 1.06) -> None:
    """Bold panel letter (a, b, c ...) at the top-left of an axes."""
    ax.text(dx, dy, letter, transform=ax.transAxes,
            fontsize=13, fontweight="bold", color=PALETTE["navy"],
            ha="left", va="top")


def event_line(ax, x: float, label: str, color: str | None = None) -> None:
    """Vertical dashed marker with a rotated label (event / policy / disturbance)."""
    color = color or PALETTE["coral"]
    ax.axvline(x, color=color, linestyle=(0, (4, 2)), linewidth=1.2, alpha=0.9)
    ax.annotate(label, xy=(x, 1.0), xycoords=("data", "axes fraction"),
                xytext=(5, -4), textcoords="offset points",
                fontsize=8, color=color, rotation=90, ha="left", va="top")
