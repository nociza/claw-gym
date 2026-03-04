"""Verify long-horizon-project task: validate project plan structure and content."""
from __future__ import annotations

import json
from pathlib import Path


def verify(workspace: Path) -> tuple[bool, str]:
    plan_path = workspace / "plan.json"
    if not plan_path.exists():
        return False, "plan.json not found"

    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except Exception as e:
        return False, f"Invalid JSON: {e}"

    passed = 0
    total = 6
    details = []

    phases = plan.get("phases", [])

    # Check 1: At least 5 phases
    if len(phases) >= 5:
        passed += 1
        details.append(f"C1-phase-count: OK ({len(phases)} phases)")
    else:
        details.append(f"C1-phase-count: FAIL ({len(phases)} phases, need >= 5)")

    # Check 2: Valid DAG (no circular dependencies)
    phase_ids = {p.get("id", f"unnamed-{i}") for i, p in enumerate(phases)}
    # Build adjacency: phase -> phases it depends on
    is_dag = True
    # Check for cycles via topological sort
    deps_map = {}
    for p in phases:
        pid = p.get("id", "")
        dep_list = p.get("dependencies", [])
        deps_map[pid] = set(dep_list)

    # Kahn's algorithm
    in_degree = {pid: len(deps) for pid, deps in deps_map.items()}
    queue = [pid for pid, deg in in_degree.items() if deg == 0]
    sorted_count = 0
    remaining = dict(deps_map)
    while queue:
        node = queue.pop(0)
        sorted_count += 1
        # Find nodes that depend on this one
        for pid, deps in remaining.items():
            if node in deps:
                deps.discard(node)
                in_degree[pid] = len(deps)
                if in_degree[pid] == 0:
                    queue.append(pid)

    if sorted_count == len(deps_map) and len(deps_map) > 0:
        passed += 1
        details.append("C2-valid-dag: OK")
    else:
        is_dag = False
        details.append("C2-valid-dag: FAIL (circular dependencies detected)")

    # Check 3: At least one root phase (empty dependencies)
    root_phases = [p for p in phases if not p.get("dependencies", ["x"])]
    if root_phases:
        passed += 1
        details.append(f"C3-root-phase: OK ({len(root_phases)} root phases)")
    else:
        details.append("C3-root-phase: FAIL (no phase with empty dependencies)")

    # Check 4: Each phase has at least 2 deliverables
    all_have_deliverables = True
    min_deliverables = float("inf")
    for p in phases:
        deliverables = p.get("deliverables", [])
        if len(deliverables) < 2:
            all_have_deliverables = False
            min_deliverables = min(min_deliverables, len(deliverables))
    if all_have_deliverables and phases:
        passed += 1
        details.append("C4-deliverables: OK (all phases have >= 2)")
    else:
        details.append(f"C4-deliverables: FAIL (some phases have < 2 deliverables)")

    # Check 5: Constraint keyword coverage (>= 6 of 8 key terms)
    plan_text = json.dumps(plan).lower()
    keywords = [
        "kafka",
        "postgres",       # PostgreSQL / postgres
        "kubernetes",     # or k8s
        "latency",        # sub-second latency
        "scal",           # horizontal scaling / scalability
        "retention",      # data retention
        "auth",           # authentication
        "monitor",        # monitoring
    ]
    matched_keywords = []
    for kw in keywords:
        if kw in plan_text:
            matched_keywords.append(kw)
        elif kw == "kubernetes" and "k8s" in plan_text:
            matched_keywords.append(kw)
        elif kw == "postgres" and "postgresql" in plan_text:
            matched_keywords.append(kw)

    if len(matched_keywords) >= 6:
        passed += 1
        details.append(f"C5-constraints: OK ({len(matched_keywords)}/8 keywords: {', '.join(matched_keywords)})")
    else:
        details.append(f"C5-constraints: FAIL ({len(matched_keywords)}/8 keywords: {', '.join(matched_keywords)})")

    # Check 6: Each phase has all required keys
    required_keys = {"id", "name", "description", "dependencies", "deliverables"}
    all_have_keys = True
    for p in phases:
        if not required_keys.issubset(p.keys()):
            all_have_keys = False
            missing = required_keys - set(p.keys())
            details.append(f"C6-phase-keys: FAIL (phase '{p.get('id', '?')}' missing: {missing})")
            break
    if all_have_keys and phases:
        passed += 1
        details.append("C6-phase-keys: OK (all phases have required keys)")
    elif not phases:
        details.append("C6-phase-keys: FAIL (no phases)")

    ok = passed >= 4
    return ok, f"{passed}/{total} checks passed. {'; '.join(details)}"
