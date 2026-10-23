USE ab_testing_analysis;

SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN row_index IS NULL THEN 1 ELSE 0 END) AS null_row_index,
    SUM(CASE WHEN user_id IS NULL THEN 1 ELSE 0 END) AS null_user_id,
    SUM(CASE WHEN test_group IS NULL OR TRIM(test_group) = '' THEN 1 ELSE 0 END) AS null_test_group,
    SUM(CASE WHEN converted IS NULL OR TRIM(converted) = '' THEN 1 ELSE 0 END) AS null_converted,
    SUM(CASE WHEN total_ads IS NULL THEN 1 ELSE 0 END) AS null_total_ads,
    SUM(CASE WHEN most_ads_day IS NULL OR TRIM(most_ads_day) = '' THEN 1 ELSE 0 END) AS null_most_ads_day,
    SUM(CASE WHEN most_ads_hour IS NULL THEN 1 ELSE 0 END) AS null_most_ads_hour
FROM ab_test_raw;

-- 02. Validate experiment groups and conversion values

SELECT
    test_group,
    converted,
    COUNT(*) AS total_users
FROM ab_test_raw
GROUP BY
    test_group,
    converted
ORDER BY
    test_group,
    converted;
    
    -- 03. Experiment group sizes and conversion rates

SELECT
    test_group,
    COUNT(*) AS total_users,
    SUM(
        CASE WHEN converted = 'True' THEN 1 ELSE 0 END
    ) AS conversions,
    ROUND(
        100.0 * SUM(
            CASE WHEN converted = 'True' THEN 1 ELSE 0 END
        ) / COUNT(*),
        4
    ) AS conversion_rate_pct
FROM ab_test_raw
GROUP BY test_group
ORDER BY test_group;

-- 04. Experiment group allocation

SELECT
    test_group,
    COUNT(*) AS total_users,
    ROUND(
        100.0 * COUNT(*) /
        (SELECT COUNT(*) FROM ab_test_raw),
        2
    ) AS share_of_users_pct
FROM ab_test_raw
GROUP BY test_group
ORDER BY test_group;

-- 05. Validate numeric ranges

SELECT
    SUM(CASE WHEN total_ads < 0 THEN 1 ELSE 0 END)
        AS negative_ads,

    SUM(CASE WHEN total_ads = 0 THEN 1 ELSE 0 END)
        AS zero_ads,

    SUM(CASE WHEN most_ads_hour NOT BETWEEN 0 AND 23
        THEN 1 ELSE 0 END)
        AS invalid_hours,

    MIN(total_ads) AS min_ads,
    MAX(total_ads) AS max_ads,

    MIN(most_ads_hour) AS min_hour,
    MAX(most_ads_hour) AS max_hour

FROM ab_test_raw;

-- 06. Analyze ad exposure distribution

SELECT
    test_group,
    COUNT(*) AS total_users,
    ROUND(AVG(total_ads), 2) AS avg_ads,
    MIN(total_ads) AS min_ads,
    MAX(total_ads) AS max_ads,
    SUM(CASE WHEN total_ads > 100 THEN 1 ELSE 0 END)
        AS users_over_100_ads,
    SUM(CASE WHEN total_ads > 500 THEN 1 ELSE 0 END)
        AS users_over_500_ads,
    SUM(CASE WHEN total_ads > 1000 THEN 1 ELSE 0 END)
        AS users_over_1000_ads
FROM ab_test_raw
GROUP BY test_group
ORDER BY test_group;

-- 07. Validate day-of-week values

SELECT
    most_ads_day,
    COUNT(*) AS total_users
FROM ab_test_raw
GROUP BY most_ads_day
ORDER BY total_users DESC;

-- 08. Validate original CSV row index

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT row_index) AS unique_row_indices,
    MIN(row_index) AS min_row_index,
    MAX(row_index) AS max_row_index,
    SUM(CASE WHEN row_index < 0 THEN 1 ELSE 0 END)
        AS negative_indices
FROM ab_test_raw;