"""Verify multi-turn-clarification task: test process_records and top_category."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def verify(workspace: Path) -> tuple[bool, str]:
    module_path = workspace / "processor.py"
    if not module_path.exists():
        return False, "processor.py not found"

    try:
        spec = importlib.util.spec_from_file_location("processor", module_path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["processor"] = mod
        spec.loader.exec_module(mod)
    except Exception as e:
        return False, f"Failed to import processor.py: {e}"

    passed = 0
    total = 4
    details = []

    process_records = getattr(mod, "process_records", None)
    top_category = getattr(mod, "top_category", None)

    if process_records is None:
        return False, "process_records function not found"
    if top_category is None:
        details.append("top_category function not found")

    # Test 1: Basic category summing
    try:
        records = [
            {"name": "a", "value": 10, "category": "X"},
            {"name": "b", "value": 20, "category": "Y"},
            {"name": "c", "value": 30, "category": "X"},
        ]
        result = process_records(records)
        if isinstance(result, dict) and result.get("X") == 40 and result.get("Y") == 20:
            passed += 1
            details.append("T1-basic-sum: OK")
        else:
            details.append(f"T1-basic-sum: FAIL (got {result})")
    except Exception as e:
        details.append(f"T1-basic-sum: FAIL ({e})")

    # Test 2: Negative value filtering
    try:
        records = [
            {"name": "a", "value": 10, "category": "X"},
            {"name": "b", "value": -5, "category": "X"},
            {"name": "c", "value": 20, "category": "Y"},
            {"name": "d", "value": -15, "category": "Y"},
        ]
        result = process_records(records)
        if isinstance(result, dict) and result.get("X") == 10 and result.get("Y") == 20:
            passed += 1
            details.append("T2-negative-filter: OK")
        else:
            details.append(f"T2-negative-filter: FAIL (got {result})")
    except Exception as e:
        details.append(f"T2-negative-filter: FAIL ({e})")

    # Test 3: Empty input
    try:
        result = process_records([])
        if isinstance(result, dict) and len(result) == 0:
            passed += 1
            details.append("T3-empty-input: OK")
        else:
            details.append(f"T3-empty-input: FAIL (got {result})")
    except Exception as e:
        details.append(f"T3-empty-input: FAIL ({e})")

    # Test 4: top_category function
    if top_category is not None:
        try:
            records = [
                {"name": "a", "value": 10, "category": "X"},
                {"name": "b", "value": 50, "category": "Y"},
                {"name": "c", "value": 30, "category": "X"},
            ]
            result = top_category(records)
            # X=10+30=40, Y=50 → Y is highest
            if result == "Y":
                passed += 1
                details.append("T4-top-category: OK")
            else:
                details.append(f"T4-top-category: FAIL (got '{result}', expected 'Y')")

            # Also test empty case
            empty_result = top_category([])
            if empty_result == "":
                details.append("T4-top-category-empty: OK")
            else:
                details.append(f"T4-top-category-empty: note (got '{empty_result}')")
        except Exception as e:
            details.append(f"T4-top-category: FAIL ({e})")
    else:
        details.append("T4-top-category: FAIL (function not found)")

    ok = passed >= 3
    return ok, f"{passed}/{total} tests passed. {'; '.join(details)}"
