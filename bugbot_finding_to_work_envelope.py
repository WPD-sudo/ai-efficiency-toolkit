#!/usr/bin/env python3
"""
Bugbot Finding → Work Envelope Draft (Transition Helper)

Narrowly scoped: accepts a Bugbot finding, deduplicates, computes a stable hash,
and produces a draft work-envelope text suitable for pasting into wpd-control.

Does NOT:
- write directly to wpd-control
- merge anything
- grant approval
- mark anything as PASS

Bugbot is only a hint source. Recurring patterns should become internal checkers.
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path

class BugbotFindingHandler:
    def __init__(self, state_dir="./bugbot_transition_state"):
        self.state = Path(state_dir)
        self.state.mkdir(exist_ok=True)
        self.seen = json.loads((self.state / "seen.json").read_text()) if (self.state / "seen.json").exists() else {}

    def _save(self):
        (self.state / "seen.json").write_text(json.dumps(self.seen, indent=2))

    def finding_hash(self, repo: str, file: str, line: int, text: str) -> str:
        payload = f"{repo}|{file}|{line}|{text.strip()}"
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    def process(self, repo: str, commit: str, file: str, line: int, finding_text: str, suggested_check: str = "") -> dict:
        h = self.finding_hash(repo, file, line, finding_text)
        if h in self.seen:
            return {"status": "duplicate", "hash": h, "existing": self.seen[h]}

        envelope = f"""# Work Envelope Draft – Bugbot Finding {h}

WPD_ROLE=CELL-QUALITY-EVIDENCE-01

## Source
- Repo: {repo}
- Commit: {commit}
- File: {file}:{line}
- Finding hash: {h}
- Timestamp: {datetime.now().isoformat()}

## Finding
{finding_text}

## Suggested internal check / component
{suggested_check or "(to be defined by producer)"}

## Status
OPEN

## Notes
- Bugbot is only a hint source. This is not a PASS.
- Producer implements the fix + a reproducible check.
- Q&E performs independent recheck before VERIFIED.
- Recurring patterns should become a permanent internal checker.
"""

        self.seen[h] = {
            "repo": repo,
            "file": file,
            "line": line,
            "hash": h,
            "created": datetime.now().isoformat(),
            "status": "drafted"
        }
        self._save()

        return {
            "status": "drafted",
            "hash": h,
            "envelope": envelope
        }

if __name__ == "__main__":
    h = BugbotFindingHandler()
    result = h.process(
        repo="WPD-sudo/wpd-platform",
        commit="abc123",
        file="apps/kurswerkstatt/app/api/assets/[id]/route.ts",
        line=42,
        finding_text="SHA-256 check happens after R2 put, not before.",
        suggested_check="Add a pre-upload digest verification middleware or unit test that fails if digest !== id."
    )
    print(json.dumps({k: v for k, v in result.items() if k != "envelope"}, indent=2))
    print("\n--- ENVELOPE ---\n")
    print(result.get("envelope", ""))
