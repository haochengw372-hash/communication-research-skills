import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/communication-prose-revision/scripts/audit_prose.py"


class CommunicationProseRevisionTests(unittest.TestCase):
    def run_audit(self, text: str, *extra: str):
        with tempfile.TemporaryDirectory() as directory:
            manuscript = Path(directory) / "manuscript.md"
            manuscript.write_text(text, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(manuscript), *extra],
                text=True,
                capture_output=True,
                encoding="utf-8",
            )

    def test_formulaic_and_stacked_hedging_are_flagged_without_authorship_score(self):
        result = self.run_audit(
            "In recent years, this topic has attracted attention.\n"
            "It is important to note that the result may potentially suggest a change.\n"
            "These findings provide valuable insights.\n"
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("FORMULAIC_OPENING", result.stdout)
        self.assertIn("STACKED_HEDGE", result.stdout)
        self.assertIn("VAGUE_CONTRIBUTION", result.stdout)
        self.assertNotIn("probability", result.stdout.lower())
        self.assertNotIn("this topic has attracted", result.stdout.lower())

    def test_direct_bounded_prose_passes(self):
        result = self.run_audit(
            "The experiment estimated the treatment contrast in the recruited sample.\n"
            "The estimate was imprecise, so the data do not distinguish the two smallest effects.\n"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("counts: none", result.stdout)

    def test_chinese_formulaic_metadiscourse_is_flagged(self):
        result = self.run_audit("随着数字技术不断发展，值得注意的是，该研究具有重要理论意义。\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("FORMULAIC_OPENING", result.stdout)
        self.assertIn("EMPTY_METADISCOURSE", result.stdout)
        self.assertIn("VAGUE_CONTRIBUTION", result.stdout)


if __name__ == "__main__":
    unittest.main()
