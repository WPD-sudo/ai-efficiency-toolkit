# Deploy Guide for Codex and ChatGPT

## For Codex CLI
1. Clone: `git clone https://github.com/WPD-sudo/ai-efficiency-toolkit.git`
2. Add as MCP in `~/.codex/config.toml` or use the router as pre-step.
3. Heavy tasks: Run `python ai_router.py "task"` first – it recommends routing heavy work to Codex itself or Grok.

## For ChatGPT
- Use Custom GPT with function calling pointing to a local OpenAI-compatible endpoint (see LiteLLM example).
- Or clone and run the event_orchestrator / router locally and paste optimized prompts.

## Simultaneous vs Separate
- MCP server (stdio) can be shared if run locally.
- Otherwise each agent clones and deploys its own instance.

This ensures capabilities are available even if not deployed for all at once.
