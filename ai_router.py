#!/usr/bin/env python3
"""Simple AI Task Router for efficient multi-model use."""
import argparse
import json
from typing import Dict

class TaskRouter:
    def classify(self, task: str) -> Dict:
        task_lower = task.lower()
        if any(w in task_lower for w in ["implement", "code", "refactor", "heavy", "complex"]):
            return {"category": "complex_coding", "recommended": "codex_cli or grok-4.7", "reason": "Save Cursor budget by routing heavy work to Codex"}
        elif any(w in task_lower for w in ["research", "latest", "realtime"]):
            return {"category": "research", "recommended": "grok", "reason": "Realtime strength"}
        else:
            return {"category": "general", "recommended": "grok-fast or composer", "reason": "Low cost"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task")
    args = parser.parse_args()
    print(json.dumps(TaskRouter().classify(args.task), indent=2))

if __name__ == "__main__":
    main()
