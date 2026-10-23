CREATE DATABASE IF NOT EXISTS ab_testing_analysis;

USE ab_testing_analysis;

USE ab_testing_analysis;

CREATE TABLE IF NOT EXISTS ab_test_raw (
    row_index INT,
    user_id BIGINT,
    test_group VARCHAR(20),
    converted VARCHAR(10),
    total_ads INT,
    most_ads_day VARCHAR(20),
    most_ads_hour INT
);

USE ab_testing_analysis;

LOAD DATA LOCAL INFILE 'C:/Users/votsi/OneDrive/Desktop/Projects Folder/AB_Testing_Conversion_Analysis/01_Data/marketing_AB.csv'
INTO TABLE ab_test_raw
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@row_index, @user_id, @test_group, @converted,
 @total_ads, @most_ads_day, @most_ads_hour)
SET
    row_index = NULLIF(TRIM(@row_index), ''),
    user_id = NULLIF(TRIM(@user_id), ''),
    test_group = TRIM(@test_group),
    converted = TRIM(@converted),
    total_ads = NULLIF(TRIM(@total_ads), ''),
    most_ads_day = TRIM(@most_ads_day),
    most_ads_hour = NULLIF(TRIM(TRAILING '\r' FROM @most_ads_hour), '');
    
    SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT user_id) AS unique_users,
    MIN(total_ads) AS min_ads,
    MAX(total_ads) AS max_ads
FROM ab_testing_analysis.ab_test_raw;