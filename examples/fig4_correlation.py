"""
Figure 4 - Correlation heatmap with significance stars (simulated).

A two-panel layout: lower triangle = Spearman rho with star annotations,
upper triangle = p-value heat map. Common need in geoscience papers.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from geoviz_templates.style import PALETTE, DIVERGE_CMAP, use_style

OUT = Path(__file__).resolve().parents[1] / "figures" / "fig4_correlation.png"

VARS = ["NDVI", "LST", "Albedo", "Precip", "Elevation", "Population", "NDBI"]


def simulate(seed: int = 11) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n = 300
    latent = rng.normal(0, 1, (n, 3))
    def jitter(i, s): return latent[:, i] + rng.normal(0, s, n)
    df = pd.DataFrame({
        "NDVI":       0.8 * jitter(0, .5) - 0.3 * jitter(1, .4) + rng.normal(0, .15, n),
        "LST":       -0.7 * jitter(0, .5) + 0.6 * jitter(1, .4) + rng.normal(0, .2, n),
        "Albedo":    -0.4 * jitter(0, .6) + 0.7 * jitter(1, .5) + rng.normal(0, .2, n),
        "Precip":     0.5 * jitter(0, .7) - 0.2 * jitter(1, .6) + rng.normal(0, .3, n),
        "Elevation":  0.2 * jitter(2, .8) + rng.normal(0, .4, n),
        "Population": 0.7 * jitter(1, .4) + rng.normal(0, .3, n),
        "NDBI":       0.6 * jitter(1, .5) - 0.5 * jitter(0, .5) + rng.normal(0, .2, n),
    })
    df = (df - df.mean()) / df.std()
    return df


def stars(p: float) -> str:
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""


def main() -> None:
    use_style(base_size=10)
    df = simulate()
    n = len(df)

    rho = df.corr(method="spearman")
    # p-values via t approximation
    from scipy import stats
    pmat = pd.DataFrame(np.ones_like(rho), index=rho.index, columns=rho.columns)
    for i in VARS:
        for j in VARS:
            if i != j:
                r = rho.loc[i, j]
                t = abs(r) * np.sqrt((n - 2) / (1 - r * r))
                pmat.loc[i, j] = 2 * (1 - stats.t.cdf(t, n - 2))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 5.4))

    # left: rho lower triangle with stars
    im = ax1.imshow(rho, cmap=DIVERGE_CMAP, vmin=-1, vmax=1)
    ax1.set_xticks(range(len(VARS)), VARS, rotation=45, ha="right")
    ax1.set_yticks(range(len(VARS)), VARS)
    for a in (ax1, ax2):
        a.grid(False)
        for s in a.spines.values():
            s.set_visible(False)
    for i in range(len(VARS)):
        for j in range(len(VARS)):
            if j < i:
                v = rho.iloc[i, j]
                color = "white" if abs(v) > 0.55 else PALETTE["navy"]
                ax1.text(j, i, f"{v:.2f}{stars(pmat.iloc[i, j])}",
                         ha="center", va="center", fontsize=8.6,
                         color=color, fontweight="bold")
            elif j == i:
                ax1.text(j, i, "1.0", ha="center", va="center",
                         fontsize=8.6, color=PALETTE["slate"])
    ax1.set_title("Spearman rho (lower triangle)", loc="left",
                  fontsize=10.5, fontweight="bold", color=PALETTE["navy"])
    cb = fig.colorbar(im, ax=ax1, shrink=0.78, pad=0.02)
    cb.outline.set_visible(False); cb.ax.tick_params(labelsize=8)

    # right: p-value heat map (upper triangle filled)
    pdisp = pmat.copy()
    im2 = ax2.imshow(pdisp, cmap="viridis_r", vmin=0, vmax=0.2)
    ax2.set_xticks(range(len(VARS)), VARS, rotation=45, ha="right")
    ax2.set_yticks(range(len(VARS)), VARS)
    for i in range(len(VARS)):
        for j in range(len(VARS)):
            if j > i:
                p = pmat.iloc[i, j]
                color = "white" if p < 0.08 else PALETTE["navy"]
                ax2.text(j, i, f"{p:.3f}", ha="center", va="center",
                         fontsize=8.2, color=color)
            elif j == i:
                ax2.text(j, i, "—", ha="center", va="center",
                         fontsize=8.6, color=PALETTE["slate"])
    ax2.set_title("p-value (upper triangle, two-sided)", loc="left",
                  fontsize=10.5, fontweight="bold", color=PALETTE["navy"])
    cb2 = fig.colorbar(im2, ax=ax2, shrink=0.78, pad=0.02)
    cb2.outline.set_visible(False); cb2.ax.tick_params(labelsize=8)

    fig.suptitle("Correlation structure with significance — simulated drivers",
                 x=0.02, ha="left", fontsize=12.5, fontweight="bold",
                 color=PALETTE["navy"])

    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT)
    print("saved:", OUT)


if __name__ == "__main__":
    main()
