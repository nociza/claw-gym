"""Verify task 06: web-search-factual."""

import json
import sys
from pathlib import Path

EXPECTED = {
    "q1": ["299792458"],
    "q2": ["jp"],
    "q3": ["1991"],
    "q4": ["w"],
    "q5": ["canberra"],
}


def normalize(val: str) -> str:
    return str(val).strip().lower().replace(",", "").replace(" ", "")


def verify(workspace: Path) -> tuple[bool, str]:
    answers_path = workspace / "answers.json"
    searches_path = workspace / "searches.txt"

    if not answers_path.exists():
        return False, "answers.json not found"

    try:
        answers = json.loads(answers_path.read_text(encoding="utf-8"))
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

    # Bonus: check searches.txt exists (proof of search usage)
    has_searches = searches_path.exists() and len(searches_path.read_text().strip()) > 10
    if has_searches:
        checks.append("searches.txt: present")
    else:
        checks.append("searches.txt: missing or empty")

    ok = passed >= 3  # 3 out of 5 facts correct
    summary = f"{passed}/5 facts correct. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
