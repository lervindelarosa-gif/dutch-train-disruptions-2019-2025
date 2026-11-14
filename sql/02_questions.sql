-- Dutch train disruptions 2025: analysis questions
-- Data: Rijden de Treinen (rijdendetreinen.nl), CC BY 4.0
-- Run 01_setup.sql once first.

USE train_delays;

-- Q1: Which type of cause has the most disruptions?
-- Result: rolling stock (broken trains) 44%, infrastructure 24%, weather only 51 of 6,676.
SELECT cause_group,
       COUNT(*) AS disruptions,
       ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM disruptions
GROUP BY cause_group
ORDER BY disruptions DESC;

-- Q2: Which causes have the most total hours of disruption?
-- Result: problems with the rolling stock about 2,400 hours, broken down train about 1,731.
SELECT cause_en,
       ROUND(SUM(duration_minutes) / 60, 1) AS hours
FROM disruptions
GROUP BY cause_en
ORDER BY hours DESC
LIMIT 10;

-- Q3: Which causes last longest on average? (only causes with 10+ disruptions)
-- Result: strikes abroad 78 hours, strikes at NS 23 hours, copper theft 15 hours.
-- Note: one strike can appear as many rows (one per route), so these are records, not events.
SELECT cause_en,
       COUNT(*) AS disruptions,
       ROUND(AVG(duration_minutes) / 60, 1) AS avg_hours
FROM disruptions
GROUP BY cause_en
HAVING COUNT(*) >= 10
ORDER BY avg_hours DESC
LIMIT 10;

-- Q4: Which month has the most disruptions?
SELECT MONTH(start_time) AS month,
       COUNT(*) AS disruptions
FROM disruptions
GROUP BY month
ORDER BY month;

-- Q5: Which hour of the day do most disruptions start?
SELECT HOUR(start_time) AS hour,
       COUNT(*) AS disruptions
FROM disruptions
GROUP BY hour
ORDER BY hour;

-- Q6: Disruptions by time of day
SELECT CASE
         WHEN HOUR(start_time) BETWEEN 6 AND 9   THEN '1 Morning rush (6-9)'
         WHEN HOUR(start_time) BETWEEN 10 AND 15 THEN '2 Daytime (10-15)'
         WHEN HOUR(start_time) BETWEEN 16 AND 19 THEN '3 Evening rush (16-19)'
         WHEN HOUR(start_time) BETWEEN 20 AND 23 THEN '4 Evening (20-23)'
         ELSE '5 Night (0-5)'
       END AS period,
       COUNT(*) AS disruptions
FROM disruptions
GROUP BY period
ORDER BY period;
