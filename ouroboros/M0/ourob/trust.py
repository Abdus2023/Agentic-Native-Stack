"""External trust anchors for journal authenticity.

A journal hash chain proves consistency only relative to its genesis. A trusted
checkpoint pins a prefix to an authority outside the mutable journal. The
runtime never creates or replaces that anchor during recovery.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from typing import Any, Mapping

from .journal import GENESIS, JOURNAL_VERSION, JournalIntegrityError

TRUST_ANCHOR_VERSION = "ouroboros.journal-trust-anchor.v1"


@dataclass(frozen=True)
class JournalTrustAnchor:
    """A pre-provisioned checkpoint whose authority is external to the journal."""

    sequence: int
    digest: str
    generation: str = ""
    version: str = TRUST_ANCHOR_VERSION

    def __post_init__(self) -> None:
        if self.version != TRUST_ANCHOR_VERSION:
            raise ValueError("unsupported trust-anchor version")
        if self.sequence < 1:
            raise ValueError("trust-anchor sequence must be positive")
        if len(self.digest) != 64 or any(c not in "0123456789abcdef" for c in self.digest):
            raise ValueError("trust-anchor digest must be a lowercase SHA-256 digest")
        if not isinstance(self.generation, str):
            raise ValueError("trust-anchor generation must be a string")

    def to_record(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "sequence": self.sequence,
            "digest": self.digest,
            "generation": self.generation,
        }

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "JournalTrustAnchor":
        if not isinstance(record, Mapping):
            raise ValueError("invalid trust-anchor record")
        return cls(
            sequence=record.get("sequence", 0),
            digest=record.get("digest", ""),
            generation=record.get("generation", ""),
            version=record.get("version", ""),
        )

    @property
    def record_binding(self) -> str:
        """Stable identifier for the externally supplied checkpoint."""
        payload = f"{self.version}\0{self.sequence}\0{self.digest}\0{self.generation}".encode("utf-8")
        return sha256(payload).hexdigest()


def verify_trust_anchor(records: list[dict[str, Any]], anchor: JournalTrustAnchor) -> None:
    """Verify that the journal contains the exact externally trusted prefix."""
    if not records:
        raise JournalIntegrityError("trusted journal is empty")
    if anchor.sequence > len(records):
        raise JournalIntegrityError("journal is shorter than trusted checkpoint")

    checkpoint = records[anchor.sequence - 1]
    if checkpoint.get("sequence") != anchor.sequence:
        raise JournalIntegrityError("trusted checkpoint sequence mismatch")
    if checkpoint.get("digest") != anchor.digest:
        raise JournalIntegrityError("trusted checkpoint digest mismatch")

    previous = GENESIS
    for index, record in enumerate(records[: anchor.sequence], 1):
        if record.get("version") != JOURNAL_VERSION:
            raise JournalIntegrityError(f"unsupported journal version at record {index}")
        if record.get("sequence") != index:
            raise JournalIntegrityError(f"invalid sequence at record {index}")
        if record.get("previous_digest") != previous:
            raise JournalIntegrityError(f"broken trusted journal chain at record {index}")
        digest = record.get("digest")
        if not isinstance(digest, str):
            raise JournalIntegrityError(f"invalid trusted journal digest at record {index}")
        unsigned = {key: value for key, value in record.items() if key != "digest"}
        canonical = json.dumps(unsigned, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        if digest != sha256(canonical).hexdigest():
            raise JournalIntegrityError(f"invalid trusted journal digest at record {index}")
        previous = digest

    if anchor.generation and checkpoint.get("generation") != anchor.generation:
        raise JournalIntegrityError("trusted checkpoint generation mismatch")
