# AI Efficiency Toolkit

Event-driven toolkit to reduce compute load and maximize effectiveness of Grok, Cursor, Codex, and ChatGPT.

## Features
- Task Router: Classifies tasks and recommends efficient models (prefer Grok or Codex CLI for heavy work to save Cursor budget).
- Context Optimizer: Compresses history, strips fillers, caches responses.
- Event-Driven Orchestrator: Processes PR comments / file events, filters noise, routes, logs claims.
- MCP Server: Native tools for Cursor, Codex, ChatGPT, Grok.
- Templates: AGENTS.md and Cursor rules for token efficiency.

## Deploy for Codex / ChatGPT
1. Clone this repo.
2. For Codex: Use as MCP or run the CLI router before heavy tasks.
3. For ChatGPT: Use custom GPTs with the tool definitions or local proxy (see LiteLLM config).
4. For simultaneous use: Run the MCP server (stdio) and connect multiple clients.

## Quick Start
```bash
git clone https://github.com/WPD-sudo/ai-efficiency-toolkit.git
cd ai-efficiency-toolkit
python -m pip install -r requirements.txt
python ai_router.py "Implement a cache layer"
```

See `docs/` for detailed deploy guides per agent.
