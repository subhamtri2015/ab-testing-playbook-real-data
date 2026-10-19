from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def ensure(path: Path):
    if not path.exists():
        raise FileNotFoundError(path)


def check_cards():
    cards = sorted((ROOT / 'assets' / 'cards').glob('*.svg'))
    assert cards, 'No cards were generated.'
    for card in cards:
        txt = card.read_text(encoding='utf-8')
        assert 'REAL RESULT' in txt or 'DIAGRAM' in txt or 'METHOD' in txt or 'NOT TESTABLE' in txt
        assert 'source' in txt.lower() or 'data' in txt.lower() or 'proof' in txt.lower() or 'card' in txt.lower()


def check_concept_csv():
    csv_path = ROOT / 'docs' / 'concept-outcomes.csv'
    with csv_path.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    assert rows
    assert all(row['evidence_file'] for row in rows)
    counts = {}
    for row in rows:
        counts[row['proof_type']] = counts.get(row['proof_type'], 0) + 1
    assert counts.get('Real result', 0) > 0
    assert counts.get('Method on real inputs', 0) > 0
    assert counts.get('Not testable with these data', 0) > 0


def check_links():
    root = ROOT / 'README.md'
    text = root.read_text(encoding='utf-8')
    for token in ['assets/cards/card-01-decision.svg', '02-cookie-cats/experiment-brief.md', 'docs/concept-coverage.md']:
        assert token in text, token
    for path in [ROOT / '02-cookie-cats' / 'experiment-brief.md', ROOT / 'docs' / 'concept-coverage.md', ROOT / '04-playbook' / 'ab-testing-playbook.md']:
        ensure(path)


def main():
    ensure(ROOT / 'data' / 'processed' / 'cc_summary.csv')
    ensure(ROOT / 'data' / 'processed' / 'cc_tests.csv')
    ensure(ROOT / 'data' / 'processed' / 'sample_size_grid.csv')
    check_cards()
    check_concept_csv()
    check_links()
    print('Consistency checks passed.')


if __name__ == '__main__':
    main()
