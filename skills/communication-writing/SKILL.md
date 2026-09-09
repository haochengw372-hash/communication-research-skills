---
name: communication-writing
description: Draft, revise, synchronize, and finalize communication and social-science manuscripts from verified research materials. Use for 传播学/社会科学论文写作, titles, abstracts, introductions, theory and literature sections, methods, results, discussions, conclusions, bilingual Chinese-English revision, reviewer responses, and submission packages. Do not invent evidence, results, citations, methods, or venue requirements.
---

# Communication Writing

## Purpose

Turn verified communication-research materials into a coherent manuscript without
letting fluent prose outrun theory, design, evidence, or uncertainty. Writing is a
research-integration stage, not a substitute for missing analysis.

## Required start

1. Identify the document type, study design, target audience/venue, language, carrier,
   requested sections, length, and permitted evidence.
2. Read the current research contract and accepted handoffs when they exist. Reject
   stale outputs and conflicting versions before drafting.
3. Build the writing packet in
   [references/writing-contract.md](references/writing-contract.md): claim–evidence
   ledger, number ledger, terminology lock, nonclaims, and section plan.
4. Label missing support `UNVERIFIED` or `AUTHOR_INPUT_NEEDED`; never fill it with
   plausible prose.

## Modes

- **Plan:** produce the storyline, contribution logic, extended outline, and evidence
  allocation without drafting the full paper.
- **Draft:** write a new section or manuscript only from authorized evidence.
- **Revise:** preserve scientific meaning, numbers, citations, equations, and locked
  terms while changing the requested scope.
- **Synchronize:** propagate an accepted change across abstract, main text, tables,
  figures, supplements, metadata, and responses.
- **Respond:** map each reviewer request to a decision, manuscript change, evidence,
  locator, and unresolved risk.
- **Finalize:** run consistency, citation, disclosure, anonymization, and submission
  checks; final submission still requires human approval.

## Writing sequence

1. Write one sentence stating the paper's problem or puzzle, one stating the mechanism,
   and one stating the evidence-backed contribution.
2. Map every planned paragraph to a reader function, claim, authorized evidence,
   inference boundary, and bridge to the next paragraph.
3. Draft sections using
   [references/section-logic.md](references/section-logic.md). Use the design-specific
   rules in [references/design-specific-writing.md](references/design-specific-writing.md).
4. Keep results and interpretation separate unless the genre explicitly combines them.
5. Run `communication-prose-revision` when the draft needs a dedicated anti-formulaic
   or defensive-writing pass; preserve the writing packet and change ledger.
6. Run a top-down audit (problem → RQ/H → design → evidence → contribution) and a
   bottom-up audit (evidence → result → interpretation → abstract/conclusion).
7. Use `communication-reviewer` for independent review; the writer does not self-certify
   a manuscript as scientifically sound.
8. Apply [references/revision-submission.md](references/revision-submission.md) for
   rebuttals, journal adaptation, and submission artifacts. Apply
   [references/bilingual-writing.md](references/bilingual-writing.md) when translating or
   writing across Chinese and English.

## Evidence and prose rules

- Preserve `evidence`, `inference`, `hypothesis`, `recommendation`, and `unverified` as
  different epistemic states.
- Report null, mixed, adverse, and failed results when they belong to the accepted
  record. Non-significance is not equivalence.
- Keep causal verbs within the identification design and population boundary.
- Use citations for the exact proposition they support; a real source can still be a
  false citation.
- Do not introduce a new construct, mechanism, robustness result, sample exclusion, or
  limitation repair during prose editing.
- Prefer precise, readable sentences over inflated formality, generic transitions,
  novelty hype, or cosmetic synonym replacement.

## Deterministic check

For Markdown drafts with a writing packet, run:

```bash
python scripts/check_manuscript.py manuscript.md writing-packet.json
```

This local, dependency-free check validates required sections, claim and number markers,
evidence status, terminology locks, and unresolved placeholders. It does not verify the
truth of evidence or replace a full manuscript audit.

## Output

Return the requested manuscript artifact plus a compact change/evidence report: sections
written, authoritative inputs, unresolved support, consistency checks run, and the next
human or auditor decision. Never label a draft submission-ready while any critical
evidence, authorship, ethics, declaration, or venue requirement is unresolved.
