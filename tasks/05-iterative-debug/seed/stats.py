"""Statistics calculator with report generation."""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path


def compute_stats(numbers: list[float]) -> dict[str, float]:
    """Compute mean, median, mode, and standard deviation."""
    if not numbers:
        raise ValueError("Cannot compute stats on empty list")

    n = len(numbers)
    mean = sum(numbers) / n

    sorted_nums = sorted(numbers)
    mid = n // 2
    if n % 2 == 0:
        median = (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    else:
        median = sorted_nums[mid]

    counts = Counter(numbers)
    mode = counts.most_common(1)[0][0]

    variance = sum((x - mean) ** 2 for x in numbers) / n
    stdev = math.sqrt(variance)

    return {
        "mean": round(mean, 4),
        "median": round(median, 4),
        "mode": round(mode, 4),
        "stdev": round(stdev, 4),
    }


def generate_report(datasets: dict[str, list]) -> dict:
    """Generate a statistics report for multiple named datasets."""
    report = {"datasets": {}}
    for name, data in datasets.items():
        stats = compute_stats(data)
        stats["count"] = len(data)
        stats["min"] = min(data)
        stats["max"] = max(data)
        # Coefficient of variation (stdev / mean)
        stats["cv"] = round(stats["stdev"] / stats["mean"], 4)
        report["datasets"][name] = stats

    all_means = [d["mean"] for d in report["datasets"].values()]
    report["summary"] = {
        "num_datasets": len(datasets),
        "grand_mean": round(sum(all_means) / len(all_means), 4),
    }
    return report


if __name__ == "__main__":
    datasets = {
        "scores": [85, 92, 78, 95, 88, 76, 91, 84, 90, 87],
        "temperatures": [72.1, 68.5, 75.3, 69.8, 71.2, 73.6, 70.0, 74.5],
        "deltas": [-3, 5, -2, 7, -5, 3, -1, 4, -8, 0],
    }

    report = generate_report(datasets)
    print(json.dumps(report, indent=2))

    output = Path(__file__).parent / "report.json"
    output.write_text(json.dumps(report, indent=2))
    print(f"\nReport written to {output}")
