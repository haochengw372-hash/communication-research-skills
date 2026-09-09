import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "communication-research-workflow"
PLANNER = SKILL / "scripts" / "plan_research_project.py"


def run_planner(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PLANNER), *args],
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


class WorkflowDesignTests(unittest.TestCase):
    def test_public_documentation_has_controller_plan_personalization_and_case(self):
        required = [
            "references/controller-planning.md",
            "references/social-science-workflows.md",
            "references/personalization-guide.md",
            "references/complete-case-study.md",
            "assets/personalization/profile.template.md",
            "scripts/plan_research_project.py",
        ]
        for relative in required:
            with self.subTest(relative=relative):
                self.assertTrue((SKILL / relative).is_file())

        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for relative in required[:4]:
            self.assertIn(relative, skill_text)

        for readme in (ROOT / "README.md", ROOT / "README.zh-CN.md"):
            text = readme.read_text(encoding="utf-8")
            self.assertIn("```mermaid", text)
            if readme.name == "README.md":
                self.assertIn("personal", text.lower())
                self.assertIn("case", text.lower())
            else:
                self.assertIn("私人", text)
                self.assertIn("案例", text)

    def test_planner_emits_a_single_controller_and_dependency_safe_packages(self):
        result = run_planner(
            "--project-id", "municipal-policy-example",
            "--title", "Municipal policy evaluation",
            "--archetype", "causal-policy-evaluation",
            "--format", "json",
            "--include-prompt-workbench",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        plan = json.loads(result.stdout)
        controllers = [window for window in plan["windows"] if window["role"] == "controller"]
        self.assertEqual(len(controllers), 1)
        self.assertEqual(controllers[0]["lifecycle"], "long-lived")
        self.assertTrue(any(window["role"] == "prompt" for window in plan["windows"]))
        package_ids = {package["task_id"] for package in plan["work_packages"]}
        self.assertIn("design-identification", package_ids)
        self.assertIn("audit-identification", package_ids)
        for package in plan["work_packages"]:
            self.assertTrue(set(package["depends_on"]).issubset(package_ids))
            self.assertIn(package["role"], {"executor", "auditor"})
            self.assertTrue(package["deliverables"])
            self.assertTrue(package["open_when"])

    def test_planner_routes_qualitative_work_without_forcing_statistical_models(self):
        result = run_planner(
            "--project-id", "interview-example",
            "--archetype", "qualitative",
            "--format", "json",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        plan = json.loads(result.stdout)
        ids = {package["task_id"] for package in plan["work_packages"]}
        self.assertIn("qualitative-analysis", ids)
        self.assertNotIn("confirmatory-model", ids)

    def test_planner_markdown_contains_mermaid_and_window_timing(self):
        result = run_planner(
            "--project-id", "panel-example",
            "--archetype", "panel-longitudinal",
            "--format", "markdown",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("```mermaid", result.stdout)
        self.assertIn("Open now", result.stdout)
        self.assertIn("Open later", result.stdout)

    def test_planner_rejects_unknown_archetype(self):
        result = run_planner(
            "--project-id", "bad-example",
            "--archetype", "unknown-design",
            "--format", "json",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid choice", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
