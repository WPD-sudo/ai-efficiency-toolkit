# ChatGPT Integration for WPD OS / Efficiency Toolkit

## Custom GPT Tools
Define these functions in your Custom GPT:

### optimize_and_route
{
  "name": "optimize_and_route",
  "description": "Classify task and recommend efficient model (heavy coding to Codex CLI, light/realtime to Grok). Compress context if needed.",
  "parameters": {
    "type": "object",
    "properties": {
      "task": {"type": "string", "description": "The task description"},
      "context": {"type": "string", "description": "Optional long context to compress"}
    },
    "required": ["task"]
  }
}

### filter_pr_noise
{
  "name": "filter_pr_noise",
  "description": "Filter noise in PR comments and decide routing for event-driven work.",
  "parameters": {
    "type": "object",
    "properties": {
      "comment": {"type": "string"}
    },
    "required": ["comment"]
  }
}

## System Prompt Snippet
"You have access to WPD Efficiency tools. Always call optimize_and_route before heavy tasks. Prefer Codex for complex coding to save Cursor budget. Use stable prefixes. New session per task."

## Deploy
Clone https://github.com/WPD-sudo/ai-efficiency-toolkit and run the kernel or MCP server locally, or paste the schemas into Custom GPT.
