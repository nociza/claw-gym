"""Verify data-analysis-pipeline task: check 5 analysis results."""
from __future__ import annotations

import csv
import json
from pathlib import Path


def verify(workspace: Path) -> tuple[bool, str]:
    analysis_path = workspace / "analysis.json"
    if not analysis_path.exists():
        return False, "analysis.json not found"

    try:
        data = json.loads(analysis_path.read_text(encoding="utf-8"))
    except Exception as e:
        return False, f"Invalid JSON: {e}"

    passed = 0
    total = 5
    details = []

    # Re-compute ground truth from seed data
    seed_csv = Path(__file__).parent / "seed" / "sales.csv"
    if seed_csv.exists():
        with open(seed_csv) as f:
            rows = list(csv.DictReader(f))
        gt_total = sum(float(r["revenue"]) for r in rows)
        by_product = {}
        for r in rows:
            by_product.setdefault(r["product"], 0)
            by_product[r["product"]] += float(r["revenue"])
        gt_top_product = max(by_product, key=by_product.get)
    else:
        gt_total = None
        gt_top_product = None

    # Check 1: total_revenue — plausibility check (should be in a reasonable range)
    total_rev = data.get("total_revenue")
    if total_rev is not None and isinstance(total_rev, (int, float)):
        if gt_total and abs(total_rev - gt_total) / gt_total < 0.05:
            passed += 1
            details.append(f"C1-total-revenue: OK ({total_rev})")
        elif not gt_total and 50000 < total_rev < 300000:
            passed += 1
            details.append(f"C1-total-revenue: OK ({total_rev}, plausibility)")
        else:
            details.append(f"C1-total-revenue: FAIL ({total_rev}, expected ~{gt_total:.2f})")
    else:
        details.append("C1-total-revenue: FAIL (missing or non-numeric)")

    # Check 2: outlier_row — must be 42
    outlier_row = data.get("outlier_row")
    if outlier_row is not None:
        try:
            if int(outlier_row) == 42:
                passed += 1
                details.append("C2-outlier-row: OK (42)")
            else:
                details.append(f"C2-outlier-row: FAIL (got {outlier_row}, expected 42)")
        except (ValueError, TypeError):
            details.append(f"C2-outlier-row: FAIL (got '{outlier_row}', expected 42)")
    else:
        details.append("C2-outlier-row: FAIL (missing)")

    # Check 3: top_product — fuzzy match
    top_product = str(data.get("top_product", "")).strip().lower()
    if gt_top_product and gt_top_product.lower() in top_product or top_product in gt_top_product.lower():
        passed += 1
        details.append(f"C3-top-product: OK ({data.get('top_product')})")
    elif "widget" in top_product:
        # At least they identified a widget product
        details.append(f"C3-top-product: PARTIAL ({data.get('top_product')})")
    else:
        details.append(f"C3-top-product: FAIL (got '{data.get('top_product')}')")

    # Check 4: month_over_month_growth — plausibility (should be a number)
    growth = data.get("month_over_month_growth")
    if growth is not None and isinstance(growth, (int, float)):
        # Growth should be a reasonable percentage (-100 to 500)
        if -100 < growth < 500:
            passed += 1
            details.append(f"C4-growth: OK ({growth}%)")
        else:
            details.append(f"C4-growth: FAIL ({growth}% out of plausible range)")
    else:
        details.append("C4-growth: FAIL (missing or non-numeric)")

    # Check 5: correlation — should be between -1 and 1, and positive (revenue ~ quantity)
    corr = data.get("revenue_quantity_correlation")
    if corr is not None and isinstance(corr, (int, float)):
        if -1 <= corr <= 1:
            passed += 1
            details.append(f"C5-correlation: OK ({corr})")
        else:
            details.append(f"C5-correlation: FAIL ({corr} out of range [-1, 1])")
    else:
        details.append("C5-correlation: FAIL (missing or non-numeric)")

    ok = passed >= 3
    return ok, f"{passed}/{total} checks passed. {'; '.join(details)}"
