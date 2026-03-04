#!/usr/bin/env python3
"""Generate a grouped bar chart PNG for the image-chart-extraction task.

Run once to create seed/chart.png. The ground truth data is embedded here
and also used by verify.py.
"""
import json
from pathlib import Path

# Ground truth data
GROUND_TRUTH = {
    "companies": [
        {"name": "Acme Corp", "q1": 120, "q2": 145, "q3": 160, "q4": 190},
        {"name": "Bolt Industries", "q1": 95, "q2": 110, "q3": 130, "q4": 155},
        {"name": "Crescent Tech", "q1": 200, "q2": 180, "q3": 210, "q4": 240},
        {"name": "Dynamo Systems", "q1": 75, "q2": 90, "q3": 105, "q4": 85},
        {"name": "Echo Ventures", "q1": 150, "q2": 170, "q3": 145, "q4": 195},
    ]
}


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    companies = GROUND_TRUTH["companies"]
    names = [c["name"] for c in companies]
    quarters = ["Q1", "Q2", "Q3", "Q4"]

    x = np.arange(len(quarters))
    width = 0.15
    fig, ax = plt.subplots(figsize=(12, 7))

    colors = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#F44336"]

    for i, company in enumerate(companies):
        values = [company["q1"], company["q2"], company["q3"], company["q4"]]
        offset = (i - len(companies) / 2 + 0.5) * width
        bars = ax.bar(x + offset, values, width, label=company["name"], color=colors[i])
        # Add value labels on top of each bar
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                    str(val), ha="center", va="bottom", fontsize=8, fontweight="bold")

    ax.set_xlabel("Quarter", fontsize=12)
    ax.set_ylabel("Revenue ($M)", fontsize=12)
    ax.set_title("Quarterly Revenue by Company (2024)", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(quarters)
    ax.legend(loc="upper left", fontsize=10)
    ax.set_ylim(0, 280)
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    out_path = Path(__file__).parent / "seed" / "chart.png"
    out_path.parent.mkdir(exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close()

    # Also save ground truth for reference
    gt_path = Path(__file__).parent / "ground_truth.json"
    with open(gt_path, "w") as f:
        json.dump(GROUND_TRUTH, f, indent=2)

    print(f"Generated {out_path} and {gt_path}")


if __name__ == "__main__":
    main()
