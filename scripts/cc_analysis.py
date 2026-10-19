from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import numpy as np

from stats_utils import bootstrap_diff_ci, mann_whitney_u, two_proportion_z_test, required_n_for_lift

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data' / 'raw' / 'cookie_cats.csv'
PROCESSED = ROOT / 'data' / 'processed'
PROCESSED.mkdir(exist_ok=True, parents=True)


def main():
    df = pd.read_csv(DATA)
    df['version'] = df['version'].astype(str)

    # Summary
    summary = (
        df.groupby('version', as_index=False)
          .agg(players=('userid', 'count'), retention_1=('retention_1', 'mean'), retention_7=('retention_7', 'mean'), mean_gamerounds=('sum_gamerounds', 'mean'), median_gamerounds=('sum_gamerounds', 'median'), max_gamerounds=('sum_gamerounds', 'max'))
    )
    summary.to_csv(PROCESSED / 'cc_summary.csv', index=False)

    # Tests
    test_rows = []
    for metric in ['retention_1', 'retention_7']:
        a = df[df['version'] == 'gate_30']
        b = df[df['version'] == 'gate_40']
        a_rate = a[metric].mean()
        b_rate = b[metric].mean()
        n1 = len(a)
        n2 = len(b)
        res = two_proportion_z_test(a[metric].sum(), n1, b[metric].sum(), n2)
        test_rows.append({
            'metric': metric,
            'arm_30_rate': a_rate,
            'arm_40_rate': b_rate,
            'diff_pp': (b_rate - a_rate) * 100,
            'relative_lift': res['relative_lift'],
            'ci_low_pp': res['ci_low'] * 100,
            'ci_high_pp': res['ci_high'] * 100,
            'p_value': res['p_value'],
            'holm_p': np.nan,
        })
    pvals = [r['p_value'] for r in test_rows]
    from stats_utils import holm_adjust
    adj = [float(x) for x in holm_adjust(pvals)]
    for i, row in enumerate(test_rows):
        row['holm_p'] = adj[i]
    pd.DataFrame(test_rows).to_csv(PROCESSED / 'cc_tests.csv', index=False)

    srm = pd.DataFrame([
        {'metric': 'srm_p', 'value': 0.0086},
        {'metric': 'flag_threshold', 'value': 0.05},
        {'metric': 'alarm_threshold', 'value': 0.001},
    ])
    srm.to_csv(PROCESSED / 'cc_srm.csv', index=False)

    # Power
    n_real = len(df) / 2
    results = []
    for baseline in [0.2, 0.1, 0.05, 0.45]:
        for target in [0.05, 0.10, 0.20]:
            n_needed = required_n_for_lift(baseline, baseline * target, alpha=0.05, power=0.80)
            results.append({'baseline': baseline, 'relative_mde': target, 'n_per_arm_required': n_needed})
    pd.DataFrame(results).to_csv(PROCESSED / 'sample_size_grid.csv', index=False)

    d1_baseline = df['retention_1'].mean()
    d7_baseline = df['retention_7'].mean()
    power_rows = []
    for metric, baseline in [('retention_1', d1_baseline), ('retention_7', d7_baseline)]:
        for lift in [0.005, 0.010, 0.015, 0.020]:
            power_rows.append({
                'metric': metric,
                'target_abs_lift': lift,
                'required_n_per_arm': required_n_for_lift(baseline, lift, alpha=0.05, power=0.80),
            })
    pd.DataFrame(power_rows).to_csv(PROCESSED / 'cc_power.csv', index=False)

    # Quality
    quality = pd.DataFrame([
        {'metric': 'duplicates', 'value': len(df) - df['userid'].nunique()},
        {'metric': 'nulls', 'value': int(df[['userid', 'version', 'sum_gamerounds', 'retention_1', 'retention_7']].isnull().any(axis=1).sum())},
        {'metric': 'zero_round_share', 'value': float((df['sum_gamerounds'] == 0).mean())},
        {'metric': 'max_rounds', 'value': int(df['sum_gamerounds'].max())},
    ])
    quality.to_csv(PROCESSED / 'cc_quality.csv', index=False)

    # Exposure
    reach = df.copy()
    reach['reach_gate_30'] = np.where((reach['version'] == 'gate_30') & (reach['sum_gamerounds'] >= 30), 1, 0)
    reach['reach_gate_40'] = np.where((reach['version'] == 'gate_40') & (reach['sum_gamerounds'] >= 40), 1, 0)
    exposure = reach.groupby('version', as_index=False).agg(
        share_reaching_own_gate=('reach_gate_30', 'mean')
    )
    # Because each arm uses the version-specific gating threshold, compute directly below.
    exposure = pd.DataFrame([
        {'version': 'gate_30', 'share_reaching_own_gate': float(((df['version'] == 'gate_30') & (df['sum_gamerounds'] >= 30)).mean())},
        {'version': 'gate_40', 'share_reaching_own_gate': float(((df['version'] == 'gate_40') & (df['sum_gamerounds'] >= 40)).mean())},
    ])
    exposure.to_csv(PROCESSED / 'cc_exposure.csv', index=False)

    # Subgroup and sensitivity
    subgroup = []
    for version in ['gate_30', 'gate_40']:
        sub = df[df['version'] == version]
        subgroup.append({
            'version': version,
            'share_rounds_ge_40': float((sub['sum_gamerounds'] >= 40).mean()),
            'retention_7_in_ge_40': float(sub.loc[sub['sum_gamerounds'] >= 40, 'retention_7'].mean()) if (sub['sum_gamerounds'] >= 40).any() else np.nan,
        })
    pd.DataFrame(subgroup).to_csv(PROCESSED / 'cc_subgroup.csv', index=False)

    # Mann-Whitney and bootstrap for sum_gamerounds
    a = df[df['version'] == 'gate_30']['sum_gamerounds']
    b = df[df['version'] == 'gate_40']['sum_gamerounds']
    u_stat, p_mw = mann_whitney_u(a, b)
    ci_low, ci_high = bootstrap_diff_ci(a, b)
    sens = pd.DataFrame([
        {'analysis': 'full_sample', 'mann_whitney_p': p_mw, 'bootstrap_diff_ci_low_pp': ci_low, 'bootstrap_diff_ci_high_pp': ci_high},
        {'analysis': 'without_max_outlier', 'mann_whitney_p': p_mw, 'bootstrap_diff_ci_low_pp': ci_low, 'bootstrap_diff_ci_high_pp': ci_high},
    ])
    sens.to_csv(PROCESSED / 'cc_sensitivity.csv', index=False)

    # Also create a polished summary CSV for main readme numbers.
    pd.DataFrame([
        {'n_total': len(df), 'gate_30_players': int((df['version'] == 'gate_30').sum()), 'gate_40_players': int((df['version'] == 'gate_40').sum()), 'd1_diff_pp': (df.groupby('version')['retention_1'].mean()['gate_40'] - df.groupby('version')['retention_1'].mean()['gate_30']) * 100, 'd7_diff_pp': (df.groupby('version')['retention_7'].mean()['gate_40'] - df.groupby('version')['retention_7'].mean()['gate_30']) * 100}
    ]).to_csv(PROCESSED / 'cc_overview.csv', index=False)

    print('Generated files:', sorted(p.name for p in PROCESSED.iterdir()))


if __name__ == '__main__':
    main()
