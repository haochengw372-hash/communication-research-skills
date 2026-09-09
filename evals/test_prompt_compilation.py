import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "communication-research-workflow"
VALIDATOR = SKILL / "scripts" / "validate_research_prompt.py"


class PromptOwnershipTests(unittest.TestCase):
    def test_main_skill_owns_prompt_compilation_reference_and_validator(self):
        self.assertTrue((SKILL / "references" / "prompt-compilation.md").is_file())
        self.assertTrue(VALIDATOR.is_file())
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("target_role=prompt", text)
        self.assertIn("references/prompt-compilation.md", text)

    def test_central_validator_accepts_standalone_prompt(self):
        prompt = """Use $communication-research-workflow.
prompt_mode=standalone
target_role=prompt
task_type=research-question
operation=plan
rigor=standard
authority=read-only
Deliverables: a reusable executor prompt
Quality gates: authority, scope, and deliverables are consistent
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "prompt.txt"
            path.write_text(prompt, encoding="utf-8")
            result = subprocess.run([sys.executable, str(VALIDATOR), str(path)], text=True, capture_output=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
