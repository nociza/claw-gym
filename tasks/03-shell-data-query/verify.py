"""Verify task 03: shell-data-query."""

import sys
from pathlib import Path

# Pre-computed correct answers from the access.log
EXPECTED = {
    "1": "20",           # total lines
    "2": "5",            # unique IPs: 192.168.1.10, 192.168.1.20, 192.168.1.30, 10.0.0.5, 172.16.0.1
    "3": "192.168.1.10", # 8 requests from this IP
    "4": "3",            # 404 responses
    "5": "/api/users",   # 8 GET + 1 POST + 1 DELETE = referenced most
}


def verify(workspace: Path) -> tuple[bool, str]:
    report_path = workspace / "report.txt"
    if not report_path.exists():
        return False, "report.txt not found"

    text = report_path.read_text(encoding="utf-8").strip()
    if not text:
        return False, "report.txt is empty"

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    passed = 0
    checks = []

    for q_num, expected_val in EXPECTED.items():
        found = False
        for line in lines:
            if not line.startswith(q_num):
                continue
            # Extract value after the question number prefix
            rest = line[len(q_num):].lstrip(".):- ")
            if expected_val.lower() in rest.lower():
                found = True
                break
        if found:
            passed += 1
            checks.append(f"Q{q_num}: PASS")
        else:
            checks.append(f"Q{q_num}: FAIL (expected {expected_val})")

    ok = passed >= 3  # 3 out of 5
    summary = f"{passed}/5 answers correct. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
