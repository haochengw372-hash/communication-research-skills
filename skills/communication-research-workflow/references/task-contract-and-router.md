# Task contract and router

## Contents

1. Contract field rules
2. Task type router
3. Authority precedence
4. Long-task state
5. Pause protocol

Before applying the generic task types below, classify the research goal with [communication-router.md](communication-router.md) and record the phenomenon, goal class, and specialist stack. For a computational communication request, also read [communication-ontology.md](communication-ontology.md) so the contract names the reasoning-graph position (theory, construct, measurement, design, evidence) rather than only the deliverable.

## Contract field rules

| Field | Rule |
|---|---|
| `task_type` | Use one task type below; use the deliverable and decision risk, not keywords alone. |
| `schema_version` | Use `codex-research-contract/v1` for project-aware contracts; legacy standalone contracts remain valid. |
| `project_id`, `task_id` | Stable project identity plus a unique work-package identity. |
| `target_role` | `controller`, `prompt`, `executor`, or `auditor`; role types may have multiple instances except controller. |
| `state_revision`, `contract_version` | Integer versions used to detect stale work and revised contracts. |
| `goal` | One concrete outcome for the current run. |
| `operation` | `diagnose`, `plan`, `execute`, `review`, or `full-pipeline`. |
| `rigor` | `quick` for exploratory triage, `standard` by default, `audit` for causal claims, formal review, submission, or high-risk evidence. |
| `authority` | `read-only`, `edit-existing`, or `create-new`; authority does not imply permission to write externally. |
| `source_of_truth` | Record authoritative paths/IDs/versions plus keys, fields, sample, estimand, and time window when applicable. If unknown, state `to-be-verified` and add uncertainty. |
| `materials` | Only inputs necessary and allowed for this task. |
| `input_artifacts` | Exact control or research artifacts that must be read before work. |
| `deliverables` | Named answers/artifacts and formats; distinguish diagnostic evidence from production output. |
| `quality_gates` | Route checks plus the six hard gates. |
| `constraints` | Word count, journal, method, language, deadline, output and “must not change” conditions. |
| `stop_conditions` | Decisions that cannot be safely inferred. |
| `uncertainties` | Time-sensitive, inaccessible, ambiguous, or not-yet-verified facts. |
| `return_handoff` | Boolean; normally true for non-controller project work. |

Do not block on harmless omissions. Infer conservatively, mark uncertainty, and continue read-only work. Ask only when a missing choice would change the research question, evidence base, result meaning, external state, or final deliverable.

## Task type router

| `task_type` | Signals | Workflow reference |
|---|---|---|
| `research-question` | topic, RQ, hypothesis, novelty, feasibility | research-workflows |
| `literature-review` | search, screening, synthesis, evidence matrix | research-workflows |
| `scientometrics-network` | OpenAlex/Overton IDs, linking, coverage, citation graph | research-workflows |
| `data-audit` | schemas, keys, variables, missingness, exclusions | empirical-workflows |
| `empirical-analysis` | estimand, identification, model, PSM/ATT, robustness | empirical-workflows |
| `computational-content-analysis` | corpus, codebook, LLM/human coding, reliability, construct-validity of text labels | empirical-workflows + communication-content-analysis |
| `network-analysis` | graph boundary, ties, diffusion, communities, ERGM/SAOM, relational events | empirical-workflows + communication-network-analysis |
| `causal-inference` | intervention, counterfactual, DiD/IV/RDD/matching/synthetic control | empirical-workflows + communication-causal-inference |
| `temporal-analysis` | time series, panels, event timing, sequences, change points | empirical-workflows + communication-temporal-analysis |
| `multimodal-analysis` | image/video/audio units, OCR/ASR, vision or multimodal coding | empirical-workflows + communication-multimodal-analysis |
| `spatial-analysis` | GIS, geocoding, spatial dependence, geographic diffusion | empirical-workflows + communication-spatial-analysis |
| `simulation-study` | ABM, opinion dynamics, generative/LLM agents, calibration | empirical-workflows + communication-simulation |
| `experiment-survey` | stimuli, manipulation checks, randomization, power, HMC/AI-disclosure designs | social-science-workflows + communication-experiment |
| `qualitative-analysis` | case selection, interview/document corpus, coding, reflexivity, negative cases | social-science-workflows |
| `mixed-methods` | integration design, sequence, connecting samples, joint displays, meta-inferences | social-science-workflows plus the relevant empirical or qualitative route |
| `research-code` | reproducible analysis pipeline, tests, debugging | empirical-workflows |
| `research-visualization` | result tables, plots, manuscript figures | empirical-workflows |
| `writing-revision` | drafting, restructuring, constrained revision | writing-review-workflows |
| `manuscript-review` | peer review, internal audit, rebuttal planning | writing-review-workflows |
| `journal-fit` | venue selection, current indexing/rank/scope | writing-review-workflows |
| `citation-finalization` | bibliography, claim-source audit, submission package | writing-review-workflows |
| `project-continuation` | “continue”, prior state, ambiguous project/history | research-workflows, then the destination workflow |
| `project-governance` | initialize, task graph, handoff, merge, freeze, window roles | project-coordination |

If several types apply, choose the type matching the current deliverable and list secondary routes. For a mixed-methods project, do not force every work package into `mixed-methods`: use that type for integration work, and route strand-specific work to its actual task type. `full-pipeline` is an operation, not a task type.

## Authority precedence

Use the narrowest jointly satisfiable interpretation:

1. Explicit prohibition: “不要读/不要写/不要改/不要运行”.
2. Explicit operation: review or diagnose before execute.
3. Explicit material and section scope.
4. Explicit deliverable.
5. General urgency or convenience language.

Examples:

- “只评价，不实施；顺手改一下” resolves to read-only evaluation. Surface the conflict only if the user must choose.
- “诊断，不修复” permits read-only commands and non-mutating inspection, not source edits.
- “执行分析并创建结果” permits project-local artifacts, not uploads, Zotero writes, submissions, or external messages.

Before each write, ask internally: is this exact target and mutation authorized by both `operation` and `authority`? If not, stop that write.

## Long-task state

Use the project-local `.codex-research/state.yaml` only for authorized multi-turn execution. If an existing project uses another state/handoff protocol, follow the project's established source-of-truth rather than creating a duplicate.

```yaml
workflow_version: "0.1.0"
project_root: absolute path
task_type: registered type
operation: execute | full-pipeline
current_stage: short stage name
completed_artifacts:
  - path: absolute or project-relative path
    purpose: why it exists
source_of_truth:
  inputs: paths, IDs, and versions
  keys: entity/row keys
  sample: population and exclusions
  estimand: target quantity if applicable
  time_window: start/end rule if applicable
key_decisions:
  - decision: choice made
    basis: evidence or user instruction
unresolved:
  - issue: remaining uncertainty
next_action: smallest safe continuation step
latest_verification:
  command: exact command or check
  result: exit status and counts
  timestamp: ISO-8601 with timezone
```

Never put raw chat logs, full papers, credentials, or sensitive unpublished content in the state file.

## Pause protocol

When a pause condition is reached, report only:

1. verified current state;
2. the changed or ambiguous element;
3. why it changes interpretation or authority;
4. the smallest concrete choice needed;
5. safe work that has continued, if any.

Do not use “need confirmation” as a reason to abandon independent read-only checks.
