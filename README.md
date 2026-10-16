# AI Efficiency Toolkit / WPD OS Kernel

Unified efficiency layer for Grok, Cursor, Codex, and ChatGPT. Replaces small parts with a claim-aware, event-driven kernel.

## Deployed Today
- `wpd_os_kernel.py`: Claim + Event Processing + Routing (heavy → Codex CLI)
- ChatGPT integration: `docs/chatgpt_integration.md` (tool schemas + system prompt)
- Codex config example: `docs/codex_config_example.toml`
- Blueprint: `WPD_OS_BLUEPRINT.md`

## Quick Start
```bash
git clone https://github.com/WPD-sudo/ai-efficiency-toolkit.git
cd ai-efficiency-toolkit
python wpd_os_kernel.py
```

See docs/ for Codex and ChatGPT specific setup. MCP server available for native tool use.

Aligned with Owner Desk (BASIS_ONLY compatible, claim fencing respected).
