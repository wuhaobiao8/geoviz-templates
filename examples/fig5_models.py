"""
Figure 5 - Model comparison + feature importance (simulated RF/XGBoost output).

Left: grouped bar chart of model metrics (R2 / RMSE on twin axis).
Right: sorted horizontal feature-importance bars with uncertainty whiskers
(repeat-run spread).
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from geoviz_templates.style import PALETTE, use_style, panel_label

OUT = Path(__file__).resolve().parents[1] / "figures" / "fig5_models.png"

MODELS = ["RF", "XGBoost", "SVR", "MLR", "PLS"]
FEATURES = ["NDVI", "LST", "NDBI", "Precip", "Elev", "Pop", "Dist-river",
            "Slope", "Soil-pH", "Clay"]


def main() -> None:
    use_style(base_size=10)
    rng = np.random.default_rng(23)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8),
                                   gridspec_kw={"width_ratios": [1, 1.25],
                                                "wspace": 0.55})

    # ---- left: metrics per model ----
    r2 = np.array([0.87, 0.89, 0.74, 0.61, 0.68])
    rmse = np.array([0.093, 0.086, 0.132, 0.162, 0.145])
    x = np.arange(len(MODELS))
    bars = ax1.bar(x - 0.19, r2, width=0.36, color=PALETTE["deep"],
                   label="R² (test)", zorder=3)
    ax1b = ax1.twinx()
    bars2 = ax1b.bar(x + 0.19, rmse, width=0.36, color=PALETTE["sand"],
                     label="RMSE (test)", zorder=3)
    for b, v in zip(bars, r2):
        ax1.text(b.get_x() + b.get_width() / 2, v + 0.012, f"{v:.2f}",
                 ha="center", fontsize=8.4, color=PALETTE["deep"],
                 fontweight="bold")
    for b, v in zip(bars2, rmse):
        ax1b.text(b.get_x() + b.get_width() / 2, v + 0.004, f"{v:.3f}",
                  ha="center", fontsize=8.4, color=PALETTE["navy"])

    ax1.set_xticks(x, MODELS)
    ax1.set_ylabel("R²")
    ax1b.set_ylabel(" ")  # legend already explains RMSE; avoid label collision
    ax1.set_ylim(0, 1.05); ax1b.set_ylim(0, 0.22)
    ax1b.grid(False); ax1b.spines["top"].set_visible(True)
    ax1b.spines["right"].set_visible(True)
    ax1b.spines["right"].set_color(PALETTE["slate"])
    ax1b.spines["top"].set_color(PALETTE["slate"])
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax1b.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper right", ncols=1)
    panel_label(ax1, "a")

    # ---- right: feature importance with repeat-run spread ----
    imp = np.sort(rng.uniform(0.02, 0.26, len(FEATURES)))[::-1]
    spread = rng.uniform(0.004, 0.02, len(FEATURES))
    order = np.argsort(imp)
    y = np.arange(len(FEATURES))
    colors = [PALETTE["deep"] if v == imp.max() else PALETTE["teal"]
              for v in imp[order]]
    ax2.barh(y, imp[order], xerr=spread[order], color=colors, height=0.62,
             error_kw=dict(ecolor=PALETTE["navy"], lw=1.0, capsize=2.5), zorder=3)
    ax2.set_yticks(y, [FEATURES[i] for i in order])
    ax2.set_xlabel("Permutation importance (mean ± SD, 20 runs)")
    ax2.set_xlim(0, imp.max() * 1.22)
    panel_label(ax2, "b")

    fig.suptitle("Model benchmark and driver ranking — simulated ML output",
                 x=0.02, ha="left", fontsize=12.5, fontweight="bold",
                 color=PALETTE["navy"])

    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT)
    print("saved:", OUT)


if __name__ == "__main__":
    main()
