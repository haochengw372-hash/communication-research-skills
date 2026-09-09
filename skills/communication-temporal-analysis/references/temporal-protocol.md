# Temporal analysis protocol

## Temporal contract

```text
Unit and population:
Clock, origin, and observation interval:
Start/end dates and inclusion rule:
State, event, exposure, and outcome definitions:
Within-unit and between-unit quantities:
Lag window and theoretical timing:
Seasonality, trends, and known shocks:
Irregular observation and missingness:
Censoring, attrition, and recurrent events:
Target claim: description, explanation, prediction, or causal effect:
```

## Method-to-question map

| Question | Candidate method | Key checks |
|---|---|---|
| How does an aggregate series evolve? | ARIMA/state-space/VAR or descriptive decomposition | stationarity, seasonality, autocorrelation, measurement consistency |
| How do effects unfold over lags? | distributed-lag/cross-lag specification | theory-led lag window, autocorrelation, reverse timing, multiplicity |
| How do units change within themselves? | fixed/random-effects panel, growth model | within/between separation, clustering, attrition, dynamic bias |
| When does an event occur? | survival/event history/recurrent-event model | risk set, censoring, proportionality or functional form |
| Which ordered trajectories recur? | sequence analysis/process mining/HMM | state validity, distance/model choice, temporal resolution |
| When did the process change? | change-point/segmented model | false discovery, alternative breakpoints, concurrent events |

## Reporting minimum

Report the time axis, row transitions, observation density, missingness pattern,
temporal resolution, lag/sequence decisions, dependence diagnostics, sensitivity to
alternative bins, and whether the reported relation is contemporaneous, lagged,
predictive, or causally identified.
