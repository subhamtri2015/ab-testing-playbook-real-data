COPY (
  SELECT
    clickability_test_id AS test_id,
    AVG(clicks::DOUBLE / impressions::DOUBLE) AS avg_ctr,
    MIN(impressions) AS min_impressions,
    MAX(impressions) AS max_impressions
  FROM read_csv_auto('data/raw/upworthy/upworthy-archive-exploratory-packages-03.12.2020.csv', header=true)
  GROUP BY clickability_test_id
  ORDER BY test_id
) TO 'data/processed/up_program_sql.csv' (HEADER, DELIMITER ',');
