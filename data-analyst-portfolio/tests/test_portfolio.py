"""End-to-end smoke tests: run every project and inspect its outputs."""
from pathlib import Path
import json
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = [
    "01-retail-sales", "02-customer-churn", "03-helpdesk-sla",
    "04-login-security", "05-seattle-weather",
]

class PortfolioTests(unittest.TestCase):
    def test_all_five_analyses(self):
        for name in PROJECTS:
            with self.subTest(project=name):
                target = ROOT / name
                run = subprocess.run(
                    [sys.executable, str(target / "analyze.py")],
                    cwd=ROOT, capture_output=True, text=True, timeout=120)
                self.assertEqual(run.returncode, 0, msg=run.stderr)
                out = target / "outputs"
                for filename in ("kpis.csv", "sql_results.csv",
                                 "summary.json", "chart.png"):
                    self.assertTrue((out / filename).exists(),
                                    msg=f"{name}/{filename} missing")
                    self.assertGreater((out / filename).stat().st_size, 10)
                report = json.loads((out / "summary.json").read_text())
                self.assertGreater(report["rows"], 100)
                sql_lines = (out / "sql_results.csv").read_text().splitlines()
                self.assertGreaterEqual(len(sql_lines), 2)

if __name__ == "__main__":
    unittest.main()
