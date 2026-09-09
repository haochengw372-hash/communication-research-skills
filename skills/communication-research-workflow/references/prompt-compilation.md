# Prompt compilation

## Contents

1. Boundary and modes
2. Compilation procedure
3. Role templates
4. Formal prompt schema
5. Route-specific controls
6. Output and validation

## 1. Boundary and modes

Use this reference only when `target_role=prompt` or the user asks to write, improve, or compile a research prompt. Generate or revise the prompt; do not execute its research task.

- `standalone`: use only information in the current request. Do not read project files. Project identifiers may be omitted when irrelevant.
- `project-aware`: after explicit authorization, read only `.codex-research/project.yaml`, `state.yaml`, the named contract, and a necessary latest audit. Do not scan papers, data, code, or chat history.

If project identity, active contract, authority, source-of-truth, estimand, or final deliverable remains materially ambiguous, ask at most three short questions. Do not invent missing facts. Audit prompts may not retain unresolved placeholders.

## 2. Compilation procedure

1. State the concrete outcome for the next task.
2. Choose one primary `task_type` by deliverable, not keyword.
3. Select the target role and safest compatible `operation`, `rigor`, and `authority`.
4. Name authoritative inputs, required reads, allowed reads, prohibited reads/writes, and exact write scope.
5. Lock relevant sample, field, key, time window, estimand, identification, or manuscript constraints.
6. Define verifiable deliverables, quality gates, stop conditions, uncertainties, and handoff requirements.
7. Remove generic exhortations and unnecessary Skill lists. Let the orchestrator select the smallest sufficient specialist stack.
8. Return the prompt only. Do not perform any step inside it.

## 3. Role templates

- `controller`: create or revise contracts, validate handoffs, update authoritative state, record decisions, or freeze snapshots. It is the only governance-state writer.
- `prompt`: compile another prompt; use `plan` or `diagnose` with `read-only`. Never execute research.
- `executor`: perform one bounded work package. Require authoritative inputs, `必须读取`, `允许读取`, a non-overlapping `写入范围`, deliverables, fresh verification, and an immutable handoff. Never update governance state.
- `auditor`: use `operation=review`, `rigor=audit`, and `authority=read-only`. The audited object remains read-only; only a contract-named report under `audits/` and handoff under `handoffs/` may be created.

Roles are types, not a fixed number of tasks. A project may have multiple executor and auditor instances.

## 4. Formal prompt schema

The first non-empty line must be exactly:

```text
Use $communication-research-workflow.
```

Then include the applicable fields:

```text
prompt_mode=standalone | project-aware
project_id=...
task_id=...
target_role=controller | prompt | executor | auditor
state_revision=...

Project and stage: ...
Goal: ...
task_type=...
operation=diagnose | plan | execute | review | full-pipeline
rigor=quick | standard | audit
authority=read-only | edit-existing | create-new

Authoritative materials: ...
Task contract: ...
Required reads: ...
Allowed reads: ...
Prohibited reads or writes: ...
Write scope: ...
Locked definitions: ...
Deliverables: ...
Quality gates: ...
Special constraints: ...
Mandatory pause conditions: ...
Unverified facts: ...
Handoff requirements: ...
```

Do not recursively invoke a prompt-compilation Skill inside the generated prompt. Do not duplicate control fields. `plan`, `review`, and `diagnose` are read-only. `execute` and `full-pipeline` require explicit write authority.

## 5. Route-specific controls

- Research question: analysis unit, outcome, mechanism, context/time, competing explanations, falsifiability, feasibility, and gap—contribution—feasibility gate.
- Literature: databases, fields, dates, languages, document types, inclusion/exclusion, deduplication, search log, evidence matrix, and candidate-versus-verified distinction.
- Scientometrics/network: source IDs, entity mapping, time field/window, node/edge semantics, direction, duplicates, self-loops, pagination, coverage, and mapping confidence.
- Data audit: authoritative version, unit, keys, fields, missingness, duplicates, exclusions, row transitions, derivation lineage, and invariants.
- Empirical analysis: population, sample, treatment/comparison/outcome, estimand, identification, model, uncertainty, clustering/weights, diagnostics, robustness, and causal-language boundary. For PSM, also lock treatment timing, ATT/ATE/ATC, control pool, support, algorithm, caliper, replacement, weights, and outcome window. For two-stage work, lock each risk set and denominator separately.
- Code: raw data read-only, output location, tests, environment, versions, seeds, commands, logs, idempotence, and no silent overwrite.
- Figures: authoritative data → analysis script → plotting data → figure → caption lineage; verify samples, weights, estimates, intervals, axes, units, and denominators.
- Writing/revision: allowed sections, length, terminology, numbers, sample, figure/table identifiers, citations, and immutable content.
- Review/audit: Critical/Major/Minor findings with location, evidence, consequence, and recommendation; do not edit the reviewed artifact.
- Journal fit: current official source and date, scope, recent articles, article type, constraints, policies, fees, and submission requirements; do not mix ranking systems.
- Citation finalization: verify both source existence and exact claim support, then bidirectional in-text/reference consistency.
- Continuation/governance: uniquely identify project, contract, state revision, authoritative inputs, dependencies, write scope, handoff, and freeze conditions.

## 6. Output and validation

Default to one standard prompt in a code block. Optionally add no more than three concise notes explaining consequential choices. Never continue by executing the prompt.

For a saved formal prompt, run `scripts/validate_research_prompt.py`. Treat validation as a structural safety check, not a substitute for human judgment about the research design.
