from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Commit:
    hash: str
    parent: Optional[str]
    message: str
    branch: str
    timestamp: str
    snapshot_ref: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_json(cls, raw: str) -> Commit:
        data = json.loads(raw)
        return cls(**data)

    @classmethod
    def from_file(cls, path) -> Commit:
        from pathlib import Path
        return cls.from_json(Path(path).read_text(encoding="utf-8"))
