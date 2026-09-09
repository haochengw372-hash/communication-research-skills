# Unified computational social science / computational communication methodology

This document is the single methodology that the skill suite operationalizes.
Computational communication research is a subfield of computational social
science (CSS): the reasoning graph, gates, and method routing are CSS-general;
the communication-specific theory anchors and measurement skills are the
domain layer on top.

## 1. The reasoning graph

Research moves through, in order:

```text
phenomenon → literature → theory → construct → mechanism
          → RQ/H → operationalization → measurement
          → design/identification → evidence → theoretical contribution
```

Every downstream step must be traceable to an upstream step. A claim at one
level cannot outrun what the lower levels established.

## 2. The seven gates

| Gate | Question | Owner Skill |
|---|---|---|
| Theory | Does the theory explain a mechanism, with boundaries and rival explanations? | communication-theory |
| Construct | Does the construct exist, is it disambiguated, and is its definition locked? | communication-construct |
| Measurement | Is the instrument valid, reliable, and invariant where needed? | communication-scale |
| Design / identification | Does the design license the claim the RQ/H requires? | communication-method-router |
| Novelty | Is the contribution non-redundant with prior work? | communication-literature |
| Contribution | Does the evidence advance theory, not just describe? | communication-reviewer |
| Evidence-to-claim | Does the conclusion stay within what the evidence shows? | communication-reviewer |

## 3. Goal-first method routing

Classify the research goal before choosing any method:

- **Description** — distribution, prevalence, patterns. May not claim causes.
- **Measurement** — construct validity and reliability. May not claim group differences.
- **Explanation** — a mechanism path consistent with theory and data. May not claim causality without identification.
- **Prediction** — out-of-sample performance and calibration. May not claim causes.
- **Causal identification** — exchangeability/randomization/identification. May not over-generalize without argument.
- **Simulation explanation** — micro rules reproduce macro patterns. May not claim the rules are the true process without calibration.

See `skills/communication-method-router/references/method-goal-table.md` and
`skills/communication-method-router/references/css-methods.md` for the
goal-to-method maps.

## 4. Evidence-to-claim discipline

- Frequency is not mechanism and not cause. Report descriptive distributions
  without "dominance" or "hegemony" language.
- A label (dictionary, topic, LLM code) is a measurement claim, so it carries
  a reliability and validation burden.
- Each manuscript claim must be traceable to a specific item, model, or test.

## 5. Five-layer scholarly access

Full text is resolved in fixed order and only with user confirmation for any
non-dry run:

```text
open access → institutional subscription → federated authentication
            → repository/author version → library delivery
```

Credentials are never stored; authentication is always the user's own action
in their own browser. See
`skills/scholarly-access/references/resolver-layers.md`.

## 6. End-to-end workflow

1. **Orchestrate** — `communication-research-workflow` plans windows, writes a
   task contract, and enforces the gates.
2. **Search and screen** — `communication-literature` builds a verified
   evidence matrix; full text goes to `scholarly-access`.
3. **Ground theory and constructs** — `communication-theory` and
   `communication-construct` lock the mechanism and the construct definition.
4. **Select measurement** — `communication-scale` locates or adapts validated
   instruments.
5. **Route the method** — `communication-method-router` maps the goal to a
   design. Specialist protocols cover experiments, content analysis, networks,
   causal inference, temporal processes, multimodal media, spatial communication,
   and agent-based or generative simulation.
6. **Audit results** — `communication-reviewer` verifies the accepted evidence,
   diagnostics, and claim strength before manuscript integration.
7. **Write and synchronize** — `communication-writing` converts accepted evidence into
   section-level prose, maintains claim/number/terminology ledgers, and propagates
   accepted changes across manuscript artifacts before independent final review.
8. **Revise prose** — `communication-prose-revision` removes formulaic scaffolding and
   defensive over-hedging without changing evidence, claims, or uncertainty.
9. **Review and freeze** — `communication-reviewer` runs the seven-gate manuscript
   review; the controller freezes a submission version only after human approval.

## 7. Quality bar

A result is publishable-quality only when every gate that the claim crosses is
passed, the method matches the goal class, and the conclusion stays inside the
identification the design actually provides.

## 8. Specialist computational method modules

| Module | Main objects |
|---|---|
| `communication-content-analysis` | text corpora, codebooks, dictionaries, embeddings, topic models, supervised or LLM coding |
| `communication-network-analysis` | ties, communities, brokerage, diffusion, ERGM, SAOM, relational events |
| `communication-causal-inference` | interventions, counterfactuals, DiD, IV, RDD, matching, synthetic control, interrupted series |
| `communication-temporal-analysis` | time series, panels, survival/event history, sequences, lags, change points |
| `communication-multimodal-analysis` | image, video, audio, OCR/ASR, vision models, multimodal fusion |
| `communication-spatial-analysis` | geocoding, GIS, spatial dependence, geographic exposure and diffusion |
| `communication-simulation` | ABM, opinion dynamics, generative or LLM agents, calibration and sensitivity |
| `communication-experiment` | survey/online/field experiments, vignettes, conjoint, manipulation and power |
| `communication-scale` | CFA, IRT, reliability, adaptation, measurement invariance |
| `communication-writing` | evidence-led outlines, section drafting, design-specific results/discussion, bilingual revision, rebuttal, synchronization, finalization |
| `communication-prose-revision` | formulaic-language diagnostics, defensive-writing repair, section-sensitive rhythm and agency revision |

The suite specifies research contracts and verification standards. It does not bundle
every estimator or model runtime; execution uses an appropriate coding/statistical
environment after the method and identification choices are locked.
