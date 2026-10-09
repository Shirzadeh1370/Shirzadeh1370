# Cybersecurity & Networking — Six Hands-On Entry-Level Portfolio Projects

Six small, runnable, defensive and offline projects aimed at junior SOC Analyst, IT Support, Network Support, and Security Analyst applications. Built for Python 3.11+ using **only the Python standard library**.

| Project | What it demonstrates | Sample input | Output |
| --- | --- | --- | --- |
| [01. SOC Log Triage](01-soc-log-triage/) | UTC timestamps, failed-login burst detection, correlation | 36 synthetic authentication events | JSON alerts |
| [02. File Integrity Monitor](02-file-integrity-monitor/) | SHA-256 inventory, baseline and change comparison | 2 simulated config files | JSON change report |
| [03. Email Phishing Triage](03-phishing-email-triage/) | .eml header parsing and explainable rule-based risk signals | 2 fictional .eml samples | JSON review assessments |
| [04. VLSM Subnet Planner](04-vlsm-subnet-planner/) | IPv4 CIDR, non-overlapping allocations, host capacity | 5 sample departments | CSV/JSON subnet plan |
| [05. Cisco Config Auditor](05-cisco-config-audit/) | Static IOS management-plane review | Insecure + hardened lab configurations | JSON security findings |
| [06. Network Health Monitor](06-network-health-monitor/) | Packet loss, p95 latency and demo quality thresholds | 60 synthetic ping observations | JSON device health report |

## One-command run + tests

~~~powershell
git clone https://github.com/Shirzadeh1370/Shirzadeh1370.git
cd Shirzadeh1370\cyber-network-portfolio
py -3.11 run_all.py
~~~

Or use python run_all.py if Python 3.11+ is already your default. On macOS/Linux: python3 run_all.py.

The runner executes all six demos and their unit tests and writes to individual outputs/ directories. GitHub Actions repeats these checks on every change and makes the generated reports available as a workflow artifact.

## Data safety, honesty and scope

All identities, emails, configurations and probe data are **fictional training examples**. Documentation-only networks use RFC 5737 ranges. Scripts are designed to run locally **without internet access**, administrator rights, third-party packages, active scans, outbound connections, or modifications to real systems. The file-integrity example modifies **a temporary copy only**.

These are reusable portfolio labs — not production deployments, live SOC investigations, approved penetration tests, security certifications, or official Cisco compliance scans. Rule matches and risk scores are **review cues**, not confirmed attacks.

## Interview and resume wording

**Cybersecurity & Network Engineering Portfolio | Independent Labs**
- Developed and tested six Python-based defensive security and networking utilities, including authentication-log triage, file integrity monitoring, email review, IPv4 subnet planning, IOS-style configuration review, and network health reporting.
- Used standard-library modules including ipaddress, hashlib, csv, email, datetime, and unittest to generate explainable reports from synthetic fixtures.
- Validated outputs with unit tests and GitHub Actions; documented rule limitations, sample-data provenance and safe offline usage.

Use the exact project's README to explain problem, approach, input grain, output, test evidence, limitations and next steps. Never claim fictional output was a real customer incident.

## Tech stack

Python 3.11+ standard library, GitHub Actions CI, JSON, CSV, Cisco IOS-style configuration snippets, RFC 5737 example IPs. No package installation.

### Reference sources
- NIST SP 800-92 log management: https://csrc.nist.gov/pubs/sp/800/92/final
- Cisco SSH access guidance: https://www.cisco.com/c/en/us/support/docs/security-vpn/secure-shell-ssh/4145-ssh.html
- Python ipaddress: https://docs.python.org/3/library/ipaddress.html
- IETF RFC 5737 IPv4 documentation ranges: https://www.rfc-editor.org/rfc/rfc5737
