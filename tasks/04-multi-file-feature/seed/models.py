"""Note data model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Note:
    id: int
    title: str
    content: str
    created_at: datetime
