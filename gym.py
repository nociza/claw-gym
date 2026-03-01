#!/usr/bin/env python3
"""claw-gym: capability evaluation harness for multi-claw AI agents.

Dispatches bite-sized tasks to ZeroClaw, PicoClaw, and OpenClaw agents,
verifies outputs, and collects timing/pass-fail results.

Each claw agent has its own restricted workspace. This harness stages seed
files into a task-specific subdirectory within the claw's workspace, points
the agent at them, and then copies results back for verification.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

TASKS_DIR = Path(__file__).parent / "tasks"
RESULTS_DIR = Path(__file__).parent / "results"

CLAW_BINARIES = {
    "zeroclaw": shutil.which("zeroclaw") or "/home/linuxbrew/.linuxbrew/bin/zeroclaw",
    "picoclaw": shutil.which("picoclaw") or str(Path.home() / ".local/bin/picoclaw"),
    "openclaw": shutil.which("openclaw") or str(Path.home() / ".local/bin/openclaw"),
}

# Each claw stores its agent workspace in a different location.
CLAW_WORKSPACES = {
    "zeroclaw": Path.home() / ".zeroclaw" / "workspace",
    "picoclaw": Path.home() / ".picoclaw" / "workspace",
    "openclaw": Path.home() / ".openclaw" / "workspace",
}


def discover_tasks(task_filter: str | None = None) -> list[dict]:
    """Find all task directories and load their definitions."""
    tasks = []
    for task_dir in sorted(TASKS_DIR.iterdir()):
        if not task_dir.is_dir():
            continue
        task_json = task_dir / "task.json"
        if not task_json.exists():
            continue
        with open(task_json) as f:
            task = json.load(f)
        task["_dir"] = str(task_dir)
        task_id = task.get("id", task_dir.name)
        task_num = task_id.split("-")[0]

        if task_filter:
            if task_filter not in (task_num, task_id, task_dir.name):
                continue
        tasks.append(task)
    return tasks


def stage_task(task: dict, claw: str) -> Path:
    """Stage seed files into the claw's workspace and return the staging dir.

    Creates:  <claw_workspace>/claw-gym/<task_id>/seed/   (seed files)
              <claw_workspace>/claw-gym/<task_id>/output/  (for agent output)
    """
    task_dir = Path(task["_dir"])
    task_id = task["id"]
    claw_ws = CLAW_WORKSPACES[claw]
    staging = claw_ws / "claw-gym" / task_id

    # Clean previous staging
    if staging.exists():
        shutil.rmtree(staging)

    seed_staging = staging / "seed"
    output_staging = staging / "output"
    seed_staging.mkdir(parents=True)
    output_staging.mkdir(parents=True)

    # Copy seed files
    seed_dir = task_dir / "seed"
    if seed_dir.exists():
        for f in seed_dir.iterdir():
            if f.is_file():
                shutil.copy2(f, seed_staging / f.name)

    return staging


def extract_code_blocks(stdout: str, expected_files: list[str]) -> dict[str, str]:
    """Extract code blocks from agent output, mapping them to expected filenames.

    Handles patterns like:
      ```python\n<code>\n```
      file_write with content
    """
    import re
    blocks: list[str] = []
    # Extract fenced code blocks (```python ... ``` or ``` ... ```)
    for match in re.finditer(r"```(?:python)?\s*\n(.*?)```", stdout, re.DOTALL):
        code = match.group(1).strip()
        if code and len(code) > 20:  # skip trivial snippets
            blocks.append(code)

    # Map blocks to expected filenames by best-guess matching
    result: dict[str, str] = {}
    basenames = [Path(f).name for f in expected_files]

    if len(blocks) == 1 and len(basenames) == 1:
        result[basenames[0]] = blocks[0]
    elif len(blocks) >= len(basenames):
        for i, name in enumerate(basenames):
            if i < len(blocks):
                result[name] = blocks[i]
    else:
        # Try to match by content hints
        for block in blocks:
            for name in basenames:
                stem = Path(name).stem
                if stem not in result:
                    # Simple heuristic: match by function/class names or filename mentions
                    if stem.lower() in block.lower() or name.lower() in stdout.lower():
                        result[name] = block
                        break
            else:
                # Assign to first unmatched
                for name in basenames:
                    if name not in result:
                        result[name] = block
                        break

    return result


def collect_results(staging: Path, task: dict, stdout: str = "") -> Path:
    """Copy results from claw staging back to the gym's local workspace for verification.

    If the agent wrote files to the output dir, use those.
    Otherwise, extract code blocks from stdout as a fallback.
    """
    task_dir = Path(task["_dir"])
    local_ws = task_dir / "workspace"

    if local_ws.exists():
        shutil.rmtree(local_ws)
    local_ws.mkdir(parents=True)

    # First: try actual files from the agent's output directory
    output_dir = staging / "output"
    files_found = 0
    if output_dir.exists():
        for f in output_dir.iterdir():
            if f.is_file():
                shutil.copy2(f, local_ws / f.name)
                files_found += 1

    # Fallback: extract code blocks from agent's text output
    if files_found == 0 and stdout:
        expected = task.get("expected_output_files", [])
        extracted = extract_code_blocks(stdout, expected)
        for filename, content in extracted.items():
            (local_ws / filename).write_text(content, encoding="utf-8")

    return local_ws


def build_agent_prompt(task: dict, staging: Path, claw: str) -> str:
    """Build the full prompt using paths relative to the claw's workspace root."""
    prompt = task["prompt"]
    claw_ws = CLAW_WORKSPACES[claw]

    # Compute relative paths from claw workspace root
    try:
        rel_staging = staging.relative_to(claw_ws)
    except ValueError:
        rel_staging = staging

    seed_rel = f"{rel_staging}/seed"
    output_rel = f"{rel_staging}/output"

    prompt = prompt.replace("seed/", f"{seed_rel}/")
    prompt = prompt.replace("workspace/", f"{output_rel}/")

    # Critical: explicit tool-use instructions to prevent hallucination
    prompt += (
        f"\n\nCRITICAL INSTRUCTIONS:"
        f"\n- Input files are in: {seed_rel}/"
        f"\n- You MUST use file_write tool to save each output file to: {output_rel}/"
        f"\n- You MUST actually call the file_read and file_write tools - do NOT just describe what you would do."
        f"\n- Call file_write for EVERY output file. Do not skip any tool calls."
    )
    return prompt


def check_claw_auth(claw: str, binary: str) -> tuple[bool, str]:
    """Quick check if a claw has working auth configured."""
    try:
        if claw == "zeroclaw":
            r = subprocess.run(
                [binary, "auth", "status"],
                capture_output=True, text=True, timeout=10,
            )
            if r.returncode == 0 and "expires" in r.stdout:
                return True, "auth ok"
            return False, "No active auth profile"

        elif claw == "picoclaw":
            r = subprocess.run(
                [binary, "auth", "status"],
                capture_output=True, text=True, timeout=10,
            )
            if "No authenticated" in r.stdout:
                return False, "No API keys configured (run: picoclaw auth login --provider openai)"
            return True, "auth ok"

        elif claw == "openclaw":
            auth_file = Path.home() / ".openclaw/agents/main/agent/auth-profiles.json"
            if not auth_file.exists():
                return False, "No auth-profiles.json (run: openclaw agents add main)"
            return True, "auth file exists"

        return True, "unknown claw, assuming ok"
    except Exception as exc:
        return False, f"Auth check failed: {exc}"


def run_with_claw(claw: str, prompt: str, timeout: int) -> dict:
    """Execute a task with a specific claw agent. Returns run metadata."""
    binary = CLAW_BINARIES.get(claw, "")
    if not binary or not Path(binary).exists():
        return {
            "status": "skip",
            "error": f"Binary not found: {binary}",
            "elapsed_seconds": 0,
            "stdout": "",
            "stderr": "",
        }

    # Pre-flight: check if the claw has working auth
    auth_ok, auth_msg = check_claw_auth(claw, binary)
    if not auth_ok:
        return {
            "status": "skip",
            "error": auth_msg,
            "elapsed_seconds": 0,
            "stdout": "",
            "stderr": "",
        }

    # Clear session state to prevent cross-task contamination
    if claw == "zeroclaw":
        sessions_dir = Path.home() / ".zeroclaw/workspace/sessions"
        if sessions_dir.exists():
            shutil.rmtree(sessions_dir, ignore_errors=True)
            sessions_dir.mkdir(exist_ok=True)

    # Build agent command based on claw type
    if claw == "zeroclaw":
        cmd = [binary, "agent", "-t", "0.0", "-m", prompt]
    elif claw == "picoclaw":
        cmd = [binary, "agent", "-m", prompt]
    elif claw == "openclaw":
        ts = str(int(time.time()))
        cmd = [binary, "agent", "-m", prompt, "--session-id", f"gym-{ts}", "--json"]
    else:
        return {"status": "skip", "error": f"Unknown claw: {claw}", "elapsed_seconds": 0}

    start = time.monotonic()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "TERM": "dumb", "NO_COLOR": "1"},
        )
        elapsed = time.monotonic() - start
        return {
            "status": "completed",
            "exit_code": result.returncode,
            "elapsed_seconds": round(elapsed, 2),
            "stdout": result.stdout[-8000:] if result.stdout else "",
            "stderr": result.stderr[-2000:] if result.stderr else "",
        }
    except subprocess.TimeoutExpired:
        elapsed = time.monotonic() - start
        return {
            "status": "timeout",
            "elapsed_seconds": round(elapsed, 2),
            "stdout": "",
            "stderr": f"Timed out after {timeout}s",
        }
    except Exception as exc:
        elapsed = time.monotonic() - start
        return {
            "status": "error",
            "error": str(exc),
            "elapsed_seconds": round(elapsed, 2),
            "stdout": "",
            "stderr": "",
        }


def run_verify(task: dict, workspace: Path) -> tuple[bool, str]:
    """Run the task's verify.py against the workspace."""
    task_dir = Path(task["_dir"])
    verify_path = task_dir / "verify.py"

    if not verify_path.exists():
        return False, "No verify.py found"

    try:
        spec = importlib.util.spec_from_file_location("verify_mod", verify_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.verify(workspace)
    except Exception as exc:
        return False, f"Verify crashed: {exc}"


def print_result_table(results: list[dict]) -> None:
    """Print a summary table of all results."""
    print("\n" + "=" * 80)
    print(f"{'Task':<30} {'Claw':<12} {'Status':<10} {'Pass':<6} {'Time':>8}")
    print("-" * 80)

    for r in results:
        status = r["run"]["status"]
        passed = "YES" if r["verify"]["passed"] else "NO"
        elapsed = f"{r['run']['elapsed_seconds']:.1f}s"
        if status == "skip":
            passed = "-"
            elapsed = "-"
        print(f"{r['task_id']:<30} {r['claw']:<12} {status:<10} {passed:<6} {elapsed:>8}")

    print("=" * 80)

    # Summary per claw
    claws = sorted(set(r["claw"] for r in results))
    print(f"\n{'Claw':<12} {'Passed':<10} {'Failed':<10} {'Skipped':<10} {'Score':>8}")
    print("-" * 50)
    for claw in claws:
        claw_results = [r for r in results if r["claw"] == claw]
        p = sum(1 for r in claw_results if r["verify"]["passed"])
        f = sum(1 for r in claw_results if not r["verify"]["passed"] and r["run"]["status"] != "skip")
        s = sum(1 for r in claw_results if r["run"]["status"] == "skip")
        total = p + f
        score = f"{p}/{total}" if total > 0 else "N/A"
        print(f"{claw:<12} {p:<10} {f:<10} {s:<10} {score:>8}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="claw-gym: evaluate claw agent capabilities")
    parser.add_argument("--task", "-t", help="Run specific task (number or id)")
    parser.add_argument("--claw", "-c", help="Run specific claw (zeroclaw/picoclaw/openclaw)")
    parser.add_argument("--timeout", type=int, default=0, help="Override task time limit")
    parser.add_argument("--dry-run", action="store_true", help="Show tasks without running")
    parser.add_argument("--list", action="store_true", dest="list_tasks", help="List all tasks")
    args = parser.parse_args()

    tasks = discover_tasks(args.task)
    claws = [args.claw] if args.claw else list(CLAW_BINARIES.keys())

    if args.list_tasks:
        print(f"\n{'ID':<30} {'Capability':<25} {'Time':>6}")
        print("-" * 65)
        for task in tasks:
            print(f"{task['id']:<30} {task['capability']:<25} {task['time_limit_seconds']:>4}s")
        return

    if not tasks:
        print("No tasks found" + (f" matching '{args.task}'" if args.task else ""))
        sys.exit(1)

    if args.dry_run:
        print(f"Would run {len(tasks)} tasks against {', '.join(claws)}")
        for task in tasks:
            print(f"  - {task['id']} ({task['capability']}, {task['time_limit_seconds']}s)")
        return

    # Run all tasks
    all_results = []
    RESULTS_DIR.mkdir(exist_ok=True)

    for task in tasks:
        for claw in claws:
            task_id = task["id"]
            timeout = args.timeout or task["time_limit_seconds"]

            print(f"\n>>> [{claw}] {task_id} (timeout: {timeout}s)")

            # Stage seed files into the claw's workspace
            staging = stage_task(task, claw)
            prompt = build_agent_prompt(task, staging, claw)

            run_result = run_with_claw(claw, prompt, timeout)
            print(f"    Status: {run_result['status']} ({run_result['elapsed_seconds']}s)")

            if run_result["status"] == "completed":
                # Copy results back for verification (falls back to extracting code blocks)
                local_ws = collect_results(staging, task, run_result.get("stdout", ""))
                passed, msg = run_verify(task, local_ws)
            else:
                passed, msg = False, f"Run status: {run_result['status']}"

            print(f"    Verify: {'PASS' if passed else 'FAIL'} - {msg}")

            result_entry = {
                "task_id": task_id,
                "capability": task["capability"],
                "claw": claw,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "run": run_result,
                "verify": {"passed": passed, "message": msg},
            }
            all_results.append(result_entry)

    # Print summary
    print_result_table(all_results)

    # Save results
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    results_file = RESULTS_DIR / f"run_{ts}.json"
    with open(results_file, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"Results saved to {results_file}")


if __name__ == "__main__":
    main()
