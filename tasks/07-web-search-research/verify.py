"""Verify task 07: web-search-research."""

import json
import sys
from pathlib import Path

# Accepted ranges for each metric (generous ranges for approximate data)
EXPECTED = {
    "russia": {
        "population_millions": (130, 160),
        "area_sq_km": (16000000, 18000000),
        "gdp_trillions_usd": (1.0, 3.0),
    },
    "canada": {
        "population_millions": (35, 45),
        "area_sq_km": (9000000, 10500000),
        "gdp_trillions_usd": (1.5, 3.0),
    },
    "usa": {
        "population_millions": (320, 345),
        "area_sq_km": (9000000, 10500000),
        "gdp_trillions_usd": (20.0, 32.0),
    },
}


def verify(workspace: Path) -> tuple[bool, str]:
    path = workspace / "countries.json"
    if not path.exists():
        return False, "countries.json not found"

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"Failed to parse countries.json: {exc}"

    passed = 0
    checks = []
    total = 0

    for country, ranges in EXPECTED.items():
        cdata = data.get(country, {})
        if not cdata:
            checks.append(f"{country}: MISSING")
            total += len(ranges)
            continue
        for metric, (lo, hi) in ranges.items():
            total += 1
            val = cdata.get(metric)
            if val is None:
                checks.append(f"{country}.{metric}: MISSING")
                continue
            try:
                val = float(val)
            except (TypeError, ValueError):
                checks.append(f"{country}.{metric}: not numeric ({val})")
                continue
            if lo <= val <= hi:
                passed += 1
            else:
                checks.append(f"{country}.{metric}: {val} not in [{lo}, {hi}]")

    ok = passed >= 6  # 6 out of 9 metrics in range
    summary = f"{passed}/{total} metrics in acceptable range"
    if checks:
        summary += f". Issues: {'; '.join(checks[:5])}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
