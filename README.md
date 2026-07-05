# TermBrain

**A privacy-first, AI-powered CLI diagnostic tool for Linux.**

TermBrain reads your system vitals and logs (Pacman, `journalctl`), then hands them to a **local** LLM via [Ollama](https://ollama.com) to explain what's going on and suggest fixes — no data ever leaves your machine.

Built with [Typer](https://typer.tiangolo.com/) for the CLI, [Rich](https://rich.readthedocs.io/) for terminal output, and [Ollama](https://github.com/ollama/ollama) for local inference.

---

## Why

Reading raw `journalctl` or `pacman.log` output is tedious, and pasting logs into a cloud chatbot means shipping potentially sensitive system data off-device. TermBrain closes that gap: it's a thin, dependency-light wrapper that formats your system state into a prompt, streams it through a local model, and renders the response as live-updating Markdown in your terminal.

## How it works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────┐
│  Typer CLI  │ ──▶ │ core/system  │ ──▶ │ core/llm.py │ ──▶ │  Ollama  │
│ (commands)  │     │ core/logs.py │     │ (prompting) │     │ (local)  │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────┘
       │                                        │
       ▼                                        ▼
  ui/display.py                     Streamed tokens → Rich Live + Markdown
```

1. A command (e.g. `doctor check`) gathers raw data — CPU load, memory, disk, or log lines — via `core/system.py` or `core/logs.py`.
2. That data is embedded into a task-specific prompt with a fixed system prompt ("You are TermBrain, a senior Linux systems engineer...").
3. `core/llm.py` streams the prompt to a local Ollama model (`llama3.2:3b` by default) and yields tokens as they arrive.
4. The command loop renders the growing response live using `rich.live.Live` + `rich.markdown.Markdown`, so the answer appears incrementally instead of all at once.

No network calls are made except to the local Ollama daemon (`localhost` by default).

## Project structure

```
termbrain/
├── setup.py                    # Package metadata, deps, console_scripts entry point
└── termbrain/
    ├── main.py                 # Typer app root; registers command groups
    ├── commands/
    │   ├── doctor.py            # `termbrain doctor check` — system health check
    │   └── diagnose.py          # `termbrain diagnose pacman|journal` — log analysis
    ├── core/
    │   ├── system.py            # Reads /proc/loadavg, `free -h`, `df -h`
    │   ├── logs.py               # Reads /var/log/pacman.log, `journalctl`
    │   └── llm.py                 # Builds prompts, streams responses from Ollama
    └── ui/
        └── display.py            # Welcome banner (Rich Panel)
```

## Requirements

- Linux (developed and tested on Manjaro/Arch — relies on `pacman.log`, `journalctl`, `/proc/loadavg`, `free`, `df`)
- Python 3.8+
- [Ollama](https://ollama.com) installed and running locally
- A pulled Ollama model (default: `llama3.2:3b` — small enough to run comfortably on CPU-only, 16GB RAM machines)

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/saivighnesh2190/termbrain.git
cd termbrain

# 2. Install in editable mode
pip install -e .

# 3. Make sure Ollama is running and has the default model
ollama pull llama3.2:3b
```

This registers the `termbrain` console script (see `entry_points` in `setup.py`), so it's available globally in your shell after install.

## Usage

### Welcome banner
```bash
termbrain welcome
```
Prints the TermBrain banner via `display_welcome()`.

### System health check
```bash
termbrain doctor check
```
Shows a Rich table with CPU load averages (1/5/15 min), memory used, and disk usage on `/`.

Add `--ai` to get a one-sentence AI-generated health summary based on those vitals:
```bash
termbrain doctor check --ai
```

### Diagnose Pacman logs
```bash
termbrain diagnose pacman
```
Reads the last 50 lines of `/var/log/pacman.log` and asks the model to summarize recent activity and flag failed transactions or errors.

### Diagnose system journal
```bash
termbrain diagnose journal
```
Reads the last 50 lines of `journalctl` output and asks the model to identify critical errors or service failures and explain how to fix them.

## Configuration

There's currently no config file — behavior is controlled by function defaults in code:

| Setting | Location | Default |
|---|---|---|
| Ollama model | `core/llm.py` → `stream_diagnostic(model=...)` | `llama3.2:3b` |
| Log line count | `core/logs.py` → `lines` param | `50` |

To use a different model, either edit the default in `core/llm.py` or (if you're extending the CLI) expose it as a `--model` Typer option.

## Error handling

- Missing `/var/log/pacman.log` → `diagnose pacman` prints an error and exits without calling the LLM.
- Ollama unreachable or errors mid-stream → `stream_diagnostic` yields an inline error message rather than raising, so the Rich `Live` block fails gracefully instead of crashing the CLI.

## Extending TermBrain

The architecture is intentionally thin, which makes it easy to add a new diagnostic:

1. Add a data-gathering function to `core/system.py` or `core/logs.py`.
2. Add a new `@app.command()` in `commands/` (or a new file + register it in `main.py` via `app.add_typer`).
3. Build a prompt string embedding that data and pass it to `stream_diagnostic()`.
4. Reuse the existing `Live` + `Markdown` streaming pattern for consistent output.

Ideas: memory-hog process diagnosis (`ps aux`), Docker container health, `dmesg` analysis, network diagnostics (`ip`, `ss`).

## Development

```bash
pip install -e .
termbrain --help
```

Since it's installed in editable mode, code changes take effect immediately without reinstalling.
