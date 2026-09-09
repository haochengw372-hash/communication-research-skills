# Spatial analysis protocol

## Spatial contract

```text
Population and observation process:
Spatial unit and why it matches the theory:
Time window and boundary version:
Location source and geocoding procedure:
Match rate, ambiguity, and positional uncertainty:
Coordinate reference system:
Spatial join keys and cardinality:
Aggregation, suppression, jitter, and privacy:
Neighborhood/weights definition:
Target claim and level of inference:
```

## Method-to-question map

| Question | Candidate method | Required checks |
|---|---|---|
| Where are observed cases concentrated? | rates, density, choropleth, point pattern | denominator/opportunity, edge effects, uncertainty |
| Is a variable spatially clustered? | global/local autocorrelation | weights matrix, multiple tests, scale sensitivity |
| Does proximity predict an outcome? | spatial regression/multilevel spatial model | dependence mechanism, residual autocorrelation, confounding |
| Does communication spread across places? | spatiotemporal diffusion/hazard/network model | temporal order, exposure path, mobility/media links |
| Did a geographically bounded intervention cause change? | spatial quasi-experiment | spillovers, border sorting, concurrent shocks, causal audit |

## Map integrity

Use rates with valid denominators, show missing areas, report classification and
projection choices, preserve uncertainty, avoid implying precision beyond the data,
and never expose sensitive individual locations.
