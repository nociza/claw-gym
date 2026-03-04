"""Verify task 13: corpus-meeting-notes."""

import json
import sys
from pathlib import Path


def normalize(val: str) -> str:
    return str(val).strip().lower().replace("-", " ").replace("_", " ")


def verify(workspace: Path) -> tuple[bool, str]:
    path = workspace / "answers.json"
    if not path.exists():
        return False, "answers.json not found"

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"Failed to parse answers.json: {exc}"

    passed = 0
    checks = []

    # Q1: Unique attendees = 8
    q1 = data.get("q1")
    try:
        if abs(int(q1) - 8) <= 1:  # tolerance of 1
            passed += 1
            checks.append("q1-attendees: PASS")
        else:
            checks.append(f"q1-attendees: FAIL (got {q1}, expected 8)")
    except (TypeError, ValueError):
        checks.append(f"q1-attendees: FAIL (got '{q1}')")

    # Q2: Total action items = 20
    q2 = data.get("q2")
    try:
        if abs(int(q2) - 20) <= 1:
            passed += 1
            checks.append("q2-action-items: PASS")
        else:
            checks.append(f"q2-action-items: FAIL (got {q2}, expected 20)")
    except (TypeError, ValueError):
        checks.append(f"q2-action-items: FAIL (got '{q2}')")

    # Q3: Sarah Chen action items = 4
    q3 = data.get("q3")
    try:
        if abs(int(q3) - 4) <= 1:
            passed += 1
            checks.append("q3-sarah-items: PASS")
        else:
            checks.append(f"q3-sarah-items: FAIL (got {q3}, expected 4)")
    except (TypeError, ValueError):
        checks.append(f"q3-sarah-items: FAIL (got '{q3}')")

    # Q4: Meetings discussing migration
    # Expected: sprint-planning, sprint-review, architecture-review, quarterly-planning
    q4 = data.get("q4", [])
    if isinstance(q4, list):
        q4_norm = {normalize(v) for v in q4}
        expected_migration = {"sprint planning", "sprint review", "architecture review", "quarterly planning"}
        matched = 0
        for exp in expected_migration:
            if any(exp.replace(" ", "") in n.replace(" ", "").replace("-", "") for n in q4_norm):
                matched += 1
        if matched >= 3:
            passed += 1
            checks.append(f"q4-migration: PASS ({matched}/4)")
        else:
            checks.append(f"q4-migration: FAIL (matched {matched})")
    else:
        checks.append("q4-migration: FAIL (not a list)")

    # Q5: Overdue action items (due before 2026-03-01) = 11
    q5 = data.get("q5")
    try:
        if abs(int(q5) - 11) <= 2:  # tolerance of 2
            passed += 1
            checks.append("q5-overdue: PASS")
        else:
            checks.append(f"q5-overdue: FAIL (got {q5}, expected ~11)")
    except (TypeError, ValueError):
        checks.append(f"q5-overdue: FAIL (got '{q5}')")

    ok = passed >= 3  # 3 out of 5
    summary = f"{passed}/5 answers correct. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
