import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/communication-writing/scripts/check_manuscript.py"


def packet():
    return {
        "schema_version": "communication-writing-packet/v1",
        "document_id": "synthetic-manuscript",
        "stage": "draft",
        "source_of_truth": ["results.json"],
        "required_sections": ["Introduction", "Methods", "Results", "Discussion"],
        "claims": [
            {
                "id": "C001",
                "status": "verified",
                "evidence": ["R001"],
                "boundary": "synthetic sample only",
                "required": True,
            }
        ],
        "numbers": [
            {"id": "N001", "value": "42", "source": "R001", "required": True}
        ],
        "terms": [{"canonical": "source credibility", "forbidden": ["source quality"]}],
    }


class CommunicationWritingCheckTests(unittest.TestCase):
    def run_check(self, manuscript: str, value: dict):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manuscript_path = root / "manuscript.md"
            packet_path = root / "packet.json"
            manuscript_path.write_text(manuscript, encoding="utf-8")
            packet_path.write_text(json.dumps(value), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(manuscript_path), str(packet_path)],
                text=True,
                capture_output=True,
                encoding="utf-8",
            )

    def test_verified_marked_manuscript_passes(self):
        manuscript = """# Synthetic paper
## Introduction
The question is bounded.
## Methodology
The synthetic design is documented.
## Results
The estimate was 42. <!-- number:N001 --> <!-- claim:C001 -->
## Discussion
The conclusion stays inside the synthetic sample.
"""
        result = self.run_check(manuscript, packet())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unverified_claim_and_placeholder_fail(self):
        value = packet()
        value["claims"][0]["status"] = "unverified"
        manuscript = """# Synthetic paper
## Introduction
[CITATION NEEDED]
## Methodology
The synthetic design is documented.
## Results
The estimate was 42. <!-- number:N001 --> <!-- claim:C001 -->
## Discussion
Boundary.
"""
        result = self.run_check(manuscript, value)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("claim:C001: status is not verified", result.stdout)
        self.assertIn("placeholder", result.stdout)

    def test_missing_number_and_forbidden_alias_fail(self):
        manuscript = """# Synthetic paper
## Introduction
The source quality construct was used.
## Methodology
The synthetic design is documented.
## Results
<!-- claim:C001 -->
## Discussion
Boundary.
"""
        result = self.run_check(manuscript, packet())
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("number:N001: required marker missing", result.stdout)
        self.assertIn("forbidden alias", result.stdout)


if __name__ == "__main__":
    unittest.main()
