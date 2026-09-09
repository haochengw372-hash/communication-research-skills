---
name: communication-causal-inference
description: Design and audit causal inference for communication research using DAGs, natural experiments, DiD/event studies, IV, RDD, matching or weighting, synthetic control, and interrupted time series. Use for 因果推断/政策评估/平台冲击/DiD/IV/RDD/匹配. Do not use when the goal is only description or prediction.
---

# Communication Causal Inference

## Overview

This Skill starts from the intervention, counterfactual, and estimand. It does not
upgrade an observational regression into a causal design by adding controls.

## Required start

1. State treatment, outcome, unit, timing, population, comparison, and estimand.
2. Draw or describe the causal graph, including selection, measurement, interference,
   anticipation, and post-treatment variables.
3. Use [references/causal-design-protocol.md](references/causal-design-protocol.md) to
   select a design only after its identifying variation is established.

## Design routing

- randomized experiments route jointly to `communication-experiment`;
- DiD/event studies require a credible untreated trend and explicit treatment timing;
- IV requires relevance, exclusion, independence, and a clear complier estimand;
- RDD requires a deterministic assignment threshold and continuity near the cutoff;
- matching/weighting requires conditional exchangeability, overlap, and pre-treatment
  covariates;
- synthetic control requires a defensible donor pool and pre-treatment fit;
- interrupted time series requires a stable pre-period and no concurrent shock;
- natural-experiment language is used only for genuinely as-if-random variation.

## Verification

Report identifying assumptions beside diagnostics and falsification tests: pre-trends,
placebos, negative controls, bandwidth/specification sensitivity, overlap, balance,
attrition, spillovers, and measurement stability. Preserve failed diagnostics and
weaken the claim when assumptions are not supported.

## Output shape

Return an estimand statement, DAG/assumption map, design and alternatives, data timing,
diagnostics and falsification plan, sensitivity analysis, and the exact population and
intervention to which the causal claim applies.

## Hard boundaries

- Temporal order alone is not identification.
- Fixed effects do not remove all time-varying confounding.
- Matching balances measured covariates; it does not create randomization.
- A policy date does not by itself create a valid intervention.
- Statistical significance is not assumption validation or practical importance.
