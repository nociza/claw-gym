"""Verify task 03: fix-syntax-bug."""

import importlib.util
import sys
from pathlib import Path


def verify(workspace: Path) -> tuple[bool, str]:
    module_path = workspace / "tokenizer.py"
    if not module_path.exists():
        return False, "tokenizer.py not found"

    # Check it compiles
    source = module_path.read_text(encoding="utf-8")
    try:
        compile(source, str(module_path), "exec")
    except SyntaxError as exc:
        return False, f"Still has syntax error: {exc}"

    # Check it runs
    try:
        spec = importlib.util.spec_from_file_location("tokenizer", module_path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["tokenizer"] = mod
        spec.loader.exec_module(mod)
    except Exception as exc:
        return False, f"Import failed: {exc}"

    # Check functions exist
    tokenize = getattr(mod, "tokenize", None)
    tokens_to_string = getattr(mod, "tokens_to_string", None)
    if tokenize is None:
        return False, "Function 'tokenize' not found"
    if tokens_to_string is None:
        return False, "Function 'tokens_to_string' not found"

    # Check behavior
    checks = 0
    try:
        tokens = tokenize("1 + 2 * (3 - 4)")
        assert len(tokens) == 9, f"Expected 9 tokens, got {len(tokens)}"
        checks += 1

        assert tokens[0].kind == "NUMBER" and tokens[0].value == "1"
        checks += 1

        assert tokens[1].kind == "OP" and tokens[1].value == "+"
        checks += 1

        result = tokens_to_string(tokens)
        assert isinstance(result, str) and len(result) > 0
        checks += 1

        tokens2 = tokenize("42")
        assert len(tokens2) == 1 and tokens2[0].value == "42"
        checks += 1

    except Exception as exc:
        return False, f"Behavioral check failed after {checks} checks: {exc}"

    return True, f"All syntax errors fixed, {checks} behavioral checks passed"


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
