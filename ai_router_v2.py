#!/usr/bin/env python3
"""
AI Task Router v2.0 – Intelligent classification with history persistence.

Integrates with WPDKernel for routing history and compounding hints.
BASIS_ONLY · stdlib only.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional


class TaskRouter:
    def __init__(self, kernel: Optional[Any] = None) -> None:
        # Late import to avoid circular dependency when used standalone
        if kernel is None:
            from wpd_os_kernel_v2 import WPDKernel  # type: ignore
            self.kernel = WPDKernel()
        else:
            self.kernel = kernel

    def classify(self, task: str) -> Dict[str, Any]:
        tl = task.lower()
        if any(w in tl for w in ["implement", "code", "refactor", "heavy", "complex", "kernel", "production"]):
            return {
                "category": "complex_coding",
                "recommended": "codex_cli",
                "reason": "Heavy work to Codex for budget + quality",
                "compounding_hint": 4.5,
            }
        if any(w in tl for w in ["research", "latest", "realtime", "search", "news"]):
            return {
                "category": "research",
                "recommended": "grok",
                "reason": "Realtime strength",
                "compounding_hint": 3.5,
            }
        if any(w in tl for w in ["error", "fail", "exception", "bug", "pain", "traceback"]):
            return {
                "category": "error_to_helper",
                "recommended": "Error-to-Helper Engine",
                "reason": "Immediate skill conversion",
                "compounding_hint": 5.0,
            }
        if any(w in tl for w in ["review", "evidence", "q&e", "quality"]):
            return {
                "category": "review",
                "recommended": "CELL-QUALITY-EVIDENCE-01",
                "reason": "Independent verification",
                "compounding_hint": 4.0,
            }
        return {
            "category": "general",
            "recommended": "grok-fast",
            "reason": "Low cost / fast path",
            "compounding_hint": 3.0,
        }

    def route_with_history(self, task: str) -> Dict[str, Any]:
        classification = self.classify(task)
        self.kernel.metrics.setdefault("routing_history", []).append({
            "task": task[:120],
            "classification": classification,
            "ts": datetime.now().isoformat(),
        })
        self.kernel._save("metrics.json", self.kernel.metrics)
        return classification


if __name__ == "__main__":
    import json
    import sys
    r = TaskRouter()
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Implement kernel reflection engine"
    print(json.dumps(r.route_with_history(task), indent=2))
