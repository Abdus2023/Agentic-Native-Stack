"""Append-only, hash-chained JSONL event journal."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any

JOURNAL_VERSION = "ouroboros.journal.v1"
GENESIS = "0" * 64


class JournalIntegrityError(RuntimeError):
    """Raised when durable journal history cannot be trusted."""


def _canonical(record: dict[str, Any]) -> bytes:
    return json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _digest(record: dict[str, Any]) -> str:
    unsigned = {key: value for key, value in record.items() if key != "digest"}
    return sha256(_canonical(unsigned)).hexdigest()


class Journal:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: Any, **payload: Any) -> dict[str, Any]:
        if is_dataclass(event):
            record = asdict(event)
            record["event"] = record.pop("kind")
            record.update(payload)
        else:
            record = {"event": str(event), **payload}
        previous = self._last_digest()
        record = {
            "version": JOURNAL_VERSION,
            "sequence": self._next_sequence(),
            "previous_digest": previous,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **record,
        }
        record["digest"] = _digest(record)
        line = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
            handle.flush()
        return record

    def read(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        records: list[dict[str, Any]] = []
        with self.path.open(encoding="utf-8") as handle:
            for number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise JournalIntegrityError(f"invalid JSON at journal line {number}") from exc
                if not isinstance(record, dict):
                    raise JournalIntegrityError(f"journal line {number} is not an object")
                records.append(record)
        self.validate(records)
        return records

    @staticmethod
    def validate(records: list[dict[str, Any]]) -> None:
        previous = GENESIS
        expected_sequence = 1
        for index, record in enumerate(records, 1):
            if record.get("version") != JOURNAL_VERSION:
                raise JournalIntegrityError(f"unsupported journal version at record {index}")
            if record.get("sequence") != expected_sequence:
                raise JournalIntegrityError(f"invalid sequence at record {index}")
            if record.get("previous_digest") != previous:
                raise JournalIntegrityError(f"broken journal chain at record {index}")
            digest = record.get("digest")
            if not isinstance(digest, str) or digest != _digest(record):
                raise JournalIntegrityError(f"invalid journal digest at record {index}")
            previous = digest
            expected_sequence += 1

    def _last_digest(self) -> str:
        records = self.read() if self.path.exists() else []
        return records[-1]["digest"] if records else GENESIS

    def _next_sequence(self) -> int:
        records = self.read() if self.path.exists() else []
        return records[-1]["sequence"] + 1 if records else 1
