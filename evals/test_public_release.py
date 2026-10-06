import importlib.util
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
SKILL = SKILLS / "communication-research-workflow"


class PublicReleaseTests(unittest.TestCase):
    def test_public_repository_files_exist(self):
        for name in [
            "README.md",
            "README.zh-CN.md",
            "LICENSE",
            "NOTICE.md",
            "CITATION.cff",
            "VERSION",
            ".gitignore",
            "scripts/install.sh",
            "scripts/uninstall.sh",
            "tools/run_evals.py",
            "tools/security_audit.py",
            "tools/privacy_audit.py",
        ]:
            with self.subTest(name=name):
                self.assertTrue((ROOT / name).is_file())

    def test_all_eighteen_skills_are_installable_directories(self):
        expected = {
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
        self.assertEqual(
            {p.name for p in SKILLS.iterdir() if p.is_dir()},
            expected,
        )
        for folder in SKILLS.iterdir():
            if not folder.is_dir():
                continue
            with self.subTest(folder=folder.name):
                self.assertTrue((folder / "SKILL.md").is_file())
                self.assertTrue((folder / "agents" / "openai.yaml").is_file())
                text = (folder / "SKILL.md").read_text(encoding="utf-8")
                self.assertRegex(text, rf"(?m)^name: {re.escape(folder.name)}$")
                self.assertNotIn("TODO", text)

        uninstall_text = (ROOT / "scripts" / "uninstall.sh").read_text(encoding="utf-8")
        for name in expected:
            with self.subTest(uninstall_name=name):
                self.assertIn(f'"{name}"', uninstall_text)

    def test_orchestrator_installable_structure_exists(self):
        required = [
            "SKILL.md", "agents/openai.yaml",
            "assets/project-control/AGENTS.fragment.md",
            "assets/personalization/profile.template.md",
            "references/profile-and-preferences.md",
            "references/task-contract-and-router.md",
            "references/project-coordination.md",
            "references/prompt-compilation.md",
            "references/research-workflows.md",
            "references/empirical-workflows.md",
            "references/writing-review-workflows.md",
            "references/integrity-and-delivery-gates.md",
            "references/skill-registry.md",
            "references/examples.md",
            "references/controller-planning.md",
            "references/social-science-workflows.md",
            "references/personalization-guide.md",
            "references/complete-case-study.md",
            "references/communication-ontology.md",
            "references/communication-router.md",
            "scripts/validate_task_contract.py",
            "scripts/init_research_project.py",
            "scripts/validate_project_control.py",
            "scripts/create_handoff.py",
            "scripts/validate_handoff.py",
            "scripts/validate_research_prompt.py",
            "scripts/plan_research_project.py",
        ]
        for relative in required:
            with self.subTest(relative=relative):
                self.assertTrue((SKILL / relative).is_file())

    def test_public_name_and_version_are_consistent(self):
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.5.0")
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertRegex(skill_text, r"(?m)^name: communication-research-workflow$")
        self.assertIn("$communication-research-workflow", skill_text)
        metadata = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("Communication Research Workflow", metadata)
        self.assertIn("$communication-research-workflow", metadata)

    def test_public_project_protocol_is_consistent(self):
        combined = "\n".join(
            path.read_text(encoding="utf-8", errors="ignore")
            for path in SKILL.rglob("*")
            if path.is_file()
        )
        self.assertIn(".codex-research/", combined)
        self.assertIn("codex-research-contract/v1", combined)
        self.assertIn("codex-research-state/v1", combined)
        self.assertIn("codex-research-handoff/v1", combined)

    def test_no_generated_caches_are_present(self):
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("__pycache__/", ignore)
        self.assertIn("*.py[cod]", ignore)

    def test_skill_references_are_one_level_and_directly_reachable(self):
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        references = sorted((SKILL / "references").glob("*.md"))
        self.assertGreaterEqual(len(references), 14)
        for path in references:
            with self.subTest(path=path.name):
                self.assertEqual(path.parent, SKILL / "references")
                self.assertIn(f"references/{path.name}", skill_text)

    def test_no_bom_and_no_nested_git_history(self):
        for path in ROOT.rglob("*"):
            if ".git" in path.parts or ".omx" in path.parts or "__pycache__" in path.parts:
                continue
            if not path.is_file():
                continue
            raw = path.read_bytes()
            self.assertFalse(raw.startswith(b"\xef\xbb\xbf"), path)

    def test_readme_documents_installation_and_usage(self):
        for name in ("README.md", "README.zh-CN.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("skills/communication-research-workflow", text)
            self.assertIn("$communication-research-workflow", text)
            self.assertIn("```mermaid", text)
            self.assertIn("MIT", text)
            self.assertIn("Apache-2.0", text)
            self.assertTrue(text.startswith("> 使用请引用"))
            self.assertIn("Haocheng Wang", text.split("\n\n")[0])
            if name == "README.md":
                self.assertIn("personal", text.lower())
                self.assertIn("case", text.lower())
            else:
                self.assertIn("私人", text)
                self.assertIn("案例", text)

    def test_license_and_citation_keep_upstream_attribution(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        notice = (ROOT / "NOTICE.md").read_text(encoding="utf-8")
        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        self.assertIn("Apache License", license_text)
        self.assertIn("Version 2.0, January 2004", license_text)
        self.assertIn("Copyright (c) 2026 Codex Research Workflow contributors", notice)
        self.assertIn("Permission is hereby granted, free of charge", notice)
        self.assertIn("not an additional condition", notice)
        self.assertIn("family-names: Wang", citation)
        self.assertIn("given-names: Haocheng", citation)
        self.assertIn("license: Apache-2.0", citation)

    def test_public_demo_is_project_agnostic(self):
        removed_project_artifacts = [
            "demo/PROPOSAL.md",
            "demo/DJ_EVIDENCE_MATRIX.md",
            "demo/CORPUS_ANALYSIS_28.json",
            "demo/analyze_existing_corpus.py",
        ]
        for relative in removed_project_artifacts:
            with self.subTest(relative=relative):
                self.assertFalse((ROOT / relative).exists())

        public_surface = "\n".join(
            path.read_text(encoding="utf-8", errors="ignore")
            for path in [ROOT / "README.md", ROOT / "README.zh-CN.md"]
            + sorted((ROOT / "demo").rglob("*"))
            if path.is_file()
        )
        for project_marker in (
            "AI disclosure",
            "party-state",
            "China pilot",
            "Hollow Mediator",
            "demo-ai-disclosure-trust",
            "demo-concept-factory",
            "计算传播文献_2024-2026",
        ):
            with self.subTest(project_marker=project_marker):
                self.assertNotIn(project_marker, public_surface)
        user_path_pattern = re.escape("/" + "Users" + "/") + r"[^/]+/"
        self.assertNotRegex(public_surface, user_path_pattern)

    def test_repository_privacy_audit_passes(self):
        script = ROOT / "tools" / "privacy_audit.py"
        self.assertTrue(script.is_file())
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_privacy_audit_detects_generic_exposure_patterns(self):
        script = ROOT / "tools" / "privacy_audit.py"
        spec = importlib.util.spec_from_file_location("privacy_audit", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertTrue(list(module.generic_matches("C:" + "\\Users\\example-user\\notes.txt")))
        self.assertTrue(list(module.generic_matches("D:" + "\\private-project\\notes.txt")))
        self.assertTrue(list(module.generic_matches("contact: person" + "@example.org")))
        self.assertTrue(list(module.generic_matches("api_" + "key = exposed-value")))


if __name__ == "__main__":
    unittest.main()
