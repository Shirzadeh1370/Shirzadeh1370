# 03 — Offline Phishing Email Triage

**Scenario:** A help desk/security analyst receives suspicious messages and needs a repeatable checklist, not a guess based on visual appearance.

**What it inspects:** From and Reply-To domains, URL domains in text bodies, urgency language, and whether an Authentication-Results header *claims* a DMARC failure. The parser does **not** independently validate SPF, DKIM, or DMARC, and must not be presented as doing so. A reported mismatch is a review signal, not evidence of malicious intent.

## Run (offline)
~~~powershell
python triage_email.py
python -m unittest test_email.py -v
~~~

Output: outputs/email_triage.json. Sample fixtures use reserved example domains. No email account, browser, DNS query, outbound request, or message sending is used.

## Sample interpretation
- benign.eml: zero heuristic signals, LOW_REVIEW
- suspicious.eml: domain mismatch, urgency, and an unverified claimed DMARC failure; HIGH_REVIEW

**Skills:** .eml parsing, email headers, phishing triage, risk scoring, careful evidence wording, unit testing.

**Interview talking point:** "I built an offline parser that helps analysts prioritize messages while clearly distinguishing reported email-authentication header claims from verified results."

**Limitations:** display-name spoofing, HTML links, redirects, Unicode homographs, domain age, authenticated infrastructure, attachment analysis and false positives require stronger tooling and human validation.
