# General end-to-end examples for computational communication research

These examples demonstrate routing and research-quality gates. They are synthetic,
replaceable fixtures: none is a default topic, preferred theory, required method, or
claim about a real project. A real run must derive its phenomenon, construct, evidence,
and deliverable from the user's current materials.

## Shared lifecycle

Every example follows the same reasoning graph:

```text
phenomenon → literature → theory → construct → mechanism → RQ/H
           → operationalization → measurement → design/identification
           → evidence → theoretical contribution → manuscript → final audit
```

The controller first classifies the research goal, writes a task contract, and opens
only the work packages whose dependencies are satisfied. Specialist Skills own their
domain gates; executor and auditor outputs return through immutable handoffs.

## Example A — computational content analysis

### Request

Compare how two types of public communication frame responsibility for an
environmental risk across two digital platforms and over time.

### Route

- **Goal:** description first; explanation only if a mechanism and comparative design
  are supplied.
- **Archetype:** `text-computational`.
- **Skill stack:** `communication-literature`, `communication-theory`,
  `communication-construct`, `communication-content-analysis`, and
  `communication-reviewer`.

### Required contract decisions

- platforms, account/content population, collection dates, language, and exclusions;
- article/post/comment as the unit of analysis;
- a definition of responsibility framing distinct from blame, causal attribution, and
  policy preference;
- codebook, coder or model protocol, reliability sample, validation cases, and claim
  boundary.

### Stop condition

Frequency differences may describe this corpus. They do not establish a shift in public
meaning, platform causality, or population opinion without additional evidence.

## Example B — network and diffusion analysis

### Request

Assess whether corrections and disputed claims follow different diffusion patterns in
a bounded public-conversation network.

### Route

- **Goal:** description or prediction; causal identification requires an assignment or
  defensible quasi-experimental strategy.
- **Archetype:** `network`.
- **Skill stack:** `communication-method-router`, `communication-content-analysis`,
  `communication-theory`, and `communication-reviewer`.

### Required contract decisions

- node types, edge meaning and direction, time window, cascade rule, self-loops,
  multiedges, missing/deleted content, and platform/quoting treatment;
- how a correction or disputed claim is identified and validated;
- whether the target is reach, speed, depth, reproduction number, structural position,
  or out-of-sample prediction;
- sensitivity to collection coverage, bot/automation rules, and alternative cascade
  definitions.

### Stop condition

Centrality is not influence, diffusion is not persuasion, and an observed network
difference is not a causal effect of message type.

## Example C — communication experiment

### Request

Test whether a source-transparency cue changes verification intention in a synthetic
news interface, and whether the effect depends on issue involvement.

### Route

- **Goal:** causal identification of the randomized cue; mechanism claims remain
  conditional unless the mediator is itself identified.
- **Archetype:** `experiment`.
- **Skill stack:** `communication-theory`, `communication-construct`,
  `communication-scale`, `communication-experiment`, and
  `communication-reviewer`.

### Required contract decisions

- transparency cue, control condition, randomization unit, stimulus population, and
  what remains visually and verbally constant;
- canonical definitions for verification intention, issue involvement, and source
  credibility;
- validated measures or an explicit adaptation/validation plan;
- manipulation pretest, power for the smallest effect of interest, attrition and
  exclusion rules, analysis model, debriefing, and preregistration.

### Stop condition

The experiment licenses claims about the manipulated cue under controlled exposure. It
does not establish long-term behavior, general institutional trust, or effects of cues
that were not manipulated.

## Completion audit

For any of the three routes, completion requires fresh evidence for all applicable
gates:

| Gate | Minimum pass evidence |
|---|---|
| Theory | Mechanism, boundary conditions, rivals, and a falsifiable implication |
| Construct | Existing-name search, stable definition, and discriminant boundary |
| Measurement | Validity, reliability, adaptation status, and proxy limits |
| Design/identification | Sample/comparison/assignment supports the stated claim |
| Novelty | Verified distinction from prior literature, not a new dataset alone |
| Contribution | Evidence changes a communication-theory or method inference |
| Evidence-to-claim | Every number and conclusion traces to current verified output |

The generated example plans under [plans/](plans/) show two archetype-level window
graphs. [run_orchestrator_e2e.py](run_orchestrator_e2e.py) validates the project-control
lifecycle in a temporary directory without using or modifying any real research data.
After result audit, `communication-writing` builds the claim/number/terminology packet
and manuscript; `communication-reviewer` remains the independent final auditor.
