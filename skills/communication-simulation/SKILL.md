---
name: communication-simulation
description: Design and audit agent-based, generative, and LLM-agent simulations of communication processes with explicit mechanisms, calibration, sensitivity, and validation. Use for ABM/生成式仿真/LLM智能体/合成公众/意见动力学. Do not present simulated agents as human evidence without empirical calibration.
---

# Communication Simulation

## Overview

This Skill treats simulation as an instrument for testing whether specified micro-rules
can reproduce macro communication patterns. It does not treat plausible model output as
evidence that the rules are true.

## Required start

1. State the macro phenomenon, proposed micro mechanisms, agents, environment,
   interaction topology, schedule, and target pattern.
2. Write the simulation contract in
   [references/simulation-protocol.md](references/simulation-protocol.md).
3. Separate explanation, prediction, measurement, and scenario exploration.

## Method routing

- classical ABM encodes explicit state-transition and interaction rules;
- opinion-dynamics models require justified update, confidence, and network rules;
- generative or LLM agents require model/version, prompt, memory, tool, sampling, and
  refusal/error provenance;
- microsimulation reproduces population composition but not interaction mechanisms by
  itself;
- system dynamics models aggregate stocks and flows and cannot answer actor-level
  questions without a bridge.

## Validation

Calibrate independent parameters to empirical data, reserve separate targets for
validation, compare against simple/null models, run repeated seeds, report stochastic
uncertainty, sweep plausible parameter ranges, test initialization/topology/schedule,
and examine equifinality. For LLM agents, compare absolute levels, rank ordering,
mechanisms, heterogeneity, and group structure against human reference data.

## Output shape

Return the mechanism map, simulation contract, calibration/validation split, parameter
table, baseline models, experiment grid, seed and uncertainty plan, sensitivity and
equifinality results, and a bounded statement of what the simulation explains.

## Hard boundaries

- Macro pattern reproduction does not identify a unique micro mechanism.
- Prompt tuning is not human calibration.
- Agent personas are not sampled populations.
- One seed or one attractive run is not a result.
- Model agreement with one target can coexist with failure on mechanisms and subgroups.
