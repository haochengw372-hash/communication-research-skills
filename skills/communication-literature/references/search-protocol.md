# Search-log and screening templates

## Search log (one block per query set)

```text
Question ID:
Object (journalism/platform/HMC/audience/discourse):
Databases searched:
Query strings (verbatim):
Date window:
Language rules:
Retrieved count:
Deduplicated count:
Exclusions applied at title/abstract/full-text with reasons:
Coverage limits:
```

## Screening decision rules

1. DOI deduplication, then normalized-title-plus-year deduplication.
2. Title screen: exclude only when the title is unambiguous for every inclusion criterion.
3. Abstract screen: apply inclusion/exclusion with one reason per exclusion.
4. Full-text screen: required for any source that will support a specific claim about design, sample, effect, or boundary.

## Evidence-matrix schema

Columns:

| Claim | Source | Design | Sample/context | Key result | Boundary | Support level |
|---|---|---|---|---|---|---|

Support levels:

- `direct` — source reports exactly this claim's empirical relation in a compatible design.
- `partial` — source supports a component or a weaker version.
- `indirect` — source is relevant background, not evidence for the claim.
- `contradicts` — source reports a finding that goes against the claim.

## Claim-support record

For every sentence that will carry an empirical or theoretical claim in the final text:

```text
Claim:
Source(s):
What the source actually reports:
Support level:
Unverified aspects:
```

Keep this record alongside the manuscript so the final claim map is auditable.
