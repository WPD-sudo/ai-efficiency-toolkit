# AGENTS.md
## Commands
- Test: `python -m pytest`
- Lint: `ruff check .`
## Efficiency Rules
- Prefer Codex CLI for heavy coding to save Cursor budget.
- New session per task.
- Filter noise before routing.
- Use stable prefixes for caching.
