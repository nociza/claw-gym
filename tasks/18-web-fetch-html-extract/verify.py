"""Verify task 18: web-fetch-html-extract.

Largest cities vary by source and definition (city proper, metro, urban).
We accept multiple valid answers with wide ranges.
"""

import json
import sys
from pathlib import Path


def normalize(val: str) -> str:
    return str(val).strip().lower()


# Cities that commonly appear in top 2 of "largest cities" lists
VALID_TOP_CITIES = {
    "tokyo", "shanghai", "delhi", "new delhi", "beijing", "mumbai",
    "sao paulo", "são paulo", "mexico city", "dhaka", "cairo",
    "osaka", "chongqing", "karachi", "istanbul", "lagos",
    "guangzhou", "kinshasa", "tianjin", "shenzhen",
}

VALID_COUNTRIES = {
    "japan", "china", "india", "brazil", "mexico", "bangladesh",
    "egypt", "turkey", "pakistan", "nigeria", "democratic republic of the congo",
    "dr congo", "drc",
}

VALID_CONTINENTS = {"asia"}  # Asia dominates all top-10 city lists


def verify(workspace: Path) -> tuple[bool, str]:
    path = workspace / "results.json"
    if not path.exists():
        return False, "results.json not found"

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"Failed to parse results.json: {exc}"

    passed = 0
    checks = []

    # Check 1: city_1 is a valid top city
    city_1 = normalize(str(data.get("city_1", "")))
    if any(c in city_1 or city_1 in c for c in VALID_TOP_CITIES):
        passed += 1
        checks.append(f"city_1: PASS ({city_1})")
    else:
        checks.append(f"city_1: FAIL (got '{data.get('city_1', '')}')")

    # Check 2: city_2 is a valid top city
    city_2 = normalize(str(data.get("city_2", "")))
    if any(c in city_2 or city_2 in c for c in VALID_TOP_CITIES):
        passed += 1
        checks.append(f"city_2: PASS ({city_2})")
    else:
        checks.append(f"city_2: FAIL (got '{data.get('city_2', '')}')")

    # Check 3: country_1 is valid
    country_1 = normalize(str(data.get("country_1", "")))
    if any(c in country_1 or country_1 in c for c in VALID_COUNTRIES):
        passed += 1
        checks.append(f"country_1: PASS ({country_1})")
    else:
        checks.append(f"country_1: FAIL (got '{data.get('country_1', '')}')")

    # Check 4: population in reasonable range (5-40 million for city proper)
    pop = data.get("population_1_millions")
    try:
        pop_val = float(pop)
        if 5.0 <= pop_val <= 40.0:
            passed += 1
            checks.append(f"population: PASS ({pop_val}M)")
        else:
            checks.append(f"population: FAIL ({pop_val}M not in [5, 40])")
    except (TypeError, ValueError):
        checks.append(f"population: FAIL (got '{pop}')")

    # Check 5: top continent = Asia
    continent = normalize(str(data.get("top_continent", "")))
    if "asia" in continent:
        passed += 1
        checks.append("top_continent: PASS")
    else:
        checks.append(f"top_continent: FAIL (got '{data.get('top_continent', '')}')")

    ok = passed >= 3  # 3 out of 5
    summary = f"{passed}/5 checks passed. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
