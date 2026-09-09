---
name: communication-multimodal-analysis
description: Design and audit image, video, audio, OCR, ASR, computer-vision, embedding, and multimodal communication analysis with explicit units and human validation. Use for 视觉传播/视频分析/音频分析/多模态/计算机视觉/OCR/ASR. Do not reduce visuals or speech to extracted text when form is part of the claim.
---

# Communication Multimodal Analysis

## Overview

This Skill treats modality as evidence, not preprocessing debris. It defines what is
lost when image, sound, speech, motion, layout, or cross-modal relations are transformed
into model features.

## Required start

1. State the communication construct and whether it resides in one modality or in the
   relation among modalities.
2. Define sampling, unitization, temporal segmentation, and provenance with
   [references/multimodal-protocol.md](references/multimodal-protocol.md).
3. Separate extraction quality (OCR/ASR/detection) from substantive coding validity.

## Method routing

- OCR and ASR recover text/speech but require error audits by language, accent, noise,
  typography, and platform format;
- object/face/logo detection measures specified visual entities, not meanings;
- visual/audio embeddings support similarity or retrieval with reference cases;
- scene, shot, speaker, gesture, prosody, and temporal features require explicit
  segmentation rules;
- early/late/joint multimodal fusion must match the theoretical cross-modal relation;
- LLM/VLM coding requires versioned prompts and a human reference set.

## Validation

Validate unit boundaries, extraction error, annotation reliability, subgroup/model bias,
known cases, negative controls, cross-platform compression, and robustness across
models, thresholds, frames, and transcript variants. Preserve original media locators
and transformation provenance.

## Output shape

Return the multimodal corpus contract, unit/segment definitions, feature or codebook
lineage, extraction and substantive validation results, bias/ethics review, robustness
plan, and claim boundaries.

## Hard boundaries

- Detected objects, faces, emotions, or topics are measures, not ground truth.
- A transcript cannot support claims about visual rhetoric, timing, or prosody.
- Frame sampling can miss transitions and short-lived content.
- Model similarity does not establish shared meaning.
- Biometric or identity inference requires necessity, lawful basis, and heightened review.
