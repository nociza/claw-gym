"""Verify task 15: long-context-codebase-nav."""

import json
import sys
from pathlib import Path


def normalize(val: str) -> str:
    return str(val).strip().lower().replace("-", "_").replace(" ", "_")


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

    # Q1: Middleware order: request_logger, request_timer, authenticate
    q1 = data.get("q1", [])
    if isinstance(q1, list):
        q1_norm = [normalize(v) for v in q1]
        expected_order = ["request_logger", "request_timer", "authenticate"]
        # Check if the expected functions appear in order
        found_order = [f for f in q1_norm if f in expected_order]
        if found_order == expected_order:
            passed += 1
            checks.append("q1-middleware: PASS")
        elif len(set(q1_norm) & set(expected_order)) >= 2:
            # Partial credit if at least 2 are present
            passed += 1
            checks.append("q1-middleware: PASS (partial)")
        else:
            checks.append(f"q1-middleware: FAIL (got {q1})")
    else:
        checks.append("q1-middleware: FAIL (not a list)")

    # Q2: Auth mechanism = JWT
    q2 = normalize(str(data.get("q2", "")))
    if "jwt" in q2:
        passed += 1
        checks.append("q2-auth: PASS")
    else:
        checks.append(f"q2-auth: FAIL (got '{data.get('q2', '')}')")

    # Q3: Bug = references undefined 'exc' instead of 'error'
    q3 = normalize(str(data.get("q3", "")))
    if "exc" in q3 and ("error" in q3 or "undefined" in q3 or "nameerror" in q3 or "wrong" in q3 or "variable" in q3):
        passed += 1
        checks.append("q3-bug: PASS")
    elif "nameerror" in q3 or "undefined" in q3 or "wrong variable" in q3:
        passed += 1
        checks.append("q3-bug: PASS (indirect)")
    else:
        checks.append(f"q3-bug: FAIL (got '{data.get('q3', '')}')")

    # Q4: Custom exception count = 7
    q4 = data.get("q4")
    try:
        if abs(int(q4) - 7) <= 1:  # tolerance of 1
            passed += 1
            checks.append("q4-exceptions: PASS")
        else:
            checks.append(f"q4-exceptions: FAIL (got {q4}, expected 7)")
    except (TypeError, ValueError):
        checks.append(f"q4-exceptions: FAIL (got '{q4}')")

    # Q5: 404 response function = format_error_response
    q5 = normalize(str(data.get("q5", "")))
    if "format_error_response" in q5:
        passed += 1
        checks.append("q5-404-func: PASS")
    elif "not_found_handler" in q5:
        # Also acceptable - it's the handler that calls format_error_response
        passed += 1
        checks.append("q5-404-func: PASS (handler)")
    else:
        checks.append(f"q5-404-func: FAIL (got '{data.get('q5', '')}')")

    ok = passed >= 3  # 3 out of 5
    summary = f"{passed}/5 answers correct. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
