"""User report generation with repeated logic."""

from __future__ import annotations

import re


def create_user_summary(first: str, last: str, email: str) -> dict[str, str]:
    """Create a user summary dict."""
    # Validate email
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise ValueError(f"Invalid email: {email}")

    # Format name
    formatted_name = f"{first.strip().title()} {last.strip().title()}"

    return {
        "name": formatted_name,
        "email": email.strip().lower(),
        "display": f"{formatted_name} <{email.strip().lower()}>",
    }


def create_user_badge(first: str, last: str, email: str, role: str) -> str:
    """Create a badge string for display."""
    # Validate email
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise ValueError(f"Invalid email: {email}")

    # Format name
    formatted_name = f"{first.strip().title()} {last.strip().title()}"

    return f"[{role.upper()}] {formatted_name} ({email.strip().lower()})"


def create_user_csv_row(first: str, last: str, email: str, department: str) -> str:
    """Create a CSV row for export."""
    # Validate email
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise ValueError(f"Invalid email: {email}")

    # Format name
    formatted_name = f"{first.strip().title()} {last.strip().title()}"

    return f'"{formatted_name}","{email.strip().lower()}","{department}"'
