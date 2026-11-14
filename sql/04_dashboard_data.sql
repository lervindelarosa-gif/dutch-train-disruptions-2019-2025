-- Data for the Power BI dashboard
-- Run each query on its own (click inside it, then Ctrl + Enter),
-- then export the result as CSV with the name shown above it.

USE train_delays;

-- 1. Save as: by_year.csv
SELECT YEAR(start_time) AS year,
       COUNT(*) AS disruptions,
       ROUND(SUM(duration_minutes) / 60, 1) AS hours
FROM disruptions
GROUP BY year
ORDER BY year;

-- 2. Save as: by_year_cause.csv
SELECT YEAR(start_time) AS year,
       cause_group,
       COUNT(*) AS disruptions,
       ROUND(SUM(duration_minutes) / 60, 1) AS hours
FROM disruptions
WHERE cause_group <> ''
GROUP BY year, cause_group
ORDER BY year, hours DESC;

-- 3. Save as: by_month.csv
SELECT YEAR(start_time) AS year,
       MONTH(start_time) AS month,
       COUNT(*) AS disruptions
FROM disruptions
GROUP BY year, month
ORDER BY year, month;

-- 4. Save as: by_hour.csv
--    Includes year so the dashboard's year slicer can filter this chart too.
SELECT YEAR(start_time) AS year,
       HOUR(start_time) AS hour,
       COUNT(*) AS disruptions
FROM disruptions
GROUP BY year, hour
ORDER BY year, hour;
