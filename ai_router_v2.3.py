#!/usr/bin/env python3
"""
AI Task Router v2.3 – Intelligent classification with history, skill injection, confidence, caching awareness.
Integrates with WPDKernel v2.3.
BASIS_ONLY · stdlib only.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, Optional

class TaskRouter:
    def __init__(self, kernel: Optional[Any] = None) -> None:
        if kernel is None:
            from wpd_os_kernel_v2_3 import WPDKernel
            self.kernel = WPDKernel()
        else:
            self.kernel = kernel

    def classify(self, task: str) -> Dict[str, Any]:
        tl = task.lower()
        top_skills = self.kernel.get_top_skills()
        injection = ", ".join(top_skills[:3]) if top_skills else "none"
        if any(w in tl for w in ["implement", "code", "refactor", "heavy", "complex", "kernel", "production", "codex"]):
            return {
                "category": "complex_coding",
                "recommended": "codex_cli",
                "reason": "Heavy software production to Codex",
                "compounding_hint": 5.0,
                "confidence": 0.94,
                "skill_injection": injection,
            }
        if any(w in tl for w in ["error", "fail", "exception", "bug", "pain", "traceback", "root cause"]):
            return {
                "category": "error_to_helper",
                "recommended": "Error-to-Helper Engine",
                "reason": "Immediate conversion to promotable skill + Pain-Asset",
                "compounding_hint": 5.5,
                "confidence": 0.96,
                "skill_injection": injection,
            }
        if any(w in tl for w in ["research", "latest", "realtime", "search", "news", "current"]):
            return {
                "category": "research",
                "recommended": "grok",
                "reason": "Realtime knowledge strength",
                "compounding_hint": 4.0,
                "confidence": 0.87,
                "skill_injection": injection,
            }
        if any(w in tl for w in ["review", "evidence", "q&e", "quality", "audit"]):
            return {
                "category": "review",
                "recommended": "CELL-QUALITY-EVIDENCE-01",
                "reason": "Independent verification path",
                "compounding_hint": 4.5,
                "confidence": 0.90,
                "skill_injection": injection,
            }
        if any(w in tl for w in ["metrics", "health", "compounding", "dashboard"]):
            return {
                "category": "metrics",
                "recommended": "Kernel Metrics Engine",
                "reason": "Persistent compounding measurement with trends",
                "compounding_hint": 4.3,
                "confidence": 0.92,
                "skill_injection": injection,
            }
        return {
            "category": "general",
            "recommended": "grok-fast",
            "reason": "Low cost / fast path",
            "compounding_hint": 3.5,
            "confidence": 0.70,
            "skill_injection": injection,
        }

    def route_with_history(self, task: str) -> Dict[str, Any]:
        classification = self.classify(task)
        self.kernel.metrics.setdefault("routing_history", []).append({
            "task": task[:160],
            "classification": classification,
            "ts": datetime.now(timezone.utc).isoformat(),
        })
        self.kernel._save("metrics.json", self.kernel.metrics)
        return classification

if __name__ == "__main__":
    import json
    import sys
    r = TaskRouter()
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Implement kernel reflection engine with receipts, caching and trends"
    print(json.dumps(r.route_with_history(task), indent=2))
