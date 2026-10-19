COPY (
  WITH raw AS (
    SELECT *
    FROM read_csv_auto('data/raw/cookie_cats.csv', header=true)
  )
  SELECT
    'duplicates' AS metric,
    COUNT(*) - COUNT(DISTINCT userid) AS value
  FROM raw
  UNION ALL
  SELECT 'nulls', COUNT(*) FILTER (WHERE userid IS NULL OR version IS NULL OR sum_gamerounds IS NULL OR retention_1 IS NULL OR retention_7 IS NULL)
  FROM raw
  UNION ALL
  SELECT 'zero_round_share', AVG(CASE WHEN sum_gamerounds = 0 THEN 1.0 ELSE 0.0 END)
  FROM raw
  UNION ALL
  SELECT 'max_rounds', MAX(sum_gamerounds)
  FROM raw
) TO 'data/processed/cc_quality.csv' (HEADER, DELIMITER ',');
