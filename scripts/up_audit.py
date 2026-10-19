from __future__ import annotations

from pathlib import Path

import pandas as pd
import numpy as np

from stats_utils import srm_test

ROOT = Path(__file__).resolve().parent.parent
EXPLORATORY = ROOT / 'data' / 'raw' / 'upworthy' / 'upworthy-archive-exploratory-packages-03.12.2020.csv'
OUT = ROOT / 'data' / 'processed'
OUT.mkdir(exist_ok=True, parents=True)


def main():
    df = pd.read_csv(EXPLORATORY)
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    df['month'] = df['created_at'].dt.to_period('M').astype(str)

    rows = []
    for test_id, g in df.groupby('clickability_test_id'):
        if g.empty:
            continue
        arm_count = g.shape[0]
        impressions = g['impressions'].tolist()
        clicks = g['clicks'].tolist()
        chi2, p = srm_test(impressions, [1 / arm_count] * arm_count)
        rows.append({
            'test_id': test_id,
            'arms': arm_count,
            'total_impressions': float(g['impressions'].sum()),
            'total_clicks': float(g['clicks'].sum()),
            'srm_chi2': float(chi2),
            'srm_p': float(p),
            'month': g['month'].iloc[0],
        })

    audit = pd.DataFrame(rows)
    audit.to_csv(OUT / 'up_audit.csv', index=False)

    srm_month = (
        audit.assign(flag_05=audit['srm_p'] < 0.05,
                     flag_001=audit['srm_p'] < 0.001)
             .groupby('month', as_index=False)
             .agg(test_count=('test_id', 'count'),
                  share_p_05=('flag_05', 'mean'),
                  share_p_001=('flag_001', 'mean'))
    )
    srm_month.to_csv(OUT / 'up_srm_by_month.csv', index=False)
    print(f'Wrote {len(audit)} audit rows and {len(srm_month)} month rows.')


if __name__ == '__main__':
    main()
