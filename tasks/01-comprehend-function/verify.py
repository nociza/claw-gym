"""Verify task 01: comprehend-function."""

import sys
from pathlib import Path


EXPECTED = {
    "1": ["o(n log n)", "n log n", "nlogn"],
    "2": ["fifo", "first in first out", "insertion order", "stable", "order they were pushed", "arbitrary", "heap order"],
    "3": ["list[str]", "list of str", "list of strings"],
    "4": ["heap", "priority queue", "heapq", "min-heap", "min heap", "binary heap"],
    "5": ["valueerror", "value error"],
}


def verify(workspace: Path) -> tuple[bool, str]:
    answers_path = workspace / "answers.txt"
    if not answers_path.exists():
        return False, "answers.txt not found in workspace"

    text = answers_path.read_text(encoding="utf-8").strip()
    if not text:
        return False, "answers.txt is empty"

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    score = 0
    details = []

    for q_num, acceptable in EXPECTED.items():
        found = False
        for line in lines:
            normalized = line.lower().replace("_", " ").replace("-", " ")
            if q_num in line[:5]:  # line starts with question number
                for answer in acceptable:
                    if answer in normalized:
                        found = True
                        break
            if found:
                break
        if found:
            score += 1
            details.append(f"Q{q_num}: PASS")
        else:
            details.append(f"Q{q_num}: FAIL")

    passed = score >= 3  # 3 out of 5 required
    summary = f"{score}/5 correct. {'; '.join(details)}"
    return passed, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
