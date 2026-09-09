import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "communication-research-workflow" / "scripts"


def run_script(name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *args],
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


class ProjectControlTests(unittest.TestCase):
    def test_dry_run_is_non_mutating(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run_script("init_research_project.py", str(root), "--project-id", "policy-example", "--dry-run")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("DRY RUN", result.stdout)
            self.assertFalse((root / ".codex-research").exists())

    def test_initializes_minimal_multi_instance_control_layer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run_script("init_research_project.py", str(root), "--project-id", "policy-example", "--title", "政策引用研究")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            control = root / ".codex-research"
            for name in ["project.yaml", "state.yaml", "windows.yaml", "decisions.md"]:
                self.assertTrue((control / name).is_file(), name)
            for name in ["contracts", "handoffs", "audits", "snapshots"]:
                self.assertTrue((control / name).is_dir(), name)
            self.assertTrue((root / "AGENTS.md").is_file())
            state = json.loads((control / "state.yaml").read_text(encoding="utf-8"))
            self.assertEqual(state["schema_version"], "codex-research-state/v1")
            self.assertEqual(state["work_packages"], {})
            windows = json.loads((control / "windows.yaml").read_text(encoding="utf-8"))
            self.assertEqual(set(windows["roles"]), {"controller", "prompt", "executor", "auditor"})
            self.assertEqual(windows["roles"]["controller"]["instances"], 1)
            self.assertIsNone(windows["roles"]["executor"]["instances"])

    def test_existing_agents_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            original = "# Existing rules\nDo not replace me.\n"
            (root / "AGENTS.md").write_text(original, encoding="utf-8")
            result = run_script("init_research_project.py", str(root), "--project-id", "policy-example")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((root / "AGENTS.md").read_text(encoding="utf-8"), original)
            fragment = root / ".codex-research" / "AGENTS.codex-research.fragment.md"
            self.assertTrue(fragment.is_file())
            self.assertIn("CODEX-RESEARCH:START", fragment.read_text(encoding="utf-8"))

    def test_reinitialization_does_not_overwrite_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            args = (str(root), "--project-id", "policy-example")
            self.assertEqual(run_script("init_research_project.py", *args).returncode, 0)
            state_path = root / ".codex-research" / "state.yaml"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["revision"] = 7
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            result = run_script("init_research_project.py", *args)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(state_path.read_text(encoding="utf-8"))["revision"], 7)

    def test_validates_initialized_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(run_script("init_research_project.py", str(root), "--project-id", "policy-example").returncode, 0)
            result = run_script("validate_project_control.py", str(root))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("VALID", result.stdout)

    def test_detects_dependency_cycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(run_script("init_research_project.py", str(root), "--project-id", "policy-example").returncode, 0)
            state_path = root / ".codex-research" / "state.yaml"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["work_packages"] = {
                "literature-001": {"status": "ready", "depends_on": ["analysis-002"]},
                "analysis-002": {"status": "blocked", "depends_on": ["literature-001"]},
            }
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            result = run_script("validate_project_control.py", str(root))
            self.assertEqual(result.returncode, 1)
            self.assertIn("dependency cycle", result.stdout)

    def test_detects_overlapping_write_scopes_for_active_packages(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(run_script("init_research_project.py", str(root), "--project-id", "policy-example").returncode, 0)
            state_path = root / ".codex-research" / "state.yaml"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["work_packages"] = {
                "model-001": {"status": "in-progress", "depends_on": [], "write_scope": ["outputs/models/"]},
                "model-002": {"status": "ready", "depends_on": [], "write_scope": ["outputs/models/main/"]},
            }
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            result = run_script("validate_project_control.py", str(root))
            self.assertEqual(result.returncode, 1)
            self.assertIn("overlapping write scope", result.stdout)

    def test_detects_case_and_dotdot_write_scope_aliases(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(run_script("init_research_project.py", str(root), "--project-id", "policy-example").returncode, 0)
            state_path = root / ".codex-research" / "state.yaml"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["work_packages"] = {
                "a": {"status": "ready", "depends_on": [], "assigned_role": "executor", "write_scope": ["Results/a/../shared/"]},
                "b": {"status": "ready", "depends_on": [], "assigned_role": "executor", "write_scope": ["results/shared/"]},
            }
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            result = run_script("validate_project_control.py", str(root))
            self.assertEqual(result.returncode, 1)
            self.assertIn("overlapping write scope", result.stdout)

    def test_rejects_mutated_role_permissions_and_invalid_state_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(run_script("init_research_project.py", str(root), "--project-id", "policy-example").returncode, 0)
            state_path = root / ".codex-research" / "state.yaml"
            state = json.loads(state_path.read_text(encoding="utf-8")); state["revision"] = -4; state["updated_by"] = "executor-17"
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            windows_path = root / ".codex-research" / "windows.yaml"
            windows = json.loads(windows_path.read_text(encoding="utf-8")); windows["roles"]["executor"]["writes"].append("state.yaml")
            windows_path.write_text(json.dumps(windows, ensure_ascii=False), encoding="utf-8")
            result = run_script("validate_project_control.py", str(root))
            self.assertEqual(result.returncode, 1)
            self.assertIn("revision", result.stdout)
            self.assertIn("updated_by", result.stdout)
            self.assertIn("role permission", result.stdout)

    def test_detects_unknown_dependency_and_invalid_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(run_script("init_research_project.py", str(root), "--project-id", "policy-example").returncode, 0)
            state_path = root / ".codex-research" / "state.yaml"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["work_packages"] = {"model-001": {"status": "finished-ish", "depends_on": ["missing-000"]}}
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            result = run_script("validate_project_control.py", str(root))
            self.assertEqual(result.returncode, 1)
            self.assertIn("unknown dependency", result.stdout)
            self.assertIn("invalid status", result.stdout)

    def test_active_packages_require_role_scope_and_completed_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(run_script("init_research_project.py", str(root), "--project-id", "policy-example").returncode, 0)
            state_path = root / ".codex-research" / "state.yaml"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["work_packages"] = {
                "upstream": {"status": "ready", "depends_on": [], "assigned_role": "executor", "write_scope": ["outputs/upstream/"]},
                "downstream": {"status": "in-progress", "depends_on": ["upstream"], "assigned_role": "unknown", "write_scope": []},
            }
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            result = run_script("validate_project_control.py", str(root))
            self.assertEqual(result.returncode, 1)
            self.assertIn("invalid assigned role", result.stdout)
            self.assertIn("write_scope", result.stdout)
            self.assertIn("dependency not completed", result.stdout)

    def test_completed_audited_package_requires_pass_and_fresh_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(run_script("init_research_project.py", str(root), "--project-id", "policy-example").returncode, 0)
            state_path = root / ".codex-research" / "state.yaml"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["work_packages"] = {"model": {"status": "completed", "depends_on": [], "assigned_role": "executor", "write_scope": ["outputs/model/"], "audit_required": True}}
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            result = run_script("validate_project_control.py", str(root))
            self.assertEqual(result.returncode, 1)
            self.assertIn("audit verdict", result.stdout)
            self.assertIn("latest verification", result.stdout)

    def test_role_specific_work_package_write_scopes(self):
        bad_scopes = {"prompt": ["scripts/"], "auditor": ["outputs/results/"], "executor": [".codex-research/state.yaml"]}
        for role, scope in bad_scopes.items():
            with self.subTest(role=role), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); self.assertEqual(run_script("init_research_project.py", str(root), "--project-id", "policy-example").returncode, 0)
                state_path = root / ".codex-research" / "state.yaml"; state=json.loads(state_path.read_text(encoding="utf-8")); state["work_packages"]={"task": {"status":"ready","depends_on":[],"assigned_role":role,"write_scope":scope}}; state_path.write_text(json.dumps(state),encoding="utf-8")
                result=run_script("validate_project_control.py",str(root)); self.assertEqual(result.returncode,1); self.assertIn("write scope violates role",result.stdout)

    def test_role_scope_prefix_requires_path_boundary(self):
        for role, scope in (("prompt", [".codex-research/handoffs-evil/"]), ("auditor", [".codex-research/audits-evil/"])):
            with self.subTest(role=role), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp); self.assertEqual(run_script("init_research_project.py",str(root),"--project-id","policy-example").returncode,0)
                state_path=root/".codex-research"/"state.yaml"; state=json.loads(state_path.read_text(encoding="utf-8")); state["work_packages"]={"task":{"status":"ready","depends_on":[],"assigned_role":role,"write_scope":scope}}; state_path.write_text(json.dumps(state),encoding="utf-8")
                result=run_script("validate_project_control.py",str(root)); self.assertEqual(result.returncode,1); self.assertIn("write scope violates role",result.stdout)

    def test_completed_verification_requires_command_and_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); self.assertEqual(run_script("init_research_project.py",str(root),"--project-id","policy-example").returncode,0)
            state_path=root/".codex-research"/"state.yaml"; state=json.loads(state_path.read_text(encoding="utf-8")); state["work_packages"]={"task":{"status":"completed","depends_on":[],"assigned_role":"executor","write_scope":["outputs/"],"latest_verification":{"result":"passed"}}}; state_path.write_text(json.dumps(state),encoding="utf-8")
            result=run_script("validate_project_control.py",str(root)); self.assertEqual(result.returncode,1); self.assertIn("latest verification",result.stdout)


class HandoffTests(unittest.TestCase):
    def initialize(self, root: Path) -> Path:
        result = run_script("init_research_project.py", str(root), "--project-id", "policy-example")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        contract = {
            "schema_version": "codex-research-contract/v1",
            "project_id": "policy-example",
            "task_id": "task-014",
            "target_role": "executor",
            "state_revision": 0,
            "contract_version": 1,
        }
        path = root / ".codex-research" / "contracts" / "task-014-v1.yaml"
        path.write_text(json.dumps(contract, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def test_creates_unique_executor_handoffs_with_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contract = self.initialize(root)
            artifact = root / "outputs" / "table.csv"
            artifact.parent.mkdir()
            artifact.write_text("x,y\n1,2\n", encoding="utf-8")
            args = (str(root), "--task-id", "task-014", "--role", "executor", "--status", "completed", "--contract", str(contract), "--artifact", str(artifact), "--verification-command", "python verify.py", "--verification-result", "passed", "--quality-gate", "artifact-hash", "--recommended-next-action", "提交独立审计")
            self.assertEqual(run_script("create_handoff.py", *args).returncode, 0)
            self.assertEqual(run_script("create_handoff.py", *args).returncode, 0)
            paths = sorted((root / ".codex-research" / "handoffs").glob("*.yaml"))
            self.assertEqual(len(paths), 2)
            self.assertNotEqual(paths[0].name, paths[1].name)
            handoff = json.loads(paths[0].read_text(encoding="utf-8"))
            self.assertEqual(len(handoff["artifacts"][0]["sha256"]), 64)
            self.assertEqual(len(handoff["contract_sha256"]), 64)

    def test_completed_handoff_requires_artifact_fresh_verification_and_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contract = self.initialize(root)
            result = run_script("create_handoff.py", str(root), "--task-id", "task-014", "--role", "executor", "--status", "completed", "--contract", str(contract))
            self.assertEqual(result.returncode, 2)
            self.assertIn("completed handoff requires", result.stderr)

    def test_completed_handoff_persists_top_level_fresh_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); contract=self.initialize(root); artifact=root/"outputs"/"x.csv"; artifact.parent.mkdir(); artifact.write_text("x\n1\n",encoding="utf-8")
            result=run_script("create_handoff.py",str(root),"--task-id","task-014","--role","executor","--status","completed","--contract",str(contract),"--artifact",str(artifact),"--verification-command","python verify.py","--verification-result","passed","--quality-gate","fresh")
            self.assertEqual(result.returncode,0,result.stdout+result.stderr); handoff=json.loads(next((root/".codex-research"/"handoffs").glob("*.yaml")).read_text(encoding="utf-8")); self.assertEqual(handoff["fresh_verification"]["result"],"passed")

    def test_completed_auditor_requires_audit_report_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); contract=self.initialize(root); value=json.loads(contract.read_text(encoding="utf-8")); value["target_role"]="auditor"; contract.write_text(json.dumps(value),encoding="utf-8")
            result=run_script("create_handoff.py",str(root),"--task-id","task-014","--role","auditor","--status","completed","--contract",str(contract),"--verdict","pass","--verification-command","python audit.py","--verification-result","passed","--quality-gate","independent-audit")
            self.assertEqual(result.returncode,2); self.assertIn("audit report",result.stderr)

    def test_stale_contract_creates_stale_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contract = self.initialize(root)
            state_path = root / ".codex-research" / "state.yaml"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["revision"] = 1
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            result = run_script("create_handoff.py", str(root), "--task-id", "task-014", "--role", "executor", "--status", "completed", "--contract", str(contract))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            handoff = json.loads(next((root / ".codex-research" / "handoffs").glob("*.yaml")).read_text(encoding="utf-8"))
            self.assertEqual(handoff["status"], "stale")

    def test_stale_handoff_rejects_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); contract = self.initialize(root)
            state_path = root / ".codex-research" / "state.yaml"; state = json.loads(state_path.read_text(encoding="utf-8")); state["revision"] = 1; state_path.write_text(json.dumps(state), encoding="utf-8")
            artifact = root / "outputs" / "table.csv"; artifact.parent.mkdir(); artifact.write_text("x\n1\n", encoding="utf-8")
            result = run_script("create_handoff.py", str(root), "--task-id", "task-014", "--role", "executor", "--status", "partial", "--contract", str(contract), "--artifact", str(artifact))
            self.assertEqual(result.returncode, 2)
            self.assertIn("stale handoff cannot include artifacts", result.stderr)

    def test_auditor_requires_verdict(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contract = self.initialize(root)
            result = run_script("create_handoff.py", str(root), "--task-id", "task-014", "--role", "auditor", "--status", "completed", "--contract", str(contract))
            self.assertEqual(result.returncode, 2)
            self.assertIn("verdict", result.stderr.lower())

    def test_validator_detects_changed_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contract = self.initialize(root)
            artifact = root / "outputs" / "table.csv"
            artifact.parent.mkdir()
            artifact.write_text("x\n1\n", encoding="utf-8")
            result = run_script("create_handoff.py", str(root), "--task-id", "task-014", "--role", "executor", "--status", "completed", "--contract", str(contract), "--artifact", str(artifact), "--verification-command", "python verify.py", "--verification-result", "passed", "--quality-gate", "artifact-hash")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            handoff_path = next((root / ".codex-research" / "handoffs").glob("*.yaml"))
            artifact.write_text("x\n2\n", encoding="utf-8")
            check = run_script("validate_handoff.py", str(root), str(handoff_path))
            self.assertEqual(check.returncode, 1)
            self.assertIn("artifact hash mismatch", check.stdout)

    def test_validator_rejects_executor_governance_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contract = self.initialize(root)
            result = run_script("create_handoff.py", str(root), "--task-id", "task-014", "--role", "executor", "--status", "completed", "--contract", str(contract), "--artifact", str(root / ".codex-research" / "state.yaml"))
            self.assertEqual(result.returncode, 2)
            self.assertIn("controller-only", result.stderr)

    def test_rejects_all_role_forbidden_artifact_scopes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); contract = self.initialize(root)
            for relative in (".codex-research/project.yaml", ".codex-research/windows.yaml"):
                result = run_script("create_handoff.py", str(root), "--task-id", "task-014", "--role", "executor", "--status", "partial", "--contract", str(contract), "--artifact", str(root / relative))
                self.assertEqual(result.returncode, 2)
                self.assertIn("controller-only", result.stderr)

    def test_handoff_self_integrity_and_schema_are_validated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); contract = self.initialize(root)
            result = run_script("create_handoff.py", str(root), "--task-id", "task-014", "--role", "executor", "--status", "partial", "--contract", str(contract))
            self.assertEqual(result.returncode, 0)
            path = next((root / ".codex-research" / "handoffs").glob("*.yaml")); handoff=json.loads(path.read_text(encoding="utf-8")); handoff["verified_findings"]=["tampered"]; handoff["schema_version"]="wrong/v9"; path.write_text(json.dumps(handoff),encoding="utf-8")
            check=run_script("validate_handoff.py",str(root),str(path))
            self.assertEqual(check.returncode,1)
            self.assertIn("schema_version",check.stdout)
            self.assertIn("handoff content hash",check.stdout)

    def test_creator_rejects_role_mismatch_with_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contract = self.initialize(root)
            result = run_script("create_handoff.py", str(root), "--task-id", "task-014", "--role", "prompt", "--status", "completed", "--contract", str(contract))
            self.assertEqual(result.returncode, 2)
            self.assertIn("role mismatch", result.stderr)

    def test_creator_rejects_contract_outside_control_layer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contract = self.initialize(root)
            external = root / "contract-copy.yaml"
            external.write_bytes(contract.read_bytes())
            result = run_script("create_handoff.py", str(root), "--task-id", "task-014", "--role", "executor", "--status", "completed", "--contract", str(external))
            self.assertEqual(result.returncode, 2)
            self.assertIn("contracts directory", result.stderr)

    def test_validator_rejects_project_and_task_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contract = self.initialize(root)
            result = run_script("create_handoff.py", str(root), "--task-id", "task-014", "--role", "executor", "--status", "partial", "--contract", str(contract))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            handoff_path = next((root / ".codex-research" / "handoffs").glob("*.yaml"))
            handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
            handoff["project_id"] = "wrong-project"
            handoff["task_id"] = "wrong-task"
            handoff_path.write_text(json.dumps(handoff, ensure_ascii=False), encoding="utf-8")
            check = run_script("validate_handoff.py", str(root), str(handoff_path))
            self.assertEqual(check.returncode, 1)
            self.assertIn("project_id mismatch", check.stdout)
            self.assertIn("task_id mismatch", check.stdout)


if __name__ == "__main__":
    unittest.main()
