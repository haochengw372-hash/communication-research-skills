# Communication specialist Skill registry

## Registry rules

- This registry records preferred routing, not guaranteed availability. Check the current session's Skills catalog before invocation.
- Use the smallest sufficient stack, normally one orchestrator plus one to three specialists.
- Read and obey every selected Skill. If two Skills conflict, follow higher-level user/system constraints and the stricter integrity rule.
- Never fabricate a Skill name, silently install a missing Skill, or treat a similar name as identical.
- Trust labels describe provenance/inspection status, not output correctness. All outputs still pass task gates.

## Installed suite routes

The current suite installs eighteen Skill folders. The orchestrator and domain Skills may appear together or alone:

| Need | Preferred Skill |
|---|---|
| Multi-stage orchestration, contracts, handoffs, freezes | `communication-research-workflow` |
| Literature search, screening, evidence matrix | `communication-literature` |
| Theory selection and mechanism audit | `communication-theory` |
| Construct existence, disambiguation, definition lock | `communication-construct` |
| Validated scale location, adaptation, invariance | `communication-scale` |
| Goal-first method selection | `communication-method-router` |
| Survey/online/HMC experiment design | `communication-experiment` |
| Computational content analysis and coding | `communication-content-analysis` |
| Networks, diffusion, communities, ERGM, SAOM | `communication-network-analysis` |
| Natural/quasi-experiments and causal identification | `communication-causal-inference` |
| Time series, panels, event history, sequences | `communication-temporal-analysis` |
| Image, video, audio, OCR/ASR, multimodal models | `communication-multimodal-analysis` |
| GIS, spatial dependence, geographic diffusion | `communication-spatial-analysis` |
| ABM, opinion dynamics, generative/LLM-agent simulation | `communication-simulation` |
| Evidence-bound manuscript drafting, revision, synchronization, rebuttal | `communication-writing` |
| Formulaic prose, defensive over-hedging, rhythm, and intellectual agency | `communication-prose-revision` |
| Seven-gate review and audit | `communication-reviewer` |
| Legal full-text acquisition and archiving | `scholarly-access` |

## General fallback routes

When a communication specialist is unavailable, do not invent a replacement. Continue with the closest general Skill present in the session, or mark the work `needs-specialist`:

| Need | Fallback logic |
|---|---|
| Statistical estimation | any audited statistical-analysis Skill present; state the estimand before choosing a model |
| Text/NLP engineering | a coding environment plus the communication content-analysis protocol; never skip reliability |
| Qualitative analysis | explicit protocol, codebook, reflexivity, and negative-case checks even without a named specialist |
| Reference management | Zotero connector/Skill when present; external writes require explicit authority |
| Final verification | fresh command reruns and artifact hashes before completion claims |

## Optional third-party Skills

No third-party Skill is a dependency of this workflow. Evaluate optional Skills outside the installed package: inspect every file, record permissions/network/dependencies, run the available security vetting process, and obtain separate user approval before installation. Add one only for a demonstrated coverage gap, not because a larger stack appears more comprehensive.

## Fallback behavior

If a preferred Skill is missing:

1. continue with the closest already available specialist when safe;
2. state the capability gap only if it affects quality or completion;
3. search for or suggest installation only when needed for the task;
4. never lower evidence, truthfulness, or verification standards to compensate.
