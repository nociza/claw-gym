"""Verify task 04: multi-file-feature."""

import importlib.util
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def verify(workspace: Path) -> tuple[bool, str]:
    models_path = workspace / "models.py"
    store_path = workspace / "store.py"

    if not models_path.exists():
        return False, "models.py not found in workspace"
    if not store_path.exists():
        return False, "store.py not found in workspace"

    try:
        models = load_module("models", models_path)
        store_mod = load_module("store", store_path)
    except Exception as exc:
        return False, f"Import failed: {exc}"

    Note = getattr(models, "Note", None)
    NoteStore = getattr(store_mod, "NoteStore", None)
    if Note is None:
        return False, "Note class not found"
    if NoteStore is None:
        return False, "NoteStore class not found"

    passed = 0
    checks = []

    # Check 1: Note has tags field
    try:
        from datetime import datetime
        note = Note(id=1, title="t", content="c", created_at=datetime.now(), tags=["python"])
        assert hasattr(note, "tags")
        assert note.tags == ["python"]
        passed += 1
        checks.append("tags-field: PASS")
    except Exception as exc:
        checks.append(f"tags-field: FAIL ({exc})")

    # Check 2: Note tags defaults to empty list
    try:
        note = Note(id=1, title="t", content="c", created_at=datetime.now())
        assert note.tags == [] or note.tags == ()
        passed += 1
        checks.append("tags-default: PASS")
    except Exception as exc:
        checks.append(f"tags-default: FAIL ({exc})")

    # Check 3: search method exists and works
    try:
        ns = NoteStore()
        n1 = ns.add("Python Tutorial", "Learn Python basics")
        n2 = ns.add("Rust Guide", "Systems programming with Rust")
        n3 = ns.add("Python Advanced", "Advanced Python patterns")

        results = ns.search("python")
        assert len(results) >= 2, f"Expected >=2 results for 'python', got {len(results)}"

        results2 = ns.search("rust")
        assert len(results2) >= 1, f"Expected >=1 results for 'rust', got {len(results2)}"

        results3 = ns.search("nonexistent-xyz")
        assert len(results3) == 0, f"Expected 0 results for nonexistent, got {len(results3)}"

        passed += 1
        checks.append("search: PASS")
    except Exception as exc:
        checks.append(f"search: FAIL ({exc})")

    # Check 4: search is case-insensitive
    try:
        ns = NoteStore()
        ns.add("Hello World", "content")
        results = ns.search("HELLO")
        assert len(results) >= 1
        passed += 1
        checks.append("search-case: PASS")
    except Exception as exc:
        checks.append(f"search-case: FAIL ({exc})")

    # Check 5: get_by_tag method
    try:
        ns = NoteStore()
        # We need to check if add supports tags parameter
        add_sig = ns.add.__code__.co_varnames
        if "tags" in add_sig:
            ns.add("Note1", "c1", tags=["python", "tutorial"])
            ns.add("Note2", "c2", tags=["rust"])
            ns.add("Note3", "c3", tags=["python", "advanced"])
        else:
            # Manually set tags
            n1 = ns.add("Note1", "c1")
            n2 = ns.add("Note2", "c2")
            n3 = ns.add("Note3", "c3")
            n1.tags = ["python", "tutorial"]
            n2.tags = ["rust"]
            n3.tags = ["python", "advanced"]

        results = ns.get_by_tag("python")
        assert len(results) >= 2, f"Expected >=2 notes with tag 'python', got {len(results)}"

        results2 = ns.get_by_tag("rust")
        assert len(results2) >= 1

        passed += 1
        checks.append("get_by_tag: PASS")
    except Exception as exc:
        checks.append(f"get_by_tag: FAIL ({exc})")

    # Check 6: search finds tags too
    try:
        ns = NoteStore()
        add_sig = ns.add.__code__.co_varnames
        if "tags" in add_sig:
            ns.add("Generic Title", "generic content", tags=["special-tag-xyz"])
        else:
            n = ns.add("Generic Title", "generic content")
            n.tags = ["special-tag-xyz"]

        results = ns.search("special-tag-xyz")
        assert len(results) >= 1, "search should find notes by tag content"
        passed += 1
        checks.append("search-tags: PASS")
    except Exception as exc:
        checks.append(f"search-tags: FAIL ({exc})")

    ok = passed >= 4  # 4 out of 6
    summary = f"{passed}/6 checks passed. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
