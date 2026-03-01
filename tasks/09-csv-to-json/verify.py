"""Verify task 09: csv-to-json."""

import json
import sys
from pathlib import Path

# Pre-computed expected values
EXPECTED = {
    "Engineering": {"count": 4, "avg_salary": 99500.0, "employees": {"Alice Chen", "Bob Smith", "Dave Wilson", "Jack White"}},
    "Marketing": {"count": 3, "avg_salary": 83666.67, "employees": {"Carol Davis", "Eve Brown", "Henry Park"}},
    "Sales": {"count": 3, "avg_salary": 71666.67, "employees": {"Frank Lee", "Grace Kim", "Ivy Zhang"}},
}


def verify(workspace: Path) -> tuple[bool, str]:
    json_path = workspace / "employees.json"
    script_path = workspace / "transform.py"

    if not json_path.exists():
        return False, "employees.json not found"
    if not script_path.exists():
        return False, "transform.py not found"

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"Invalid JSON: {exc}"

    departments = data.get("departments", data)  # allow top-level or nested
    if not isinstance(departments, dict):
        return False, "Expected 'departments' dict in JSON"

    passed = 0
    checks = []

    for dept_name, expected in EXPECTED.items():
        dept = departments.get(dept_name)
        if dept is None:
            checks.append(f"{dept_name}: NOT FOUND")
            continue

        dept_ok = True
        # Check count
        count = dept.get("count", dept.get("employee_count", -1))
        if count != expected["count"]:
            checks.append(f"{dept_name}-count: FAIL (expected {expected['count']}, got {count})")
            dept_ok = False

        # Check avg salary (allow 1.0 tolerance)
        avg = dept.get("avg_salary", dept.get("average_salary", -1))
        if abs(float(avg) - expected["avg_salary"]) > 1.0:
            checks.append(f"{dept_name}-avg: FAIL (expected {expected['avg_salary']}, got {avg})")
            dept_ok = False

        # Check employees list
        emps = set(dept.get("employees", []))
        if emps != expected["employees"]:
            missing = expected["employees"] - emps
            if missing:
                checks.append(f"{dept_name}-employees: FAIL (missing {missing})")
                dept_ok = False

        if dept_ok:
            passed += 1
            checks.append(f"{dept_name}: PASS")

    # Check transform.py is valid Python
    try:
        compile(script_path.read_text(encoding="utf-8"), str(script_path), "exec")
        passed += 1
        checks.append("transform.py-syntax: PASS")
    except SyntaxError as exc:
        checks.append(f"transform.py-syntax: FAIL ({exc})")

    ok = passed >= 3  # 3 out of 4 (3 departments + script syntax)
    summary = f"{passed}/4 checks passed. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
