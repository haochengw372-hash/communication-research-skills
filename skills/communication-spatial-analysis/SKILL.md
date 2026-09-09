---
name: communication-spatial-analysis
description: Design and audit geographic and spatial communication analysis using geocoding, spatial joins, autocorrelation, hotspots, spatial regression, and diffusion/exposure models. Use for GIS/空间传播/地理扩散/地区差异/空间网络. Do not infer individual behavior from area-level patterns.
---

# Communication Spatial Analysis

## Overview

This Skill makes place, scale, and spatial dependence explicit. It prevents maps from
becoming evidence without a defensible geographic unit and observation process.

## Required start

1. Define the communication process, spatial unit, population, time window, and target
   claim.
2. Record geocoding, coordinate reference system, joins, aggregation, and privacy in
   [references/spatial-protocol.md](references/spatial-protocol.md).
3. Distinguish place effects, spatial exposure, mobility, diffusion, and area-level
   association.

## Method routing

- choropleths and kernel density describe mapped observations, not causes;
- Moran's I/LISA and hotspot tests diagnose spatial pattern under a specified weights
  matrix;
- spatial lag/error/Durbin and multilevel spatial models address different dependence
  mechanisms;
- point-process models require a meaningful observation window and opportunity surface;
- spatial diffusion and exposure models require temporal order and defensible movement,
  proximity, or media-market links;
- causal spatial interventions also route to `communication-causal-inference`.

## Validation

Audit geocoding match rates and uncertainty, CRS, join cardinality, duplicate places,
boundary changes, modifiable areal unit problem (MAUP), spatial weights, edge effects,
multiple testing, missing regions, and sensitivity across scales and neighborhood rules.

## Output shape

Return the spatial contract, geocoding/join audit, scale and weights decisions, method
and diagnostics, uncertainty-preserving map plan, privacy review, sensitivities, and
individual-versus-area claim boundaries.

## Hard boundaries

- Area-level relations do not establish individual relations.
- Hotspots are conditional on scale, weights, and testing choices.
- Geotagged posts are not representative of residents or all platform users.
- Administrative boundaries may not match communication markets or lived places.
- Jittering, aggregation, and redaction must be disclosed because they alter analysis.
