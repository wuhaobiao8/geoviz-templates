"""
Figure 6 - Polar seasonal climatology with anomaly ribbons (simulated).

Left: 12-month polar plot of climatology + per-year lines.
Right: monthly anomaly ribbon (min/max envelope) in cartesian form.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from geoviz_templates.style import PALETTE, use_style, panel_label

OUT = Path(__file__).resolve().parents[1] / "figures" / "fig6_polar_season.png"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def simulate(seed: int = 31, years: int = 6):
    rng = np.random.default_rng(seed)
    m = np.arange(1, 13)
    clim = 0.35 + 0.28 * np.exp(-((m - 8.2) ** 2) / 12.0)  # summer peak
    yearly = np.array([
        clim + rng.normal(0, 0.05, 12) + 0.012 * y - 0.03
        for y in range(years)
    ])
    return m, clim, yearly


def main() -> None:
    use_style(base_size=10)
    m, clim, yearly = simulate()
    theta = np.linspace(0, 2 * np.pi, 12, endpoint=False)
    theta_c = np.linspace(0, 2 * np.pi, 361)

    fig = plt.figure(figsize=(11.0, 5.2))
    axp = fig.add_subplot(1, 2, 1, projection="polar")
    axc = fig.add_subplot(1, 2, 2)

    # ---- polar ----
    axp.set_theta_offset(np.pi / 2)   # Jan at top
    axp.set_theta_direction(-1)
    for row, alpha, lw in [(yearly[0], 0.55, 1.1), (yearly[-1], 0.95, 2.0)]:
        vals = np.concatenate([row, row[:1]])
        th = np.concatenate([theta, theta[:1] + 2 * np.pi])
        axp.plot(th, vals, color=PALETTE["deep"], alpha=alpha, lw=lw)
    axp.fill_between(theta_c,
                     np.interp(theta_c, theta, yearly.min(axis=0), period=12),
                     np.interp(theta_c, theta, yearly.max(axis=0), period=12),
                     color=PALETTE["aqua"], alpha=0.30, lw=0)
    axp.plot(np.concatenate([theta, theta[:1] + 2 * np.pi]),
             np.concatenate([clim, clim[:1]]),
             color=PALETTE["coral"], lw=1.8, ls=(0, (4, 2)),
             label="Climatology")
    axp.set_xticks(theta, MONTHS, fontsize=9)
    axp.set_ylim(0, 0.75)
    axp.set_yticks([0.2, 0.4, 0.6])
    axp.set_yticklabels(["0.2", "0.4", "0.6"], fontsize=8, color=PALETTE["slate"])
    axp.grid(alpha=0.35, lw=0.6)
    axp.text(-0.08, 1.10, "a", transform=axp.transAxes, fontsize=13,
             fontweight="bold", color=PALETTE["navy"], ha="left", va="top")
    axp.legend(loc="lower left", bbox_to_anchor=(-0.12, -0.16))

    # ---- cartesian anomaly ribbon ----
    anom = yearly - clim
    lo, hi = anom.min(axis=0), anom.max(axis=0)
    axc.axhline(0, color=PALETTE["slate"], lw=0.9, alpha=0.7)
    axc.fill_between(m, lo, hi, color=PALETTE["aqua"], alpha=0.4, lw=0,
                     label="Year range")
    axc.plot(m, anom.mean(axis=0), color=PALETTE["deep"], lw=2.0,
             label="Mean anomaly")
    axc.plot(m, anom[-1], color=PALETTE["moss"], lw=1.6, ls=(0, (4, 2)),
             label="Latest year")
    for x, y in zip(m, lo):
        if y < -0.06:
            axc.annotate("", xy=(x, y), xytext=(x, y - 0.02),
                         arrowprops=dict(arrowstyle="-|>", color=PALETTE["coral"]))
    axc.set_xticks(m, MONTHS, fontsize=8.5)
    axc.set_ylabel("Anomaly vs climatology")
    axc.legend(loc="upper left")
    panel_label(axc, "b")

    fig.suptitle("Monthly climatology and anomalies — simulated multi-year record",
                 x=0.02, ha="left", fontsize=12.5, fontweight="bold",
                 color=PALETTE["navy"])

    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT)
    print("saved:", OUT)


if __name__ == "__main__":
    main()
