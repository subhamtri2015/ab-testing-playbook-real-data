COPY (
  SELECT version, COUNT(*) AS players
  FROM read_csv_auto('data/raw/cookie_cats.csv', header=true)
  GROUP BY version
  ORDER BY version
) TO 'data/processed/cc_srm.csv' (HEADER, DELIMITER ',');
