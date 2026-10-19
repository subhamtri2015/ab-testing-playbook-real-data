import pandas as pd



def test_cookie_cats_reference_figures():
    df = pd.read_csv('data/cookie_cats.csv')
    assert len(df) == 90189
    c = df['version'].value_counts()
    assert c['gate_30'] == 44700
    assert c['gate_40'] == 45489
    d1 = df.groupby('version')['retention_1'].mean()
    d7 = df.groupby('version')['retention_7'].mean()
    assert abs(d1['gate_30'] - 0.44818) < 0.01
    assert abs(d1['gate_40'] - 0.44228) < 0.01
    assert abs(d7['gate_30'] - 0.19020) < 0.01
    assert abs(d7['gate_40'] - 0.18200) < 0.01
