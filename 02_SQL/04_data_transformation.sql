USE ab_testing_analysis;

CREATE TABLE IF NOT EXISTS ab_test_clean AS
SELECT
    user_id,
    test_group,
    CASE
        WHEN converted = 'True' THEN 1
        WHEN converted = 'False' THEN 0
    END AS converted,
    total_ads,
    most_ads_day,
    most_ads_hour
FROM ab_test_raw;

-- 02. Validate transformed dataset

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT user_id) AS unique_users,
    SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) AS conversions,
    SUM(CASE WHEN converted = 0 THEN 1 ELSE 0 END) AS non_conversions,
    SUM(CASE WHEN converted IS NULL THEN 1 ELSE 0 END) AS null_conversions,
    SUM(CASE WHEN converted NOT IN (0, 1) THEN 1 ELSE 0 END) AS invalid_conversions
FROM ab_test_clean;