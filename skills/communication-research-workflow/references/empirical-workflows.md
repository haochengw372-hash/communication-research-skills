# Data, empirical analysis, code, and figures

## Contents

1. Data audit and variables
2. Empirical design and statistics
3. PSM/ATT and two-stage designs
4. Reproducible analysis code
5. Figures and result display

## 1. Data audit and variables

**Route:** `exploratory-data-analysis`, `polars`; add `spreadsheets:Spreadsheets` or `xlsx` for spreadsheet artifacts.

Before analysis, record the authoritative input path/version, unit of observation, primary/composite keys, join cardinality, time granularity, fields, coding rules, missingness, duplicates, exclusions, and expected row-count transitions.

Validate variables against their conceptual definition. For every derived variable record source fields, transformation, timing, allowable range, missing-value rule, and invariants. Treat an unexpected row-count change as a diagnostic event, not a cosmetic discrepancy.

## 2. Empirical design and statistics

**Route:** start with `communication-method-router`, then use
`communication-experiment`, `communication-causal-inference`,
`communication-network-analysis`, `communication-temporal-analysis`,
`communication-multimodal-analysis`, `communication-spatial-analysis`, or
`communication-simulation` according to the locked goal and data structure. A coding
environment executes the selected estimator; the domain Skill owns its assumptions and
claim boundaries.

Required analysis contract:

- target population and analysis sample;
- unit and time structure;
- estimand and contrast;
- treatment/exposure, outcome, covariates, mediators/moderators;
- identification assumptions and plausible violations;
- model specification, standard errors, clustering/weights;
- diagnostics, robustness, multiplicity, missing-data treatment;
- scope of causal language.

Do not choose a method because it yields the expected sign or significance. Report effect sizes, uncertainty, model diagnostics, and material limitations. Association does not become causation through stronger prose.

## 3. PSM/ATT and two-stage designs

### PSM/ATT

Lock before running: treatment timing, ATT versus ATE/ATC, eligible controls, pre-treatment covariates, propensity model, common support, matching algorithm/caliper/replacement, estimand weights, outcome window, and standard-error method.

Verify:

1. propensity overlap and support exclusions;
2. treated/control counts at every transition;
3. effective sample and weights;
4. covariate balance before and after matching, including SMD definitions;
5. outcome estimation using the same matched sample/weights;
6. sensitivity to specifications and unmeasured confounding where warranted;
7. tables, Love plot, ATT text, and captions all use the same run.

Never cap SMD points, delete observations for appearance, or retain old ATT tables after rematching. If balance fails, disclose it or revise the design and recompute all dependent results.

### Two-stage outcomes

For designs such as entry into policy followed by post-entry policy influence:

- define each risk set and denominator separately;
- state whether stage 2 is conditional on stage-1 entry and address selection implications;
- distinguish hypotheses, outcomes, samples, estimands, and missingness by stage;
- prevent post-treatment variables from entering stage-1 adjustment;
- verify that prose does not interpret a conditional stage-2 association as a population-wide effect.

Any change to estimand, stage membership, or identification strategy is a mandatory pause.

## 4. Reproducible analysis code

**Route:** use the selected communication method Skill to lock the scientific contract,
then implement in the available coding environment and verify at delivery.

- Keep raw data read-only. Write derived data and results to separate, named locations.
- Use configuration or explicit parameters for paths, windows, samples, seeds, and model choices.
- Build tests around keys, schemas, row-count transitions, deterministic transformations, estimand weights, and known small examples.
- Record environment, package versions, random seeds, commands, inputs, outputs, logs, and timestamps.
- Make reruns idempotent or fail safely; never silently overwrite authoritative results.
- On a bug, reproduce it with a failing test before fixing it.

## 5. Figures and result display

**Route:** `scientific-visualization`; add `matplotlib` or `seaborn`, and the appropriate document/slide Skill for embedding.

Every final figure must have a reproducible lineage:

`authoritative data → transformation script → plotted table/array → figure file → manuscript caption`

Check numerical identity between plotted data, tables, text, and captions; axes, units, denominators, uncertainty, categories, color semantics, accessibility, resolution, and export format. Store intermediate plotted data when it materially improves auditability.

Styling may improve legibility but may not alter values, hide adverse diagnostics, truncate axes deceptively, or remove observations without a documented analytic rule.
