COPY (
  SELECT
    version,
    COUNT(*) AS players,
    AVG(retention_1::DOUBLE) AS retention_1,
    AVG(retention_7::DOUBLE) AS retention_7,
    AVG(sum_gamerounds) AS mean_gamerounds,
    MEDIAN(sum_gamerounds) AS median_gamerounds,
    MAX(sum_gamerounds) AS max_gamerounds
  FROM read_csv_auto('data/raw/cookie_cats.csv', header=true)
  GROUP BY version
  ORDER BY version
) TO 'data/processed/cc_summary.csv' (HEADER, DELIMITER ',');
