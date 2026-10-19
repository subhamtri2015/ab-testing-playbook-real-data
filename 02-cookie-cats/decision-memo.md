# Decision memo

## Recommendation

Do not ship gate_40 on retention evidence.

## Evidence

- D7 retention is 19.02% in gate_30 vs 18.20% in gate_40, a -0.82 pp difference.
- The D7 difference is statistically significant at p=0.0016, but it is below the decision MDE of 1.0 pp.
- D1 retention is not significant at p=0.074, so there is no positive short-term signal.

## Risks and unknowns

- No revenue data means monetization impact is unknown.
- No timestamps mean we cannot estimate novelty or weekday effects.
- The treatment arm is exposed less often because fewer players reach the gate.

## Rollback and next steps

Rollback is straightforward because the change is a simple level-value treatment. The next step is to run a stronger follow-up experiment that changes the gate with a clearer user value proposition or a more precise retention hypothesis.
