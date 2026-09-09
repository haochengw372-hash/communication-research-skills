import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "communication-research-workflow" / "scripts" / "validate_task_contract.py"


VALID = {
    "task_type": "empirical-analysis",
    "goal": "核对 PSM 后的 ATT 与平衡性",
    "operation": "review",
    "rigor": "audit",
    "authority": "read-only",
    "source_of_truth": {"dataset": "matched.parquet", "estimand": "ATT"},
    "materials": ["analysis.py", "matched.parquet"],
    "deliverables": ["诊断报告"],
    "quality_gates": ["authority", "empirical-truthfulness"],
    "constraints": ["不得修改文件"],
    "stop_conditions": ["estimand 发生变化"],
    "uncertainties": ["匹配口径待核验"],
}


class TaskContractValidatorTests(unittest.TestCase):
    def run_validator(self, value):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "contract.json"
            path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                text=True,
                capture_output=True,
                encoding="utf-8",
            )

    def test_valid_contract_passes(self):
        result = self.run_validator(VALID)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("VALID", result.stdout)

    def test_specialized_task_types_are_registered(self):
        for task_type in (
            "qualitative-analysis", "mixed-methods", "network-analysis",
            "causal-inference", "temporal-analysis", "multimodal-analysis",
            "spatial-analysis", "simulation-study",
        ):
            with self.subTest(task_type=task_type):
                contract = dict(VALID, task_type=task_type)
                result = self.run_validator(contract)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_required_field_fails(self):
        invalid = dict(VALID)
        invalid.pop("source_of_truth")
        result = self.run_validator(invalid)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source_of_truth", result.stdout + result.stderr)

    def test_invalid_enum_fails(self):
        invalid = dict(VALID, operation="make-it-significant")
        result = self.run_validator(invalid)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("operation", result.stdout + result.stderr)

    def test_review_cannot_request_write_authority(self):
        invalid = dict(VALID, operation="review", authority="edit-existing")
        result = self.run_validator(invalid)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("read-only", result.stdout + result.stderr)

    def test_yaml_subset_is_supported_without_dependency(self):
        yaml_text = """task_type: literature-review
goal: 建立证据矩阵
operation: plan
rigor: standard
authority: read-only
source_of_truth: Zotero 与 OpenAlex 核验记录
materials:
  - zotero-library
deliverables:
  - evidence-matrix
quality_gates:
  - citation-support
constraints:
  - 不写入外部系统
stop_conditions:
  - 需要外部写入
uncertainties:
  - DOI 待核验
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "contract.yaml"
            path.write_text(yaml_text, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                text=True,
                capture_output=True,
                encoding="utf-8",
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_example_contract_from_reference_passes(self):
        examples = (
            ROOT
            / "skills"
            / "communication-research-workflow"
            / "references"
            / "examples.md"
        ).read_text(encoding="utf-8")
        yaml_text = examples.split("```yaml", 1)[1].split("```", 1)[0].strip()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.yaml"
            path.write_text(yaml_text, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                text=True,
                capture_output=True,
                encoding="utf-8",
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_accepts_v1_project_contract(self):
        contract = dict(VALID)
        contract.update(
            {
                "schema_version": "codex-research-contract/v1",
                "project_id": "policy-citation-example",
                "task_id": "task-014",
                "target_role": "executor",
                "state_revision": 12,
                "contract_version": 2,
                "input_artifacts": [".codex-research/state.yaml"],
                "return_handoff": True,
                "task_type": "project-governance",
                "operation": "execute",
                "authority": "create-new",
            }
        )
        result = self.run_validator(contract)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_project_yaml_subset_supports_integer_and_boolean_fields(self):
        yaml_text = """schema_version: codex-research-contract/v1
project_id: policy-example
task_id: task-014
target_role: executor
state_revision: 12
contract_version: 2
task_type: project-governance
goal: 创建执行交接
operation: execute
rigor: standard
authority: create-new
source_of_truth: state revision 12
materials:
  - .codex-research/state.yaml
input_artifacts:
  - .codex-research/project.yaml
deliverables:
  - handoff
quality_gates:
  - state-version
constraints:
  - controller-single-writer
stop_conditions:
  - stale-state
uncertainties:
return_handoff: true
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "contract.yaml"
            path.write_text(yaml_text, encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], text=True, capture_output=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_project_contract_without_coordination_fields(self):
        contract = dict(VALID, schema_version="codex-research-contract/v1")
        result = self.run_validator(contract)
        self.assertEqual(result.returncode, 1)
        self.assertIn("project_id", result.stdout)

    def test_rejects_non_controller_contract_that_writes_governance_state(self):
        contract = dict(VALID)
        contract.update(
            {
                "schema_version": "codex-research-contract/v1",
                "project_id": "policy-citation-example",
                "task_id": "task-014",
                "target_role": "executor",
                "state_revision": 12,
                "contract_version": 1,
                "input_artifacts": [],
                "return_handoff": True,
                "operation": "execute",
                "authority": "create-new",
                "deliverables": ["修改 .codex-research/state.yaml"],
            }
        )
        result = self.run_validator(contract)
        self.assertEqual(result.returncode, 1)
        self.assertIn("controller-only", result.stdout)

    def test_rejects_prompt_and_auditor_role_matrix_conflicts(self):
        base = dict(VALID, schema_version="codex-research-contract/v1", project_id="policy-example", task_id="task-014", state_revision=1, contract_version=1, input_artifacts=[], return_handoff=True)
        prompt_contract = dict(base, target_role="prompt", operation="execute", authority="create-new")
        auditor_contract = dict(base, target_role="auditor", operation="execute", authority="create-new", rigor="standard")
        for contract in (prompt_contract, auditor_contract):
            result = self.run_validator(contract)
            self.assertEqual(result.returncode, 1)
            self.assertIn("role matrix", result.stdout)

    def test_rejects_executor_snapshot_governance_write(self):
        contract = dict(VALID, schema_version="codex-research-contract/v1", project_id="policy-example", task_id="task-014", target_role="executor", state_revision=1, contract_version=1, input_artifacts=[], return_handoff=True, deliverables=[".codex-research/snapshots/freeze.yaml"])
        result = self.run_validator(contract)
        self.assertEqual(result.returncode, 1)
        self.assertIn("controller-only", result.stdout)

    def test_project_versions_must_be_non_negative_and_positive(self):
        contract = dict(VALID, schema_version="codex-research-contract/v1", project_id="policy-example", task_id="task-014", target_role="executor", state_revision=-1, contract_version=0, input_artifacts=[], return_handoff=True)
        result = self.run_validator(contract)
        self.assertEqual(result.returncode, 1)
        self.assertIn("state_revision must be non-negative", result.stdout)
        self.assertIn("contract_version must be positive", result.stdout)


if __name__ == "__main__":
    unittest.main()
