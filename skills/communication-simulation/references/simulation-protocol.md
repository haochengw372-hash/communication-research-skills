# Communication simulation protocol

## Simulation contract

```text
Macro phenomenon and target statistics:
Agent types, states, and population composition:
Environment and interaction topology:
Micro decision/update rules and theoretical source:
Time step, scheduling, stopping rule, and feedback:
Initial conditions and exogenous inputs:
Parameters fixed from data vs estimated vs explored:
Calibration data and held-out validation data:
Random seeds, repetitions, and uncertainty summary:
LLM model/version/prompt/memory/tools if applicable:
Ethics, stereotypes, sensitive attributes, and misuse risks:
Claim class: mechanism sufficiency, prediction, or scenario exploration:
```

## Validation ladder

1. **Verification:** code implements the stated rules; toy cases and invariants pass.
2. **Micro validation:** agent decisions match independent behavioral evidence.
3. **Macro calibration:** selected aggregate targets constrain parameters.
4. **Held-out validation:** distinct patterns, periods, or groups are reproduced.
5. **Sensitivity:** parameters, topology, initialization, schedule, prompts, and seeds.
6. **Alternatives:** simpler/null and rival-mechanism models are compared.

## LLM-agent calibration

Evaluate more than textual plausibility: absolute response levels, rank order, treatment
effects, temporal consistency, subgroup structure, refusals, and failure cases. Preserve
model snapshots and prompts; provider updates can change the simulated instrument.

## Claim language

Prefer “these rules are sufficient to generate the pattern under the tested conditions.”
Avoid “the simulation proves people behave this way” or “the synthetic sample represents
the population” unless independent empirical validation supports those stronger claims.
