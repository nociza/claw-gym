"""Verify image-document-ocr task: check 5 invoice questions with fuzzy matching."""
from __future__ import annotations

import json
from pathlib import Path


def normalize(s: str) -> str:
    return str(s).strip().lower().replace("-", "").replace("_", "").replace(" ", "")


def verify(workspace: Path) -> tuple[bool, str]:
    answers_path = workspace / "answers.json"
    if not answers_path.exists():
        return False, "answers.json not found"

    try:
        data = json.loads(answers_path.read_text(encoding="utf-8"))
    except Exception as e:
        return False, f"Invalid JSON: {e}"

    passed = 0
    total = 5
    details = []

    # Q1: Invoice number — INV-2025-0847
    q1 = normalize(data.get("q1", ""))
    if "inv20250847" in q1 or "0847" in q1:
        passed += 1
        details.append("Q1-invoice-num: OK")
    else:
        details.append(f"Q1-invoice-num: FAIL (got '{data.get('q1', '')}')")

    # Q2: Company name — Northstar Consulting Group
    q2 = normalize(data.get("q2", ""))
    if "northstar" in q2:
        passed += 1
        details.append("Q2-company: OK")
    else:
        details.append(f"Q2-company: FAIL (got '{data.get('q2', '')}')")

    # Q3: Total amount — $9,450.00
    q3 = normalize(data.get("q3", ""))
    if "9450" in q3 or "9,450" in str(data.get("q3", "")):
        passed += 1
        details.append("Q3-total: OK")
    else:
        details.append(f"Q3-total: FAIL (got '{data.get('q3', '')}')")

    # Q4: Invoice date — 2025-11-03
    q4 = str(data.get("q4", "")).strip()
    q4_norm = normalize(q4)
    if "20251103" in q4_norm or "november" in q4.lower() or "nov" in q4.lower() or "11/03" in q4 or "11-03" in q4:
        passed += 1
        details.append("Q4-date: OK")
    else:
        details.append(f"Q4-date: FAIL (got '{q4}')")

    # Q5: Line items — 5
    q5 = str(data.get("q5", "")).strip()
    if "5" in q5:
        passed += 1
        details.append("Q5-line-items: OK")
    else:
        details.append(f"Q5-line-items: FAIL (got '{q5}')")

    ok = passed >= 3
    return ok, f"{passed}/{total} checks passed. {'; '.join(details)}"
