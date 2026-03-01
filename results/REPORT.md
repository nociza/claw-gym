# claw-gym Evaluation Report

**Date**: 2026-03-01
**Environment**: Linux x86_64, Python 3.14.3

## Executive Summary

10 capability tasks were designed from first principles to evaluate three claw agents
(ZeroClaw, PicoClaw, OpenClaw). Each task targets a specific, representative coding
agent capability with automated verification.

### Auth Status
| Claw | Auth | Model | Status |
|------|------|-------|--------|
| ZeroClaw | OAuth (openai-codex) | gpt-5.3-codex-spark | Tested |
| PicoClaw | None configured | (ollama offline) | Skipped |
| OpenClaw | None configured | (no API key) | Skipped |

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

## ZeroClaw Results (gpt-5.3-codex-spark)

### Scores: 0/10 tasks passed automated verification

| Task | Time | Tool Calls | file_read | file_write | Verdict |
|------|------|-----------|-----------|------------|---------|
| 01-comprehend | 5.6s | 3 | Yes | No | Agent read file, answered in text (not to file) |
| 02-generate | 5.8s | 0 | No | No | Hallucinated completion |
| 03-fix-syntax | 17.1s | 0 | No | No | Hallucinated completion |
| 04-fix-logic | 4.3s | 1 | Yes | No | Read file, output code block (wrong task) |
| 05-refactor | 3.6s | 1 | No | No | Memory recall only, session contamination |
| 06-shell-query | 39.2s | 0 | No | No | Hallucinated completion |
| 07-write-tests | 28.4s | 0 | No | No | No output produced |
| 08-multi-file | 4.7s | 1 | No | No | Memory recall, claimed completion |
| 09-csv-to-json | 27.6s | 0 | No | No | No output produced |
| 10-iterative | 20.9s | 0 | No | No | Hallucinated completion |

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
fundamental limitation of the model's behavior in one-shot mode.

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

#### 5. Autonomy Configuration Impact
- `supervised` mode blocks all tool calls with interactive prompts (unusable non-interactively)
- `full` autonomy with auto-approve for file_write still doesn't fix the chaining issue
- The root cause is model behavior, not sandbox configuration

## PicoClaw & OpenClaw

Both agents were **skipped** due to missing API authentication:
- **PicoClaw**: No cloud provider API keys configured. Only has local ollama
  model (not running). Would need `picoclaw auth login --provider openai` to configure.
- **OpenClaw**: No auth-profiles.json for the main agent. Would need
  `openclaw agents add main` with Anthropic API key to configure.

These agents could not be evaluated without working LLM backends.

## Recommendations

1. **For ZeroClaw**: The single-message mode is fundamentally limited for multi-step
   file operations. Consider:
   - Interactive mode with a script feeding responses
   - A dedicated "task runner" that handles file I/O around the agent
   - Model upgrade to one that supports multi-turn tool chaining

2. **For PicoClaw/OpenClaw**: Configure API authentication to enable testing:
   ```bash
   picoclaw auth login --provider openai --device-code
   openclaw agents add main  # then paste Anthropic API key
   ```

3. **For the Gym Framework**: The code-block extraction fallback partially works
   but session contamination degrades results. Future improvements:
   - Use separate zeroclaw memory databases per task
   - Parse agent stdout for verification when file_write fails
   - Add a "reasoning quality" metric separate from "file output" metric

## Methodology Notes

- Tasks were designed from first principles based on research into:
  - SWE-bench evaluation methodology
  - Real-world claw agent use cases (GitHub automation, code review, data processing)
  - Common coding agent capabilities (file I/O, shell commands, multi-step reasoning)
- Each task has automated verification via `verify.py` with specific pass/fail criteria
- Time limits range from 60-120s per task
- The gym framework supports all three claws with provider-specific workspace staging
