"""Does the weather make train disruptions worse?

Joins daily train disruptions (Rijden de Treinen, 2019-2025) with daily weather
from KNMI station De Bilt (260), then compares normal days with days of
storm gusts, heavy rain and hard frost.

Before running, download the KNMI daily data for De Bilt and unzip it into
weather/etmgeg_260.txt:
https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_260.zip

Run from the repository root:
    python analysis/weather_vs_disruptions.py

Output: dashboard/by_day_weather.csv and the comparison tables printed below.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
YEARS = range(2019, 2026)


def load_daily_disruptions() -> pd.DataFrame:
    frames = [pd.read_csv(ROOT / f"disruptions-{y}.csv", usecols=["start_time", "duration_minutes"]) for y in YEARS]
    df = pd.concat(frames, ignore_index=True)
    df["date"] = pd.to_datetime(df["start_time"]).dt.normalize()
    daily = df.groupby("date").agg(
        disruptions=("date", "size"),
        hours=("duration_minutes", lambda m: m.sum() / 60),
    )
    # Days without any disruption still count, as zero
    all_days = pd.date_range(f"{min(YEARS)}-01-01", f"{max(YEARS)}-12-31", freq="D")
    return daily.reindex(all_days, fill_value=0)


def load_knmi(path: Path) -> pd.DataFrame:
    lines = path.read_text(encoding="latin-1").splitlines()
    header_row = next(i for i, line in enumerate(lines) if line.startswith("# STN,YYYYMMDD"))
    columns = [c.strip() for c in lines[header_row].lstrip("# ").split(",")]
    rows = [line.split(",") for line in lines[header_row + 1:] if line.strip()]
    w = pd.DataFrame(rows, columns=columns).apply(lambda s: pd.to_numeric(s.str.strip(), errors="coerce"))
    w.index = pd.to_datetime(w["YYYYMMDD"].astype(int).astype(str))
    return pd.DataFrame({
        "max_gust_ms": w["FXX"] / 10,           # strongest gust, 0.1 m/s -> m/s
        "rain_mm": w["RH"].clip(lower=0) / 10,  # daily rain, 0.1 mm -> mm (-1 = trace -> 0)
        "min_temp_c": w["TN"] / 10,             # lowest temperature, 0.1 C -> C
    })


def main() -> None:
    daily = load_daily_disruptions()
    weather = load_knmi(ROOT / "weather" / "etmgeg_260.txt")
    d = daily.join(weather, how="inner")
    d.index.name = "date"

    out = ROOT / "dashboard" / "by_day_weather.csv"
    d.round(1).to_csv(out)
    print(f"Saved {len(d)} days to {out.relative_to(ROOT)}")

    # Medians, not means: one multi-day disruption can blow up a day's hours.
    groups = {
        "Normal day": (d.max_gust_ms < 20) & (d.rain_mm < 20) & (d.min_temp_c > -5),
        "Heavy rain (>= 20 mm)": d.rain_mm >= 20,
        "Storm gusts (>= 20 m/s, 72 km/h)": d.max_gust_ms >= 20,
        "Hard frost (<= -5 C)": d.min_temp_c <= -5,
    }
    rows = []
    for name, mask in groups.items():
        s = d[mask]
        rows.append({"weather": name, "days": len(s),
                     "median_disruptions": s.disruptions.median(),
                     "median_hours": round(s.hours.median())})
    table = pd.DataFrame(rows).set_index("weather")
    normal = table.loc["Normal day", "median_disruptions"]
    table["vs_normal"] = (table.median_disruptions / normal - 1).map("{:+.0%}".format)
    print("\n" + table.to_string())

    print("\nSpearman correlation with disruptions per day (all days):")
    for col in ["max_gust_ms", "rain_mm", "min_temp_c"]:
        print(f"  {col}: {d.disruptions.corr(d[col], method='spearman'):+.2f}")

    autumn = d.index.month.isin([10, 11])
    print(f"\nAverage disruptions per day, Oct-Nov: {d[autumn].disruptions.mean():.1f}"
          f" vs other months: {d[~autumn].disruptions.mean():.1f}")


if __name__ == "__main__":
    main()
