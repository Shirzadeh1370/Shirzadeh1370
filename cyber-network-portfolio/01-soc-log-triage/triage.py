"""Offline log triage; no claim that a detected burst is an intrusion."""
import argparse
import csv
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path


def parse_timestamp(value):
    stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        raise ValueError("timestamps must contain a timezone")
    return stamp.astimezone(timezone.utc)


def analyze(path, window_minutes=15, min_failures=5):
    if window_minutes <= 0 or min_failures < 2:
        raise ValueError("window_minutes must be >0 and min_failures >=2")
    rows = []
    with Path(path).open(newline="", encoding="utf-8") as stream:
        for item in csv.DictReader(stream):
            if item["outcome"] not in ("FAIL", "SUCCESS"):
                raise ValueError("unsupported outcome")
            item["at"] = parse_timestamp(item["timestamp_utc"])
            rows.append(item)
    if len({row["event_id"] for row in rows}) != len(rows):
        raise ValueError("duplicate event_id")
    groups = defaultdict(list)
    for row in rows:
        groups[(row["username"], row["source_ip"])].append(row)
    alerts = []
    window = timedelta(minutes=window_minutes)
    for (user, ip), events in sorted(groups.items()):
        events.sort(key=lambda item: item["at"])
        recent_failures = deque()
        peak = []
        peak_end = None
        for row in events:
            if row["outcome"] != "FAIL":
                continue
            recent_failures.append(row)
            while recent_failures and row["at"] - recent_failures[0]["at"] > window:
                recent_failures.popleft()
            if len(recent_failures) > len(peak):
                peak = list(recent_failures)
                peak_end = row["at"]
        if len(peak) < min_failures:
            continue
        followup_success = any(
            e["outcome"] == "SUCCESS" and
            peak_end <= e["at"] <= peak_end + window
            for e in events
        )
        alerts.append({
            "username": user,
            "source_ip": ip,
            "max_failures_in_window": len(peak),
            "window_start_utc": peak[0]["at"].isoformat(),
            "window_end_utc": peak_end.isoformat(),
            "success_within_15m_after_burst": followup_success
            if window_minutes == 15 else None,
            "followup_success_within_window": followup_success,
            "priority": "HIGH" if followup_success else "MEDIUM",
            "reason": "Repeated authentication failures; analyst review required",
        })
    alerts.sort(key=lambda item: (item["priority"] != "HIGH", -item["max_failures_in_window"]))
    return {
        "source": "synthetic_offline_auth_log",
        "event_count": len(rows),
        "failed_events": sum(row["outcome"] == "FAIL" for row in rows),
        "alert_count": len(alerts),
        "policy": {"window_minutes": window_minutes, "min_failures": min_failures},
        "alerts": alerts,
    }


def main():
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Offline authentication event triage")
    parser.add_argument("--input", type=Path, default=base / "data/auth_events.csv")
    parser.add_argument("--output", type=Path, default=base / "outputs/alerts.json")
    args = parser.parse_args()
    report = analyze(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "alerts"}, indent=2))


if __name__ == "__main__":
    main()
