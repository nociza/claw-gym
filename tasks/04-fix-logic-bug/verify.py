"""Verify task 04: fix-logic-bug."""

import importlib.util
import sys
from pathlib import Path


def verify(workspace: Path) -> tuple[bool, str]:
    module_path = workspace / "inventory.py"
    if not module_path.exists():
        return False, "inventory.py not found"

    try:
        spec = importlib.util.spec_from_file_location("inventory", module_path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["inventory"] = mod
        spec.loader.exec_module(mod)
    except Exception as exc:
        return False, f"Import failed: {exc}"

    Inventory = getattr(mod, "Inventory", None)
    if Inventory is None:
        return False, "Class 'Inventory' not found"

    passed = 0
    checks = []

    # Bug 1: restock should ADD to quantity, not replace
    try:
        inv = Inventory()
        inv.add_product("widget", 10.0, 5)
        new_qty = inv.restock("widget", 3)
        assert new_qty == 8, f"restock(3) on qty=5 should give 8, got {new_qty}"
        passed += 1
        checks.append("restock-add: PASS")
    except Exception as exc:
        checks.append(f"restock-add: FAIL ({exc})")

    # Bug 2: sell should not allow overselling
    try:
        inv = Inventory()
        inv.add_product("widget", 10.0, 2)
        try:
            inv.sell("widget", 5)
            checks.append("sell-overstock: FAIL (no error raised)")
        except (ValueError, RuntimeError):
            passed += 1
            checks.append("sell-overstock: PASS")
    except Exception as exc:
        checks.append(f"sell-overstock: FAIL ({exc})")

    # Bug 3: total_value should sum all products
    try:
        inv = Inventory()
        inv.add_product("apple", 1.0, 10)
        inv.add_product("banana", 2.0, 5)
        total = inv.total_value()
        assert total == 20.0, f"total_value should be 20.0, got {total}"
        passed += 1
        checks.append("total-value: PASS")
    except Exception as exc:
        checks.append(f"total-value: FAIL ({exc})")

    # Normal sell should work
    try:
        inv = Inventory()
        inv.add_product("widget", 10.0, 5)
        price = inv.sell("widget", 2)
        assert price == 20.0, f"sell price should be 20.0, got {price}"
        assert inv.get_quantity("widget") == 3
        passed += 1
        checks.append("sell-normal: PASS")
    except Exception as exc:
        checks.append(f"sell-normal: FAIL ({exc})")

    ok = passed >= 3  # at least 3/4 must pass
    summary = f"{passed}/4 checks passed. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
