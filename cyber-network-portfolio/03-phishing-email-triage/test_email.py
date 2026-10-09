from pathlib import Path
import unittest
from triage_email import inspect


class EmailTests(unittest.TestCase):
    def setUp(self):
        self.samples = Path(__file__).parent / "samples"

    def test_benign_fixture(self):
        report = inspect(self.samples / "benign.eml")
        self.assertEqual(report["score"], 0)
        self.assertEqual(report["triage"], "LOW_REVIEW")

    def test_suspicious_fixture(self):
        report = inspect(self.samples / "suspicious.eml")
        self.assertEqual(report["triage"], "HIGH_REVIEW")
        self.assertIn("reply_to_domain_mismatch", report["signals"])
        self.assertIn("header_reports_dmarc_fail_unverified", report["signals"])
        self.assertGreaterEqual(report["score"], 4)


if __name__ == "__main__":
    unittest.main()
