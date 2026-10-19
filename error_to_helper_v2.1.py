#!/usr/bin/env python3
"""
Error-to-Helper Engine v2.1 – Convert errors into promotable Helper Skills + Pain-Assets.
Self-improving with demotion, usage tracking, automatic promotion log.
BASIS_ONLY · stdlib only.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


class ErrorToHelper:
    def __init__(self, lib_dir: str = "./skills", kernel: Optional[Any] = None) -> None:
        self.lib = Path(lib_dir)
        self.lib.mkdir(exist_ok=True)
        if kernel is None:
            from wpd_os_kernel_v2_1 import WPDKernel
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
**Last Updated:** {datetime.now(timezone.utc).date().isoformat()}
"""
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in error_name)
        path = self.lib / f"{safe_name}.md"
        path.write_text(skill_md, encoding="utf-8")
        track = self.kernel.track_skill_usage(safe_name, success=True)
        # Create linked Pain-Asset reference
        self.kernel._create_pain_asset(error_name, evidence)
        return {
            "status": "created",
            "path": str(path),
            "promotion": "CANDIDATE",
            "binding": binding,
            "track": track,
            "pain_created": True,
        }

    def promote_if_ready(self, skill_name: str) -> dict:
        usage = self.kernel.skills.get(skill_name, {})
        rate = usage.get("successes", 0) / max(usage.get("usage", 1), 1)
        if usage.get("usage", 0) >= 3 and rate >= 0.8:
            usage["promoted"] = True
            usage["demoted"] = False
            self.kernel._save("skills_usage.json", self.kernel.skills)
            # Log promotion as asset
            self.kernel.sync_living_index(f"PROMO-{skill_name}", 5.0)
            return {"status": "promoted", "skill": skill_name, "success_rate": round(rate, 2)}
        return {"status": "not_ready", "usage": usage.get("usage", 0), "rate": round(rate, 2)}


if __name__ == "__main__":
    e = ErrorToHelper()
    result = e.convert(
        error_name="PackagingHold",
        trigger="local storage duplicate / NaN BOM / missing SHA",
        root_cause="Missing pre-upload SHA256 verification and fail-closed check",
        evidence="Issue #32 comment / Drive binding",
        prevention_prompt="Always verify digest before upload. Fail closed if mismatch. Bind SHA256 in EVENT_WORK_ENVELOPE.",
    )
    print(result)
