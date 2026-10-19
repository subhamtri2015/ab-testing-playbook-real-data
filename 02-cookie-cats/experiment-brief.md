# The Case in Plain English

This document mirrors the same narrative as the root README and is intended for a hiring manager or PM reviewer.

This repo is not affiliated with the original dataset owners or product teams. The analysis is written as if I were the PM.

## What is a gate?

A gate is a forced pause where the player must wait or pay to continue. The first gate is the first such pause. The experimental question is whether moving the first gate later changes retention.

## The experiment

The treatment group moved the first gate from level 30 to level 40. Players were randomly assigned at install. The dataset provided in this repo has 90,189 players: 44,700 in gate_30 and 45,489 in gate_40.

## Problem statement

Should the first gate move from level 30 to level 40?

## Hypothesis

A later gate gives more free play before the first pause and could improve retention. The trade-off is that it may reduce the feeling of progress and increase exit behavior.

## Metrics hierarchy

- Primary metric: 7-day retention
- Secondary metric: 1-day retention
- Guardrail: 14-day total game rounds (`sum_gamerounds`)

## What the data says

- 7-day retention is 19.02% in gate_30 and 18.20% in gate_40.
- 1-day retention is 44.82% in gate_30 and 44.23% in gate_40.
- The difference is a -0.82 pp lift for the treatment on D7 retention, which is statistically significant but below the decision threshold.

## Recommendation

The recommendation is to not ship gate_40 on retention evidence. The effect is not directionally positive on the primary metric and does not clear the pre-set MDE.

## What this data cannot tell us

This dataset has no revenue or purchase data and no timestamps. That means we cannot estimate novelty effects, weekday traffic mix, or the effect of user-level behavior over longer time windows.
