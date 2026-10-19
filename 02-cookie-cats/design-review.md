# Design review

## SRM

The sample ratio mismatch test is a check for assignment integrity. In this repo, the SRM p-value is about 0.0086, which is a flag under the 0.05 threshold and a warning sign that the split should be checked before trusting the result. The next step would be to validate the assignment logic, data pipeline, and user IDs.

## MDE reality check

The experiment was sized to detect roughly a 1.0 pp difference on D7 retention. That is a realistic choice for a product experiment, but it is larger than the actual observed effect. That means the result should be considered a small, negative estimate rather than evidence that the change was a success.

## Duration notes

The dataset does not contain timestamps, so we cannot check when players were assigned or when retention was measured. Without timestamps, we cannot assess day-of-week effects, novelty effects, or early peeking.

## What cannot be known

- Novelty effects
- Day-of-week traffic changes
- Peeking after partial rollout
- Revenue or monetization impact
