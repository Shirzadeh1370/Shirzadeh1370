"""Reproduce a change detection scenario without touching committed samples."""
import json
from pathlib import Path
import shutil
import tempfile
from fim import snapshot, compare

ROOT = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as temp:
    working = Path(temp) / "sample"
    shutil.copytree(ROOT / "sample_files", working)
    baseline = snapshot(working)
    (working / "app.conf").write_text("app_name=demo-service\nlog_level=debug\n")
    (working / "allowed_hosts.txt").unlink()
    (working / "new_file.txt").write_text("new file\n")
    result = compare(baseline, snapshot(working))

output = ROOT / "outputs/demo_changes.json"
output.parent.mkdir(exist_ok=True)
output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(output)
print(result)
