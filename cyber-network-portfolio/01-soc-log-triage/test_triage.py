import csv
import tempfile
import unittest
from pathlib import Path
from triage import analyze, parse_timestamp


class TriageTests(unittest.TestCase):
    def setUp(self):
        self.sample = Path(__file__).parent / "data" / "auth_events.csv"

    def test_real_fixture_alerts_and_success_correlation(self):
        report = analyze(self.sample)
        self.assertEqual(report["alert_count"], 2)
        by_user = {a["username"]: a for a in report["alerts"]}
        self.assertEqual(by_user["alex"]["max_failures_in_window"], 6)
        self.assertEqual(by_user["alex"]["priority"], "HIGH")
        self.assertEqual(by_user["admin-lab"]["priority"], "MEDIUM")
        self.assertFalse(by_user["admin-lab"]["followup_success_within_window"])

    def test_invalid_timezone(self):
        with self.assertRaises(ValueError):
            parse_timestamp("2026-10-01T09:00:00")

    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):
            analyze(self.sample, min_failures=1)

    def test_duplicate_ids_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "d.csv"
            with self.sample.open(newline="", encoding="utf-8") as f:
                entries = list(csv.DictReader(f))
            with p.open("w", newline="", encoding="utf-8") as f:
                wr = csv.DictWriter(f, fieldnames=entries[0].keys())
                wr.writeheader()
                wr.writerows(entries + [entries[0]])
            with self.assertRaises(ValueError):
                analyze(p)


if __name__ == "__main__":
    unittest.main()
