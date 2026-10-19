# A/B testing playbook

## Lifecycle

1. Plan: define the business question, the metric, and the pre-analysis decision rule.
2. Design: decide on unit of randomization, traffic assumptions, and protection against confounders.
3. Implement: validate instrumentation, logging, and assignments.
4. Monitor: watch for SRM and data quality issues.
5. Analyse: run the pre-registered checks and sensitivity analyses.
6. Decide: ship only if the evidence is positive and the practical significance is strong.

## Hypothesis format

Use a single sentence: "If we change X for Y users, then Z will move because of mechanism M." This prevents testing without a causal story.

## Metrics

- Primary: the one metric used to decide.
- Secondary: supportive metrics that help interpret the story.
- Guardrail: operational or fairness metrics that must not regress materially.

## Sample size and duration

Use an MDE and power calculation before the experiment starts. The repo includes a sample size table and a D7 baseline from the real Cookie Cats data.

## Confounders and tracking QA

Check assignment integrity, missing values, duplicate IDs, exposure quality, and any post-randomization segmentation. No timestamps means no direct audit of novelty effects or peeking.

## SRM monitoring

Monitor the arm split during the run and check for assignment imbalance. A p-value below 0.05 is a warning and below 0.001 is an alarm.

## Analysis

Use a pre-defined z-test or exact test, report confidence intervals, and adjust for multiple testing. Always separate statistical significance from practical significance.

## Pitfalls

- Peeking: use a pre-specified rule and avoid repeated interim checks.
- Multiple testing: correct the family of tests (e.g., Holm or BH).
- Simpson's paradox: subgroup splits can reverse direction.
- Selection bias: post-randomization segments are not causal proof.
- Low traffic: small differences become hard to measure and easy to misinterpret.

## Decision framework

Ship only if the result is statistically significant and the lower bound of the confidence interval clears the pre-set MDE. Otherwise, do not ship.

## PM use cases

- UI: compare copy or page layout changes
- Feature: assess adoption of a new capability
- Messaging: test headline performance or call-to-action wording
- Pricing: test price or packaging if there is a valid experiment design
- Algorithms: test ranking or recommendation changes with guardrails

## When not to A/B test

- The product is already constrained by low traffic.
- The change is too large to isolate cleanly from other changes.
- Instrumentation is not trustworthy.
- The decision must be made under extreme time pressure.
