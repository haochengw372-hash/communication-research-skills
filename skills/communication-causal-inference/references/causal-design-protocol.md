# Causal design protocol

## Causal contract

```text
Treatment/intervention and versions:
Outcome and measurement time:
Unit and population:
Assignment or identifying variation:
Counterfactual comparison:
Estimand (ATE/ATT/LATE/dynamic or other):
Treatment timing, anticipation, and carryover:
Interference and spillovers:
Pre-treatment covariates and post-treatment variables:
Missingness, attrition, and sample transitions:
```

## Design audit

| Design | Identification question | Minimum diagnostics |
|---|---|---|
| DiD/event study | Would treated and comparison units have followed parallel untreated trends? | pre-trends, staggered-timing estimator, composition, anticipation, spillovers |
| IV | Does the instrument affect outcome only through treatment for the relevant compliers? | first stage, exclusion argument, weak-IV diagnostics, LATE population |
| RDD | Are potential outcomes and sorting continuous at the assignment cutoff? | density, covariate continuity, bandwidth, polynomial sensitivity |
| Matching/weighting | Are all treatment-outcome confounders measured with adequate overlap? | balance, overlap, weight stability, sensitivity to hidden bias |
| Synthetic control | Does a weighted donor pool reproduce the untreated trajectory? | pre-fit, donor sensitivity, in-time/in-space placebos |
| Interrupted series | Is the level/slope break distinguishable from seasonality and co-interventions? | sufficient pre-period, autocorrelation, seasonality, concurrent-event audit |

## Communication-specific threats

Platform changes may alter measurement as well as behavior; media events create
simultaneous shocks; messages spill through networks; algorithms adapt to users; and
exposure is often mismeasured. Put each threat in the DAG and connect it to a diagnostic,
sensitivity analysis, or explicit limitation.
