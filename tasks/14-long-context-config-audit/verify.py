"""Verify task 14: long-context-config-audit."""

import json
import sys
from pathlib import Path


def normalize(val: str) -> str:
    return str(val).strip().lower().replace("-", " ").replace("_", " ")


def check_list(got: list, expected: set, label: str, min_match: int) -> tuple[bool, str]:
    """Check if a list matches expected values with fuzzy matching."""
    if not isinstance(got, list):
        return False, f"{label}: not a list"
    got_norm = {normalize(v) for v in got}
    matched = sum(1 for e in expected if any(e in g for g in got_norm))
    if matched >= min_match:
        return True, f"{label}: PASS ({matched}/{len(expected)})"
    return False, f"{label}: FAIL (matched {matched}/{len(expected)}, got {got})"


def verify(workspace: Path) -> tuple[bool, str]:
    path = workspace / "audit.json"
    if not path.exists():
        return False, "audit.json not found"

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"Failed to parse audit.json: {exc}"

    passed = 0
    checks = []

    # Q1: debug=true services: auth-service, notification-service, scheduler-service
    ok, msg = check_list(
        data.get("q1", []),
        {"auth", "notification", "scheduler"},
        "q1-debug", 2
    )
    if ok:
        passed += 1
    checks.append(msg)

    # Q2: hardcoded secrets: auth-service, payment-service, notification-service, scheduler-service
    ok, msg = check_list(
        data.get("q2", []),
        {"auth", "payment", "notification", "scheduler"},
        "q2-secrets", 3
    )
    if ok:
        passed += 1
    checks.append(msg)

    # Q3: bind 0.0.0.0: api-gateway, payment-service, notification-service, scheduler-service
    ok, msg = check_list(
        data.get("q3", []),
        {"api gateway", "api", "payment", "notification", "scheduler"},
        "q3-bind", 3
    )
    if ok:
        passed += 1
    checks.append(msg)

    # Q4: insecure DB: auth-service, notification-service, scheduler-service
    ok, msg = check_list(
        data.get("q4", []),
        {"auth", "notification", "scheduler"},
        "q4-insecure-db", 2
    )
    if ok:
        passed += 1
    checks.append(msg)

    # Q5: missing health check: notification-service, analytics-service
    ok, msg = check_list(
        data.get("q5", []),
        {"notification", "analytics"},
        "q5-no-healthcheck", 1
    )
    if ok:
        passed += 1
    checks.append(msg)

    ok = passed >= 3  # 3 out of 5
    summary = f"{passed}/5 audit findings correct. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
