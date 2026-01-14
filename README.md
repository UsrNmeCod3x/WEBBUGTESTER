# RAVEN-BB 🦅
### Bug Bounty Oriented Web Vulnerability Framework

RAVEN-BB is a **signal-based bug bounty framework** designed to help security researchers
identify **high-impact attack surfaces** such as:

- Hidden JavaScript endpoints
- Wayback (archived) endpoints
- IDOR candidates
- Open redirects
- Reflected XSS
- SQL injection signals

⚠️ This tool is **NOT an automatic exploitation scanner**.
It assists **manual bug hunting**, following real-world bounty workflows.

---

## ✨ Features

- Wayback URL discovery
- JavaScript endpoint extraction
- Open redirect detection
- Reflected XSS signals
- SQLi time-based signals
- IDOR indicators
- Burp Suite proxy support
- LOW / MEDIUM / HIGH confidence findings

---

## 🧠 Philosophy

> Automation should **assist thinking**, not replace it.

RAVEN-BB highlights **interesting attack surfaces** so researchers can
manually exploit logic flaws and chained vulnerabilities.

---

## 🚀 Installation

```bash
git clone https://github.com/UsrNmeCod3x/WEBBUGTESTER.git
cd WEBBUGTESTER
pip install -r requirements.txt
