"""Simple calculator with history tracking."""

from __future__ import annotations


class Calculator:
    def __init__(self) -> None:
        self._history: list[str] = []

    def add(self, a: float, b: float) -> float:
        result = a + b
        self._history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a: float, b: float) -> float:
        result = a - b
        self._history.append(f"{a} - {b} = {result}")
        return result

    def multiply(self, a: float, b: float) -> float:
        result = a * b
        self._history.append(f"{a} * {b} = {result}")
        return result

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        result = a / b
        self._history.append(f"{a} / {b} = {result}")
        return result

    @property
    def history(self) -> list[str]:
        return list(self._history)

    def clear(self) -> None:
        self._history.clear()
