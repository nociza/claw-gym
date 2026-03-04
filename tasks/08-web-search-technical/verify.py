"""Verify task 08: web-search-technical."""

import json
import sys
from pathlib import Path

EXPECTED = {
    "q1": ["343"],
    "q2": ["429"],
    "q3": ["2005"],
    "q4": ["init.defaultbranch", "init.defaultbranchname", "defaultbranch"],
    "q5": ["128"],
    "q6": ["linus torvalds", "torvalds"],
}


def normalize(val: str) -> str:
    return str(val).strip().lower()


def verify(workspace: Path) -> tuple[bool, str]:
    path = workspace / "answers.json"
    if not path.exists():
        return False, "answers.json not found"

    try:
        answers = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"Failed to parse answers.json: {exc}"

    passed = 0
    checks = []

    for qkey, accepted in EXPECTED.items():
        val = normalize(str(answers.get(qkey, "")))
        if any(normalize(a) in val or val in normalize(a) for a in accepted):
            passed += 1
            checks.append(f"{qkey}: PASS")
        else:
            checks.append(f"{qkey}: FAIL (got '{answers.get(qkey, '')}')")

    ok = passed >= 4  # 4 out of 6
    summary = f"{passed}/6 technical facts correct. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
