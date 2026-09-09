import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import resolve_paper as resolver  # noqa: E402
import fetch_institutional as institutional  # noqa: E402


class ResolverUnitTests(unittest.TestCase):
    def test_normalize_doi_strips_common_prefixes(self):
        self.assertEqual(
            resolver.normalize_doi("https://doi.org/10.1080/1234.5678"),
            "10.1080/1234.5678",
        )
        self.assertEqual(resolver.normalize_doi("doi:10.1111/AB12"), "10.1111/ab12")

    def test_openalex_pdf_url_classifies_as_oa(self):
        metadata = {
            "doi": "10.1080/1234",
            "title": "OA Paper",
            "best_oa_location": {"pdf_url": "https://example.org/o.pdf", "is_oa": True},
            "locations": [{"pdf_url": "https://example.org/o.pdf", "is_oa": True}],
        }
        row = resolver.classify_from_openalex("10.1080/1234", metadata)
        self.assertEqual(row.status, "oa")
        self.assertTrue(row.source.endswith("o.pdf"))

    def test_institutional_publisher_pdf_urls(self):
        self.assertEqual(
            institutional.publisher_pdf_url({"doi": "10.1080/1", "journal_slug": "cmm"}),
            "https://www.tandfonline.com/doi/pdf/10.1080/1?needAccess=true",
        )
        self.assertEqual(
            institutional.publisher_pdf_url({"doi": "10.1080/2", "journal_slug": "dj"}),
            "https://www.tandfonline.com/doi/pdf/10.1080/2?needAccess=true",
        )
        self.assertEqual(
            institutional.publisher_pdf_url({"doi": "10.1177/3", "journal_slug": "nms"}),
            "https://journals.sagepub.com/doi/pdf/10.1177/3?download=true",
        )
        # Oxford needs a landing-page step, not a direct DOI PDF.
        self.assertIsNone(
            institutional.publisher_pdf_url({"doi": "10.1093/joc/jqae046", "journal_slug": "joc"})
        )

    def test_repository_pdf_url_classifies_as_repository(self):
        metadata = {
            "doi": "10.1000/rep1",
            "title": "Repo Paper",
            "best_oa_location": None,
            "locations": [{"pdf_url": "https://archive.org/paper.pdf", "is_oa": False}],
        }
        row = resolver.classify_from_openalex("10.1000/rep1", metadata)
        self.assertEqual(row.status, "repository")

    def test_no_pdf_with_institution_requires_user_auth(self):
        institution = {
            "homepage": "https://library.example.edu",
            "resources": ["CNKI", "EBSCOhost"],
        }
        metadata = {"doi": "10.1000/pay", "title": "Paywalled", "locations": []}
        row = resolver.classify_from_openalex(
            "10.1000/pay", metadata, institution=institution, layers={1, 2, 3, 4}
        )
        self.assertEqual(row.status, "institution")
        self.assertTrue(row.auth_required)

    def test_delivery_is_last_configured_route(self):
        institution = {
            "homepage": "https://library.example.edu",
            "resources": ["百链 (document delivery)"],
        }
        metadata = {"doi": "10.1000/rare", "title": "Rare", "locations": []}
        row = resolver.classify_from_openalex(
            "10.1000/rare", metadata, institution=institution, layers={1, 5}
        )
        self.assertEqual(row.status, "delivery")

    def test_offline_without_institution_is_unavailable(self):
        row = resolver.classify_from_openalex(
            "10.1000/x",
            {},
            offline=True,
        )
        self.assertEqual(row.status, "unavailable")
        self.assertIn("offline", row.reason.lower())

    def test_parse_layers(self):
        self.assertEqual(resolver.parse_layers(["1,4"]), {1, 4})
        self.assertEqual(resolver.parse_layers(["1-3", "5"]), {1, 2, 3, 5})


class ResolverCliTests(unittest.TestCase):
    def run_cli(self, *args: str):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "resolve_paper.py"), *args],
            text=True,
            capture_output=True,
            encoding="utf-8",
        )

    def test_offline_cli_returns_json_without_network(self):
        result = self.run_cli("--doi", "10.1000/fake", "--offline", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["dry_run"])
        self.assertEqual(payload["items"][0]["status"], "unavailable")

    def test_cli_table_marks_dry_run(self):
        result = self.run_cli("--title", "Some Title", "--offline", "--format", "table")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DRY RUN", result.stdout)

    def test_cuc_adapter_reads_resources_without_credentials(self):
        config = resolver.read_institution_config(ROOT / "institutions" / "cuc.yaml")
        self.assertTrue(any(item.startswith("CNKI") for item in config["resources"]))
        self.assertNotIn("password", config)
        self.assertNotIn("token", config)


if __name__ == "__main__":
    unittest.main()
