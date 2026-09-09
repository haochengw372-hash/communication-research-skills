# Goal-to-method mapping

## Goal classes and their licenses

| Goal class | The design must establish | The design may NOT claim |
|---|---|---|
| Description | Distribution, prevalence, patterns | Mechanisms or causes |
| Measurement | Construct validity, reliability | Level differences between unmeasured groups |
| Explanation | Mechanism path consistent with theory and data | The path is causal without identification |
| Prediction | Out-of-sample performance, calibration | Causes of the outcome |
| Causal identification | Exchangeability/randomization/identification | Generalization beyond design limits without argument |
| Simulation explanation | Micro rules reproduce macro patterns under varied parameters | The rules are the true human process without calibration evidence |

## Text and platform data

| Task | Methods | Gate owner |
|---|---|---|
| Describe corpus content | Descriptive statistics, topic discovery, close reading of exemplars | communication-content-analysis |
| Measure a predefined construct in text | Dictionary, embedding distance, supervised classifier, LLM coding with reliability | communication-content-analysis + communication-construct/scale |
| Explain diffusion or cascade | Network measures, temporal models, exposure-response designs | communication-network-analysis + communication-temporal-analysis |
| Predict platform outcomes | Supervised models with time-split validation | communication-content-analysis |
| Causal effect of a platform intervention | RCT/natural or quasi-experiment on platform | communication-experiment + communication-causal-inference |
| Audience/behavior mechanism | Survey experiment, vignette, conjoint, panel survey | communication-experiment |
| Analyze image/video/audio communication | OCR/ASR, computer vision, embeddings, multimodal coding/fusion | communication-multimodal-analysis |
| Analyze change, timing, or trajectories | Time series, panel, event history, sequence models | communication-temporal-analysis |
| Analyze geographic concentration or diffusion | GIS, spatial autocorrelation/regression, spatiotemporal models | communication-spatial-analysis |
| Test micro-to-macro mechanism sufficiency | ABM, opinion dynamics, generative/LLM-agent simulation | communication-simulation |

## Analysis families by target quantity

| Target quantity | Typical family | Precision required before fitting |
|---|---|---|
| Construct level in a group | Measurement model | Unidimensionality, invariance if comparing |
| Relation between constructs | Regression/structural model | Design identifies the relation |
| Conditional effect | Moderation | Analytic power and centered interpretation |
| Indirect effect | Mediation | Temporal order and no unobserved confound |
| Treatment effect | Experimental or quasi-experimental estimator | Assignment mechanism and attrition |
| Emergent pattern | Simulation/ABM/LLM agents | Calibration, held-out validation, alternatives, sensitivity, seeds |

## Decision order

1. Goal class.
2. Units and population.
3. Target quantity.
4. Design family.
5. Analysis family.
6. Specialist Skill and gates.

Changing any earlier item invalidates the later choices; return to the top instead of patching the analysis.
