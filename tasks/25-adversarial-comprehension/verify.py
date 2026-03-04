"""Verify adversarial-comprehension task: contradictory reports analysis."""
from __future__ import annotations

import json
from pathlib import Path


def normalize(s: str) -> str:
    return str(s).strip().lower().replace("-", " ").replace("_", " ")


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

    # Q1: Project name — should be "Atlas" or "Project Atlas"
    q1 = normalize(data.get("q1", ""))
    if "atlas" in q1:
        passed += 1
        details.append("Q1-project-name: OK")
    else:
        details.append(f"Q1-project-name: FAIL (got '{data.get('q1', '')}')")

    # Q2: A vs B disagreement — launch quarter (A says Q1, B says Q2)
    q2 = normalize(data.get("q2", ""))
    # Must mention launch/timeline AND q1/q2 or the quarters
    has_topic = any(kw in q2 for kw in ["launch", "timeline", "quarter", "schedule"])
    has_values = ("q1" in q2 and "q2" in q2) or ("q1 2025" in q2 and "q2 2025" in q2)
    if has_topic and has_values:
        passed += 1
        details.append("Q2-AB-disagreement: OK")
    else:
        details.append(f"Q2-AB-disagreement: FAIL (topic={has_topic}, values={has_values})")

    # Q3: A vs C disagreement — budget (A says $500K, C says $750K)
    q3 = normalize(data.get("q3", ""))
    has_topic = any(kw in q3 for kw in ["budget", "cost", "funding", "financial"])
    has_values = ("500" in q3 and "750" in q3)
    if has_topic and has_values:
        passed += 1
        details.append("Q3-AC-disagreement: OK")
    else:
        details.append(f"Q3-AC-disagreement: FAIL (topic={has_topic}, values={has_values})")

    # Q4: Majority launch quarter — Q1 2025 (A and C agree)
    q4 = normalize(data.get("q4", ""))
    if "q1" in q4 and "2025" in q4:
        passed += 1
        details.append("Q4-majority-launch: OK")
    else:
        details.append(f"Q4-majority-launch: FAIL (got '{data.get('q4', '')}')")

    # Q5: Majority budget — $500,000 (A and B agree)
    q5 = normalize(data.get("q5", ""))
    if "500" in q5:
        passed += 1
        details.append("Q5-majority-budget: OK")
    else:
        details.append(f"Q5-majority-budget: FAIL (got '{data.get('q5', '')}')")

    ok = passed >= 3
    return ok, f"{passed}/{total} checks passed. {'; '.join(details)}"
