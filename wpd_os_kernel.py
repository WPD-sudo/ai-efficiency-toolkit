#!/usr/bin/env python3
"""
WPD OS Kernel - Unified efficiency + claim + event layer.
Replaces small parts. BASIS_ONLY safe. For Codex, ChatGPT, Cursor, Grok.
"""
import hashlib
import json
from datetime import datetime
from pathlib import Path

class WPDKernel:
    def __init__(self, state_dir="./wpd_os_state"):
        self.state = Path(state_dir)
        self.state.mkdir(exist_ok=True)
        self.claims = json.loads((self.state / "claims.json").read_text()) if (self.state / "claims.json").exists() else {}

    def _save(self):
        (self.state / "claims.json").write_text(json.dumps(self.claims, indent=2))

    def claim_key(self, original, input_hash, intent, role="KERNEL"):
        return f"{original}|{input_hash}|{intent}|{role}"

    def start_claim(self, key, holder, source):
        if key in self.claims and self.claims[key].get("state") in ("STARTED", "COMPLETED"):
            return {"status": "already_claimed", "existing": self.claims[key]}
        token = hashlib.sha256(f"{key}{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        claim = {"key": key, "holder": holder, "state": "STARTED", "source": source, "token": token, "started": datetime.now().isoformat()}
        self.claims[key] = claim
        self._save()
        return {"status": "claimed", "claim": claim}

    def process_event(self, event_type, payload, role="EFFICIENCY"):
        h = hashlib.sha256(payload.encode()).hexdigest()[:16]
        key = self.claim_key(f"EVENT:{event_type}", h, "PROCESS", role)
        res = self.start_claim(key, "WPD_OS_KERNEL", event_type)
        if res["status"] != "claimed":
            return res
        noise = any(w in payload.lower() for w in ["ack", "status", "waiting", "echo", "::skip"])
        if noise:
            self.claims[key].update({"state": "COMPLETED", "result": "skipped_noise", "disposition": "NO_ACTION"})
            self._save()
            return {"action": "skip", "reason": "noise", "claim": key}
        heavy = any(w in payload.lower() for w in ["implement", "code", "refactor", "heavy", "complex"])
        rec = "codex_cli" if heavy else "grok_or_cursor"
        self.claims[key].update({"state": "COMPLETED", "result": f"Routed to {rec}", "disposition": "ROUTED"})
        self._save()
        return {"action": "route", "recommended": rec, "claim": key, "tips": ["New session", "Stable prefix for cache"]}

if __name__ == "__main__":
    k = WPDKernel()
    print(json.dumps(k.process_event("pr_comment", "Implement unified OS kernel"), indent=2))
