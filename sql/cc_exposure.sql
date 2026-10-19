COPY (
  WITH raw AS (
    SELECT *
    FROM read_csv_auto('data/raw/cookie_cats.csv', header=true)
  )
  SELECT
    version,
    AVG(CASE WHEN version = 'gate_30' AND sum_gamerounds >= 30 THEN 1.0 ELSE 0.0 END) AS reach_gate_30,
    AVG(CASE WHEN version = 'gate_40' AND sum_gamerounds >= 40 THEN 1.0 ELSE 0.0 END) AS reach_gate_40
  FROM raw
  GROUP BY version
  ORDER BY version
) TO 'data/processed/cc_exposure.csv' (HEADER, DELIMITER ',');
