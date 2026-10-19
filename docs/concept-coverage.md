# Concept coverage

| ID | Concept | Type | Outcome | Evidence |
|---|---|---|---|---|
| c1 | Definition and origin in randomized trials | Real result | Randomized allocation is the design that supports causal comparison. | [01-research/data-sources.md](../01-research/data-sources.md) |
| c2 | Control vs treatment | Real result | gate_30 is the control and gate_40 is the treatment. | [data/processed/cc_summary.csv](../data/processed/cc_summary.csv) |
| c3 | Primary metric / KPI | Real result | 7-day retention is 19.02% vs 18.20%. | [data/processed/cc_tests.csv](../data/processed/cc_tests.csv) |
| c4 | CTR vs click-through probability | Method on real inputs | CTR is a probability-like rate built from impressions and clicks. | [data/processed/up_baselines.csv](../data/processed/up_baselines.csv) |
| c5 | H0 / H1 | Real result | Null is no difference; alternative is any difference. | [01-research/prereg.md](../01-research/prereg.md) |
| c6 | Alpha | Method on real inputs | alpha = 0.05 two-sided. | [01-research/prereg.md](../01-research/prereg.md) |
| c7 | Beta | Method on real inputs | power = 0.80, so beta = 0.20. | [01-research/prereg.md](../01-research/prereg.md) |
| c8 | Power | Real result | The experiment is sized to deliver 80% power. | [data/processed/cc_power.csv](../data/processed/cc_power.csv) |
| c9 | MDE | Real result | Decision MDE is a 1.0 pp absolute lift on D7 retention. | [data/processed/cc_power.csv](../data/processed/cc_power.csv) |
| c10 | Power analysis and sample size | Real result | Required n per arm for 1.0 pp at D7 is around 24,259. | [data/processed/cc_power.csv](../data/processed/cc_power.csv) |
| c11 | Duration | Method on real inputs | The outcome window and round exposure are 14-day and 7-day. | [01-research/prereg.md](../01-research/prereg.md) |
| c12 | Confounders | Method on real inputs | No timestamps means we cannot isolate novelty or weekday effects. | [02-cookie-cats/analysis.md](../02-cookie-cats/analysis.md) |
| c13 | Implementation and QA | Real result | No nulls and no duplicates in the Cookie Cats data. | [data/processed/cc_quality.csv](../data/processed/cc_quality.csv) |
| c14 | Monitoring and SRM | Real result | SRM p-value is 0.0086, so the split is flagged. | [data/processed/cc_srm.csv](../data/processed/cc_srm.csv) |
| c15 | z-test | Real result | Primary result uses a two-proportion z-test. | [data/processed/cc_tests.csv](../data/processed/cc_tests.csv) |
| c16 | Confidence intervals | Real result | D7 difference 95% CI is approximately -1.33 to -0.31 pp. | [data/processed/cc_tests.csv](../data/processed/cc_tests.csv) |
| c17 | Effect size | Real result | Difference is -0.82 pp, which is a small but real harm. | [data/processed/cc_tests.csv](../data/processed/cc_tests.csv) |
| c18 | Statistical vs practical significance | Real result | Significant but below MDE means do not ship. | [02-cookie-cats/decision-memo.md](../02-cookie-cats/decision-memo.md) |
| c19 | Early stopping | Not testable with these data | No timestamps means peeking cannot be audited. | [02-cookie-cats/data-quality.md](../02-cookie-cats/data-quality.md) |
| c20 | Multiple testing | Real result | Holm adjustment is used across three tests. | [data/processed/cc_tests.csv](../data/processed/cc_tests.csv) |
| c21 | Simpson's paradox | Method on real inputs | A selected subgroup can reverse direction and should be treated as exploratory. | [data/processed/cc_subgroup.csv](../data/processed/cc_subgroup.csv) |
| c22 | Selection bias | Real result | Exposure is low because many players never reach the gate. | [data/processed/cc_exposure.csv](../data/processed/cc_exposure.csv) |
| c23 | Segments | Real result | Segment analysis is conducted on rounds >= 40 players. | [data/processed/cc_subgroup.csv](../data/processed/cc_subgroup.csv) |
| c24 | Decision making | Real result | Decision is not to ship gate_40. | [02-cookie-cats/decision-memo.md](../02-cookie-cats/decision-memo.md) |
| c25 | When not to test | Method on real inputs | Low traffic and missing instrumentation reduce value of A/B testing. | [04-playbook/ab-testing-playbook.md](../04-playbook/ab-testing-playbook.md) |
