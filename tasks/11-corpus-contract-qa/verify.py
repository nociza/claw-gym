"""Verify task 11: corpus-contract-qa."""

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

    # Q1: Highest value vendor = HyperScale Compute ($200k)
    q1 = normalize(str(data.get("q1", "")))
    if "hyperscale" in q1:
        passed += 1
        checks.append("q1-highest: PASS")
    else:
        checks.append(f"q1-highest: FAIL (got '{data.get('q1', '')}')")

    # Q2: Auto-renewal count = 5
    q2 = data.get("q2")
    try:
        if int(q2) == 5:
            passed += 1
            checks.append("q2-autorenewal: PASS")
        else:
            checks.append(f"q2-autorenewal: FAIL (got {q2}, expected 5)")
    except (TypeError, ValueError):
        checks.append(f"q2-autorenewal: FAIL (got '{q2}')")

    # Q3: Contracts expiring in 2026
    q3 = data.get("q3", [])
    if isinstance(q3, list):
        q3_normalized = {normalize(v) for v in q3}
        # Vendors expiring in 2026: BrightData, DataFlow, Frontline, GreenLeaf, HyperScale, Acme Cloud
        expected_2026 = {"brightdata", "dataflow", "frontline", "greenleaf", "hyperscale", "acme"}
        matched = sum(1 for e in expected_2026 if any(e in n for n in q3_normalized))
        if matched >= 4:
            passed += 1
            checks.append(f"q3-expiring2026: PASS ({matched} matched)")
        else:
            checks.append(f"q3-expiring2026: FAIL (matched {matched}, need 4+)")
    else:
        checks.append("q3-expiring2026: FAIL (not a list)")

    # Q4: Total annual value = $835,000
    q4 = data.get("q4")
    try:
        val = float(str(q4).replace("$", "").replace(",", ""))
        if abs(val - 835000) <= 5000:
            passed += 1
            checks.append("q4-total: PASS")
        else:
            checks.append(f"q4-total: FAIL (got {val}, expected ~835000)")
    except (TypeError, ValueError):
        checks.append(f"q4-total: FAIL (got '{q4}')")

    # Q5: Shortest notice = DataFlow (30 days)
    q5 = normalize(str(data.get("q5", "")))
    if "dataflow" in q5:
        passed += 1
        checks.append("q5-shortest-notice: PASS")
    else:
        checks.append(f"q5-shortest-notice: FAIL (got '{data.get('q5', '')}')")

    ok = passed >= 3  # 3 out of 5
    summary = f"{passed}/5 answers correct. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
