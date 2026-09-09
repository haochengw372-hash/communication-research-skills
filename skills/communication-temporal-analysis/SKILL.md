---
name: communication-temporal-analysis
description: Design and audit temporal communication research using time series, longitudinal panels, event history, survival, sequence analysis, change points, and distributed lags. Use for 时间序列/纵向面板/事件史/生存分析/序列分析/动态传播. Route causal intervention claims to communication-causal-inference.
---

# Communication Temporal Analysis

## Overview

This Skill preserves communication as a process in time. It locks the clock, sequence,
risk set, temporal aggregation, and observation process before fitting a dynamic model.

## Required start

1. State whether time is the outcome, exposure, ordering device, moderator, or source of
   dependence.
2. Define the unit, clock, origin, interval, observation frequency, censoring, and
   missingness in [references/temporal-protocol.md](references/temporal-protocol.md).
3. Separate within-unit change from between-unit differences and description from
   causal intervention claims.

## Method routing

- time-series and distributed-lag models address serial dependence and delayed relations;
- panel models separate within- and between-unit variation with attrition and clustering;
- event-history/survival models analyze event timing under a defined risk set;
- sequence analysis compares ordered states or actions without reducing them to totals;
- change-point models detect distributional breaks but do not identify their causes;
- interrupted series and event studies route to `communication-causal-inference` when
  they support intervention claims.

## Validation

Check temporal order, stationarity or trend specification, autocorrelation, seasonality,
aggregation sensitivity, lag choice, irregular observation, informative missingness,
censoring, attrition, and multiple-event dependence. Compare results across defensible
time bins and lag windows.

## Output shape

Return the temporal contract, method choice, diagnostics, missingness/censoring plan,
lag or sequence definition, sensitivity analyses, and a claim map that distinguishes
change, association, prediction, and causation.

## Hard boundaries

- Before/after is not automatically causal.
- A detected change point does not identify the event that caused it.
- Aggregated time bins can create or erase relations.
- Lagged regression alone does not solve confounding or establish direction.
- Panel attrition and platform deletion can redefine the observed population over time.
