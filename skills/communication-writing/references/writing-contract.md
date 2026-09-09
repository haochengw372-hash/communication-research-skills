# Communication writing contract

## Source hierarchy

Use current accepted materials in this order:

1. frozen research question, construct definitions, estimand, and design;
2. verified results, tables, figures, diagnostics, and analysis logs;
3. claim-verified literature matrix and reference library;
4. approved outline, journal requirements, terminology, and style decisions;
5. prior prose only when it remains consistent with items 1–4.

Historical chat, memory, filenames, and polished prior paragraphs are context, not
authority.

## Writing packet

```json
{
  "schema_version": "communication-writing-packet/v1",
  "document_id": "stable-id",
  "stage": "draft",
  "document_type": "research-article",
  "design_family": "experiment",
  "language": "en",
  "target_venue": "to-be-verified",
  "source_of_truth": ["results/table-1.csv", "analysis/model.json"],
  "required_sections": ["Introduction", "Methods", "Results", "Discussion"],
  "claims": [
    {
      "id": "C001",
      "status": "verified",
      "section": "Results",
      "evidence": ["R001"],
      "boundary": "sample and design boundary",
      "required": true
    }
  ],
  "numbers": [
    {"id": "N001", "value": "327", "source": "R001", "required": true}
  ],
  "terms": [
    {"canonical": "news credibility", "forbidden": ["media trust"]}
  ],
  "nonclaims": ["No population prevalence claim"]
}
```

The JSON is a minimal interchange format, not a replacement for project governance.
For each claim, preserve its status, exact evidence source, boundary, and intended
section. `verified` means an accountable researcher or accepted audit has checked the
support; model fluency does not set that status.

In the auditable Markdown source, place hidden `<!-- claim:C001 -->` and
`<!-- number:N001 -->` markers beside the supported sentence or number. Keep them in
the source-of-truth manuscript; a rendered delivery copy may omit comments only after
the ledger and manuscript locators have passed final audit.

## Extended outline

For every planned paragraph record:

```text
Section / paragraph:
Reader function:
Controlling claim:
Authorized evidence IDs:
Epistemic status:
Inference boundary or nonclaim:
Bridge to the next paragraph:
```

Do not draft a paragraph whose controlling claim lacks authorized evidence unless its
function is explicitly theoretical, hypothetical, procedural, or a limitation.

## Change ledger

For revisions record location, change type, reason, evidence affected, downstream
sections requiring synchronization, and verification result. Scientific changes
(construct, sample, estimand, model, result, or claim strength) return to the appropriate
research gate; the writer cannot approve them as stylistic edits.
