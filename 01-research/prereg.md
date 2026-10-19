# Preregistration

Date: 2026-10-19

## Cookie Cats: pre-registered plan

Hypothesis in plain language: a later gate could increase early free play and therefore lead to stronger retention because more players are exposed to the game before the first forced pause. The alternative is that the later gate makes the game feel less rewarding, harming retention.

- H0: the 7-day retention rate is the same for gate_30 and gate_40.
- H1: the 7-day retention rate differs between gate_30 and gate_40.
- Unit of randomization: player-level assignment at install.
- Primary metric: 7-day retention. Reason: it captures longer-term engagement, which is more relevant to a retention-first product decision than the immediately visible 1-day metric.
- Secondary metric: 1-day retention.
- Guardrail / diagnostic: total game rounds in the first 14 days (sum_gamerounds), used to check exposure and whether players actually reached the gate.
- Alpha: 0.05 two-sided.
- Power: 0.80.
- Decision MDE: 1.0 pp absolute lift on 7-day retention. This is a product judgment chosen before analysis.
- Analysis plan: two-proportion z-test with pooled standard error for p-values, unpooled Wald CI for the difference, bootstrap percentile CI on real rows, Holm correction across the three metric tests, and a sensitivity check that removes the maximum-rounds outlier from the game-rounds analysis.
- Outlier handling: the highest sum_gamerounds player is reported in the quality and sensitivity outputs; we inspect whether a single extreme player drives the distribution.
- Exposure analysis: the share reaching the gate is treated as exploratory because it is post-randomization and not a pre-specified outcome.
- What would make me not ship: any statistically significant harm to 7-day retention, any failure to clear the decision MDE, or evidence that the treatment is materially misaligned with the actual exposure mechanism.

## Upworthy pre-registration

To be completed in Phase 2 when the confirmatory archive is analysed.
