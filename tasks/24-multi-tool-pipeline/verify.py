"""Verify multi-tool-pipeline task: check cleaned CSV and summary JSON."""
from __future__ import annotations

import csv
import json
from pathlib import Path


def verify(workspace: Path) -> tuple[bool, str]:
    passed = 0
    total = 5
    details = []

    # Check 1: cleaned.csv exists and has rows
    cleaned_path = workspace / "cleaned.csv"
    if not cleaned_path.exists():
        return False, "cleaned.csv not found"

    try:
        rows = list(csv.DictReader(cleaned_path.open(encoding="utf-8")))
    except Exception as e:
        return False, f"Failed to parse cleaned.csv: {e}"

    # Expected: 30 rows original, remove: 1 negative, 1 outlier (>10000),
    # 1 invalid region (Central), 1 duplicate = 4 removed => 26 rows
    # Allowing some tolerance in case of edge interpretation
    row_count = len(rows)
    if 24 <= row_count <= 27:
        passed += 1
        details.append(f"C1-row-count: OK ({row_count} rows)")
    else:
        details.append(f"C1-row-count: FAIL ({row_count} rows, expected 24-27)")

    # Check 2: No negative revenue in cleaned data
    has_negative = False
    for row in rows:
        try:
            rev = float(row.get("revenue", 0))
            if rev < 0:
                has_negative = True
                break
        except (ValueError, TypeError):
            pass
    if not has_negative:
        passed += 1
        details.append("C2-no-negative: OK")
    else:
        details.append("C2-no-negative: FAIL (negative revenue found in cleaned data)")

    # Check 3: summary.json exists and parses
    summary_path = workspace / "summary.json"
    if not summary_path.exists():
        details.append("C3-summary-exists: FAIL (summary.json not found)")
        details.append("C4-total-rows: FAIL (no summary)")
        details.append("C5-unique-products: FAIL (no summary)")
        ok = passed >= 4
        return ok, f"{passed}/{total} checks passed. {'; '.join(details)}"

    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    except Exception as e:
        details.append(f"C3-summary-exists: FAIL (invalid JSON: {e})")
        details.append("C4-total-rows: FAIL (no summary)")
        details.append("C5-unique-products: FAIL (no summary)")
        ok = passed >= 4
        return ok, f"{passed}/{total} checks passed. {'; '.join(details)}"

    passed += 1
    details.append("C3-summary-exists: OK")

    # Check 4: total_rows matches rows_removed
    total_rows = summary.get("total_rows", 0)
    rows_removed = summary.get("rows_removed", 0)
    # Original has 30 rows, so total_rows + rows_removed should equal 30
    if isinstance(total_rows, (int, float)) and isinstance(rows_removed, (int, float)):
        if 24 <= total_rows <= 27 and 3 <= rows_removed <= 6:
            passed += 1
            details.append(f"C4-total-rows: OK (total={total_rows}, removed={rows_removed})")
        else:
            details.append(f"C4-total-rows: FAIL (total={total_rows}, removed={rows_removed})")
    else:
        details.append("C4-total-rows: FAIL (missing or non-numeric fields)")

    # Check 5: unique_products should be 5 (Widget A-E)
    unique_products = summary.get("unique_products", 0)
    if unique_products == 5:
        passed += 1
        details.append("C5-unique-products: OK (5)")
    else:
        details.append(f"C5-unique-products: FAIL ({unique_products}, expected 5)")

    ok = passed >= 4
    return ok, f"{passed}/{total} checks passed. {'; '.join(details)}"
