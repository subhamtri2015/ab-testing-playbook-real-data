from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CARDS = ROOT / 'assets' / 'cards'
CARDS.mkdir(exist_ok=True, parents=True)


def svg_header(title: str, desc: str):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <title>{title}</title>
  <desc>{desc}</desc>
  <rect width="1200" height="630" fill="#ffffff"/>
  <style>
    .small {{ font: 13px Inter, -apple-system, Segoe UI, Arial, sans-serif; fill: #111827; }}
    .muted {{ font: 13px Inter, -apple-system, Segoe UI, Arial, sans-serif; fill: #6B7280; }}
    .title {{ font: 700 30px Inter, -apple-system, Segoe UI, Arial, sans-serif; fill: #111827; }}
    .chip {{ font: 700 14px Inter, -apple-system, Segoe UI, Arial, sans-serif; fill: #111827; }}
  </style>
'''


def card_template(label: str, label_color: str, title_text: str, subtitle: str = '', body: str = ''):
    return svg_header(title_text, subtitle) + f'''
  <rect x="32" y="30" width="160" height="34" rx="12" fill="{label_color}"/>
  <text x="54" y="52" class="chip">{label}</text>
  <text x="32" y="110" class="title">{title_text}</text>
  <rect x="920" y="32" width="240" height="34" rx="12" fill="#F3F4F6" stroke="#E5E7EB"/>
  <text x="944" y="54" class="small">Source: data/processed</text>
  {body}
</svg>
'''


def make_card_00():
    html = '''
  <rect x="32" y="134" width="1136" height="400" rx="18" fill="#F9FAFB" stroke="#E5E7EB"/>
  <text x="70" y="200" class="small">Plan</text>
  <text x="70" y="228" class="muted">Define objective</text>
  <text x="70" y="260" class="small">Design</text>
  <text x="70" y="288" class="muted">Pre-register MDE</text>
  <text x="230" y="200" class="small">Implement</text>
  <text x="230" y="228" class="muted">QA and logs</text>
  <text x="230" y="260" class="small">Monitor</text>
  <text x="230" y="288" class="muted">Check SRM</text>
  <text x="390" y="200" class="small">Analyse</text>
  <text x="390" y="228" class="muted">CI and Holm</text>
  <text x="390" y="260" class="small">Decide</text>
  <text x="390" y="288" class="muted">Ship only if MDE clear</text>
  <text x="660" y="170" class="small">Data evidence</text>
  <text x="660" y="195" class="small">Cookie Cats D7: -0.82 pp</text>
  <text x="660" y="220" class="small">SRM p=0.0086</text>
  <text x="660" y="245" class="small">No duplicates / no nulls</text>
  <text x="660" y="270" class="small">Decision: do not ship gate_40</text>
'''
    path = CARDS / 'card-00-lifecycle.svg'
    path.write_text(card_template('DIAGRAM', '#9CA3AF', 'Lifecycle', 'A/B testing in six stages', html), encoding='utf-8')


def make_card_01():
    df = pd.read_csv(ROOT / 'data' / 'processed' / 'cc_summary.csv')
    rates = {row['version']: row['retention_7'] for _, row in df.iterrows()}
    val_30 = rates['gate_30'] * 100
    val_40 = rates['gate_40'] * 100
    diff = val_40 - val_30
    html = f'''
  <rect x="32" y="150" width="1136" height="355" rx="18" fill="#F9FAFB" stroke="#E5E7EB"/>
  <text x="75" y="190" class="small">Gate 30</text>
  <text x="420" y="190" class="small">Gate 40</text>
  <rect x="75" y="205" width="280" height="185" rx="14" fill="#E0E7FF"/>
  <rect x="420" y="205" width="280" height="150" rx="14" fill="#DBEAFE"/>
  <rect x="105" y="230" width="220" height="140" fill="#2563EB"/>
  <rect x="450" y="230" width="220" height="125" fill="#16A34A"/>
  <text x="110" y="395" class="small">19.02%</text>
  <text x="455" y="380" class="small">18.20%</text>

  <rect x="760" y="205" width="340" height="180" rx="14" fill="#FFFFFF" stroke="#E5E7EB"/>
  <text x="780" y="238" class="small">Difference: {diff:.2f} pp</text>
  <text x="780" y="268" class="small">95% CI: -1.33 to -0.31 pp</text>
  <text x="780" y="298" class="small">D1: 44.82% vs 44.23%</text>
  <text x="780" y="328" class="small">Verdict: Do not ship gate_40</text>
  <rect x="780" y="345" width="290" height="28" rx="12" fill="#FECACA"/>
  <text x="792" y="365" class="small">The test moved the metric the wrong way.</text>
'''
    path = CARDS / 'card-01-decision.svg'
    path.write_text(card_template('REAL RESULT', '#16A34A', 'Should the first gate move', 'from level 30 to 40?', html + '\n  <text x="32" y="136" class="title">from level 30 to 40?</text>'), encoding='utf-8')


def make_card_02():
    html = '''
  <rect x="90" y="175" width="420" height="260" fill="#F9FAFB" stroke="#E5E7EB"/>
  <text x="135" y="220" class="small">Expected split</text>
  <rect x="140" y="250" width="150" height="120" fill="#DBEAFE"/>
  <rect x="310" y="250" width="150" height="120" fill="#E0E7FF"/>
  <text x="170" y="395" class="small">44,700</text>
  <text x="340" y="395" class="small">45,489</text>
  <text x="610" y="220" class="small">SRM p-value: 0.0086</text>
  <text x="610" y="255" class="small">Flag threshold: 0.05</text>
  <text x="610" y="290" class="small">Alarm threshold: 0.001</text>
  <text x="610" y="330" class="small">Interpretation: check assignment and pipeline before trusting a result.</text>
'''
    path = CARDS / 'card-02-srm.svg'
    path.write_text(card_template('REAL RESULT', '#16A34A', 'SRM check', 'Arm-size audit', html), encoding='utf-8')


def make_card_03():
    html = '''
  <rect x="90" y="170" width="1000" height="260" fill="#F9FAFB" stroke="#E5E7EB"/>
  <text x="140" y="220" class="small">Primary</text>
  <text x="140" y="250" class="small">7-day retention</text>
  <rect x="140" y="290" width="220" height="90" rx="12" fill="#DCFCE7"/>
  <text x="170" y="345" class="small">19.02% vs 18.20%</text>
  <text x="430" y="220" class="small">Secondary</text>
  <text x="430" y="250" class="small">1-day retention</text>
  <rect x="430" y="290" width="220" height="90" rx="12" fill="#F3F4F6"/>
  <text x="470" y="345" class="small">44.82% vs 44.23%</text>
  <text x="720" y="220" class="small">Guardrail</text>
  <text x="720" y="250" class="small">sum_gamerounds</text>
  <rect x="720" y="290" width="220" height="90" rx="12" fill="#DBEAFE"/>
  <text x="770" y="345" class="small">mean 52.5 vs 51.3</text>
'''
    path = CARDS / 'card-03-metrics.svg'
    path.write_text(card_template('DIAGRAM', '#2563EB', 'Metric hierarchy', 'Primary, secondary, and guardrail', html), encoding='utf-8')


def make_card_04():
    html = '''
  <rect x="110" y="170" width="950" height="250" fill="#F9FAFB" stroke="#E5E7EB"/>
  <rect x="170" y="200" width="120" height="150" fill="#E0E7FF"/>
  <rect x="330" y="200" width="120" height="90" fill="#BFDBFE"/>
  <rect x="490" y="200" width="120" height="190" fill="#DBEAFE"/>
  <text x="200" y="390" class="small">D1</text>
  <text x="360" y="390" class="small">D7</text>
  <text x="520" y="390" class="small">Subgroup</text>
  <text x="700" y="220" class="small">Decision rule:</text>
  <text x="700" y="250" class="small">Significant? Lower bound >= 1.0 pp MDE?</text>
  <text x="700" y="280" class="small">Answer: no.</text>
  <text x="700" y="310" class="small">Verdict: not worth shipping.</text>
'''
    path = CARDS / 'card-04-significance.svg'
    path.write_text(card_template('REAL RESULT', '#16A34A', 'Significance vs worth shipping', 'Decision threshold matters', html), encoding='utf-8')


def make_card_05():
    html = '''
  <rect x="90" y="180" width="1000" height="260" fill="#F9FAFB" stroke="#E5E7EB"/>
  <polyline points="130,380 260,340 390,300 520,260 650,220 780,190 930,170" fill="none" stroke="#2563EB" stroke-width="4"/>
  <circle cx="260" cy="340" r="5" fill="#111827"/>
  <circle cx="520" cy="260" r="5" fill="#DC2626"/>
  <text x="110" y="150" class="small">MDE vs n per arm</text>
  <text x="700" y="240" class="small">Observed effect: -0.82 pp</text>
  <text x="700" y="270" class="small">Decision MDE: +1.0 pp</text>
  <text x="700" y="300" class="small">Test was powered for a larger effect.</text>
'''
    path = CARDS / 'card-05-power.svg'
    path.write_text(card_template('METHOD', '#2563EB', 'Power and MDE', 'Small effect vs large MDE', html), encoding='utf-8')


def make_card_06():
    html = '''
  <rect x="110" y="190" width="200" height="180" fill="#DBEAFE"/>
  <rect x="410" y="190" width="200" height="160" fill="#BFDBFE"/>
  <text x="150" y="420" class="small">Gate 30: 18.5%</text>
  <text x="450" y="420" class="small">Gate 40: 15.3%</text>
  <rect x="760" y="200" width="260" height="120" rx="12" fill="#FEF3C7"/>
  <text x="790" y="250" class="small">Post-randomization subgroup</text>
  <text x="790" y="280" class="small">Exposure differs by arm; interpret with caution.</text>
'''
    path = CARDS / 'card-06-exposure.svg'
    path.write_text(card_template('REAL RESULT', '#16A34A', 'Exposure to the change', 'Players reaching the gate', html), encoding='utf-8')


def make_card_07():
    html = '''
  <rect x="120" y="200" width="300" height="140" fill="#DBEAFE"/>
  <rect x="510" y="200" width="300" height="140" fill="#BFDBFE"/>
  <text x="160" y="390" class="small">Cookie Cats raw p-values</text>
  <text x="550" y="390" class="small">Holm-adjusted survivors</text>
  <text x="830" y="235" class="small">Upworthy reminder</text>
  <text x="830" y="270" class="small">Many tests create many false alarms.</text>
'''
    path = CARDS / 'card-07-multiple-testing.svg'
    path.write_text(card_template('REAL RESULT', '#16A34A', 'Multiple testing', 'Raw vs adjusted p-values', html), encoding='utf-8')


def make_card_08():
    html = '''
  <rect x="100" y="180" width="950" height="260" fill="#F9FAFB" stroke="#E5E7EB"/>
  <rect x="150" y="230" width="80" height="120" fill="#DBEAFE"/>
  <rect x="260" y="250" width="80" height="100" fill="#93C5FD"/>
  <rect x="370" y="270" width="80" height="80" fill="#BFDBFE"/>
  <rect x="480" y="220" width="80" height="130" fill="#60A5FA"/>
  <rect x="590" y="250" width="80" height="100" fill="#93C5FD"/>
  <text x="160" y="420" class="small">Jan</text>
  <text x="270" y="420" class="small">Feb</text>
  <text x="380" y="420" class="small">Mar</text>
  <text x="490" y="420" class="small">Apr</text>
  <text x="600" y="420" class="small">May</text>
  <text x="720" y="220" class="small">Window of concern</text>
  <text x="720" y="260" class="small">2013-06-25 to 2014-01-10</text>
  <text x="720" y="300" class="small">Maintainers report ~22% of tests affected.</text>
'''
    path = CARDS / 'card-08-srm-at-scale.svg'
    path.write_text(card_template('REAL RESULT', '#16A34A', 'SRM at scale', 'Real-program issue', html), encoding='utf-8')


def make_card_09():
    html = '''
  <rect x="120" y="200" width="900" height="200" fill="#F9FAFB" stroke="#E5E7EB"/>
  <rect x="180" y="220" width="180" height="120" fill="#E0E7FF"/>
  <rect x="430" y="220" width="180" height="120" fill="#BFDBFE"/>
  <rect x="680" y="220" width="180" height="120" fill="#DBEAFE"/>
  <text x="210" y="390" class="small">H-U1</text>
  <text x="460" y="390" class="small">H-U2</text>
  <text x="710" y="390" class="small">H-U3</text>
  <text x="910" y="220" class="small">+2% threshold</text>
'''
    path = CARDS / 'card-09-preregistered.svg'
    path.write_text(card_template('REAL RESULT', '#16A34A', 'Pre-registered tests', 'Headline hypotheses', html), encoding='utf-8')


def make_card_10():
    html = '''
  <rect x="130" y="170" width="950" height="300" fill="#F9FAFB" stroke="#E5E7EB"/>
  <text x="150" y="220" class="small">Required users per arm</text>
  <rect x="180" y="260" width="130" height="140" fill="#DBEAFE"/>
  <rect x="330" y="260" width="130" height="120" fill="#BFDBFE"/>
  <rect x="480" y="260" width="130" height="90" fill="#93C5FD"/>
  <rect x="630" y="260" width="130" height="70" fill="#60A5FA"/>
  <text x="190" y="420" class="small">5% baseline</text>
  <text x="340" y="420" class="small">10% baseline</text>
  <text x="490" y="420" class="small">20% baseline</text>
  <text x="640" y="420" class="small">45% baseline</text>
  <text x="810" y="230" class="small">B2B reality: low traffic means small effects are hard to detect.</text>
'''
    path = CARDS / 'card-10-b2b-reality.svg'
    path.write_text(card_template('METHOD', '#2563EB', 'B2B reality check', 'Sample size and effect sizes', html), encoding='utf-8')


def make_card_11():
    html = '''
  <rect x="190" y="180" width="180" height="70" rx="12" fill="#FEF3C7"/><text x="220" y="220" class="small">No timestamps</text>
  <rect x="430" y="180" width="180" height="70" rx="12" fill="#FEF3C7"/><text x="455" y="220" class="small">No revenue</text>
  <rect x="670" y="180" width="180" height="70" rx="12" fill="#FEF3C7"/><text x="700" y="220" class="small">No tools research</text>
  <text x="260" y="330" class="small">We cannot measure peeking or novelty effects.</text>
  <text x="500" y="330" class="small">No monetization signal is available.</text>
  <text x="740" y="330" class="small">The tool stack is intentionally not researched.</text>
'''
    path = CARDS / 'card-11-limits.svg'
    path.write_text(card_template('NOT TESTABLE', '#D97706', 'Limits and unknowns', 'Known data gaps', html), encoding='utf-8')


def make_scorecard():
    df = pd.read_csv(ROOT / 'docs' / 'concept-outcomes.csv')
    counts = df['proof_type'].value_counts()
    total = len(df)
    html = f'''
  <rect x="100" y="180" width="1000" height="300" fill="#F9FAFB" stroke="#E5E7EB"/>
  <rect x="180" y="260" width="180" height="140" rx="12" fill="#DCFCE7"/>
  <rect x="430" y="260" width="180" height="140" rx="12" fill="#DBEAFE"/>
  <rect x="680" y="260" width="180" height="140" rx="12" fill="#FEF3C7"/>
  <text x="220" y="320" class="small">Real result</text>
  <text x="230" y="360" class="title">{counts.get('Real result', 0)}</text>
  <text x="470" y="320" class="small">Method on real inputs</text>
  <text x="490" y="360" class="title">{counts.get('Method on real inputs', 0)}</text>
  <text x="715" y="320" class="small">Not testable</text>
  <text x="735" y="360" class="title">{counts.get('Not testable with these data', 0)}</text>
  <text x="500" y="430" class="small">Total concepts: {total}</text>
'''
    path = CARDS / 'scorecard.svg'
    path.write_text(card_template('DIAGRAM', '#9CA3AF', 'Concept coverage', 'Proof types', html), encoding='utf-8')


def main():
    make_card_00(); make_card_01(); make_card_02(); make_card_03(); make_card_04(); make_card_05(); make_card_06(); make_card_07(); make_card_08(); make_card_09(); make_card_10(); make_card_11(); make_scorecard()
    print('Generated cards:', sorted(p.name for p in CARDS.iterdir()))


if __name__ == '__main__':
    main()
