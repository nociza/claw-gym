"""Product inventory tracker."""

from __future__ import annotations


class Inventory:
    def __init__(self) -> None:
        self._products: dict[str, dict] = {}

    def add_product(self, name: str, price: float, quantity: int = 0) -> None:
        """Register a new product."""
        if name in self._products:
            raise ValueError(f"Product '{name}' already exists")
        self._products[name] = {"price": price, "quantity": quantity}

    def restock(self, name: str, amount: int) -> int:
        """Add stock. Returns new quantity."""
        product = self._get_product(name)
        if amount > 0:  # BUG: should be >= 0, but actually the real bug is different
            product["quantity"] = amount  # BUG: should be += not =
        return product["quantity"]

    def sell(self, name: str, amount: int) -> float:
        """Sell items. Returns total sale price."""
        product = self._get_product(name)
        if amount <= 0:
            raise ValueError("Amount must be positive")
        # BUG: no stock check
        product["quantity"] -= amount
        return product["price"] * amount

    def get_quantity(self, name: str) -> int:
        """Get current stock level."""
        return self._get_product(name)["quantity"]

    def total_value(self) -> float:
        """Calculate total inventory value (price * quantity for all products)."""
        total = 0.0
        for product in self._products.values():
            total = product["price"] * product["quantity"]  # BUG: = instead of +=
        return total

    def _get_product(self, name: str) -> dict:
        if name not in self._products:
            raise KeyError(f"Product '{name}' not found")
        return self._products[name]
