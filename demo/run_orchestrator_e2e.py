#!/usr/bin/env python3
"""Run the communication orchestrator's full project-control lifecycle.

End-to-end dry run in a temporary directory: initialize the control layer,
generate a plan, write and validate a task contract, create and validate a
handoff, then validate the whole control layer. Nothing is written outside the
temporary directory.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "communication-research-workflow" / "scripts"


def run(args: list[str]) -> subprocess.CompletedProcess:
    result = subprocess.run(
        [sys.executable, *args], text=True, capture_output=True, encoding="utf-8"
    )
    print(f"$ {' '.join(args[-3:])}")
    print((result.stdout or "").strip())
    if result.returncode != 0:
        print("STDERR:", (result.stderr or "").strip())
    return result


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="comm-e2e-") as directory:
        project = Path(directory)
        init = run([
            str(SCRIPTS / "init_research_project.py"),
            "--project-id", "demo-e2e",
            "--title", "Generic communication research lifecycle (dry run)",
            str(project),
        ])
        assert init.returncode == 0, "init failed"

        plan = run([
            str(SCRIPTS / "plan_research_project.py"),
            "--project-id", "demo-e2e",
            "--title", "Generic communication research lifecycle",
            "--archetype", "experiment",
            "--format", "json",
        ])
        assert plan.returncode == 0, "plan failed"

        state_path = project / ".codex-research" / "state.yaml"
        state = json.loads(state_path.read_text(encoding="utf-8"))

        contract = {
            "schema_version": "codex-research-contract/v1",
            "project_id": state["project_id"],
            "task_id": "randomization-protocol",
            "target_role": "executor",
            "state_revision": state["revision"],
            "contract_version": 1,
            "return_handoff": True,
            "input_artifacts": [".codex-research/state.yaml"],
            "task_type": "experiment-survey",
            "goal": "验证随机传播实验的设计、测量、分析与交接流程",
            "operation": "execute",
            "rigor": "audit",
            "authority": "edit-existing",
            "source_of_truth": {"estimand": "ATE", "design": "experiment"},
            "materials": ["design-protocol.md"],
            "deliverables": ["研究计划", "门禁清单"],
            "quality_gates": ["authority", "empirical-truthfulness"],
            "constraints": ["不得写治理状态"],
            "stop_conditions": ["estimand 发生变化"],
            "uncertainties": ["目标构念的量表改编状态待定"],
        }
        contracts_dir = project / ".codex-research" / "contracts"
        contracts_dir.mkdir(parents=True, exist_ok=True)
        contract_path = contracts_dir / "contract.json"
        contract_path.write_text(json.dumps(contract, ensure_ascii=False), encoding="utf-8")

        validate_contract = run([
            str(SCRIPTS / "validate_task_contract.py"), str(contract_path),
        ])
        assert validate_contract.returncode == 0, "contract validation failed"

        artifact = project / "outputs" / "randomization-protocol" / "design-protocol.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(
            "# Design protocol\n\nRandomized communication cue with explicit measurement and validity gates.\n",
            encoding="utf-8",
        )

        handoff = run([
            str(SCRIPTS / "create_handoff.py"),
            "--task-id", "randomization-protocol",
            "--role", "executor",
            "--status", "completed",
            "--contract", str(contract_path),
            "--artifact", str(artifact),
            "--verification-command", "python -m py_compile design-protocol.py",
            "--verification-result", "ok",
            "--quality-gate", "empirical-truthfulness",
            "--verdict", "pass",
            "--recommended-next-action", "proceed to confirmatory-model",
            str(project),
        ])
        assert handoff.returncode == 0, "handoff creation failed"

        handoff_dir = sorted(
            list((project / ".codex-research" / "handoffs").glob("*.json"))
            + list((project / ".codex-research" / "handoffs").glob("*.yaml"))
        )
        assert handoff_dir, "no handoff written"
        validate_handoff = run([
            str(SCRIPTS / "validate_handoff.py"), str(project), str(handoff_dir[-1]),
        ])
        assert validate_handoff.returncode == 0, "handoff validation failed"

        control = run([str(SCRIPTS / "validate_project_control.py"), str(project)])
        assert control.returncode == 0, "control validation failed"

        print("END-TO-END ORCHESTRATOR DRY RUN: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
