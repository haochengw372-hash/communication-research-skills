---
name: communication-method-router
description: Classify a communication research goal before selecting any method and route to the appropriate specialist design or analysis. Distinguishes description, measurement, explanation, prediction, causal identification, and simulation explanation. Use for research method selection, methodological planning, 研究方法选择/方法路由/研究目标分类/计算传播方法. Do not use when the goal and design are already fixed and only execution remains.
---

# Communication Method Router

## Overview

This Skill prevents method-led research ("there is text, so topic model"). It first classifies the research goal, then selects a method family and routes to the specialist Skill that owns the design.

## Required start

Classify the goal with the decision tree before looking at data or algorithms:

1. **Description** — What exists, how is it distributed?
2. **Measurement** — Can a construct be validly measured in this material/population?
3. **Explanation** — What mechanism links constructs (mediation, moderation, process)?
4. **Prediction** — Can outcomes be anticipated in new data?
5. **Causal identification** — Does a specific intervention change the outcome?
6. **Simulation explanation** — Can micro rules reproduce a macro communication pattern?

If more than one applies, name the primary goal and list secondary goals; the design is built for the primary one.

## Routing table

| Goal class | Representative communication methods | Route to |
|---|---|---|
| Description | Content/text, multimodal, temporal, spatial, or network description | communication-content-analysis or the modality-specific Skill |
| Measurement | Scale validation, text-measurement validation (dictionary/embedding/LLM labels), psychometric analysis | communication-scale or communication-content-analysis |
| Explanation (mechanism) | Survey with mediation/moderation, experiment, process-tracing, panel mediation | communication-experiment or communication-scale |
| Prediction | Supervised classification, forecasting, calibration evaluation | communication-content-analysis or communication-temporal-analysis |
| Causal identification | Randomized experiment, natural experiment, IV, RDD, DiD, field intervention | communication-experiment or communication-causal-inference |
| Simulation explanation | Agent-based, opinion-dynamics, generative, or LLM-agent simulation | communication-simulation |

Specialized relational and media routes are: `communication-network-analysis`,
`communication-temporal-analysis`, `communication-multimodal-analysis`, and
`communication-spatial-analysis`.

Read [references/method-goal-table.md](references/method-goal-table.md) when a finer mapping is needed, and [references/css-methods.md](references/css-methods.md) for the general computational social science method families behind this routing.

## Method families inside a goal

For computational text work, choose within the goal:

- dictionary/count methods only when the construct is narrow, transparent, and dictionary validity is shown;
- topic models for discovering latent topical structure, not for measuring a predefined construct;
- embeddings/semantic similarity for continuous similarity or clustering with an explicit meaning reference;
- supervised classification when labeled data define the target and leakage is controlled;
- LLM-assisted coding when the codebook is reproducible and a human-verified sample establishes reliability;
- LLM-simulation only as a simulation instrument whose calibration is measured.

## Output shape

End with a route memo:

1. goal class and primary claim;
2. units, population, and time window;
3. target quantity (estimand, construct, or emergent pattern);
4. selected method family and why alternatives were rejected;
5. required specialist Skill and next design decisions;
6. methods the goal does NOT license (causal language from prediction, etc.).

## Common anti-patterns

- "Has text → topic model" and "has variables → SEM" and "has time → time series".
- Letting an available dataset choose the question.
- Presenting a predictive classifier as causal evidence.
- Choosing a method before stating the units or the target quantity.
- Confusing data collection method with analysis goal (e.g., "survey" as a goal).

## Reference

- [references/method-goal-table.md](references/method-goal-table.md) maps goals to design families, analysis families, and gate ownership in detail.
- [references/css-methods.md](references/css-methods.md) lists the general CSS method families (causal designs, network science, text and multimodal data, temporal/spatial analysis, simulation, experiments, digital traces, ML, measurement, and data donation) with assumptions and anti-patterns.
