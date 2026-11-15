# Dutch train disruptions 2019–2025

Power BI dashboard and SQL analysis of **38,571 disruptions** on the Dutch railway network between 2019 and 2025: how much time is lost, what causes it, and when it happens.

![Dashboard](dashboard/dashboard.png)

📄 **[Full report as PDF](dashboard/train-delays-dashboard.pdf)** (dashboard + key findings)

## Key findings

1. **Disruptions are getting longer, not just more frequent, mostly because of the worst cases.**
   The number of disruptions grew 12% (5,940 in 2019 → 6,676 in 2025), but the hours lost almost doubled (9,592 → 18,610). The *typical* disruption is only a bit longer (median 40 → 51 minutes), while disruptions of **more than 8 hours went from 159 to 413 a year**. In most years the longest 5% of disruptions cause about half of all hours lost. Durations are very skewed, so this uses the median and counts of long disruptions instead of the mean or standard deviation.

2. **2023 was the worst year, driven by staff-related causes.**
   Staff causes accounted for 8,426 hours in 2023 (38% of that year's hours), up from just 164 hours in 2019. That year the average disruption lasted 258 minutes.

3. **Infrastructure is the biggest cause overall.**
   Across 2019–2025, infrastructure caused 28,162 hours of disruption, ahead of rolling stock (22,078) and staff (18,869).

4. **Disruptions follow the daily timetable, not the seasons.**
   80% start between 06:00 and 20:00, peaking in the late afternoon (15:00–18:00). Monthly totals vary little: April is the quietest month and June the busiest.

## Part 2: Does the weather make it worse?

I joined the disruptions per day with daily weather from KNMI station **De Bilt** (2,557 days, 2019–2025) and compared a normal day with days of extreme weather. I used medians, because one very long disruption can make a single day's total look huge.

| Weather at De Bilt | Days | Disruptions on a typical day | vs normal day | Hours lost on a typical day |
|---|---|---|---|---|
| Normal day | 2,434 | 14 | – | 23 |
| Heavy rain (20 mm or more) | 40 | 18 | **+29%** | 39 |
| Storm gusts (72 km/h or more) | 57 | 19 | **+36%** | 36 |
| **Hard frost (−5 °C or colder)** | 33 | **22** | **+57%** | **53** |

- **On a normal day, the weather barely matters.** The correlation between weather and disruptions per day is about zero.
- **Extreme weather does matter, and frost the most:** frozen switches and ice on the overhead wires.
- **Leaf fall (herfstblad) is real but small.** Slippery-rail disruptions cluster in October–November, but those months have only 4% more disruptions per day than the rest of the year.
- **Storm days stand out:** 9 Feb 2020 (25 m/s gusts, 38 disruptions) and 2 Nov 2023 (23 m/s gusts, 59 disruptions), against 14 on a normal day.

Limitations: weather from one station in the middle of the country, so a storm on the coast can be stronger than De Bilt measured. On the windiest day (18 Feb 2022, 31 m/s gusts) there were only 4 disruptions, probably because trains were stopped in advance, which the data does not record as disruptions.

Script: `analysis/weather_vs_disruptions.py` · Daily data: `dashboard/by_day_weather.csv`

## How it was built

| Step | Tool | Files |
|---|---|---|
| Load 7 yearly CSV files into one table | MySQL | `sql/01_setup.sql`, `sql/03_load_all_years.sql` |
| Explore with analysis questions | MySQL | `sql/02_questions.sql` |
| Aggregate data for the dashboard | MySQL → CSV | `sql/04_dashboard_data.sql` → `dashboard/by_*.csv` |
| Build the dashboard | Power BI Desktop | `dashboard/train-delays-dashboard.pbix` |
| Compare with daily weather | Python (pandas) | `analysis/weather_vs_disruptions.py` → `dashboard/by_day_weather.csv` |

**Power BI features used**
- Data model with `by_year` as the hub table, related one-to-many to the other tables on `year`, so one year slicer filters every visual
- DAX measures: `Total disruptions`, `Total hours disrupted`, `Avg minutes per disruption` (using `DIVIDE`)
- KPI cards, stacked column chart by cause, and month and hour-of-day charts
- Power Query (M) for loading the CSVs
- Custom report theme (`dashboard/train-delays-theme.json`)

## Run it yourself

1. Run `sql/01_setup.sql`, then `sql/03_load_all_years.sql` in MySQL. Change the file paths in the `LOAD DATA` lines to where you saved the CSVs.
2. Run each query in `sql/04_dashboard_data.sql` and export it as the CSV named above it.
3. Open the `.pbix` file in Power BI Desktop. If it can't find the CSVs, go to **Transform data → Data source settings** and point it to your `dashboard` folder, then click **Refresh**.

## Data

[Rijden de Treinen](https://www.rijdendetreinen.nl) open data on train disruptions, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The raw yearly files are included in this repository (`disruptions-2019.csv` … `disruptions-2025.csv`).

Weather: daily data for station De Bilt (260) from the [KNMI](https://www.knmi.nl) (Royal Netherlands Meteorological Institute). The raw file is not included; download `etmgeg_260.zip` from KNMI and unzip it into `weather/` to rerun the script.

Note: the cause chart and cause figures leave out disruptions with no recorded cause.
