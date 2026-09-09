---
name: communication-prose-revision
description: Revise communication and social-science prose to reduce formulaic AI-style language, defensive over-hedging, empty metadiscourse, vague agency, repetitive transitions, and uniform sentence rhythm while preserving claims, evidence, citations, numbers, constructs, and uncertainty. Use for 去AI感/降低AI味/减少防御性写作/academic humanization/学术润色. Do not optimize for AI-detector evasion or conceal AI use.
---

# Communication Prose Revision

## Purpose

Make communication and social-science writing sound like accountable scholarly
argument rather than generated scaffolding. The target is clearer intellectual agency,
not an “AI probability” score.

## Required start

1. Lock the permitted passage, language, intervention level, claims, evidence, numbers,
   citations, constructs, terminology, and causal strength.
2. Identify the section function and study design. A Methods sentence, Results sentence,
   and Discussion sentence should not be revised by the same stylistic rule.
3. Read [references/prose-diagnostics.md](references/prose-diagnostics.md) for the smell
   taxonomy. Read [references/defensive-writing.md](references/defensive-writing.md)
   when the main problem is over-qualification or claim burial. Read
   [references/section-sensitive-editing.md](references/section-sensitive-editing.md)
   for full-section or manuscript passes.

## Revision passes

1. **Remove scaffolding:** delete generic scene-setting, throat-clearing, redundant
   previews, and transitions that add no logical relation.
2. **Recover the claim:** place the substantive proposition early and name the actor,
   process, comparison, or evidence responsible for it.
3. **Calibrate commitment:** keep the one hedge required by design and uncertainty;
   remove stacked hedges, disclaimer chains, and defensive self-protection.
4. **Repair paragraph logic:** one controlling claim, evidence and interpretation in
   the appropriate order, a real bridge to the next paragraph.
5. **Vary rhythm by function:** vary sentence length and structure because reasoning
   requires it, not by cosmetic synonym swapping or random sentence splitting.
6. **Restore scientific fidelity:** compare before/after claims, numbers, citations,
   causal verbs, populations, limitations, and nonclaims.

## Defensive writing rule

Do not confuse caution with vagueness. Good qualification names the exact boundary:
sample, design, measurement, uncertainty, or context. Defensive writing delays or
obscures a claim through generic caveats, repeated “may/might/could,” anonymous
authority, excessive citation shielding, or apologies before evidence.

Prefer:

```text
Claim → evidence or reasoning → exact boundary
```

over:

```text
General caveat → literature shield → method apology → tentative claim → another caveat
```

## Non-negotiable boundaries

- Never remove null, adverse, failed, or contradictory evidence to sound confident.
- Never strengthen association into causation, possibility into evidence, or a measured
  path into a demonstrated mechanism.
- Never delete limitations that materially bound interpretation; relocate and specify
  them when necessary.
- Never fabricate authorial voice. Use user-approved writing samples only as structural
  evidence and do not copy their sentences.
- Never claim text is “human-written,” predict detector outcomes, or help conceal
  required AI-use disclosure.
- Do not replace every repeated technical term with a synonym; construct stability is
  more important than lexical variety.

## Audit tool

Run the optional local diagnostic before and after revision:

```bash
python scripts/audit_prose.py manuscript.md
```

It reports line-located rhetorical patterns, not authorship or detector probabilities.
Treat every flag as a review candidate, not an automatic edit.

## Output

Return the revised passage plus a concise ledger of deleted scaffolding, strengthened
agency, hedge changes, paragraph repairs, and preserved scientific boundaries. If a
sentence cannot be made more direct without changing the scientific claim, keep it and
state why.
