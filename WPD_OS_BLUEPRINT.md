# WPD Unified OS Blueprint

Layered system replacing small parts:
- Control Plane: Owner Desk Lifecycle + PR20 Event Bus (unchanged)
- Efficiency Plane: This toolkit + wpd_os_kernel.py as MCP/CLI
- Bootstrap: Claim key + fresh Lifecycle read
- Identification: Existing claim system
- Communication: PR20 + MCP + team chat

Blockers (to resolve with Owner Desk): BASIS_ONLY Hold, claim fencing, no single runtime, Hausbuch access.

Deploy today: Kernel + ChatGPT schemas + Codex config ready.
