"""
Figure 2 - Regional change-timing panels (simulated).

Small multiples of gridded cells colored by the detected change timing
(month index 0 = Jan 2020 ... 59 = Dec 2024) — the "timing GeoTIFF" concept.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from geoviz_templates.style import PALETTE, GRADE_CMAP, use_style, panel_label

OUT = Path(__file__).resolve().parents[1] / "figures" / "fig2_timing_panels.png"

REGIONS = ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F"]


def region_grid(seed: int, rows: int = 16, cols: int = 12) -> np.ndarray:
    rng = np.random.default_rng(seed)
    base = rng.normal(0, 1, (3, 3))
    grid = np.kron(base, np.ones((rows // 3 + 1, cols // 3 + 1)))[:rows, :cols]
    grid = (grid - grid.min()) / (grid.max() - grid.min())
    timing = 8 + grid * 44 + rng.normal(0, 2.4, grid.shape)
    timing[rng.random(grid.shape) < 0.06] = np.nan
    return timing


def main() -> None:
    use_style(base_size=10)
    fig, axes = plt.subplots(2, 3, figsize=(9.6, 5.6))

    norm = BoundaryNorm(np.arange(0, 61, 6) - 3, GRADE_CMAP.N)
    for ax, name, seed in zip(axes.flat, REGIONS, range(10, 16)):
        g = region_grid(seed)
        im = ax.imshow(g, cmap=GRADE_CMAP, norm=norm, interpolation="nearest")
        ax.set_title(name, fontsize=10.5, fontweight="bold",
                     color=PALETTE["navy"], pad=4)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
        ax.add_patch(plt.Rectangle((0, 0), g.shape[1], g.shape[0], fill=False,
                                   ec=PALETTE["slate"], lw=0.6, alpha=0.5))
    for ax, letter in zip(axes.flat, "abcdef"):
        panel_label(ax, letter)

    cbar = fig.colorbar(im, ax=axes, shrink=0.72, pad=0.02, aspect=26,
                        ticks=np.arange(0, 61, 12))
    cbar.ax.set_yticklabels(
        ["2020-01", "2021-01", "2022-01", "2023-01", "2024-01", "2024-12"]
    )
    cbar.set_label("Detected change timing (month index)", fontsize=9.5)
    cbar.outline.set_visible(False)

    fig.suptitle("Change-timing panels — simulated multi-band GeoTIFF concept",
                 x=0.02, ha="left", fontsize=12.5, fontweight="bold",
                 color=PALETTE["navy"])

    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT)
    print("saved:", OUT)


if __name__ == "__main__":
    main()
