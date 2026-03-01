"""Verify task 05: refactor-extract."""

import importlib.util
import sys
from pathlib import Path


def verify(workspace: Path) -> tuple[bool, str]:
    module_path = workspace / "report.py"
    if not module_path.exists():
        return False, "report.py not found"

    try:
        spec = importlib.util.spec_from_file_location("report", module_path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["report"] = mod
        spec.loader.exec_module(mod)
    except Exception as exc:
        return False, f"Import failed: {exc}"

    passed = 0
    checks = []

    # Check helper functions exist
    validate_email = getattr(mod, "validate_email", None)
    format_name = getattr(mod, "format_name", None)

    if validate_email is None:
        checks.append("validate_email: MISSING")
    else:
        try:
            assert validate_email("test@example.com") is True
            assert validate_email("bad-email") is False
            passed += 1
            checks.append("validate_email: PASS")
        except Exception as exc:
            checks.append(f"validate_email: FAIL ({exc})")

    if format_name is None:
        checks.append("format_name: MISSING")
    else:
        try:
            assert format_name("john", "doe") == "John Doe"
            assert format_name("  jane  ", "  SMITH  ") == "Jane Smith"
            passed += 1
            checks.append("format_name: PASS")
        except Exception as exc:
            checks.append(f"format_name: FAIL ({exc})")

    # Check original functions still work
    create_user_summary = getattr(mod, "create_user_summary", None)
    create_user_badge = getattr(mod, "create_user_badge", None)
    create_user_csv_row = getattr(mod, "create_user_csv_row", None)

    if create_user_summary:
        try:
            result = create_user_summary("john", "doe", "john@example.com")
            assert result["name"] == "John Doe"
            assert result["email"] == "john@example.com"
            passed += 1
            checks.append("create_user_summary: PASS")
        except Exception as exc:
            checks.append(f"create_user_summary: FAIL ({exc})")
    else:
        checks.append("create_user_summary: MISSING")

    if create_user_badge:
        try:
            result = create_user_badge("john", "doe", "john@example.com", "admin")
            assert "John Doe" in result
            assert "ADMIN" in result
            passed += 1
            checks.append("create_user_badge: PASS")
        except Exception as exc:
            checks.append(f"create_user_badge: FAIL ({exc})")
    else:
        checks.append("create_user_badge: MISSING")

    if create_user_csv_row:
        try:
            result = create_user_csv_row("john", "doe", "john@example.com", "engineering")
            assert "John Doe" in result
            assert "engineering" in result
            passed += 1
            checks.append("create_user_csv_row: PASS")
        except Exception as exc:
            checks.append(f"create_user_csv_row: FAIL ({exc})")
    else:
        checks.append("create_user_csv_row: MISSING")

    # Check DRY: original functions should USE the helpers
    source = module_path.read_text(encoding="utf-8")
    helper_calls = source.count("validate_email(") + source.count("format_name(")
    if helper_calls >= 6:  # At least 3 calls to each (definition + 3 uses each)
        passed += 1
        checks.append("DRY-refactor: PASS")
    else:
        checks.append(f"DRY-refactor: FAIL (only {helper_calls} helper calls found)")

    ok = passed >= 4  # 4 out of 6
    summary = f"{passed}/6 checks passed. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
