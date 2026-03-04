"""Verify constrained-output task: check 6 mechanical constraints on essay."""
from __future__ import annotations

import re
from pathlib import Path


def verify(workspace: Path) -> tuple[bool, str]:
    essay_path = workspace / "essay.txt"
    if not essay_path.exists():
        return False, "essay.txt not found"

    text = essay_path.read_text(encoding="utf-8").strip()
    if not text:
        return False, "essay.txt is empty"

    passed = 0
    total = 6
    details = []

    # Split into paragraphs (blocks of text separated by blank lines)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    # Constraint 1: Exactly 3 paragraphs
    if len(paragraphs) == 3:
        passed += 1
        details.append("C1-paragraphs: OK (3)")
    else:
        details.append(f"C1-paragraphs: FAIL (found {len(paragraphs)}, expected 3)")

    # Constraint 2: Word "framework" appears >= 2 times
    framework_count = len(re.findall(r"\bframework\b", text, re.IGNORECASE))
    if framework_count >= 2:
        passed += 1
        details.append(f"C2-framework: OK ({framework_count} occurrences)")
    else:
        details.append(f"C2-framework: FAIL ({framework_count} occurrences, need >= 2)")

    # Constraint 3: First paragraph >= 50 words
    if paragraphs:
        first_para_words = len(paragraphs[0].split())
        if first_para_words >= 50:
            passed += 1
            details.append(f"C3-first-para-words: OK ({first_para_words} words)")
        else:
            details.append(f"C3-first-para-words: FAIL ({first_para_words} words, need >= 50)")
    else:
        details.append("C3-first-para-words: FAIL (no paragraphs found)")

    # Constraint 4: No bullet points or numbered lists
    lines = text.splitlines()
    has_bullets = any(re.match(r"^\s*[-*]\s", line) for line in lines)
    has_numbered = any(re.match(r"^\s*\d+[.)]\s", line) for line in lines)
    if not has_bullets and not has_numbered:
        passed += 1
        details.append("C4-no-lists: OK")
    else:
        details.append(f"C4-no-lists: FAIL (bullets={has_bullets}, numbered={has_numbered})")

    # Constraint 5: Last sentence ends with ?
    # Find the last sentence-ending punctuation
    stripped = text.rstrip()
    if stripped.endswith("?"):
        passed += 1
        details.append("C5-ends-question: OK")
    else:
        last_char = stripped[-1] if stripped else ""
        details.append(f"C5-ends-question: FAIL (ends with '{last_char}')")

    # Constraint 6: Title in ALL CAPS (first non-empty line)
    first_line = ""
    for line in lines:
        if line.strip():
            first_line = line.strip()
            break
    # Check that all alpha characters are uppercase
    alpha_chars = [c for c in first_line if c.isalpha()]
    if alpha_chars and all(c.isupper() for c in alpha_chars):
        passed += 1
        details.append("C6-title-caps: OK")
    else:
        details.append(f"C6-title-caps: FAIL (title: '{first_line[:50]}')")

    ok = passed >= 5
    return ok, f"{passed}/{total} constraints satisfied. {'; '.join(details)}"
