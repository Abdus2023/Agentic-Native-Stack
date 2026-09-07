"""Append-only, hash-chained JSONL event journal."""

from __future__ import annotations

import json
import os
from contextlib import contextmanager
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterator, TYPE_CHECKING

if TYPE_CHECKING:
    from .trust import JournalTrustAnchor

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows has no fcntl.
    fcntl = None

JOURNAL_VERSION = "ouroboros.journal.v1"
GENESIS = "0" * 64


class JournalIntegrityError(RuntimeError):
    """Raised when durable journal history cannot be trusted."""


class JournalLockError(RuntimeError):
    """Raised when the journal cannot establish its append lock."""


def _canonical(record: dict[str, Any]) -> bytes:
    return json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _digest(record: dict[str, Any]) -> str:
    unsigned = {key: value for key, value in record.items() if key != "digest"}
    return sha256(_canonical(unsigned)).hexdigest()


class Journal:
    """Hash-chained journal with serialized POSIX appends and stable-storage flushes."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def _append_lock(self, handle) -> Iterator[None]:
        if fcntl is None:
            raise JournalLockError("journal append locking is unavailable on this platform")
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        except OSError as exc:
            raise JournalLockError("unable to acquire journal append lock") from exc
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def append(self, event: Any, **payload: Any) -> dict[str, Any]:
        if is_dataclass(event):
            record = asdict(event)
            record["event"] = record.pop("kind")
            record.update(payload)
        else:
            record = {"event": str(event), **payload}

        with self.path.open("a+", encoding="utf-8") as handle:
            with self._append_lock(handle):
                handle.seek(0)
                records = self._read_handle(handle)
                previous = records[-1]["digest"] if records else GENESIS
                sequence = records[-1]["sequence"] + 1 if records else 1
                record = {
                    "version": JOURNAL_VERSION,
                    "sequence": sequence,
                    "previous_digest": previous,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    **record,
                }
                record["digest"] = _digest(record)
                line = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
                handle.seek(0, os.SEEK_END)
                handle.write(line + "\n")
                handle.flush()
                os.fsync(handle.fileno())
        return record

    def read(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        with self.path.open(encoding="utf-8") as handle:
            records = self._read_handle(handle)
        self.validate(records)
        return records

    def read_trusted(self, anchor: "JournalTrustAnchor") -> list[dict[str, Any]]:
        """Read only after ordinary integrity and an external checkpoint both pass."""
        records = self.read()
        from .trust import verify_trust_anchor

        verify_trust_anchor(records, anchor)
        return records

    @staticmethod
    def _read_handle(handle) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        handle.seek(0)
        for number, line in enumerate(handle, 1):
            if not line.strip():
                raise JournalIntegrityError(f"blank journal record at line {number}")
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise JournalIntegrityError(f"invalid JSON at journal line {number}") from exc
            if not isinstance(record, dict):
                raise JournalIntegrityError(f"journal line {number} is not an object")
            records.append(record)
        Journal.validate(records)
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
