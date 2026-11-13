"""
Figure 3 - Ridgeline distributions by year (simulated).

Joyplot-style stacked densities showing a distribution shifting right and
tightening year by year — recovery, restoration, or policy effect.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from geoviz_templates.style import PALETTE, use_style

OUT = Path(__file__).resolve().parents[1] / "figures" / "fig3_ridgeline.png"

YEARS = list(range(2019, 2025))


def year_samples(seed: int = 7) -> dict[int, np.ndarray]:
    rng = np.random.default_rng(seed)
    out = {}
    for i, y in enumerate(YEARS):
        mean = 0.42 + 0.055 * i
        sd = 0.10 - 0.008 * i
        out[y] = np.clip(rng.normal(mean, sd, 420), 0.05, 0.92)
    return out


def main() -> None:
    use_style(base_size=10)
    data = year_samples()

    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    xs = np.linspace(0.02, 0.95, 400)
    overlap = 0.62
    for i, y in enumerate(YEARS):
        kde = gaussian_kde(data[y])
        dens = kde(xs)
        dens = dens / dens.max() * 0.85
        base = -i * overlap
        color = PALETTE["deep"] if i < 3 else PALETTE["moss"]
        ax.fill_between(xs, base, base + dens, color=color, alpha=0.16 + 0.10 * i,
                        lw=0, zorder=i + 1)
        ax.plot(xs, base + dens, color=color, lw=1.6, zorder=i + 2)
        ax.axhline(base, color=PALETTE["slate"], lw=0.5, alpha=0.5, zorder=i)
        ax.text(0.955, base + 0.10, str(y), ha="right", va="bottom",
                fontsize=10, fontweight="bold", color=PALETTE["navy"], zorder=12)

    for i, y in enumerate(YEARS):
        med = np.median(data[y])
        base = -i * overlap
        ax.plot([med], [base + 0.04], marker="v", ms=5, color=PALETTE["coral"],
                zorder=13)

    ax.set_xlim(0, 1.0)
    ax.set_ylim(-len(YEARS) * overlap + 0.1, 1.15)
    ax.set_yticks([])
    ax.set_xticks([0.1, 0.3, 0.5, 0.7, 0.9])
    ax.set_xlabel("Vegetation index (NDVI)")
    ax.spines["left"].set_visible(False)
    ax.grid(axis="x", alpha=0.18)

    ax.annotate("early period", xy=(0.24, 0.62), fontsize=8.5,
                color=PALETTE["slate"], style="italic")
    ax.annotate("later period", xy=(0.70, -1.4), fontsize=8.5,
                color=PALETTE["moss"], style="italic")
    ax.annotate("median", xy=(0.615, 0.36), fontsize=8, color=PALETTE["coral"])

    ax.set_title("Year-by-year distribution shift — ridgeline view",
                 loc="left", fontweight="bold", color=PALETTE["navy"], pad=12)

    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT)
    print("saved:", OUT)


if __name__ == "__main__":
    main()
