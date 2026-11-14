-- Dutch train disruptions: setup
-- Data: Rijden de Treinen (rijdendetreinen.nl), CC BY 4.0

-- 1. Allow loading a file from your computer (needed once)
SET GLOBAL local_infile = 1;

-- 2. Make the database and the table
CREATE DATABASE IF NOT EXISTS train_delays;
USE train_delays;

DROP TABLE IF EXISTS disruptions;
CREATE TABLE disruptions (
  rdt_id               INT PRIMARY KEY,
  ns_lines             VARCHAR(500),
  rdt_lines            VARCHAR(500),
  rdt_lines_id         VARCHAR(100),
  rdt_station_names    TEXT,
  rdt_station_codes    TEXT,
  cause_nl             VARCHAR(200),
  cause_en             VARCHAR(200),
  statistical_cause_nl VARCHAR(200),
  statistical_cause_en VARCHAR(200),
  cause_group          VARCHAR(100),
  start_time           DATETIME,
  end_time             DATETIME,
  duration_minutes     INT
);

-- 3. Load the 2025 file (empty end times become NULL)
LOAD DATA LOCAL INFILE 'C:/Users/lervi/Downloads/train-delays/disruptions-2025.csv'
INTO TABLE disruptions
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(rdt_id, ns_lines, rdt_lines, rdt_lines_id, rdt_station_names, rdt_station_codes,
 cause_nl, cause_en, statistical_cause_nl, statistical_cause_en, cause_group,
 start_time, @end_time, @duration)
SET end_time = NULLIF(@end_time, ''),
    duration_minutes = NULLIF(@duration, '');

-- 4. Check: should be 6676
SELECT COUNT(*) AS disruptions FROM disruptions;
SELECT * FROM disruptions LIMIT 10;
