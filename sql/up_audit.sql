COPY (
  SELECT
    clickability_test_id AS test_id,
    COUNT(*) AS arms,
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    MIN(created_at) AS first_created,
    MAX(created_at) AS last_created
  FROM read_csv_auto('data/raw/upworthy/upworthy-archive-exploratory-packages-03.12.2020.csv', header=true)
  GROUP BY clickability_test_id
  ORDER BY test_id
) TO 'data/processed/up_audit_sql.csv' (HEADER, DELIMITER ',');
