"""Job scheduler using a priority heap."""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field


@dataclass(order=True)
class Job:
    priority: int
    name: str = field(compare=False)
    duration: float = field(compare=False)


def schedule_jobs(jobs: list[dict[str, object]]) -> list[str]:
    """Schedule jobs by priority (lower number = higher priority).

    Args:
        jobs: List of dicts with keys 'name' (str), 'priority' (int),
              and 'duration' (float).

    Returns:
        Ordered list of job names from highest to lowest priority.

    Raises:
        ValueError: If any job is missing required keys.
    """
    required_keys = {"name", "priority", "duration"}
    heap: list[Job] = []

    for job in jobs:
        missing = required_keys - set(job.keys())
        if missing:
            raise ValueError(f"Job missing required keys: {missing}")

        heapq.heappush(
            heap,
            Job(
                priority=int(job["priority"]),
                name=str(job["name"]),
                duration=float(job["duration"]),
            ),
        )

    result: list[str] = []
    while heap:
        result.append(heapq.heappop(heap).name)
    return result
