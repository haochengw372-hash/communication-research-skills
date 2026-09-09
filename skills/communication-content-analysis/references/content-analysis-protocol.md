# Content-analysis protocol template

## Corpus

```text
Population to which claims will be made:
Sampling frame actually collected:
Collection procedure and time:
Deduplication:
Unit definition and unitizing rule:
Language/translation:
Licensing/ToS/privacy review:
```

Record row-count transitions (retrieved → deduplicated → included → analyzed) with reasons.

## Codebook entry format

```text
Dimension:
Category/code:
Definition:
Examples:
Non-examples:
Boundary decision rule:
```

## Coding protocol

Human:

- coder training with practice sets;
- independent coding on a reliability sample;
- disagreement log and resolution rule;
- final reliability report.

LLM-assisted:

- model and version; prompt file path/version; date; temperature and seed;
- few-shot examples and their source;
- random human-verified sample with size and selection rule;
- agreement table between LLM and human reference;
- statement of what the LLM labels may be used for.

## Reliability reporting

```text
Statistic and justification:
Coders/LLM runs:
Sample size and selection:
Per-dimension result:
Final-dataset result:
Threshold and decision:
```

## Validation

- Negative controls: items that should NOT receive the code.
- Known cases: hand-verified exemplars the model must recover.
- Leakage check for supervised and LLM coding (timing, duplicates, near-duplicates).
- Robustness table for preprocessing/seed/threshold/corpus boundary.

## Claim map

For each planned claim, list: label/dimension used, reliability evidence, validation evidence, and the boundary of inference (corpus → population).
