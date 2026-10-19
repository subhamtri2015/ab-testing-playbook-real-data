from __future__ import annotations

import argparse
import hashlib
from datetime import datetime
from pathlib import Path

import pandas as pd
import numpy as np

from stats_utils import benjamini_hochberg, random_effects_meta_analysis, two_proportion_z_test

ROOT = Path(__file__).resolve().parent.parent
CONFIRM = ROOT / 'data' / 'raw' / 'upworthy' / 'upworthy-archive-confirmatory-packages-03.12.2020.csv'
PREREG = ROOT / '03-upworthy-program' / 'prereg-confirmatory.md'
RUNLOG = ROOT / '03-upworthy-program' / 'RUNLOG.md'
OUT = ROOT / 'data' / 'processed' / 'up_confirmatory.csv'


def find_feature(headline, feature):
    if feature == 'question':
        return '?' in str(headline)
    if feature == 'digit':
        return any(ch.isdigit() for ch in str(headline))
    if feature == 'long':
        return len(str(headline)) > 40
    return False


def build_rows(df):
    rows = []
    for test_id, g in df.groupby('clickability_test_id'):
        if len(g) != 2:
            continue
        if g['impressions'].min() < 1000:
            continue
        left, right = g.iloc[0], g.iloc[1]
        a_ctr = left['clicks'] / left['impressions']
        b_ctr = right['clicks'] / right['impressions']
        rel = (b_ctr - a_ctr) / max(a_ctr, 1e-9)
        zres = two_proportion_z_test(left['clicks'], left['impressions'], right['clicks'], right['impressions'])
        rows.append({
            'test_id': test_id,
            'headline_a': left['headline'],
            'headline_b': right['headline'],
            'ctr_a': a_ctr,
            'ctr_b': b_ctr,
            'relative_lift': rel,
            'raw_p': zres['p_value'],
        })
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--confirm', action='store_true')
    args = parser.parse_args()
    if not args.confirm:
        raise SystemExit('Use --confirm to run the confirmatory analysis once.')
    if not PREREG.exists():
        raise SystemExit('Missing preregistration file 03-upworthy-program/prereg-confirmatory.md')

    df = pd.read_csv(CONFIRM)
    rows = build_rows(df)
    if rows.empty:
        rows = pd.DataFrame(columns=['test_id', 'hypothesis', 'pooled_lift', 'ci_low', 'ci_high', 'tau_squared', 'raw_p', 'holm_p', 'verdict'])
        rows.to_csv(OUT, index=False)
        with RUNLOG.open('a', encoding='utf-8') as f:
            f.write(f"\n- {datetime.utcnow().isoformat()}Z — confirmatory run: no qualifying tests; prereg hash {hashlib.sha256(PREREG.read_bytes()).hexdigest()[:12]}\n")
        return

    hypotheses = [
        ('H-U1', 'question'),
        ('H-U2', 'digit'),
        ('H-U3', 'long'),
    ]
    results = []
    for name, feature in hypotheses:
        subset = rows.copy()
        subset['feature_a'] = subset['headline_a'].apply(lambda h: find_feature(h, feature))
        subset['feature_b'] = subset['headline_b'].apply(lambda h: find_feature(h, feature))
        subset = subset[(subset['feature_a'] ^ subset['feature_b'])]
        if subset.empty:
            results.append({
                'hypothesis': name,
                'tests': 0,
                'pooled_lift': np.nan,
                'ci_low': np.nan,
                'ci_high': np.nan,
                'tau_squared': np.nan,
                'raw_p': np.nan,
                'holm_p': np.nan,
                'verdict': 'No qualifying tests',
            })
            continue
        effect_sizes = []
        variances = []
        for _, r in subset.iterrows():
            a = r['ctr_a']
            b = r['ctr_b']
            diff = np.log((b + 1e-9) / (a + 1e-9))
            var = 1 / max(r['ctr_a'] * 1, 1e-9) - 1 / max(r['ctr_a'] * 1, 1e-9)
            effect_sizes.append(diff)
            variances.append(1e-4)
        pooled, se, ci_low, ci_high, tau2 = random_effects_meta_analysis(effect_sizes, variances)
        raw_p = 2 * (1 - __import__('scipy.stats').stats.norm.cdf(abs(pooled / se))) if se and not np.isnan(se) else np.nan
        results.append({
            'hypothesis': name,
            'tests': int(len(subset)),
            'pooled_lift': pooled,
            'ci_low': ci_low,
            'ci_high': ci_high,
            'tau_squared': tau2,
            'raw_p': raw_p,
            'holm_p': np.nan,
            'verdict': 'No detectable effect' if pd.isna(raw_p) or raw_p > 0.05 else 'Signal',
        })

    raw_ps = [r['raw_p'] for r in results if pd.notna(r['raw_p'])]
    adj = benjamini_hochberg(raw_ps) if raw_ps else []
    for idx, r in enumerate(results):
        if pd.notna(r['raw_p']):
            r['holm_p'] = adj.pop(0)
            r['verdict'] = 'No detectable effect' if r['holm_p'] > 0.05 else 'Signal'
    output = pd.DataFrame(results)
    output.to_csv(OUT, index=False)

    with RUNLOG.open('a', encoding='utf-8') as f:
        f.write(f"\n- {datetime.utcnow().isoformat()}Z — confirmatory run on raw archive; prereg hash {hashlib.sha256(PREREG.read_bytes()).hexdigest()[:12]}; qualifying tests {', '.join(str(x['tests']) for x in results)}\n")

    print(output.to_string(index=False))


if __name__ == '__main__':
    main()
