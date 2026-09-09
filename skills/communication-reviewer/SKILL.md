---
name: communication-reviewer
description: Run structured seven-gate review and audit of communication research manuscripts, proposals, and analyses, and diagnose journal fit and writing maturity. Use for peer review, internal manuscript audit, proposal review, revision planning, 论文评审/审稿/研究审计/七道门/投稿前检查. Review mode is read-only unless the user separately asks for edits.
---

# Communication Reviewer

## Overview

This Skill audits a communication research product through seven gates, each with an evidence-located verdict, and separates research quality from journal fit and writing maturity.

## The seven gates

Apply all seven. For each, return `Pass`, `Conditional`, or `Fail` with a location (section/table/line) and one-sentence reason.

1. **Theory gate**: does the theory explain the mechanism; are boundary conditions and rival explanations present?
2. **Construct gate**: do constructs exist, stay stable across sections, and avoid invented labels?
3. **Measurement gate**: are measures validated scales or audited operationalizations, with reliability/validity and adaptation evidence where needed?
4. **Design / identification gate**: does sampling, randomization, comparison, and causal language match the evidence?
5. **Novelty gate**: what is new relative to the field, not merely the setting, dataset, or model?
6. **Contribution gate**: what does the paper change about communication theory or accumulated evidence?
7. **Evidence-to-claim gate**: do reported numbers, reliability, and diagnostics support every claim without overclaiming?

## Separate scores

- Research quality: theoretical meaningfulness, method credibility, evidentiary strength.
- Journal fit: whether the object and contribution fit communication venues (do not hardcode one journal's norms; note when the fit is journalism, HMC, computational, or general communication).
- Writing maturity: structure, claim discipline, transparency, readability.

## Severity and output shape

Classify every finding:

- `Critical` — invalidates a conclusion or the design's core inference.
- `Major` — requires a substantive change before submission.
- `Minor` — polish, reporting, or clarification.

End with:

1. verdict table (gate × verdict × severity × location);
2. evidence-located finding list;
3. three priority revision actions;
4. an explicit statement of what was not examined.

## Role discipline

- Reviewing is read-only unless the user explicitly asks for edits in the same turn.
- Do not fix the manuscript while reviewing it; separate diagnosis from implementation.
- Do not let review severity inflate to protect or punish the author.

## Common anti-patterns

- Reviewing only theory or only statistics and ignoring construct/measurement fit.
- Treating a "real" but unrelated citation as supporting evidence.
- Accepting a wording-only label experiment as evidence about an unmanipulated institutional effect.
- Demanding a specific method (SEM, topic model) instead of judging whether the goal and evidence match.
- Scoring "writing" by style alone without checking whether claims are supported.

See [references/review-rubric.md](references/review-rubric.md) for the full gate-by-gate rubric.
