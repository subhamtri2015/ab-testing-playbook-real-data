from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from stats_utils import benjamini_hochberg, two_proportion_z_test

ROOT = Path(__file__).resolve().parent.parent
EXPLORATORY = ROOT / 'data' / 'raw' / 'upworthy' / 'upworthy-archive-exploratory-packages-03.12.2020.csv'
OUT = ROOT / 'data' / 'processed'
OUT.mkdir(exist_ok=True, parents=True)


def compute_test_stats(df):
    rows = []
    for test_id, g in df.groupby('clickability_test_id'):
        if len(g) != 2:
            continue
        a, b = g.iloc[0], g.iloc[1]
        ctr_a = a['clicks'] / a['impressions']
        ctr_b = b['clicks'] / b['impressions']
        if min(a['impressions'], b['impressions']) < 1000:
            continue
        result = two_proportion_z_test(a['clicks'], a['impressions'], b['clicks'], b['impressions'])
        rows.append({
            'test_id': test_id,
            'ctr_a': ctr_a,
            'ctr_b': ctr_b,
            'abs_diff': abs(ctr_b - ctr_a),
            'rel_diff': abs(ctr_b - ctr_a) / max(ctr_a, 1e-9),
            'p_value': result['p_value'],
            'ci_low': result['ci_low'],
            'ci_high': result['ci_high'],
            'baseline_ctr': (a['clicks'] + b['clicks']) / (a['impressions'] + b['impressions']),
        })
    return pd.DataFrame(rows)


def main():
    df = pd.read_csv(EXPLORATORY)
    df = df[['clickability_test_id', 'headline', 'impressions', 'clicks', 'created_at']].copy()
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    rows = compute_test_stats(df)

    # baseline and MDE summary
    baselines = rows[['baseline_ctr', 'abs_diff']].copy()
    baselines['n_per_arm'] = ((df['impressions'].sum() / len(df)) if len(df) else 0)
    baselines.to_csv(OUT / 'up_baselines.csv', index=False)

    mde = rows['rel_diff'].describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]).to_frame('relative_mde')
    mde.to_csv(OUT / 'up_mde.csv', index=False)

    rows['raw_sig_05'] = rows['p_value'] < 0.05
    rows['bh_adj'] = benjamini_hochberg(rows['p_value'].tolist())
    rows['bh_sig_05'] = np.array(rows['bh_adj']) < 0.05
    rows[['test_id', 'p_value', 'raw_sig_05', 'bh_adj', 'bh_sig_05']].to_csv(OUT / 'up_pvalues.csv', index=False)

    multiplicity = pd.DataFrame({
        'tests_total': [len(rows)],
        'raw_significant_005': [int(rows['raw_sig_05'].sum())],
        'expected_by_chance': [len(rows) * 0.05],
        'survivors_bh_5pct': [int(rows['bh_sig_05'].sum())],
    })
    multiplicity.to_csv(OUT / 'up_multiplicity.csv', index=False)

    rows['effect_abs'] = rows['abs_diff']
    rows['effect_rel'] = rows['rel_diff']
    rows[['test_id', 'abs_diff', 'rel_diff']].rename(columns={'abs_diff': 'abs_ctr_diff', 'rel_diff': 'relative_ctr_diff'}).to_csv(OUT / 'up_effects.csv', index=False)

    print(f'Qualified tests: {len(rows)}')


if __name__ == '__main__':
    main()
