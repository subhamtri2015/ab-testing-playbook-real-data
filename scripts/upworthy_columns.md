# Upworthy archive columns

The exploratory archive in this workspace does not include the maintainers' randomization imbalance flag described in the documentation. The file contains these columns instead:

- Unnamed: 0
- created_at
- updated_at
- clickability_test_id
- excerpt
- headline
- lede
- slug
- eyecatcher_id
- impressions
- clicks
- significance
- first_place
- winner
- share_text
- square
- test_week

The repository therefore uses the available archive metadata and matches on the column family `*test*`, `*impression*`, `*click*`, `*headline*`, and `*created*` instead of a missing `randomization_imbalace_risk` column.
