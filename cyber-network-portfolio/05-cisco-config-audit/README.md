# 05 — Cisco IOS-Style Configuration Security Auditor

**Scenario:** Review a saved router/switch configuration before a change window, without logging into devices or making network changes.

**Rules:** checks for explicitly configured SSHv2, VTY transport including Telnet, missing explicit local/AAA VTY login commands, legacy enable password directives, and SNMP community lines. Findings are **review prompts**; they are not a certification or a full configuration assessment. The static parser is intended for small training snippets, not every IOS syntax/version.

## Run
~~~powershell
python audit.py --input samples/insecure_lab.cfg --output outputs/insecure.json
python audit.py --input samples/hardened_lab.cfg --output outputs/hardened.json
python -m unittest test_audit.py -v
~~~

**Expected:** insecure training sample produces several findings, hardened sample produces zero under these narrowly scoped rules. Reports include rule IDs and line numbers but **do not echo secret values**.

**Skills:** Cisco IOS configuration reading, SSH and VTY hardening concepts, secure management protocols, configuration linting, test-driven scripting.

**Interview talking point:** "I created a read-only rule-based validator to catch common management-plane configuration risks in Cisco IOS-style backups."

**Important:** Actual device hardening requires review of model/IOS version, management ACLs, AAA, cryptographic choices, secret handling and organizational policy; no real-world compliance claim is made.

Reference: Cisco SSH configuration guidance, https://www.cisco.com/c/en/us/support/docs/security-vpn/secure-shell-ssh/4145-ssh.html
