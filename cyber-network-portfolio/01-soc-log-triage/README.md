# 01 — SOC Authentication Log Triage

**Scenario:** A junior SOC analyst receives an authentication CSV and must distinguish routine failures from concentrated user/source activity.

**What the script actually does:** parses UTC timestamps, validates unique IDs, groups by username + source IP, finds the highest number of failures within a rolling 15-minute interval, and flags groups with 5+ failures. If the same user/source then succeeds within 15 minutes after the burst, the rule increases review priority. Flags are **not a diagnosis of compromise**.

## Run
From this project folder using Python 3.11+ (no third-party packages):

~~~powershell
python triage.py
python -m unittest test_triage.py -v
~~~

**Data:** 36 entirely synthetic events. Addresses are documentation-only TEST-NET ranges (RFC 5737). No production SIEM connection and no live authentication.

**Expected sample results:** 2 groups flagged: alex has 6 failures with a later success (HIGH review); admin-lab has 5 failures without that correlation (MEDIUM review). Generated output: outputs/alerts.json.

**Skills:** incident-triage thinking, log parsing, datetime, rolling windows, detection rules, careful interpretation, unit tests.

**Interview example:** "I built and tested a transparent authentication-log triage rule, validated input quality, and prioritized correlated failure-to-success sequences for analyst review."

**Limitations/next step:** no baseline by user, host inventory, alert deduplication across users, geo-validation, or verified attacker identity. Real monitoring would require approved logs, time synchronization, tuning, and false-positive review.

Reference: NIST SP 800-92 (log management): https://csrc.nist.gov/pubs/sp/800/92/final
