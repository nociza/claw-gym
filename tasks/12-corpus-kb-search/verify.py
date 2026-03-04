"""Verify task 12: corpus-kb-search."""

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

    # Q1: Articles mentioning circuit breaker
    # Expected: microservices-patterns, caching-strategies, observability, resilience-patterns
    q1 = data.get("q1", [])
    if isinstance(q1, list):
        q1_norm = {normalize(v) for v in q1}
        expected_cb = {"microservices patterns", "caching strategies", "observability", "resilience patterns"}
        # Also accept with hyphens
        matched = 0
        for exp in expected_cb:
            if any(exp.replace(" ", "") in n.replace(" ", "").replace("-", "") for n in q1_norm):
                matched += 1
        if matched >= 3 and len(q1) >= 3:
            passed += 1
            checks.append(f"q1-circuit-breaker: PASS ({matched}/4 found)")
        else:
            checks.append(f"q1-circuit-breaker: FAIL (matched {matched})")
    else:
        checks.append("q1-circuit-breaker: FAIL (not a list)")

    # Q2: Distinct caching levels = 4
    q2 = data.get("q2")
    try:
        if int(q2) == 4:
            passed += 1
            checks.append("q2-cache-levels: PASS")
        else:
            checks.append(f"q2-cache-levels: FAIL (got {q2}, expected 4)")
    except (TypeError, ValueError):
        checks.append(f"q2-cache-levels: FAIL (got '{q2}')")

    # Q3: Load testing tool = k6
    q3 = normalize(str(data.get("q3", "")))
    if "k6" in q3:
        passed += 1
        checks.append("q3-load-tool: PASS")
    else:
        checks.append(f"q3-load-tool: FAIL (got '{data.get('q3', '')}')")

    # Q4: CAP theorem references = 2
    q4 = data.get("q4")
    try:
        if int(q4) == 2:
            passed += 1
            checks.append("q4-cap-refs: PASS")
        else:
            checks.append(f"q4-cap-refs: FAIL (got {q4}, expected 2)")
    except (TypeError, ValueError):
        checks.append(f"q4-cap-refs: FAIL (got '{q4}')")

    # Q5: Migration strategy = blue-green
    q5 = normalize(str(data.get("q5", "")))
    if "blue" in q5 and "green" in q5:
        passed += 1
        checks.append("q5-migration: PASS")
    else:
        checks.append(f"q5-migration: FAIL (got '{data.get('q5', '')}')")

    ok = passed >= 3  # 3 out of 5
    summary = f"{passed}/5 answers correct. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
