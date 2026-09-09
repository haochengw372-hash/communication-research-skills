---
name: communication-construct
description: Check whether a communication construct already exists, disambiguate overlapping names and definitions, and lock a definition before measurement. Use for construct identification, conceptual definition, construct disambiguation, and avoiding ad hoc invented constructs (构念界定/构念查重/消歧/避免造概念). Do not use for scale psychometrics, which routes to communication-scale.
---

# Communication Construct

## Overview

This Skill runs the Construct Gate: it prevents "perceived X-ness" invention, same-construct-different-name drift, and construct-name instability across a manuscript.

## Required start

Before proposing a construct, search in this order:

1. published construct inventories and measurement reviews in communication;
2. scale-development papers and appendices (a construct with a validated scale almost always exists under some name);
3. theoretical and review articles that name the construct and its neighbors;
4. adjacent fields only after communication sources are exhausted, and only with an adaptation argument.

If the term does not exist but the concept is described under another name, the search result is a rename or merge, not a new construct.

## Disambiguation rules

- Same construct, different names: prefer the name with the canonical definition and scale literature; record synonyms.
- Same name, different constructs: distinguish by definition, dimensions, and measurement family; do not merge because the labels match.
- Construct vs proxy: a behavioral proxy (e.g., clicking, sharing, viewing time) is not the construct unless a validity argument connects them.
- Construct vs operationalization: one construct may have several admissible operationalizations; changing the operationalization does not change the construct and does not license changing the definition.

## Definition-lock format

Lock each construct as:

```text
Construct:
Canonical citation:
Definition:
Dimensions (if multidimensional):
Closest neighbors and discriminant boundary:
Allowed measurement families:
Forbidden substitutions:
```

The same definition must then appear unchanged in theory, method, results, and discussion.

## Verdicts

Return one verdict with evidence paths:

- `EXISTING` — use the established name, definition, and scale; no new construct needed.
- `RENAME` — the concept exists under another name; adopt the canonical name and cite it.
- `MERGE` — two proposed constructs are the same; keep one definition and record the discarded term.
- `NEW-CONSTRUCT-JUSTIFIED` — only after the search: a demonstrated theoretical gap, a definition distinct from every neighbor, and a discriminant-validity plan.

A new construct without all three conditions is a label, not a contribution.

## Output shape

End with: the searched sources, the closest existing constructs with citations, the definition-lock entries, and the verdict for every proposed construct in the study.

## Common anti-patterns

- Inventing "perceived X" because the measure was a Likert item.
- Renaming a construct between introduction, method, and results to fit the finding.
- Importing a construct from psychology or computer science without arguing that its definition transfers.
- Treating a measurement instrument as the construct's definition.
- Counting a synonym search failure as evidence of novelty.

Use [references/construct-checklist.md](references/construct-checklist.md) when the construct set is large or the discriminant boundaries are contested.
