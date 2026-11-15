"""Build the small JSON file behind the interactive web dashboard.

Run from the repository root (after weather_vs_disruptions.py):
    python analysis/build_web_data.py <output path>
Default output: web/data.json
"""
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
YEARS = list(range(2019, 2026))
TOP_CAUSES = ["infrastructure", "rolling stock", "staff", "accidents", "logistical", "engineering work"]

df = pd.concat([pd.read_csv(ROOT / f"disruptions-{y}.csv",
                            usecols=["cause_group", "start_time", "duration_minutes"]) for y in YEARS],
               ignore_index=True)
df["start_time"] = pd.to_datetime(df["start_time"])
df["year"] = df.start_time.dt.year
df["month"] = df.start_time.dt.month
df["hour"] = df.start_time.dt.hour
df["cause"] = df.cause_group.where(df.cause_group.isin(TOP_CAUSES), "other")
df.loc[df.cause_group.isna() | (df.cause_group == ""), "cause"] = None  # no recorded cause


def kpis(s: pd.DataFrame) -> dict:
    dur = s.duration_minutes.dropna()
    return {
        "disruptions": int(len(s)),
        "hours": round(float(dur.sum() / 60)),
        "median_min": round(float(dur.median())),
        "over_8h": int((dur > 480).sum()),
    }


def by_year(s: pd.DataFrame) -> dict:
    hrs = s.groupby("year").duration_minutes.sum().div(60).reindex(YEARS, fill_value=0)
    return {"hours": [round(float(v)) for v in hrs]}


def causes(s: pd.DataFrame) -> dict:
    c = s.dropna(subset=["cause"])
    t = c.pivot_table(index="year", columns="cause", values="duration_minutes", aggfunc="sum").div(60)
    t = t.reindex(index=YEARS, columns=TOP_CAUSES + ["other"]).fillna(0)
    return {k: [round(float(v)) for v in t[k]] for k in t.columns}


def counts(s: pd.DataFrame, col: str, idx) -> list:
    return [int(v) for v in s.groupby(col).size().reindex(idx, fill_value=0)]


# Hours per year come from by_year.csv (the SQL export Power BI uses), so every
# place shows the same totals.
sql_hours = pd.read_csv(ROOT / "dashboard" / "by_year.csv").set_index("year")["hours"]
kpi_all = kpis(df)
kpi_all["hours"] = round(float(sql_hours.sum()))

data = {
    "years": YEARS,
    "causes": TOP_CAUSES + ["other"],
    "kpi": {"all": kpi_all, **{str(y): {**kpis(df[df.year == y]), "hours": round(float(sql_hours[y]))} for y in YEARS}},
    "hours_by_year": [round(float(sql_hours[y])) for y in YEARS],
    "cause_hours_by_year": causes(df),
    "by_month": {"all": counts(df, "month", range(1, 13)),
                 **{str(y): counts(df[df.year == y], "month", range(1, 13)) for y in YEARS}},
    "by_hour": {"all": counts(df, "hour", range(24)),
                **{str(y): counts(df[df.year == y], "hour", range(24)) for y in YEARS}},
}

# Weather comparison (all years), from the daily file made by weather_vs_disruptions.py
d = pd.read_csv(ROOT / "dashboard" / "by_day_weather.csv")
groups = [
    ("Normal day", (d.max_gust_ms < 20) & (d.rain_mm < 20) & (d.min_temp_c > -5)),
    ("Heavy rain (20 mm+)", d.rain_mm >= 20),
    ("Storm (gusts 72 km/h+)", d.max_gust_ms >= 20),
    ("Hard frost (−5 °C or colder)", d.min_temp_c <= -5),
]
data["weather"] = [{"label": name, "days": int(m.sum()), "median_disruptions": float(d[m].disruptions.median())}
                   for name, m in groups]

out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "web" / "data.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
print("saved", out, f"({out.stat().st_size / 1024:.1f} KB)")
print("check all:", data["kpi"]["all"], "| 2023:", data["kpi"]["2023"])
