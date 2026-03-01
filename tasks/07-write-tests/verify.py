"""Verify task 07: write-tests."""

import subprocess
import sys
from pathlib import Path


def verify(workspace: Path) -> tuple[bool, str]:
    test_path = workspace / "test_calculator.py"
    if not test_path.exists():
        return False, "test_calculator.py not found"

    source = test_path.read_text(encoding="utf-8")

    # Check minimum test count
    test_count = source.count("def test_")
    if test_count < 8:
        return False, f"Only {test_count} test functions found (need at least 8)"

    # Check coverage of key topics
    checks = []
    topics = {
        "add": ["add", "addition"],
        "subtract": ["subtract", "sub"],
        "multiply": ["multiply", "mul"],
        "divide": ["divide", "div"],
        "zero_division": ["zero", "ZeroDivisionError", "zero_div"],
        "history": ["history"],
        "clear": ["clear"],
    }

    topic_hits = 0
    for topic, keywords in topics.items():
        if any(kw.lower() in source.lower() for kw in keywords):
            topic_hits += 1
            checks.append(f"{topic}: covered")
        else:
            checks.append(f"{topic}: NOT covered")

    if topic_hits < 5:
        return False, f"Only {topic_hits}/7 topics covered. {'; '.join(checks)}"

    # Copy calculator.py to workspace so tests can import it
    seed_calc = workspace.parent / "seed" / "calculator.py"
    if seed_calc.exists():
        (workspace / "calculator.py").write_text(
            seed_calc.read_text(encoding="utf-8"), encoding="utf-8"
        )

    # Run the tests
    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_path), "-v", "--tb=short"],
        capture_output=True,
        text=True,
        cwd=str(workspace),
        timeout=30,
    )

    if result.returncode != 0:
        output = (result.stdout + result.stderr)[-500:]
        return False, f"Tests failed (exit {result.returncode}): {output}"

    # Count passed tests from output
    passed_line = [l for l in result.stdout.splitlines() if "passed" in l]
    summary = f"{test_count} test functions, {topic_hits}/7 topics covered, all tests pass"
    if passed_line:
        summary += f". pytest: {passed_line[-1].strip()}"

    return True, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
