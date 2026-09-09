<!-- CODEX-RESEARCH:START -->
# Codex research project coordination

Use `$communication-research-workflow` for consequential multi-stage research work.
Treat the four roles as role types, not a fixed count of tasks: one controller, optional prompt workbenches, multiple executor work packages, and multiple independent auditors.

- `.codex-research/project.yaml`, `state.yaml`, and accepted contracts are authoritative coordination artifacts.
- Only the controller may edit `state.yaml`, `contracts/`, `decisions.md`, or `snapshots/`.
- Executors and auditors must compare contract `state_revision` before writing and return an immutable handoff package.
- Research materials remain in their existing locations; do not copy raw papers, chats, credentials, or large data into `.codex-research/`.
- Do not infer permission from a path. Follow the exact task contract and pause on changes to source-of-truth, sample, estimand, identification, or submission state.
<!-- CODEX-RESEARCH:END -->
