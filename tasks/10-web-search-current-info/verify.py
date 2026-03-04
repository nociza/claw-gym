"""Verify task 10: web-search-current-info."""

import json
import sys
from pathlib import Path

UN_MEMBERS = {"china", "france", "russia", "united kingdom", "united states",
              "uk", "us", "usa", "britain", "great britain", "russian federation",
              "prc", "people's republic of china"}
OLYMPIC_COLORS = {"blue", "yellow", "black", "green", "red"}


def normalize(val: str) -> str:
    return str(val).strip().lower()


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

    # Q1: UN Security Council permanent members
    q1 = data.get("q1", [])
    if isinstance(q1, list):
        normalized_members = {normalize(m) for m in q1}
        # Check that all 5 canonical members are covered
        canonical = {"china", "france", "russia", "united kingdom", "united states"}
        matched = 0
        for canon in canonical:
            if any(canon in m or m in UN_MEMBERS for m in normalized_members):
                matched += 1
        if matched >= 4:
            passed += 1
            checks.append("q1-un: PASS")
        else:
            checks.append(f"q1-un: FAIL (matched {matched}/5)")
    else:
        checks.append("q1-un: FAIL (not a list)")

    # Q2: JPY
    q2 = normalize(str(data.get("q2", "")))
    if "jpy" in q2:
        passed += 1
        checks.append("q2-currency: PASS")
    else:
        checks.append(f"q2-currency: FAIL (got '{data.get('q2', '')}')")

    # Q3: Burj Khalifa
    q3 = normalize(str(data.get("q3", "")))
    if "burj khalifa" in q3 or "burj" in q3:
        passed += 1
        checks.append("q3-building: PASS")
    else:
        checks.append(f"q3-building: FAIL (got '{data.get('q3', '')}')")

    # Q4: Olympic ring colors
    q4 = data.get("q4", [])
    if isinstance(q4, list):
        colors = {normalize(c) for c in q4}
        if colors >= OLYMPIC_COLORS or len(colors & OLYMPIC_COLORS) >= 4:
            passed += 1
            checks.append("q4-colors: PASS")
        else:
            checks.append(f"q4-colors: FAIL (got {colors})")
    else:
        checks.append("q4-colors: FAIL (not a list)")

    # Q5: Gold
    q5 = normalize(str(data.get("q5", "")))
    if "gold" in q5 or q5 == "au":
        passed += 1
        checks.append("q5-element: PASS")
    else:
        checks.append(f"q5-element: FAIL (got '{data.get('q5', '')}')")

    ok = passed >= 3  # 3 out of 5
    summary = f"{passed}/5 facts correct. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
