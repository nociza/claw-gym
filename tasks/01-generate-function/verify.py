"""Verify task 01: generate-function."""

import importlib.util
import sys
from pathlib import Path


TEST_CASES = [
    ([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
    ([[1, 4], [4, 5]], [[1, 5]]),
    ([], []),
    ([[1, 4], [0, 4]], [[0, 4]]),
    ([[1, 4], [2, 3]], [[1, 4]]),
    ([[1, 1]], [[1, 1]]),
    ([[1, 10], [2, 3], [4, 5], [6, 7]], [[1, 10]]),
    ([[1, 2], [3, 4], [5, 6]], [[1, 2], [3, 4], [5, 6]]),
]


def verify(workspace: Path) -> tuple[bool, str]:
    module_path = workspace / "merge_intervals.py"
    if not module_path.exists():
        return False, "merge_intervals.py not found"

    try:
        spec = importlib.util.spec_from_file_location("merge_intervals", module_path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["merge_intervals"] = mod
        spec.loader.exec_module(mod)
    except Exception as exc:
        return False, f"Failed to import: {exc}"

    fn = getattr(mod, "merge_intervals", None)
    if fn is None:
        return False, "Function 'merge_intervals' not found in module"

    passed = 0
    failed_cases = []
    for intervals, expected in TEST_CASES:
        try:
            result = fn([list(iv) for iv in intervals])
            if result == expected:
                passed += 1
            else:
                failed_cases.append(f"input={intervals} expected={expected} got={result}")
        except Exception as exc:
            failed_cases.append(f"input={intervals} raised {exc}")

    total = len(TEST_CASES)
    ok = passed >= total - 1  # allow 1 failure
    summary = f"{passed}/{total} test cases passed"
    if failed_cases:
        summary += f". Failures: {'; '.join(failed_cases[:3])}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
