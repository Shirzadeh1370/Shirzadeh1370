# 02 — File Integrity Monitor (SHA-256)

**Scenario:** Identify unauthorized or unexpected changes in a local configuration-file directory.

**Features:** A read-only directory inventory, SHA-256 hashes, a JSON baseline, and a comparison report listing files that were added, removed, modified, or unchanged. Symlink entries are deliberately skipped. The baseline and reports must be placed outside the monitored directory.

## Reproducible demonstration
~~~powershell
python demo.py
python -m unittest test_fim.py -v
~~~

Produces outputs/demo_changes.json from a temporary copy of sample_files, without altering committed fixtures.

## Real local run
~~~powershell
python fim.py init sample_files --manifest outputs/baseline.json
python fim.py check sample_files --manifest outputs/baseline.json --report outputs/latest_check.json
~~~

**Expected demo:** app.conf modified; allowed_hosts.txt removed; new_file.txt added.

**Skills:** SHA-256, defensive monitoring, change detection, pathlib, JSON, safe temporary-directory tests.

**Caveats:** A baseline stored on a compromised system can be tampered with. This is **not** an antivirus, an EDR agent, a real-time monitor, or a tamper-proof integrity service. The tool does not acquire permissions or modify monitored files.

**Interview talking point:** "I used SHA-256 file hashing and a baseline comparison to detect three kinds of changes, including automated negative/positive tests."
