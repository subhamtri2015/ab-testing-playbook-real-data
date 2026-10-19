# Data sources

This repo uses two public experiments and does not claim any affiliation with the original companies or maintainers.

## Cookie Cats
- Source: Kaggle, "Mobile Games A/B Testing - Cookie Cats".
- Downloaded manually into `data/raw/cookie_cats.csv`.
- Rows: 90,189.
- Columns kept: `userid`, `version`, `sum_gamerounds`, `retention_1`, `retention_7`.
- Excluded: none in the final analytic file; all rows were used after validating that the identifiers and metrics were complete.
- Licence note: the Cookie Cats licence is unverified and therefore treated as a public dataset for analysis only.

## Upworthy Research Archive
- Source: Matias, Munger, Le Quere, Ebersole (2021), Scientific Data 8:195, https://doi.org/10.1038/s41597-021-00934-7, data at https://osf.io/jd64p/.
- Download date: 2026-10-19 (the repo uses the archive snapshot under `data/raw/upworthy/`).
- Rows: exploratory archive contains 22,666 rows across 4,873 tests; confirmatory archive contains 105,551 packages across 22,743 tests in the published archive metadata.
- Columns inspected: `clickability_test_id`, `headline`, `impressions`, `clicks`, `created_at`, `updated_at`, and other archive metadata. The advertised randomization imbalance flag was not present in the extracted file in this workspace; the repo documents the actual columns in `scripts/upworthy_columns.md`.
- Kept: rows used for the exploratory and confirmatory analyses in `data/processed`.
- Excluded: holdout and undeployed files are not used in this repo.

The repository is analysed as if I were the PM and does not claim the original firms' decisions or intentions.
