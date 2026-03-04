"""Verify task 05: iterative-debug."""

import importlib.util
import subprocess
import sys
from pathlib import Path


def verify(workspace: Path) -> tuple[bool, str]:
    module_path = workspace / "stats.py"
    if not module_path.exists():
        return False, "stats.py not found"

    passed = 0
    checks = []

    # Check 1: script compiles
    source = module_path.read_text(encoding="utf-8")
    try:
        compile(source, str(module_path), "exec")
        passed += 1
        checks.append("compiles: PASS")
    except SyntaxError as exc:
        return False, f"Syntax error: {exc}"

    # Check 2: script runs without error
    result = subprocess.run(
        [sys.executable, str(module_path)],
        capture_output=True,
        text=True,
        timeout=15,
    )
    if result.returncode == 0:
        passed += 1
        checks.append("runs: PASS")
    else:
        checks.append(f"runs: FAIL ({result.stderr[-200:]})")
        return False, f"Script still crashes. {'; '.join(checks)}"

    # Check 3: compute_stats works correctly
    try:
        spec = importlib.util.spec_from_file_location("stats", module_path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["stats"] = mod
        spec.loader.exec_module(mod)

        compute_stats = getattr(mod, "compute_stats")
        stats = compute_stats([1, 2, 3, 4, 5])
        assert stats["mean"] == 3.0
        assert stats["median"] == 3.0
        passed += 1
        checks.append("compute_stats: PASS")
    except Exception as exc:
        checks.append(f"compute_stats: FAIL ({exc})")

    # Check 4: generate_report handles zero-mean dataset
    try:
        generate_report = getattr(mod, "generate_report")
        report = generate_report({
            "positive": [1, 2, 3],
            "zeros": [-1, 0, 1],  # mean=0
        })
        assert "positive" in report.get("datasets", report)
        assert "zeros" in report.get("datasets", report)
        passed += 1
        checks.append("zero-mean: PASS")
    except Exception as exc:
        checks.append(f"zero-mean: FAIL ({exc})")

    # Check 5: output includes all three original datasets
    if "deltas" in result.stdout and "scores" in result.stdout and "temperatures" in result.stdout:
        passed += 1
        checks.append("all-datasets: PASS")
    else:
        checks.append("all-datasets: FAIL (not all dataset names in output)")

    ok = passed >= 4  # 4 out of 5
    summary = f"{passed}/5 checks passed. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
