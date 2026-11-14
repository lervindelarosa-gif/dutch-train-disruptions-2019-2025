-- Load all years 2019-2025 into the disruptions table
-- Data: Rijden de Treinen (rijdendetreinen.nl), CC BY 4.0
-- Run this whole file once (the plain lightning button).
-- It empties the table first, so 2025 is not loaded twice.

USE train_delays;
TRUNCATE TABLE disruptions;

LOAD DATA LOCAL INFILE 'C:/Users/lervi/Downloads/train-delays/disruptions-2019.csv'
INTO TABLE disruptions CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
(rdt_id, ns_lines, rdt_lines, rdt_lines_id, rdt_station_names, rdt_station_codes,
 cause_nl, cause_en, statistical_cause_nl, statistical_cause_en, cause_group,
 start_time, @end_time, @duration)
SET end_time = NULLIF(@end_time, ''), duration_minutes = NULLIF(@duration, '');

LOAD DATA LOCAL INFILE 'C:/Users/lervi/Downloads/train-delays/disruptions-2020.csv'
INTO TABLE disruptions CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
(rdt_id, ns_lines, rdt_lines, rdt_lines_id, rdt_station_names, rdt_station_codes,
 cause_nl, cause_en, statistical_cause_nl, statistical_cause_en, cause_group,
 start_time, @end_time, @duration)
SET end_time = NULLIF(@end_time, ''), duration_minutes = NULLIF(@duration, '');

LOAD DATA LOCAL INFILE 'C:/Users/lervi/Downloads/train-delays/disruptions-2021.csv'
INTO TABLE disruptions CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
(rdt_id, ns_lines, rdt_lines, rdt_lines_id, rdt_station_names, rdt_station_codes,
 cause_nl, cause_en, statistical_cause_nl, statistical_cause_en, cause_group,
 start_time, @end_time, @duration)
SET end_time = NULLIF(@end_time, ''), duration_minutes = NULLIF(@duration, '');

LOAD DATA LOCAL INFILE 'C:/Users/lervi/Downloads/train-delays/disruptions-2022.csv'
INTO TABLE disruptions CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
(rdt_id, ns_lines, rdt_lines, rdt_lines_id, rdt_station_names, rdt_station_codes,
 cause_nl, cause_en, statistical_cause_nl, statistical_cause_en, cause_group,
 start_time, @end_time, @duration)
SET end_time = NULLIF(@end_time, ''), duration_minutes = NULLIF(@duration, '');

LOAD DATA LOCAL INFILE 'C:/Users/lervi/Downloads/train-delays/disruptions-2023.csv'
INTO TABLE disruptions CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
(rdt_id, ns_lines, rdt_lines, rdt_lines_id, rdt_station_names, rdt_station_codes,
 cause_nl, cause_en, statistical_cause_nl, statistical_cause_en, cause_group,
 start_time, @end_time, @duration)
SET end_time = NULLIF(@end_time, ''), duration_minutes = NULLIF(@duration, '');

LOAD DATA LOCAL INFILE 'C:/Users/lervi/Downloads/train-delays/disruptions-2024.csv'
INTO TABLE disruptions CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
(rdt_id, ns_lines, rdt_lines, rdt_lines_id, rdt_station_names, rdt_station_codes,
 cause_nl, cause_en, statistical_cause_nl, statistical_cause_en, cause_group,
 start_time, @end_time, @duration)
SET end_time = NULLIF(@end_time, ''), duration_minutes = NULLIF(@duration, '');

LOAD DATA LOCAL INFILE 'C:/Users/lervi/Downloads/train-delays/disruptions-2025.csv'
INTO TABLE disruptions CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
(rdt_id, ns_lines, rdt_lines, rdt_lines_id, rdt_station_names, rdt_station_codes,
 cause_nl, cause_en, statistical_cause_nl, statistical_cause_en, cause_group,
 start_time, @end_time, @duration)
SET end_time = NULLIF(@end_time, ''), duration_minutes = NULLIF(@duration, '');

-- Check: should be 38571 in total
SELECT COUNT(*) AS disruptions FROM disruptions;
