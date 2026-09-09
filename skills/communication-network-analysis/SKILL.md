---
name: communication-network-analysis
description: Design and audit communication network, diffusion, cascade, community, ERGM, SAOM, and multiplex analyses with explicit graph boundaries and selection-versus-influence claims. Use for 传播网络/扩散/级联/社群/ERGM/SIENA/关系数据. Do not use for non-relational content analysis or spatial proximity without ties.
---

# Communication Network Analysis

## Overview

This Skill treats a network as a research design, not a visualization. It locks what
nodes and edges mean, how the graph was observed, and which relational claim the data
can support before selecting a metric or model.

## Required start

1. State the communication phenomenon, goal class, and target quantity.
2. Write the graph contract in [references/network-protocol.md](references/network-protocol.md).
3. Distinguish description, prediction, diffusion, selection, influence, and causal
   intervention; they require different evidence.

## Method routing

- centrality and community detection describe a specified graph;
- ERGM models cross-sectional tie dependence, conditional on the specified terms;
- SAOM/SIENA models co-evolution of ties and actor attributes in panel networks;
- relational-event models use event order and timing rather than aggregated ties;
- cascade and diffusion models require explicit exposure and adoption definitions;
- temporal, multiplex, bipartite, and multilayer networks retain their native structure
  unless a justified projection or aggregation is tested for sensitivity.

## Validation

- test direction, weighting, duplicate ties, self-loops, isolates, components, and time
  ordering on known cases;
- report missing nodes/edges, API and deletion coverage, boundary sensitivity, bot or
  automation rules, and projection loss;
- compare plausible graph constructions before interpreting centrality or communities;
- separate homophily, shared context, and prior similarity from social influence.

## Output shape

Return the graph contract, construction audit, selected method and rejected
alternatives, diagnostics, sensitivity plan, and a claim map stating what each network
quantity can and cannot mean.

## Hard boundaries

- Centrality is not influence, brokerage, authority, or importance without a mechanism.
- Community detection does not discover natural social groups by itself.
- Contemporaneous similarity does not identify contagion.
- A platform crawl is not automatically the whole network.
- Layout coordinates are visual encodings, not analytical results.
