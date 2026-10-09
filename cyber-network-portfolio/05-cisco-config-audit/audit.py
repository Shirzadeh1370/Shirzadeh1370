"""Static, read-only Cisco IOS-style configuration reviewer."""
import argparse
import json
from pathlib import Path


def review(content):
    lines = content.splitlines()
    findings = []
    def flag(rule, severity, line, explanation):
        findings.append({"rule": rule, "severity": severity,
                         "line": line, "explanation": explanation})

    has_ssh_v2 = any(line.strip().lower() == "ip ssh version 2" for line in lines)
    blocks = []
    current = None
    for number, raw in enumerate(lines, 1):
        token = raw.strip().lower()
        if token.startswith("line vty "):
            current = {"start": number, "commands": []}
            blocks.append(current)
            continue
        if raw and not raw[0].isspace() or token == "!":
            current = None
        if current and token and token != "!":
            current["commands"].append((number, token))
        if token.startswith("enable password "):
            flag("ENABLE_PASSWORD_LEGACY", "HIGH", number,
                 "Legacy enable password directive found; review use of enable secret.")
        if token.startswith("snmp-server community "):
            flag("SNMP_COMMUNITY_PRESENT", "MEDIUM", number,
                 "SNMPv1/v2c community configured; evaluate SNMPv3 and controls.")
    if not has_ssh_v2:
        flag("SSH_V2_NOT_EXPLICIT", "REVIEW", None,
             "SSH version 2 not explicitly configured in this text.")
    if not blocks:
        flag("NO_VTY_BLOCK", "REVIEW", None,
             "No VTY section found; verify device/platform and intended access.")
    for block in blocks:
        commands = block["commands"]
        transports = [(num, cmd) for num, cmd in commands if cmd.startswith("transport input ")]
        is_disabled = any(cmd == "transport input none" for _, cmd in transports)
        if not transports:
            flag("VTY_TRANSPORT_UNSPECIFIED", "REVIEW", block["start"],
                 "VTY transport policy not explicit in this block.")
        for num, cmd in transports:
            if "telnet" in cmd.split() or "all" in cmd.split():
                flag("VTY_ALLOWS_TELNET", "HIGH", num,
                     "VTY transport permits a potentially plaintext Telnet path.")
            elif cmd not in ("transport input ssh", "transport input none"):
                flag("VTY_TRANSPORT_REVIEW", "REVIEW", num,
                     "Review VTY transport list for this platform.")
        has_auth = any(cmd == "login local" or cmd.startswith("login authentication ")
                       for _, cmd in commands)
        if not is_disabled and not has_auth:
            flag("VTY_AUTH_POLICY_REVIEW", "MEDIUM", block["start"],
                 "No explicit local/AAA login policy detected in VTY block.")
    return {
        "scope": "static IOS-style text heuristic; not an official CIS audit",
        "vty_blocks": len(blocks),
        "finding_count": len(findings),
        "counts_by_severity": {severity: sum(
            f["severity"] == severity for f in findings)
            for severity in ("HIGH", "MEDIUM", "REVIEW")},
        "findings": findings,
    }


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Audit an offline IOS-style config")
    parser.add_argument("--input", type=Path, default=root / "samples/insecure_lab.cfg")
    parser.add_argument("--output", type=Path, default=root / "outputs/config_findings.json")
    args = parser.parse_args()
    report = review(args.input.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report["counts_by_severity"], indent=2))


if __name__ == "__main__":
    main()
