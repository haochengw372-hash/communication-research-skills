# Project coordination: four role types, multiple task instances

## Contents

1. Control layer
2. Roles and ownership
3. Work-package graph
4. Handoff and merge protocol
5. Freeze and usage-audit protocol

## 1. Control layer

Use `.codex-research/` as a compact coordination layer. It references research artifacts in place and never duplicates raw papers, chats, credentials, or large datasets.

- `project.yaml`: stable project identity and boundary.
- `state.yaml`: current controller-owned authoritative state.
- `windows.yaml`: role permissions; roles are types, not a fixed count of tasks.
- `contracts/`: controller-issued work-package contracts.
- `handoffs/`: immutable returns from prompt, executor, or auditor instances.
- `audits/`: detailed audit reports.
- `snapshots/`: frozen governance snapshots at consequential changes.
- `decisions.md`: accepted decisions and their basis.

Start project-aware tasks by reading only `project.yaml`, `state.yaml`, the assigned contract, and the necessary latest audit. Read research materials only as the contract permits.

## 2. Roles and ownership

| Role type | Instances | May write | Must not write |
|---|---:|---|---|
| controller | exactly one | state, contracts, decisions, snapshots | unauthorized research results |
| prompt | zero or more | chat output or authorized handoff | research artifacts and governance state |
| executor | multiple work packages | contract-authorized outputs and handoff | state, contracts, decisions |
| auditor | multiple independent audits | a new report in `audits/` and a new immutable handoff in `handoffs/` | audited artifacts and governance state |

Use a new executor instance when inputs, specialist Skill stack, authority, deliverable, verification method, dependency boundary, or context burden changes materially. Continue the same instance for small iterations on the same artifact with unchanged source-of-truth and estimand.

## 3. Work-package graph

The controller models work as a directed acyclic graph. Each package records `depends_on`, status, contract, latest handoff, audit requirement, and a non-overlapping `write_scope`. Allowed statuses are `planned`, `draft`, `ready`, `in-progress`, `blocked`, `needs-decision`, `needs-audit`, `revision`, `stale`, `completed`, and `cancelled`.

Parallel execution is allowed only when packages have no unresolved dependency and no overlapping write scope. A package becomes `completed` only after its required audit and current validation pass. If an upstream frozen definition changes, mark dependent packages `blocked` or `revision`; never silently reuse downstream outputs.

## 4. Handoff and merge protocol

Before writing, compare contract `state_revision` to current state. On mismatch, stop mutation and return `status=stale` with both revisions. Do not refresh the contract locally.

Each handoff records project/task/role, state revision read, contract path and hash, unique filename, status, artifact paths and hashes, fresh verification, findings, inferences, uncertainty, needed decisions, and next action. Auditor handoffs also include verdict and Critical/Major/Minor findings.

For an auditor, `authority=read-only` means the audited object and all governance state remain read-only. The only write exception is the contract-named reporting sink in `audits/` plus its immutable `handoffs/` return. A completed handoff requires a non-empty fresh verification command/result and quality gate; an executor completion also requires at least one artifact. A stale handoff contains no research artifacts.

Only the controller merges a validated handoff. Merge steps:

1. validate structure, contract hash, artifact hashes, role authority, and state revision;
2. inspect audit verdict and unresolved decisions;
3. accept, reject, or issue a new contract version;
4. increment `state.revision` once and update the task graph;
5. record consequential decisions and create a snapshot when required.

## 5. Freeze and usage-audit protocol

Freeze a snapshot before or immediately after an approved change to primary RQ, source-of-truth, entity mapping, core field/key, sample/exclusions, estimand, identification, formal results, or submission version. A snapshot contains only governance definitions, artifact locators/hashes, and verification evidence.

After every five controller-accepted real work packages, review observed failures, unnecessary friction, trigger errors, state conflicts, and audit escapes. Add actual failures to repository evals before changing either Skill. The Skill never edits itself.
