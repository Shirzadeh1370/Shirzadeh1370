"""Run five independent analytics scripts with the current Python interpreter."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PROJECTS = [
    "01-retail-sales",
    "02-customer-churn",
    "03-helpdesk-sla",
    "04-login-security",
    "05-seattle-weather",
]
if __name__ == "__main__":
    for project in PROJECTS:
        print(f"\n=== {project} ===", flush=True)
        subprocess.run([sys.executable, str(ROOT / project / "analyze.py")],
                       check=True, cwd=ROOT)
    print("\nAll five projects completed. Inspect each outputs/ folder.")
