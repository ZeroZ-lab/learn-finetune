from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class ReplayLogger:
    def __init__(self, path: str = "runs/replay.jsonl"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event: Dict[str, Any]) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

