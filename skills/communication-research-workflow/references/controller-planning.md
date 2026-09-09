# Controller planning and dynamic window design

## Contents

1. Controller outcome
2. Planning procedure
3. Window decision rules
4. Work-package contract
5. Rolling replanning
6. Controller prompt

## 1. Controller outcome

Keep exactly one long-lived controller per project. Have it propose the research lifecycle, work-package graph, window plan, audits, definition freezes, and decision points. Do not have it perform every research task or silently treat its first plan as authoritative evidence.

The controller may propose and compile windows. Do not automatically create Codex tasks, subagents, external messages, or files unless the user authorizes that action. A window plan is a reviewable proposal until the controller accepts it into project state.

## 2. Planning procedure

1. Identify the project boundary and distinguish the substantive topic from an answerable question.
2. Classify the study archetype using [social-science-workflows.md](social-science-workflows.md).
3. Record current evidence, unresolved definitions, data feasibility, target audience, ethics, and delivery constraints.
4. Build a directed acyclic graph of work packages. Separate tasks whose inputs, authority, specialist Skills, deliverables, verification, or context burden differ materially.
5. Label each proposed window as `Open now`, `Open later`, or `Not currently needed`.
6. Add independent audit packages for consequential design, confirmatory results, causal claims, final citations, and submission versions.
7. Present the plan, assumptions, and decisions that only the researcher can make.
8. Issue only the first one to three ready contracts. Keep later windows dormant.

Use the deterministic planner as a starting scaffold when an archetype is known:

```powershell
python scripts/plan_research_project.py --project-id example-project --archetype panel-longitudinal --format markdown
```

The script never opens tasks or changes project state. The controller must review and adapt its output.

## 3. Window decision rules

Always keep:

- one controller for project identity, contracts, decisions, freezes, and state merges;
- at least one bounded executor when research work is ready;
- an independent auditor whenever the contract or route requires one.

Use a prompt workbench only when the task is complex enough to benefit from reusable role prompts. It reads the control layer and current contract, not the full research corpus.

Open a new executor when at least one materially changes:

- authoritative inputs or source-of-truth;
- research stage or dependency boundary;
- specialist Skill stack;
- write authority or output location;
- deliverable and acceptance test;
- estimand, identification, or verification method;
- context size needed to work reliably.

Continue an existing executor for bounded iterations on the same artifact when definitions, authority, and verification stay unchanged.

Do not open all planned windows at project start. A typical project uses several stage windows over its lifetime while keeping only three to five active at once.

## 4. Work-package contract

Each planned package records:

```yaml
task_id: stable work-package ID
stage: research stage
target_role: executor | auditor
goal: one verifiable outcome
depends_on: accepted upstream packages
inputs: exact required artifacts
deliverables: named outputs
write_scope: non-overlapping authorized paths
skill_stack: preferred available specialist Skills
rigor: quick | standard | audit
audit_required: true | false
open_when: readiness condition
close_when: handoff and acceptance condition
stop_conditions: changes requiring controller decision
```

Parallelize only ready packages with non-overlapping write scopes. A task is not completed merely because its executor returned; required audit and current verification must pass.

## 5. Rolling replanning

After every accepted, rejected, blocked, or stale handoff:

1. verify the handoff, contract hash, artifacts, and state revision;
2. reassess the research question, constructs, evidence, data feasibility, sample, estimand, and identification;
3. mark newly ready packages and block invalidated downstream packages;
4. freeze consequential definitions or results;
5. issue revised contracts rather than letting executors refresh their own scope;
6. keep an explicit record of why the plan changed.

The researcher must decide changes to the primary question, target population, core construct, estimand, identification strategy, external write, or final submission. The controller may recommend but not silently decide them.

## 6. Controller prompt

```text
Use $communication-research-workflow.

Act as the sole controller for this project. Plan only; do not execute literature search,
data analysis, modeling, manuscript editing, or external writes.

Classify the study archetype, propose the research lifecycle and dependency graph, and
separate windows into Open now, Open later, and Not currently needed. For every proposed
window specify role, goal, dependencies, allowed inputs, write scope, deliverables,
specialist Skills, rigor, audit requirement, opening condition, closing condition, and
mandatory pause points. Recommend only the first one to three ready windows and provide
their contracts. Treat the plan as rolling and revise it only through controller decisions.
```
