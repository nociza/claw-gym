"""Verify transcript-analysis task: check 5 questions about transcript + WAV."""
from __future__ import annotations

import json
from pathlib import Path


def normalize(s: str) -> str:
    return str(s).strip().lower()


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

    # Q1: Number of speakers — 4
    q1 = data.get("q1")
    try:
        if int(q1) == 4:
            passed += 1
            details.append("Q1-speakers: OK (4)")
        else:
            details.append(f"Q1-speakers: FAIL (got {q1}, expected 4)")
    except (ValueError, TypeError):
        details.append(f"Q1-speakers: FAIL (got '{q1}')")

    # Q2: Decision — PostgreSQL migration
    q2 = normalize(data.get("q2", ""))
    if "postgre" in q2 and ("migrat" in q2 or "move" in q2 or "switch" in q2 or "adopt" in q2):
        passed += 1
        details.append("Q2-decision: OK")
    elif "postgre" in q2:
        # Mention of PostgreSQL is sufficient
        passed += 1
        details.append("Q2-decision: OK (mentioned PostgreSQL)")
    else:
        details.append(f"Q2-decision: FAIL (got '{data.get('q2', '')}')")

    # Q3: WAV duration — 5.0 seconds
    q3 = data.get("q3")
    try:
        dur = float(q3)
        if abs(dur - 5.0) < 0.5:
            passed += 1
            details.append(f"Q3-duration: OK ({dur}s)")
        else:
            details.append(f"Q3-duration: FAIL (got {dur}s, expected 5.0)")
    except (ValueError, TypeError):
        details.append(f"Q3-duration: FAIL (got '{q3}')")

    # Q4: Sample rate — 44100
    q4 = data.get("q4")
    try:
        sr = int(q4)
        if sr == 44100:
            passed += 1
            details.append("Q4-sample-rate: OK (44100)")
        else:
            details.append(f"Q4-sample-rate: FAIL (got {sr}, expected 44100)")
    except (ValueError, TypeError):
        details.append(f"Q4-sample-rate: FAIL (got '{q4}')")

    # Q5: Action items — 4
    q5 = data.get("q5")
    try:
        if int(q5) == 4:
            passed += 1
            details.append("Q5-action-items: OK (4)")
        else:
            details.append(f"Q5-action-items: FAIL (got {q5}, expected 4)")
    except (ValueError, TypeError):
        details.append(f"Q5-action-items: FAIL (got '{q5}')")

    ok = passed >= 3
    return ok, f"{passed}/{total} checks passed. {'; '.join(details)}"
