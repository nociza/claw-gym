# claw-gym

A capability evaluation harness for multi-claw AI agents (ZeroClaw, PicoClaw, OpenClaw).

Each task tests **one core agent capability** with:
- A clear natural-language prompt
- Seed files (starting state)
- An automated verifier (`verify.py`)
- A configurable time limit

## Tasks (27)

### Coding (01–05)

| # | Task | Capability | Time |
|---|------|-----------|------|
| 01 | `generate-function` | Code generation | 90s |
| 02 | `fix-logic-bug` | Bug fixing (logic) | 90s |
| 03 | `shell-data-query` | Shell/tool usage | 90s |
| 04 | `multi-file-feature` | Multi-file editing | 120s |
| 05 | `iterative-debug` | Iterative debugging | 120s |

### Web Search (06–10)

| # | Task | Capability | Time |
|---|------|-----------|------|
| 06 | `web-search-factual` | Factual lookup | 120s |
| 07 | `web-search-research` | Multi-source research | 150s |
| 08 | `web-search-technical` | Technical facts | 120s |
| 09 | `web-search-calculation` | Search + compute | 150s |
| 10 | `web-search-current-info` | Current information | 120s |

### Corpus QA (11–13)

| # | Task | Capability | Time |
|---|------|-----------|------|
| 11 | `corpus-contract-qa` | Contract document QA | 150s |
| 12 | `corpus-kb-search` | Knowledge base search | 150s |
| 13 | `corpus-meeting-notes` | Meeting notes analysis | 150s |

### Long Context (14–16)

| # | Task | Capability | Time |
|---|------|-----------|------|
| 14 | `long-context-config-audit` | Config security audit | 150s |
| 15 | `long-context-codebase-nav` | Codebase navigation | 180s |
| 16 | `long-context-data-reconcile` | Data reconciliation | 150s |

### Web Fetch (17–18)

| # | Task | Capability | Time |
|---|------|-----------|------|
| 17 | `web-fetch-api` | REST API consumption | 120s |
| 18 | `web-fetch-html-extract` | HTML data extraction | 150s |

### Vision (19–20)

| # | Task | Capability | Time |
|---|------|-----------|------|
| 19 | `image-chart-extraction` | Chart data extraction from PNG | 150s |
| 20 | `image-document-ocr` | Invoice OCR / document analysis | 150s |

### Instruction Following (21)

| # | Task | Capability | Time |
|---|------|-----------|------|
| 21 | `constrained-output` | Mechanically verifiable writing constraints | 90s |

### Analytics (22)

| # | Task | Capability | Time |
|---|------|-----------|------|
| 22 | `data-analysis-pipeline` | CSV statistics, outlier detection, correlation | 120s |

### Multimodal (23)

| # | Task | Capability | Time |
|---|------|-----------|------|
| 23 | `transcript-analysis` | Meeting transcript + WAV metadata extraction | 150s |

### Tool Orchestration (24)

| # | Task | Capability | Time |
|---|------|-----------|------|
| 24 | `multi-tool-pipeline` | Multi-step read → clean → write pipeline | 150s |

### Robustness (25)

| # | Task | Capability | Time |
|---|------|-----------|------|
| 25 | `adversarial-comprehension` | Contradictory source analysis, majority reasoning | 120s |

### Conversational (26)

| # | Task | Capability | Time |
|---|------|-----------|------|
| 26 | `multi-turn-clarification` | Progressive refinement over 3 turns | 180s |

### Planning (27)

| # | Task | Capability | Time |
|---|------|-----------|------|
| 27 | `long-horizon-project` | System design project planning (DAG phases) | 180s |

## Usage

```bash
# Run all tasks against all claws
python gym.py

# Run specific task against specific claw
python gym.py --task 01 --claw picoclaw

# Run with custom timeout
python gym.py --timeout 180

# List all tasks
python gym.py --list

# Filter by tag
python gym.py --list --tag vision
python gym.py --tag coding --claw openclaw

# Dry run (show what would execute)
python gym.py --dry-run
```

### Tags

Tasks are tagged for filtering: `coding`, `web_search`, `corpus`, `long_context`, `web_fetch`, `vision`, `instruction_following`, `data_analysis`, `multimodal`, `audio`, `tool_orchestration`, `robustness`, `adversarial`, `multi_turn`, `planning`, and more.

## Latest Results

| Claw | Score | Notes |
|------|-------|-------|
| **PicoClaw** | **26/27 (96%)** | Failed: image-chart-extraction |
| **OpenClaw** | **25/27 (93%)** | Failed: image-chart-extraction, constrained-output, transcript-analysis |
| ZeroClaw | — | Cannot chain tool calls in single-message mode |

## Results

Results are written to `results/` as JSON with pass/fail, timing, and output per task per claw.

## Regenerating Seed Files

Some tasks have generated seed files (images, CSV, WAV). To regenerate:

```bash
python tasks/19-image-chart-extraction/generate_chart.py
python tasks/20-image-document-ocr/generate_document.py
python tasks/22-data-analysis-pipeline/generate_sales.py
python tasks/23-transcript-analysis/generate_audio.py
```

Requires `matplotlib` and `Pillow` for image generation. The WAV and CSV generators use only stdlib.
