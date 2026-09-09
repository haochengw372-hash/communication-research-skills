---
name: communication-content-analysis
description: Plan and audit computational content analysis of communication, media, and platform text for corpus construction, sampling, codebooks, dictionary/embedding/topic models, supervised classification, LLM-assisted coding, reliability, validation, and reporting. Use for content analysis, computational text, coding, reliability, 内容分析/计算内容分析/编码/信度/语料库/LLM编码. Do not use for construct definition or scale work, which route to communication-construct and communication-scale.
---

# Communication Content Analysis

## Overview

This Skill runs content analysis as measurement, not as file processing. Corpus, units, codebook, reliability, and validation are decided before any model is run, and automated labels are treated as measures whose quality must be demonstrated.

## Required start

1. Confirm the construct or descriptive target with communication-construct/communication-scale when the analysis claims measurement.
2. Write the corpus contract before collecting data.
3. Decide the unit before choosing a model.

## Corpus contract

```text
Platform/source and collection method:
Time window and sampling strategy:
Deduplication rule:
Language and translation handling:
Unit definition (message/article/post/thread/turn):
Population and exclusions:
Licensing, ToS, and ethics boundaries:
Provenance record:
```

Sampling must be justified against the population the claim targets. A convenience corpus can describe itself but cannot stand in for a population.

## Codebook and labels

- Define units, dimensions, categories, and unitizing rules.
- Give examples and non-examples for each category.
- Separate the codebook (construct definitions) from the coding instructions (how to apply them).
- For human annotation: coder training, independence, disagreement resolution logged.
- For LLM-assisted coding: record model, prompt version, date, temperature, few-shot examples, sample records, and a human-verified subset; never present raw LLM output as validated labels.

## Reliability

- Choose the agreement statistic appropriate to the design (e.g., Krippendorff's alpha for multi-coder nominal/ordinal content; Cohen's kappa or percent agreement only with justification).
- Report reliability on a random sample separate from training; do not report training agreement as study reliability.
- Report the final coded dataset's reliability, not only the pilot.
- When LLM coding is used, report agreement between LLM and human reference set and the human-verified sample size, and state the claim boundary.

## Method selection within the goal

| Task | Prefer | Avoid unless validated |
|---|---|---|
| Predefined narrow construct | Dictionary or supervised classifier with validation | Topic model |
| Discovering latent topical structure | Topic model (LDA/STM/BERTopic) with diagnostics | Pretending topics are constructs |
| Continuous similarity | Embeddings with explicit reference texts | Raw nearest-neighbor claims |
| Reproducible coding at scale | LLM coding with human verification or supervised classifier | Unvalidated LLM labels |
| Comparing meanings across time/platform | Matched corpora and invariance checks, not raw frequency | Frequency = meaning change |

## Validation layers

1. Software: sample checks, unit/schema checks, expected failures.
2. Method: model diagnostics, reliability, leakage controls, time-split splits for prediction.
3. Substantive: close reading of exemplars, known cases, negative controls, face validity against theory.
4. Robustness: alternative preprocessing, seeds, thresholds, corpus boundaries.

## Output shape

End with: corpus table and provenance, codebook, reliability results, validation plan, label-claim mapping, and the claims the analysis can and cannot support.

## Common anti-patterns

- Running a topic model on all text because "it is text".
- Reporting model fit (perplexity/coherence) as if it validated a construct.
- No leakage control when supervised labels come from the same time window being predicted.
- Training and reliability on the same coded set.
- Interpreting frequency, co-occurrence, or classifier accuracy as meaning, causality, or public opinion.
- Downloading platform data without checking license/ToS and privacy boundaries.

See [references/content-analysis-protocol.md](references/content-analysis-protocol.md) for the corpus/codebook/protocol template.
