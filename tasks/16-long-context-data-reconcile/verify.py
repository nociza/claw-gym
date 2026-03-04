"""Verify task 16: long-context-data-reconcile."""

import json
import sys
from pathlib import Path


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

    # Q1: Revenue by region
    q1 = data.get("q1", {})
    expected_revenue = {
        "north": 3629.82,
        "south": 3979.84,
        "east": 3114.82,
        "west": 2374.89,
    }
    if isinstance(q1, dict):
        q1_norm = {normalize(k): v for k, v in q1.items()}
        region_matches = 0
        for region, expected in expected_revenue.items():
            val = q1_norm.get(region)
            if val is not None:
                try:
                    if abs(float(val) - expected) <= expected * 0.05:  # 5% tolerance
                        region_matches += 1
                except (TypeError, ValueError):
                    pass
        if region_matches >= 3:
            passed += 1
            checks.append(f"q1-revenue: PASS ({region_matches}/4 regions)")
        else:
            checks.append(f"q1-revenue: FAIL ({region_matches}/4 regions matched)")
    else:
        checks.append("q1-revenue: FAIL (not an object)")

    # Q2: Customers with no orders = Quinn Walker, Rachel Hall, Sam Young, Tina King
    q2 = data.get("q2", [])
    if isinstance(q2, list):
        q2_norm = {normalize(v) for v in q2}
        expected_no_orders = {"quinn walker", "rachel hall", "sam young", "tina king",
                              "quinn", "rachel", "sam", "tina"}
        matched = sum(1 for name in q2_norm if any(e in name for e in expected_no_orders))
        if matched >= 3 and len(q2) >= 3:
            passed += 1
            checks.append(f"q2-no-orders: PASS ({matched} matched)")
        else:
            checks.append(f"q2-no-orders: FAIL (matched {matched})")
    else:
        checks.append("q2-no-orders: FAIL (not a list)")

    # Q3: Orphan orders = [1029, 1041, 1050]
    q3 = data.get("q3", [])
    if isinstance(q3, list):
        q3_ints = set()
        for v in q3:
            try:
                q3_ints.add(int(v))
            except (TypeError, ValueError):
                pass
        expected_orphans = {1029, 1041, 1050}
        if q3_ints >= expected_orphans or len(q3_ints & expected_orphans) >= 2:
            passed += 1
            checks.append("q3-orphans: PASS")
        else:
            checks.append(f"q3-orphans: FAIL (got {q3})")
    else:
        checks.append("q3-orphans: FAIL (not a list)")

    # Q4: Average order value by category
    q4 = data.get("q4", {})
    expected_avg = {
        "electronics": 338.14,
        "furniture": 288.20,
        "books": 64.98,
    }
    if isinstance(q4, dict):
        q4_norm = {normalize(k): v for k, v in q4.items()}
        cat_matches = 0
        for cat, expected in expected_avg.items():
            val = q4_norm.get(cat)
            if val is not None:
                try:
                    if abs(float(val) - expected) <= expected * 0.10:  # 10% tolerance
                        cat_matches += 1
                except (TypeError, ValueError):
                    pass
        if cat_matches >= 2:
            passed += 1
            checks.append(f"q4-avg-category: PASS ({cat_matches}/3)")
        else:
            checks.append(f"q4-avg-category: FAIL ({cat_matches}/3 matched)")
    else:
        checks.append("q4-avg-category: FAIL (not an object)")

    # Q5: Highest spending customer = Eva Martinez (c5)
    q5 = normalize(str(data.get("q5", "")))
    if "eva" in q5 or "martinez" in q5:
        passed += 1
        checks.append("q5-highest-spender: PASS")
    else:
        checks.append(f"q5-highest-spender: FAIL (got '{data.get('q5', '')}')")

    ok = passed >= 3  # 3 out of 5
    summary = f"{passed}/5 answers correct. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
