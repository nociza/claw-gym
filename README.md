# claw-gym

A capability evaluation harness for multi-claw AI agents (ZeroClaw, PicoClaw, OpenClaw).

Each task tests **one core agent capability** with:
- A clear natural-language prompt
- Seed files (starting state)
- An automated verifier (`verify.py`)
- A configurable time limit (default 120s)

## Tasks

| # | Task | Capability | Time |
|---|------|-----------|------|
| 01 | `comprehend-function` | Code comprehension | 60s |
| 02 | `generate-function` | Code generation | 90s |
| 03 | `fix-syntax-bug` | Bug fixing (syntax) | 60s |
| 04 | `fix-logic-bug` | Bug fixing (logic) | 90s |
| 05 | `refactor-extract` | Refactoring | 120s |
| 06 | `shell-data-query` | Shell/tool usage | 90s |
| 07 | `write-tests` | Test generation | 120s |
| 08 | `multi-file-feature` | Multi-file editing | 120s |
| 09 | `csv-to-json` | Data transformation | 90s |
| 10 | `iterative-debug` | Iterative debugging | 120s |

## Usage

```bash
# Run all tasks against all claws
python gym.py

# Run specific task against specific claw
python gym.py --task 01 --claw zeroclaw

# Run with custom timeout
python gym.py --timeout 180
```

## Results

Results are written to `results/` as JSON with pass/fail, timing, and output per task per claw.
