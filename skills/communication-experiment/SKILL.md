---
name: communication-experiment
description: Design communication survey and online experiments, including human-machine communication and AI-disclosure studies, stimuli and manipulation checks, conjoint/vignette designs, power, and preregistration. Use for experimental design, stimulus design, manipulation checks, 实验设计/操纵检验/人机传播实验/AI披露实验/情境实验. Do not use for pure questionnaire scale work without experimental conditions.
---

# Communication Experiment

## Overview

This Skill turns hypotheses into a fieldable experimental protocol with clean conditions, checked manipulations, and a preregistrable analysis plan. It is designed for the communication problems that generic experiment templates miss: disclosure cues, institutional context, perceived agency, and platform realism.

## Required start

1. Lock each hypothesis to a construct and mechanism (construct gate and measurement gate come first; do not skip them).
2. Choose the design family: between-subjects, within-subjects, factorial, vignette, or conjoint; state why.
3. Write the experiment contract before creating stimuli.

## Experiment contract

```text
Design and unit:
Conditions and randomization:
Stimulus description:
Manipulation check (item, expected direction, threshold):
Primary outcomes and instruments:
Exclusions and attention checks:
Power analysis (target effect, n per cell):
Preregistration items:
Attrition and missing-data plan:
```

## Stimulus rules for communication and HMC

- Pre-test stimuli before fielding: realism, clarity, and confound checks.
- Manipulate one construct at a time. If a second cue must vary, cross it factorially rather than bundling it.
- When an AI cue is the manipulation, do not also change author name, author photo, institution, article length, visual layout, or platform branding.
- Use realistic news/platform materials and state exactly what was fictionalized or adapted.
- Verify that the manipulation changes the intended construct and not only comprehension ("Did you notice AI" is not the same as attribution or trust).

## Communication-specific design decisions

- Institutional trust: decide whether institution is a moderator, a baseline, or a separate condition before analysis; do not let it emerge from the data.
- State vs commercial media cues: treat as one or more explicit conditions with a theoretical reason, and pretest that the cue reads as intended across participants.
- Perceived humanness vs perceived machine agency: these are distinct constructs; measure them separately when both are plausible.
- Wording-only label experiments ("AI" vs no label with identical content) are acceptable only when the research question is about labeling itself; otherwise they are confounded-by-nothing tests with limited generalizability.
- For platform field experiments or natural experiments, state the assignment mechanism, unit, platform policy constraints, and ethics review terms.

## Validity checklist

- Internal: randomization, no differential attrition, manipulation check timing, no demand-characteristic cues.
- Construct: outcomes match the locked constructs; manipulation is distinct from outcome.
- External: population and platform realism vs control tradeoff is explicit.
- Ethical: debriefing, consent, deception justification, data protection for participants.

## Output shape

End with a protocol that another researcher could preregister: hypotheses mapped to constructs and scales, design and randomization plan, stimuli summary, manipulation checks, analysis plan, and stop/attrition rules.

## Common anti-patterns

- Bundling disclosure with other differences and attributing the effect to disclosure.
- Manipulation check after outcome measures or only among a subset.
- Analyzing a factorial design as separate one-factor tests.
- Concluding that an institutional or source cue "does not matter" when the manipulation failed.
- Using a platform screenshot that no longer reflects the interface and failing to record the version.

See [references/experiment-contract.md](references/experiment-contract.md) for the full protocol template and preregistration checklist.
