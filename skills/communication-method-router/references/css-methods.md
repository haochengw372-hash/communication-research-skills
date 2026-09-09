# Computational social science (CSS) method families

Companion to [method-goal-table.md](method-goal-table.md). These are the
general CSS method families behind the communication-specific routing. The
goal class always precedes method choice; a method is a candidate only when
the goal class and identification requirements are met.

| Method family | Goal class | Core assumptions to state | Common anti-pattern |
|---|---|---|---|
| Natural experiments / quasi-experiments | Causal identification | A real as-if-random shock; parallel trends; no spillover | Calling any before-after comparison a "natural experiment" |
| DiD / IV / RDD / matching | Causal identification | Instrument relevance and exclusion; discontinuity sharpness; ignorability | Adding covariates to "fix" identification instead of designing it |
| Network science (ERGM, community detection, diffusion) | Description, explanation | Boundary specification; tie meaning; sampling of the graph | Whole-network statistics used for node-level claims |
| Text-as-data (dictionaries, embeddings, topic models, LLM coding) | Description, measurement, prediction | Construct-to-text mapping validity; reliability | "There is text, so LDA" before defining the construct |
| Agent-based / generative simulation | Simulation explanation | Micro-rule realism; calibration; sensitivity across seeds | Uncalibrated simulation presented as empirical evidence |
| Online / field experiments, A/B | Causal identification | Randomization; no interference (SUTVA); attrition | Ignoring network interference or multiple testing |
| Digital trace / passive sensing | Description, measurement | Representativeness; known data-generating process | Treating platform trace data as population-representative |
| Multilevel and panel models | Explanation | Nesting structure; time dependence; within/between separation | Ignoring clustered or temporal dependence |
| Supervised ML and causal ML | Prediction, heterogeneous effects | Leakage control; honest train/test split; overlap | Confusing predictive accuracy with causal validity |
| Measurement models (IRT, CFA, invariance) | Measurement | Dimensionality; reliability; cross-group invariance | Using unvalidated translations or ad hoc scales |
| Data donation / privacy-preserving access | Description, measurement | Informed consent; self-selection bias of donors | Ignoring donor bias and treating donation as a census |
| Temporal process analysis (time series, event history, sequences) | Description, explanation, prediction | Clock, risk set, aggregation, lags, censoring, dependence | Treating a before/after pattern or lag as causal identification |
| Multimodal analysis (image, video, audio, OCR/ASR, VLMs) | Description, measurement, prediction | Unitization; extraction error; construct validity; modality loss | Reducing media to transcripts or model labels without validation |
| Spatial/GIS analysis | Description, explanation | Spatial unit, geocoding uncertainty, weights, MAUP, ecological boundary | Treating a hotspot or area-level relation as an individual causal effect |

## Decision order

1. Goal class (description / measurement / explanation / prediction / causal /
   simulation explanation).
2. Units, population, and target quantity.
3. Design family.
4. Analysis family.
5. Specialist Skill and its gate owner: content, network, causal, temporal,
   multimodal, spatial, simulation, experiment, or measurement.

Changing an earlier item invalidates the later choices; restart from the top
rather than patching the analysis.
