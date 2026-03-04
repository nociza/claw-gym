"""Verify task 09: web-search-calculation."""

import json
import sys
from pathlib import Path

# Accepted values with tolerance
CHECKS = {
    "q1_ratio": {"expected": 585.0, "tolerance": 100.0},
    "q2_celsius": {"expected": 100.0, "tolerance": 1.0},
    "q3_eiffel_year": {"expected": 1889, "tolerance": 1},
    "q3_empire_year": {"expected": 1931, "tolerance": 1},
    "q3_difference": {"expected": 42, "tolerance": 2},
}


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

    for key, spec in CHECKS.items():
        val = data.get(key)
        if val is None:
            checks.append(f"{key}: MISSING")
            continue
        try:
            val = float(val)
        except (TypeError, ValueError):
            checks.append(f"{key}: not numeric ({val})")
            continue
        if abs(val - spec["expected"]) <= spec["tolerance"]:
            passed += 1
            checks.append(f"{key}: PASS")
        else:
            checks.append(f"{key}: FAIL (got {val}, expected ~{spec['expected']})")

    ok = passed >= 3  # 3 out of 5 calculations correct
    total = len(CHECKS)
    summary = f"{passed}/{total} calculations correct. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
