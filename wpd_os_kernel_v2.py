#!/usr/bin/env python3
"""
WPD OS Kernel v2.0 – Claim, Event, Reflection, Compounding, Metrics Persistence,
Living Index Sync, Skill Tracking & Auto-Promotion.

BASIS_ONLY · Fail-closed · stdlib only (Python 3.10+)
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class WPDKernel:
    def __init__(self, state_dir: str = "./wpd_os_state") -> None:
        self.state = Path(state_dir)
        self.state.mkdir(exist_ok=True)
        self.claims: Dict[str, Any] = self._load("claims.json")
        self.metrics: Dict[str, Any] = self._load("metrics.json")
        self.reflections: Dict[str, Any] = self._load("reflections.json")
        self.skills: Dict[str, Any] = self._load("skills_usage.json")
        self.living_index_log: Dict[str, Any] = self._load("living_index_sync.json")

    def _load(self, name: str) -> dict:
        p = self.state / name
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                return {}
        return {}

    def _save(self, name: str, data: dict) -> None:
        (self.state / name).write_text(
            json.dumps(data, indent=2, default=str, ensure_ascii=False),
            encoding="utf-8",
        )

    def claim_key(self, original: str, input_hash: str, intent: str, role: str = "KERNEL") -> str:
        return f"{original}|{input_hash}|{intent}|{role}"

    def start_claim(self, key: str, holder: str, source: str) -> dict:
        if key in self.claims and self.claims[key].get("state") in ("STARTED", "COMPLETED"):
            return {"status": "already_claimed", "existing": self.claims[key]}
        token = hashlib.sha256(f"{key}{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        binding = hashlib.sha256(source.encode()).hexdigest()[:16]
        claim = {
            "key": key,
            "holder": holder,
            "state": "STARTED",
            "source": source,
            "token": token,
            "started": datetime.now().isoformat(),
            "binding": binding,
        }
        self.claims[key] = claim
        self._save("claims.json", self.claims)
        return {"status": "claimed", "claim": claim}

    def process_event(self, event_type: str, payload: str, role: str = "EFFICIENCY") -> dict:
        h = hashlib.sha256(payload.encode()).hexdigest()[:16]
        key = self.claim_key(f"EVENT:{event_type}", h, "PROCESS", role)
        res = self.start_claim(key, "WPD_OS_KERNEL", event_type)
        if res["status"] != "claimed":
            return res

        noise_words = ["ack", "status", "waiting", "echo", "::skip"]
        if any(w in payload.lower() for w in noise_words) or len(payload.strip()) < 20:
            self.claims[key].update({
                "state": "COMPLETED",
                "result": "skipped_noise",
                "disposition": "NO_ACTION",
            })
            self._save("claims.json", self.claims)
            return {"action": "skip", "reason": "noise", "claim": key}

        heavy_words = ["implement", "code", "refactor", "heavy", "complex", "kernel", "production"]
        rec = "codex_cli" if any(w in payload.lower() for w in heavy_words) else "grok_or_cursor"
        self.claims[key].update({
            "state": "COMPLETED",
            "result": f"Routed to {rec}",
            "disposition": "ROUTED",
        })
        self._save("claims.json", self.claims)
        return {
            "action": "route",
            "recommended": rec,
            "claim": key,
            "tips": ["New session", "Stable prefix for cache", "Use EVENT_WORK_ENVELOPE"],
        }

    def generate_reflection(
        self,
        ewe_id: str,
        outcomes: List[str],
        errors: List[str],
        skills_used: List[str],
        hours: float = 1.0,
    ) -> dict:
        score = self.calculate_compounding(len(outcomes), len(skills_used), hours)
        reflection = {
            "source_binding": hashlib.sha256(ewe_id.encode()).hexdigest()[:16],
            "lauf": ewe_id,
            "was_funktioniert": outcomes,
            "was_nicht": errors,
            "skill_kandidaten": [f"helper_{e}" for e in errors[:3]],
            "compounding_score": score,
            "naechste_aktion": "Promote skill if usage >= 3 and success >= 80% else log",
            "timestamp": datetime.now().isoformat(),
        }
        self.reflections[ewe_id] = reflection
        self._save("reflections.json", self.reflections)

        self.metrics.setdefault("scores", []).append({
            "score": score,
            "ts": datetime.now().isoformat(),
            "ewe": ewe_id,
        })
        self._save("metrics.json", self.metrics)
        self.sync_living_index(ewe_id, score)
        return reflection

    def calculate_compounding(self, assets_created: int, skills_reused: int, hours: float) -> float:
        return round((assets_created + skills_reused) / max(hours, 0.1), 2)

    def track_skill_usage(self, skill_name: str, success: bool) -> None:
        entry = self.skills.setdefault(skill_name, {"usage": 0, "successes": 0, "promoted": False})
        entry["usage"] += 1
        if success:
            entry["successes"] += 1
        if (
            entry["usage"] >= 3
            and entry["successes"] / entry["usage"] >= 0.8
            and not entry["promoted"]
        ):
            entry["promoted"] = True
        self._save("skills_usage.json", self.skills)

    def sync_living_index(self, asset_id: str, score: float) -> None:
        entry = {
            "asset": asset_id,
            "score": score,
            "ts": datetime.now().isoformat(),
            "status": "synced",
        }
        self.living_index_log.setdefault("syncs", []).append(entry)
        self._save("living_index_sync.json", self.living_index_log)

    def get_health_summary(self) -> dict:
        scores = [s["score"] for s in self.metrics.get("scores", [])]
        avg = round(sum(scores) / len(scores), 2) if scores else 0.0
        return {
            "total_claims": len(self.claims),
            "avg_compounding": avg,
            "promoted_skills": sum(1 for s in self.skills.values() if s.get("promoted")),
            "reflections": len(self.reflections),
            "living_index_syncs": len(self.living_index_log.get("syncs", [])),
        }


if __name__ == "__main__":
    k = WPDKernel()
    print(json.dumps(k.process_event("pr_comment", "Implement unified OS kernel v2.0 with compounding"), indent=2))
    print(json.dumps(k.get_health_summary(), indent=2))
