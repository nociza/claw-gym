#!/usr/bin/env python3
"""Generate deterministic sales.csv for the data-analysis-pipeline task.

Uses random.seed(42) for reproducibility. Row 42 is an outlier.
"""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


def main():
    random.seed(42)

    products = ["Widget Alpha", "Widget Beta", "Widget Gamma", "Widget Delta", "Widget Epsilon"]
    regions = ["North", "South", "East", "West"]

    start_date = datetime(2024, 1, 1)
    rows = []

    for i in range(100):
        # Spread dates across 6 months (Jan-Jun 2024)
        day_offset = int(i * 1.8)  # ~180 days spread
        date = start_date + timedelta(days=day_offset)
        product = random.choice(products)
        region = random.choice(regions)

        if i == 41:  # Row 42 (1-based) is the outlier
            revenue = 99999.99
            quantity = 500
            returns = 0
        else:
            # Normal revenue: 100-3000 range
            base_revenue = random.uniform(100, 3000)
            # Slight upward trend over time
            trend_factor = 1 + (i / 100) * 0.3
            revenue = round(base_revenue * trend_factor, 2)
            quantity = random.randint(1, 50)
            # Correlation: quantity roughly proportional to revenue
            quantity = max(1, int(revenue / 80 + random.gauss(0, 3)))
            returns = random.randint(0, max(1, quantity // 5))

        rows.append({
            "date": date.strftime("%Y-%m-%d"),
            "product": product,
            "region": region,
            "revenue": revenue,
            "quantity": quantity,
            "returns": returns,
        })

    out_path = Path(__file__).parent / "seed" / "sales.csv"
    out_path.parent.mkdir(exist_ok=True)

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "product", "region", "revenue", "quantity", "returns"])
        writer.writeheader()
        writer.writerows(rows)

    # Compute and print ground truth for reference
    total_rev = sum(r["revenue"] for r in rows)
    by_product = {}
    for r in rows:
        by_product.setdefault(r["product"], 0)
        by_product[r["product"]] += r["revenue"]
    top_product = max(by_product, key=by_product.get)

    print(f"Generated {out_path}")
    print(f"Total revenue: {total_rev:.2f}")
    print(f"Outlier row: 42 (revenue={rows[41]['revenue']})")
    print(f"Top product: {top_product} ({by_product[top_product]:.2f})")
    print(f"Product totals: {json.dumps({k: round(v, 2) for k, v in sorted(by_product.items())}, indent=2)}")


if __name__ == "__main__":
    import json
    main()
