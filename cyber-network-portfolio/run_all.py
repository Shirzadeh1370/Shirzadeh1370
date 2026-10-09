"""Run six offline demos and all per-project unit tests."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PROJECTS = [
    ("01-soc-log-triage", "triage.py"),
    ("02-file-integrity-monitor", "demo.py"),
    ("03-phishing-email-triage", "triage_email.py"),
    ("04-vlsm-subnet-planner", "planner.py"),
    ("05-cisco-config-audit", "audit.py"),
    ("06-network-health-monitor", "monitor.py"),
]


def main():
    for name, script in PROJECTS:
        workdir = ROOT / name
        print(f"\n=== {name}: run demo ===", flush=True)
        subprocess.run([sys.executable, script], cwd=workdir, check=True)
        print(f"=== {name}: test ===", flush=True)
        subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", ".",
             "-p", "test_*.py", "-v"],
            cwd=workdir, check=True,
        )
    print("\nAll six demos and test suites passed.", flush=True)


if __name__ == "__main__":
    main()
