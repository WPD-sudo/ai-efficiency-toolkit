#!/usr/bin/env python3
"""
Error-to-Helper Engine v2.0 – Convert errors into promotable Helper Skills.

Self-improving library with automatic promotion tracking.
BASIS_ONLY · stdlib only.
"""

from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


class ErrorToHelper:
    def __init__(self, lib_dir: str = "./skills", kernel: Optional[Any] = None) -> None:
        self.lib = Path(lib_dir)
        self.lib.mkdir(exist_ok=True)
        if kernel is None:
            from wpd_os_kernel_v2 import WPDKernel  # type: ignore
            self.kernel = WPDKernel()
        else:
            self.kernel = kernel

    def convert(
        self,
        error_name: str,
        trigger: str,
        root_cause: str,
        evidence: str,
        prevention_prompt: str,
    ) -> dict:
        binding = hashlib.sha256(evidence.encode()).hexdigest()[:16]
        skill_md = f"""# Helper Skill: {error_name}

**Trigger:** {trigger}

**Root Cause:** {root_cause}

**Evidence:** {evidence}

**Prevention Prompt:**

{prevention_prompt}

**Usage Count:** 0
**Success Rate:** -
**Promotion Status:** CANDIDATE
**Source Binding:** {binding}
**Owner:** Error-to-Helper
**Last Updated:** {datetime.now().date().isoformat()}
"""
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in error_name)
        path = self.lib / f"{safe_name}.md"
        path.write_text(skill_md, encoding="utf-8")
        self.kernel.track_skill_usage(safe_name, success=True)
        return {"status": "created", "path": str(path), "promotion": "CANDIDATE", "binding": binding}

    def promote_if_ready(self, skill_name: str) -> dict:
        usage = self.kernel.skills.get(skill_name, {})
        rate = usage.get("successes", 0) / max(usage.get("usage", 1), 1)
        if usage.get("usage", 0) >= 3 and rate >= 0.8:
            usage["promoted"] = True
            self.kernel._save("skills_usage.json", self.kernel.skills)
            return {"status": "promoted", "skill": skill_name, "success_rate": round(rate, 2)}
        return {"status": "not_ready", "usage": usage.get("usage", 0), "rate": round(rate, 2)}


if __name__ == "__main__":
    e = ErrorToHelper()
    result = e.convert(
        error_name="PackagingHold",
        trigger="local storage duplicate / NaN BOM",
        root_cause="Missing pre-upload SHA256 verification",
        evidence="Issue #32 comment",
        prevention_prompt="Always verify digest before upload. Fail closed if mismatch.",
    )
    print(result)
