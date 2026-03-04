"""Verify image-chart-extraction task: compare extracted data to ground truth."""
from __future__ import annotations

import json
from pathlib import Path

GROUND_TRUTH = {
    "Acme Corp": {"q1": 120, "q2": 145, "q3": 160, "q4": 190},
    "Bolt Industries": {"q1": 95, "q2": 110, "q3": 130, "q4": 155},
    "Crescent Tech": {"q1": 200, "q2": 180, "q3": 210, "q4": 240},
    "Dynamo Systems": {"q1": 75, "q2": 90, "q3": 105, "q4": 85},
    "Echo Ventures": {"q1": 150, "q2": 170, "q3": 145, "q4": 195},
}

TOLERANCE = 2  # ±2 tolerance for extracted values


def normalize_name(name: str) -> str:
    return name.strip().lower().replace("-", " ").replace("_", " ")


def verify(workspace: Path) -> tuple[bool, str]:
    extracted_path = workspace / "extracted.json"
    if not extracted_path.exists():
        return False, "extracted.json not found"

    try:
        data = json.loads(extracted_path.read_text(encoding="utf-8"))
    except Exception as e:
        return False, f"Invalid JSON: {e}"

    companies = data.get("companies", [])
    if not companies:
        return False, "No companies found in extracted.json"

    # Match extracted companies to ground truth
    companies_matched = 0
    total_values = 0
    correct_values = 0
    details = []

    gt_normalized = {normalize_name(k): v for k, v in GROUND_TRUTH.items()}

    for extracted in companies:
        name = normalize_name(extracted.get("name", ""))
        # Find best match in ground truth
        matched_gt = None
        for gt_name, gt_vals in gt_normalized.items():
            # Fuzzy match: check if key words match
            if gt_name == name or gt_name in name or name in gt_name:
                matched_gt = gt_vals
                break
            # Check if first word matches
            gt_first = gt_name.split()[0] if gt_name.split() else ""
            ext_first = name.split()[0] if name.split() else ""
            if gt_first and ext_first and gt_first == ext_first:
                matched_gt = gt_vals
                break

        if matched_gt is None:
            continue

        companies_matched += 1
        for q in ["q1", "q2", "q3", "q4"]:
            total_values += 1
            try:
                extracted_val = float(extracted.get(q, -9999))
                expected_val = matched_gt[q]
                if abs(extracted_val - expected_val) <= TOLERANCE:
                    correct_values += 1
            except (ValueError, TypeError):
                pass

    details.append(f"companies_matched={companies_matched}/5")
    details.append(f"values_correct={correct_values}/{total_values}")

    # Pass criteria: >= 3 companies matched AND >= 60% values correct
    value_pct = correct_values / total_values if total_values > 0 else 0
    ok = companies_matched >= 3 and value_pct >= 0.6
    return ok, f"Matched {companies_matched}/5 companies, {correct_values}/{total_values} values correct ({value_pct:.0%}). {'; '.join(details)}"
