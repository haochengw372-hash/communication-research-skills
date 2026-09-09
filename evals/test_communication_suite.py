import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORCH = ROOT / "skills" / "communication-research-workflow"
SUITE_NAMES = {
    "communication-research-workflow",
    "communication-literature",
    "communication-theory",
    "communication-construct",
    "communication-scale",
    "communication-method-router",
    "communication-experiment",
    "communication-content-analysis",
    "communication-network-analysis",
    "communication-causal-inference",
    "communication-temporal-analysis",
    "communication-multimodal-analysis",
    "communication-spatial-analysis",
    "communication-simulation",
    "communication-writing",
    "communication-prose-revision",
    "communication-reviewer",
    "scholarly-access",
}


def load_planner():
    spec = importlib.util.spec_from_file_location(
        "communication_planner",
        ORCH / "scripts" / "plan_research_project.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CommunicationSuiteTests(unittest.TestCase):
    def test_registry_lists_all_suite_skills(self):
        text = (ORCH / "references" / "skill-registry.md").read_text(encoding="utf-8")
        for name in SUITE_NAMES:
            with self.subTest(name=name):
                self.assertIn(name, text)

    def test_router_and_ontology_references_exist_and_are_linked(self):
        skill_text = (ORCH / "SKILL.md").read_text(encoding="utf-8")
        for relative in ("references/communication-router.md", "references/communication-ontology.md"):
            with self.subTest(relative=relative):
                self.assertTrue((ORCH / relative).is_file())
                self.assertIn(relative, skill_text)

    def test_skill_body_names_all_seven_gates(self):
        text = (ORCH / "SKILL.md").read_text(encoding="utf-8")
        for gate in ("Theory Gate", "Construct Gate", "Measurement Gate", "Design / Identification Gate",
                     "Novelty Gate", "Contribution Gate", "Evidence-to-Claim Gate"):
            self.assertIn(gate, text)

    def test_planner_universal_packages_route_to_communication_skills(self):
        planner = load_planner()
        stacks = {name for package in planner.universal_packages() for name in package["skill_stack"]}
        self.assertIn("communication-theory", stacks)
        self.assertIn("communication-literature", stacks)
        self.assertIn("communication-construct", stacks)
        self.assertIn("communication-scale", stacks)
        self.assertIn("communication-method-router", stacks)

    def test_planner_keeps_registered_archetypes(self):
        planner = load_planner()
        for archetype in (
            "survey", "experiment", "text-computational", "network", "temporal",
            "multimodal", "spatial", "simulation", "qualitative",
        ):
            self.assertIn(archetype, planner.ARCHETYPES)

    def test_planner_never_emits_non_suite_skill_names(self):
        planner = load_planner()
        packages = planner.universal_packages()
        for archetype in planner.ARCHETYPES:
            packages.extend(planner.archetype_packages(archetype))
        for package in packages:
            for skill in package["skill_stack"]:
                with self.subTest(skill=skill):
                    self.assertIn(skill, SUITE_NAMES)

    def test_specialist_archetypes_route_to_dedicated_skills(self):
        planner = load_planner()
        expected = {
            "network": "communication-network-analysis",
            "causal-policy-evaluation": "communication-causal-inference",
            "temporal": "communication-temporal-analysis",
            "multimodal": "communication-multimodal-analysis",
            "spatial": "communication-spatial-analysis",
            "simulation": "communication-simulation",
        }
        for archetype, skill in expected.items():
            with self.subTest(archetype=archetype):
                stacks = {
                    name
                    for package in planner.archetype_packages(archetype)
                    for name in package["skill_stack"]
                }
                self.assertIn(skill, stacks)

    def test_writer_and_reviewer_have_separate_pipeline_roles(self):
        planner = load_planner()
        packages = {
            package["task_id"]: package
            for package in planner.archetype_packages("experiment")
        }
        self.assertIn("communication-writing", packages["results-integration"]["skill_stack"])
        self.assertEqual(packages["manuscript-integration"]["skill_stack"], ["communication-writing"])
        self.assertEqual(packages["prose-revision"]["skill_stack"], ["communication-prose-revision"])
        self.assertEqual(packages["audit-final"]["depends_on"], ["prose-revision"])
        self.assertEqual(packages["audit-results"]["skill_stack"], ["communication-reviewer"])
        self.assertIn("communication-reviewer", packages["audit-final"]["skill_stack"])

    def test_benchmark_prompts_exist(self):
        for name in ("survey-experiment.md", "content-analysis.md", "platform-network.md",
                     "llm-calibration.md", "access-batch.md", "manuscript-writing.md",
                     "prose-revision.md"):
            with self.subTest(name=name):
                self.assertTrue((ROOT / "evals" / "prompts" / name).is_file())

    def test_orchestrator_end_to_end_dry_run(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "demo" / "run_orchestrator_e2e.py")],
            text=True,
            capture_output=True,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("END-TO-END ORCHESTRATOR DRY RUN: PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
