#!/usr/bin/env python3
"""Event-driven orchestrator for PR noise filter and routing."""
import re
import json

class PREventProcessor:
    NOISE = [r"ack", r"status", r"waiting", r"echo", r"::SKIP"]
    def is_noise(self, body: str) -> bool:
        return any(re.search(p, body.lower()) for p in self.NOISE) or len(body) < 40
    def process(self, body: str) -> dict:
        if self.is_noise(body):
            return {"action": "skip", "reason": "noise"}
        if any(w in body.lower() for w in ["implement", "code", "heavy"]):
            return {"action": "route_codex", "reason": "heavy_to_codex_save_cursor"}
        return {"action": "route_grok_or_cursor", "reason": "light"}

if __name__ == "__main__":
    proc = PREventProcessor()
    print(json.dumps(proc.process("Implement efficient router"), indent=2))
