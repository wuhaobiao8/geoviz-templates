"""
Figure 1 - Vegetation index time series with disturbance and recovery.
(Simulated 8-day observations, 2019-2024; generic change-detection template.)
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from geoviz_templates.style import PALETTE, use_style, event_line

OUT = Path(__file__).resolve().parents[1] / "figures" / "fig1_timeseries_event.png"


def simulate(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2019-01-05", "2024-12-28", freq="8D")
    doy = dates.dayofyear.values
    year = dates.year.values

    seasonal = 0.62 + 0.18 * np.sin(2 * np.pi * (doy - 105) / 365.0)
    event = pd.Timestamp("2022-08-15")
    dt_after = (dates - event).days.values / 365.0
    recovery = np.where(dt_after > 0, 0.10 * (1 - np.exp(-1.6 * dt_after)), 0.0)
    disturbance = np.where(
        (dates >= event) & (dates < event + pd.Timedelta(days=45)), -0.42, 0.0
    )
    trend = 0.004 * (year - 2019)
    noise = rng.normal(0, 0.035, len(dates))
    ndvi = np.clip(seasonal + recovery + disturbance + trend + noise, 0.08, 0.95)
    return pd.DataFrame({"date": dates, "ndvi": ndvi})


def main() -> None:
    use_style()
    df = simulate()

    fig, ax = plt.subplots(figsize=(9.2, 4.4))

    band = df.set_index("date")["ndvi"].rolling("90D", min_periods=5)
    lo, hi = band.min(), band.max()
    ax.fill_between(lo.index, lo, hi, color=PALETTE["aqua"], alpha=0.28, lw=0)

    monthly = df.set_index("date").resample("MS")["ndvi"].mean()
    ax.plot(df["date"], df["ndvi"], "o", ms=2.2, color=PALETTE["teal"],
            alpha=0.45, lw=0, label="Observations (8 d)")
    ax.plot(monthly.index, monthly.values, color=PALETTE["deep"], lw=2.2,
            label="Monthly mean")

    event = pd.Timestamp("2022-08-15")
    for mask, color, lab in [
        (df["date"] < event, PALETTE["slate"], "Trend before"),
        (df["date"] >= event, PALETTE["moss"], "Trend after"),
    ]:
        sub = df[mask]
        xn = sub["date"].map(mdates.date2num).values
        z = np.polyfit(xn, sub["ndvi"], 1)
        ax.plot(sub["date"], np.polyval(z, xn), ls=(0, (5, 2)), lw=1.4,
                color=color, alpha=0.9, label=lab)

    event_line(ax, event, "Disturbance 2022-08")

    ax.set_ylabel("NDVI")
    ax.set_ylim(0.05, 0.95)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(loc="lower left", ncols=2)
    ax.set_title("Vegetation index recovery after disturbance — simulated time series",
                 loc="left", fontweight="bold", color=PALETTE["navy"])

    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT)
    print("saved:", OUT)


if __name__ == "__main__":
    main()
