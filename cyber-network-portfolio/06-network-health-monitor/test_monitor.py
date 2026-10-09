from pathlib import Path
import tempfile
import unittest
from monitor import analyze, percentile_nearest_rank


class MonitorTests(unittest.TestCase):
    def test_known_fixture_results(self):
        report = analyze(Path(__file__).parent / "data/synthetic_probes.csv")
        got = {item["device"]: item for item in report["devices"]}
        self.assertEqual(len(got), 3)
        self.assertEqual(got["router-A"]["status"], "HEALTHY")
        self.assertEqual(got["switch-B"]["loss_pct"], 20.0)
        self.assertEqual(got["switch-B"]["status"], "DEGRADED")
        self.assertEqual(got["wifi-AP"]["status"], "DEGRADED")
        self.assertEqual(got["wifi-AP"]["p95_latency_ms"], 210.0)

    def test_nearest_rank(self):
        self.assertEqual(percentile_nearest_rank([3, 1, 4, 2, 5], 0.95), 5)
        self.assertIsNone(percentile_nearest_rank([], 0.95))

    def test_reject_failed_probe_with_latency(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.csv"
            path.write_text("timestamp_utc,device,success,latency_ms\n"
                            "2026-10-01T12:00:00Z,router,0,20\n")
            with self.assertRaises(ValueError):
                analyze(path)

    def test_reject_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.csv"
            path.write_text("timestamp_utc,device,success,latency_ms\n")
            with self.assertRaises(ValueError):
                analyze(path)


if __name__ == "__main__":
    unittest.main()
