"""Chart for the Part 2 post: train disruptions on a typical day, by weather.

Run from the repository root after weather_vs_disruptions.py:
    python analysis/weather_chart.py
Output: dashboard/weather_chart.png (1200 x 675 px)
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
d = pd.read_csv(ROOT / "dashboard" / "by_day_weather.csv", parse_dates=["date"])

groups = [
    ("Normal day", (d.max_gust_ms < 20) & (d.rain_mm < 20) & (d.min_temp_c > -5)),
    ("Heavy rain\n(20 mm or more)", d.rain_mm >= 20),
    ("Storm\n(gusts 72 km/h or more)", d.max_gust_ms >= 20),
    ("Hard frost\n(−5 °C or colder)", d.min_temp_c <= -5),
]
labels = [g[0] for g in groups]
values = [d[m].disruptions.median() for _, m in groups]
days = [int(m.sum()) for _, m in groups]
normal = values[0]

NAVY, GREY = "#1D3557", "#B8C0CC"
INK, MUTED, GRID = "#1D3557", "#5B6577", "#E6E9EE"

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
fig.patch.set_facecolor("white")
y = list(range(len(labels)))[::-1]  # Normal day on top
colors = [GREY] + [NAVY] * (len(labels) - 1)
ax.barh(y, values, height=0.56, color=colors, edgecolor="white", linewidth=2)

for yi, v, n, i in zip(y, values, days, range(len(values))):
    extra = "" if i == 0 else f"  (+{v / normal - 1:.0%})"
    ax.text(v + 0.4, yi, f"{v:.0f} disruptions{extra}", va="center", ha="left",
            fontsize=10.5, color=INK, fontweight="bold" if i == len(values) - 1 else "normal")

ax.set_yticks(y, labels, fontsize=10, color=INK)
ax.set_xlim(0, max(values) * 1.55)
ax.xaxis.set_visible(False)
for s in ["top", "right", "bottom"]:
    ax.spines[s].set_visible(False)
ax.spines["left"].set_color(GRID)
ax.tick_params(axis="y", length=0, pad=8)

fig.text(0.03, 0.93, "Frost brings the most extra train disruptions", fontsize=15, fontweight="bold", color=INK)
fig.text(0.03, 0.865, "Train disruptions in the Netherlands on a typical day, by weather · 2019–2025",
         fontsize=10, color=MUTED)
fig.text(0.03, 0.03, "Typical day = median. Weather measured at KNMI De Bilt. "
         "Data: Rijden de Treinen, KNMI.", fontsize=8, color=MUTED)

fig.subplots_adjust(left=0.27, right=0.97, top=0.80, bottom=0.12)
out = ROOT / "dashboard" / "weather_chart.png"
fig.savefig(out, dpi=150, facecolor="white")
print("saved", out, "| values:", values, "| days:", days)
