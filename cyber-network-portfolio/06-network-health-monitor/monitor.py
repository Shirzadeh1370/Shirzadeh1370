"""Analyze pre-recorded synthetic ping probes. Does not send network packets."""
import argparse
import csv
from collections import defaultdict
from datetime import datetime
import json
import math
from pathlib import Path

MAX_LOSS_PCT = 5.0
MAX_P95_LATENCY_MS = 100.0


def percentile_nearest_rank(values, p):
    if not values:
        return None
    ordered = sorted(values)
    return ordered[max(0, math.ceil(p * len(ordered)) - 1)]


def analyze(path):
    devices = defaultdict(list)
    with Path(path).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not {"timestamp_utc", "device", "success", "latency_ms"}.issubset(reader.fieldnames):
            raise ValueError("missing columns")
        for row in reader:
            datetime.fromisoformat(row["timestamp_utc"].replace("Z", "+00:00"))
            if row["success"] not in ("0", "1"):
                raise ValueError("success must be 0 or 1")
            if not row["device"].strip():
                raise ValueError("empty device")
            success = row["success"] == "1"
            if success and (not row["latency_ms"] or float(row["latency_ms"]) < 0):
                raise ValueError("successful probes need nonnegative latency")
            if not success and row["latency_ms"]:
                raise ValueError("failed probes must have blank latency")
            devices[row["device"]].append(float(row["latency_ms"]) if success else None)
    summary = []
    for name, samples in sorted(devices.items()):
        successes = [x for x in samples if x is not None]
        loss_pct = round(100 * (1 - len(successes) / len(samples)), 1)
        p95 = percentile_nearest_rank(successes, 0.95)
        degraded = loss_pct > MAX_LOSS_PCT or p95 is None or p95 > MAX_P95_LATENCY_MS
        summary.append({"device": name, "probes": len(samples),
                        "successes": len(successes), "loss_pct": loss_pct,
                        "p95_latency_ms": p95,
                        "status": "DEGRADED" if degraded else "HEALTHY"})
    if not summary:
        raise ValueError("no probe rows")
    return {"source": "synthetic_offline_probes",
            "thresholds": {"max_loss_pct": MAX_LOSS_PCT,
                           "max_p95_latency_ms": MAX_P95_LATENCY_MS},
            "devices": summary}


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Offline network quality report")
    parser.add_argument("--input", type=Path, default=root / "data/synthetic_probes.csv")
    parser.add_argument("--output", type=Path, default=root / "outputs/health.json")
    args = parser.parse_args()
    report = analyze(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for d in report["devices"]:
        print(f'{d["device"]:12} loss={d["loss_pct"]:5}% '
              f'p95={str(d["p95_latency_ms"]):>6} ms {d["status"]}')


if __name__ == "__main__":
    main()
