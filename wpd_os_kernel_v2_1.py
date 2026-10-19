#!/usr/bin/env python3
"""
WPD OS Kernel v2.1 – Hardened Claim, Event, Reflection, Compounding, Metrics,
Living Index Sync, Skill Tracking, Auto-Promotion/Demotion, Receipt Generation.

BASIS_ONLY · Fail-closed · Source-first · stdlib only (Python 3.10+)
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
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
        self.receipts: Dict[str, Any] = self._load("receipts.json")
        self.pains: Dict[str, Any] = self._load("pains.json")

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

    def _sha256(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def claim_key(self, original: str, input_hash: str, intent: str, role: str = "KERNEL") -> str:
        return f"{original}|{input_hash}|{intent}|{role}"

    def start_claim(self, key: str, holder: str, source: str, envelope: Optional[dict] = None) -> dict:
        if key in self.claims and self.claims[key].get("state") in ("STARTED", "COMPLETED"):
            return {"status": "already_claimed", "existing": self.claims[key]}
        token = self._sha256(f"{key}{datetime.now(timezone.utc).isoformat()}")[:16]
        binding = self._sha256(source)[:16]
        claim = {
            "key": key,
            "holder": holder,
            "state": "STARTED",
            "source": source,
            "token": token,
            "started": datetime.now(timezone.utc).isoformat(),
            "binding": binding,
            "envelope": envelope or {},
        }
        self.claims[key] = claim
        self._save("claims.json", self.claims)
        return {"status": "claimed", "claim": claim}

    def process_event(self, event_type: str, payload: str, role: str = "EFFICIENCY", envelope: Optional[dict] = None) -> dict:
        h = self._sha256(payload)[:16]
        key = self.claim_key(f"EVENT:{event_type}", h, "PROCESS", role)
        res = self.start_claim(key, "WPD_OS_KERNEL", event_type, envelope)
        if res["status"] != "claimed":
            return res

        # Fail-closed noise filter
        noise_patterns = [r"\back\b", r"status", r"waiting", r"echo", r"::skip", r"noop"]
        if any(re.search(p, payload.lower()) for p in noise_patterns) or len(payload.strip()) < 15:
            self._complete_claim(key, "skipped_noise", "NO_ACTION")
            return {"action": "skip", "reason": "noise", "claim": key, "receipt": self._issue_receipt(key, "SKIPPED")}

        # Routing decision
        heavy = any(w in payload.lower() for w in ["implement", "code", "refactor", "kernel", "production", "codex"])
        errorish = any(w in payload.lower() for w in ["error", "fail", "exception", "bug", "pain", "traceback"])
        if errorish:
            rec = "error_to_helper"
        elif heavy:
            rec = "codex_cli"
        else:
            rec = "grok_or_cursor"

        self._complete_claim(key, f"Routed to {rec}", "ROUTED")
        receipt = self._issue_receipt(key, "ROUTED", {"recommended": rec})
        return {
            "action": "route",
            "recommended": rec,
            "claim": key,
            "receipt": receipt,
            "tips": ["Use full EVENT_WORK_ENVELOPE", "Bind SHA256", "Generate reflection on major runs"],
        }

    def _complete_claim(self, key: str, result: str, disposition: str) -> None:
        if key in self.claims:
            self.claims[key].update({
                "state": "COMPLETED",
                "result": result,
                "disposition": disposition,
                "completed": datetime.now(timezone.utc).isoformat(),
            })
            self._save("claims.json", self.claims)

    def _issue_receipt(self, key: str, status: str, extra: Optional[dict] = None) -> dict:
        receipt_id = f"RCPT-{self._sha256(key + status)[:12]}"
        receipt = {
            "id": receipt_id,
            "claim_key": key,
            "status": status,
            "ts": datetime.now(timezone.utc).isoformat(),
            "binding": self.claims.get(key, {}).get("binding", ""),
            **(extra or {}),
        }
        self.receipts[receipt_id] = receipt
        self._save("receipts.json", self.receipts)
        return receipt

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
            "source_binding": self._sha256(ewe_id)[:16],
            "lauf": ewe_id,
            "was_funktioniert": outcomes,
            "was_nicht": errors,
            "skill_kandidaten": [f"helper_{e.replace(' ', '_')}" for e in errors[:3]],
            "compounding_score": score,
            "naechste_aktion": "Promote skills with usage>=3 and success>=80%; demote if <40%",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.reflections[ewe_id] = reflection
        self._save("reflections.json", self.reflections)

        self.metrics.setdefault("scores", []).append({
            "score": score,
            "ts": datetime.now(timezone.utc).isoformat(),
            "ewe": ewe_id,
        })
        self._save("metrics.json", self.metrics)
        self.sync_living_index(ewe_id, score)
        # Auto pain assets for errors
        for err in errors:
            self._create_pain_asset(err, ewe_id)
        return reflection

    def calculate_compounding(self, assets_created: int, skills_reused: int, hours: float) -> float:
        return round((assets_created + skills_reused) / max(hours, 0.1), 2)

    def track_skill_usage(self, skill_name: str, success: bool) -> dict:
        entry = self.skills.setdefault(skill_name, {"usage": 0, "successes": 0, "promoted": False, "demoted": False})
        entry["usage"] += 1
        if success:
            entry["successes"] += 1
        rate = entry["successes"] / entry["usage"]
        if entry["usage"] >= 3 and rate >= 0.8 and not entry["promoted"]:
            entry["promoted"] = True
            entry["demoted"] = False
        elif entry["usage"] >= 5 and rate < 0.4 and not entry["demoted"]:
            entry["demoted"] = True
            entry["promoted"] = False
        self._save("skills_usage.json", self.skills)
        return {"skill": skill_name, "usage": entry["usage"], "rate": round(rate, 2), "promoted": entry["promoted"]}

    def sync_living_index(self, asset_id: str, score: float) -> None:
        entry = {
            "asset": asset_id,
            "score": score,
            "ts": datetime.now(timezone.utc).isoformat(),
            "status": "synced",
        }
        self.living_index_log.setdefault("syncs", []).append(entry)
        self._save("living_index_sync.json", self.living_index_log)

    def _create_pain_asset(self, error_name: str, source: str) -> None:
        pain_id = f"PAIN-{self._sha256(error_name + source)[:10]}"
        self.pains[pain_id] = {
            "id": pain_id,
            "error": error_name,
            "source": source,
            "status": "OPEN",
            "created": datetime.now(timezone.utc).isoformat(),
            "conversion_target": "Helper Skill within 24h",
        }
        self._save("pains.json", self.pains)

    def get_health_summary(self) -> dict:
        scores = [s["score"] for s in self.metrics.get("scores", [])]
        avg = round(sum(scores) / len(scores), 2) if scores else 0.0
        return {
            "total_claims": len(self.claims),
            "avg_compounding": avg,
            "promoted_skills": sum(1 for s in self.skills.values() if s.get("promoted")),
            "demoted_skills": sum(1 for s in self.skills.values() if s.get("demoted")),
            "reflections": len(self.reflections),
            "open_pains": sum(1 for p in self.pains.values() if p.get("status") == "OPEN"),
            "receipts_issued": len(self.receipts),
            "living_index_syncs": len(self.living_index_log.get("syncs", [])),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def validate_envelope(self, envelope: dict) -> dict:
        required = ["id", "source_binding", "task_type", "input", "expected_output", "success_criteria"]
        missing = [f for f in required if f not in envelope]
        if missing:
            return {"valid": False, "missing": missing, "fail_closed": True}
        return {"valid": True, "binding": self._sha256(json.dumps(envelope, sort_keys=True))[:16]}


if __name__ == "__main__":
    k = WPDKernel()
    print(json.dumps(k.process_event("pr_comment", "Implement unified OS kernel v2.1 with self-improving compounding and receipts"), indent=2))
    print(json.dumps(k.get_health_summary(), indent=2))
