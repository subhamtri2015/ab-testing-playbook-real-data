# Upworthy confirmatory pre-registration

Date: 2026-10-19

This document sets the confirmatory hypotheses for the Upworthy archive before the confirmatory file is analysed.

## Hypotheses

1. H-U1: Headlines with a question mark produce a different CTR than headlines without a question mark.
2. H-U2: Headlines with a digit produce a different CTR than headlines without a digit.
3. H-U3: Longer headlines produce a different CTR than shorter headlines.

## Qualifying tests

- Exactly two arms
- At least 1,000 impressions per arm
- Outside the flagged risk window if the file includes that information
- One arm includes the feature and the other does not
- Same exclusions as the exploratory program analysis

## Estimand

The estimand is the pooled relative CTR lift across qualifying tests using a random-effects meta-analysis.

## Decision threshold

The decision threshold is a lower 95% CI of >= +2% relative lift, and the three hypotheses are corrected with Holm across the family.

## Analysis note

The exploratory archive is used only to debug the processing and qualifying logic. The confirmatory archive is used once, exactly at the end, to test the set of hypotheses stated here.
