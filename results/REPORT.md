# claw-gym Evaluation Report

**Date**: 2026-03-01
**Environment**: Linux x86_64, Python 3.14.3
**Model**: gpt-5.3-codex-spark (OpenAI Codex, ChatGPT Pro subscription OAuth)

## Executive Summary

10 capability tasks were designed from first principles to evaluate three claw agents
(ZeroClaw, PicoClaw, OpenClaw). Each task targets a specific coding agent capability
with automated verification. All three claws use the same underlying model
(gpt-5.3-codex-spark) via OpenAI Codex OAuth.

### Scorecard

| Claw | Score | Notes |
|------|-------|-------|
| **PicoClaw** | **9/10** | Fast, reliable tool use. Only failed task 07 (env issue). |
| **OpenClaw** | **9/10** | Slightly slower but equally capable. Same env failure on 07. |
| **ZeroClaw** | **0/10** | Tool-call hallucination; cannot chain file_read → file_write. |

### Auth Configuration

| Claw | Auth | Model | Binary |
|------|------|-------|--------|
| ZeroClaw | OAuth (openai-codex) | gpt-5.3-codex-spark | `/home/linuxbrew/.linuxbrew/bin/zeroclaw` |
| PicoClaw | OAuth (openai) | openai/gpt-5.3-codex-spark | `~/.local/bin/picoclaw` |
| OpenClaw | OAuth (openai-codex) | openai-codex/gpt-5.3-codex-spark | `~/.local/bin/openclaw` |

## Task Design

| # | Task | Capability | Time Limit | Rationale |
|---|------|-----------|------------|-----------|
| 01 | comprehend-function | Code comprehension | 60s | Can the agent read & understand code? |
| 02 | generate-function | Code generation | 90s | Can it write correct code from spec? |
| 03 | fix-syntax-bug | Bug fix (syntax) | 60s | Can it fix obvious syntax errors? |
| 04 | fix-logic-bug | Bug fix (logic) | 90s | Can it find and fix logic bugs? |
| 05 | refactor-extract | Refactoring | 120s | Can it restructure code preserving behavior? |
| 06 | shell-data-query | Shell/tool usage | 90s | Can it use shell commands to analyze data? |
| 07 | write-tests | Test generation | 120s | Can it write meaningful pytest tests? |
| 08 | multi-file-feature | Multi-file editing | 120s | Can it coordinate changes across files? |
| 09 | csv-to-json | Data transformation | 90s | Can it parse/transform structured data? |
| 10 | iterative-debug | Iterative debugging | 120s | Can it run, observe errors, and fix them? |

## Full Results

| Task | ZeroClaw | PicoClaw | OpenClaw |
|------|----------|----------|----------|
| 01 - Comprehend Function | FAIL (5.6s) | **PASS** (3.1s) 5/5 | **PASS** (8.0s) 5/5 |
| 02 - Generate Function | FAIL (5.8s) | **PASS** (19.1s) 8/8 | **PASS** (11.6s) 8/8 |
| 03 - Fix Syntax Bug | FAIL (17.1s) | **PASS** (3.2s) 5/5 | **PASS** (15.1s) 5/5 |
| 04 - Fix Logic Bug | FAIL (4.3s) | **PASS** (3.5s) 4/4 | **PASS** (8.4s) 4/4 |
| 05 - Refactor Extract | FAIL (3.6s) | **PASS** (5.1s) 6/6 | **PASS** (8.1s) 6/6 |
| 06 - Shell Data Query | FAIL (39.2s) | **PASS** (19.8s) 5/5 | **PASS** (9.2s) 5/5 |
| 07 - Write Tests | FAIL (28.4s) | FAIL* (4.6s) | FAIL* (18.3s) |
| 08 - Multi-File Feature | FAIL (4.7s) | **PASS** (7.5s) 6/6 | **PASS** (12.0s) 6/6 |
| 09 - CSV to JSON | FAIL (27.6s) | **PASS** (6.0s) 3/4† | **PASS** (14.1s) 4/4 |
| 10 - Iterative Debug | FAIL (20.9s) | **PASS** (11.3s) 5/5 | **PASS** (26.3s) 5/5 |
| **Total** | **0/10** | **9/10** | **9/10** |

\* Task 07 failed on both PicoClaw and OpenClaw because `pytest` is not installed in this
  environment. Both agents wrote valid test files, but the verifier couldn't execute them.
  This is an environment limitation, not an agent capability failure.

† PicoClaw got 3/4 on task 09 (Engineering department average salary was slightly off:
  97000.0 vs expected 99500.0) but still passed overall threshold.

### Performance Comparison

| Metric | PicoClaw | OpenClaw |
|--------|----------|----------|
| Avg task time | 8.3s | 13.1s |
| Fastest task | 3.1s (task 01) | 8.0s (task 01) |
| Slowest task | 19.8s (task 06) | 26.3s (task 10) |
| Perfect scores | 8/9 passed tasks | 9/9 passed tasks |

PicoClaw is ~60% faster on average. OpenClaw scored a perfect 4/4 on task 09
where PicoClaw got 3/4. Both demonstrate strong multi-step tool chaining.

## ZeroClaw Analysis (0/10)

### Key Findings

#### 1. Tool Call Hallucination (Critical)
The agent consistently **claims to have written files** without actually calling the
`file_write` tool. In 4/10 tasks, the agent's text output explicitly states "I wrote
the file to X" but no `<tool_call>` for `file_write` was ever emitted. The files do
not exist on disk.

**Evidence**: Manual testing confirms `file_write` works when called directly:
```
zeroclaw agent -m 'Call file_write with path "test.txt" and content "hello"'
→ <tool_call>{"name":"file_write","arguments":{"path":"test.txt","content":"hello"}}</tool_call>
→ File created successfully ✓
```
But in multi-step prompts (read → modify → write), the model stops after the first
tool call and generates text instead of continuing with additional tool calls.

#### 2. No Multi-Step Tool Chaining
The model in single-message mode (`-m`) cannot reliably execute:
  file_read → process → file_write

After `file_read` returns, the model generates a text response (often with correct
code in markdown blocks) but does NOT call `file_write`. This appears to be a
fundamental limitation of ZeroClaw's agent loop in one-shot mode.

#### 3. Code Quality in Text Output is Good
When the agent DOES output code (in markdown blocks), the code quality is high:
- Task 03: Correctly fixed all 4 syntax errors in tokenizer.py
- Task 04: Produced correct inventory.py fix (but for wrong task due to session leak)
- The agent demonstrates genuine code comprehension and generation ability

#### 4. Session Memory Contamination
Despite clearing sessions between tasks, the agent's memory/context leaks:
- Task 04's output contained tokenizer.py code (from task 03)
- Task 05's output contained scheduler.py code (from task 01)
- The zeroclaw memory SQLite database persists across session clears

## PicoClaw Analysis (9/10)

PicoClaw demonstrated strong, reliable tool-use capabilities:
- **Multi-step chaining works**: file_read → modify → file_write executed flawlessly
- **Fast execution**: Most tasks completed in under 10 seconds
- **Shell tool usage**: Successfully used shell commands for data analysis (task 06)
- **Multi-file editing**: Correctly coordinated changes across models.py and store.py (task 08)
- **Iterative debugging**: Ran code, observed errors, and fixed them (task 10)

Only substantive issue: task 09 Engineering department average was slightly off (97000 vs 99500).

## OpenClaw Analysis (9/10)

OpenClaw performed identically to PicoClaw in capability, with slightly higher latency:
- **Perfect accuracy on passed tasks**: 9/9 tasks that weren't blocked by env issues scored full marks
- **Strongest on data transformation**: Got 4/4 on task 09 where PicoClaw missed one check
- **Multi-file editing**: All 6 checks passed on task 08
- **Gateway fallback**: Fell back to embedded mode (gateway not running) but functioned correctly

## Recommendations

1. **ZeroClaw** needs a fix for its agent loop to support multi-turn tool chaining in
   single-message mode. The underlying model capability is there (code quality in text
   is high), but the tool dispatch is broken for multi-step workflows.

2. **Task 07 (write-tests)**: Install `pytest` in the eval environment to get a true
   capability measurement. Both PicoClaw and OpenClaw likely score 10/10 with pytest available.

3. **Credential porting**: The manual credential porting process (ZeroClaw → PicoClaw/OpenClaw)
   should be automated by clawie. Key format differences discovered:
   - PicoClaw: `~/.picoclaw/auth.json` with `{"credentials": {"openai": {access_token, refresh_token, ...}}}`
   - OpenClaw: `~/.openclaw/agents/main/agent/auth-profiles.json` with `{"version": 1, "profiles": {"openai-codex:default": {type: "oauth", access, refresh, expires (ms), ...}}}`
   - Codex CLI: `~/.codex/auth.json` with `{"auth_mode": "chatgpt", "tokens": {id_token, access_token, refresh_token, ...}}`

## Methodology Notes

- Tasks were designed from first principles based on SWE-bench methodology and real-world use cases
- Each task has automated verification via `verify.py` with specific pass/fail criteria
- Time limits range from 60-120s per task
- All three claws tested against the same model (gpt-5.3-codex-spark) via the same OAuth credentials
- The gym framework stages files in each claw's workspace and collects results for verification
