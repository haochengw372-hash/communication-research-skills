# Multimodal analysis protocol

## Corpus and unit contract

```text
Platform/source, collection procedure, dates, and license:
Media types, formats, codecs, and transformations:
Population, sampling frame, and exclusions:
Unit: item/frame/shot/scene/speaker/turn/audio window/layout region:
Segmentation and frame/audio sampling rule:
Languages, captions, OCR, ASR, and translation:
Cross-modal relation being measured:
Model/version/prompt/threshold provenance:
Human reference sample and reliability statistic:
Privacy, identity, biometric, and sensitive-content handling:
```

## Validation layers

1. **File/media:** corruption, duration, resolution, sampling, duplicate/repost handling.
2. **Extraction:** OCR word error, ASR error, detection precision/recall, segmentation.
3. **Measurement:** construct validity, coder agreement, subgroup and language error.
4. **Cross-modal:** whether agreement, contradiction, timing, or dominance is preserved.
5. **Robustness:** alternative models, thresholds, samples, frames, transcripts, prompts.

## Method-selection table

| Target | Candidate method | Invalid shortcut |
|---|---|---|
| Visible entities | detector/manual annotation | assuming detection equals salience |
| Visual rhetoric or framing | validated codebook plus close reading/model assistance | object counts alone |
| Speech content | ASR plus transcript validation | unaudited transcript |
| Prosody/emotion display | acoustic features plus human reference | universal emotion inference |
| Cross-modal meaning | aligned multimodal coding/fusion | concatenating features without a mechanism |
| Similarity/retrieval | embeddings plus reference-set evaluation | nearest neighbors as substantive truth |
