"""Offline, heuristic .eml triage. Never fetches or opens email links."""
import argparse
from email import policy
from email.parser import BytesParser
from email.utils import parseaddr
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

URL_PATTERN = re.compile(r"https?://[^\s<>'\"]+", re.IGNORECASE)
URGENCY_PATTERN = re.compile(
    r"\b(urgent|immediately|verify your password|access will expire)\b",
    re.IGNORECASE,
)


def domain_of(addr):
    address = parseaddr(addr or "")[1].lower()
    return address.rsplit("@", 1)[-1] if "@" in address else ""


def inspect(path):
    with Path(path).open("rb") as stream:
        msg = BytesParser(policy=policy.default).parse(stream)
    sender_domain = domain_of(msg.get("From", ""))
    reply_domain = domain_of(msg.get("Reply-To", "")) if msg.get("Reply-To") else ""
    text_parts = []
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                text_parts.append(part.get_content())
    elif msg.get_content_type() == "text/plain":
        text_parts.append(msg.get_content())
    body = "\n".join(str(x) for x in text_parts)
    urls = [urlsplit(u.rstrip(".,;")).hostname or ""
            for u in URL_PATTERN.findall(body)]
    auth_results = " ".join(msg.get_all("Authentication-Results", []))
    signals = []
    if not sender_domain:
        signals.append("missing_sender_domain")
    if reply_domain and reply_domain != sender_domain:
        signals.append("reply_to_domain_mismatch")
    if any(u and u != sender_domain for u in urls):
        signals.append("external_link_domain_mismatch")
    if URGENCY_PATTERN.search((msg.get("Subject", "") or "") + "\n" + body):
        signals.append("urgency_language")
    if re.search(r"\bdmarc=fail\b", auth_results, re.IGNORECASE):
        signals.append("header_reports_dmarc_fail_unverified")
    score = len(signals)
    return {
        "file": Path(path).name,
        "sender_domain": sender_domain,
        "reply_to_domain": reply_domain,
        "link_domains": sorted(set(urls)),
        "signals": signals,
        "score": score,
        "triage": "HIGH_REVIEW" if score >= 3 else
                  "REVIEW" if score >= 1 else "LOW_REVIEW",
        "auth_result_warning": "Authentication-Results can be spoofed; header claims are not independently verified.",
        "note": "Offline heuristic demo, not a finding of phishing.",
    }


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Inspect local .eml files (offline)")
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--output", type=Path, default=root / "outputs/email_triage.json")
    args = parser.parse_args()
    files = args.files or sorted((root / "samples").glob("*.eml"))
    output = [inspect(path) for path in files]
    args.output.parent.mkdir(exist_ok=True, parents=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps([{"file": p["file"], "triage": p["triage"], "score": p["score"]}
                      for p in output], indent=2))


if __name__ == "__main__":
    main()
