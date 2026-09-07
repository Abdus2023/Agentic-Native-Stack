"""Cryptographically signed journal checkpoints and trust-key lifecycle.

Private signing keys are deliberately outside OUROBOROS repository state. This
module verifies externally supplied Ed25519 public keys and signed checkpoints;
it does not provide a repository-controlled root of trust.
"""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from typing import Any, Mapping, Protocol

from .trust import JournalTrustAnchor

SIGNED_CHECKPOINT_VERSION = "ouroboros.signed-journal-checkpoint.v1"
TRUST_KEY_VERSION = "ouroboros.trust-key.v1"
TRUST_STORE_VERSION = "ouroboros.trust-store.v1"
SUPPORTED_ALGORITHM = "Ed25519"


class TrustKeyState(StrEnum):
    ACTIVE = "ACTIVE"
    RETIRED = "RETIRED"
    REVOKED = "REVOKED"


class SignatureBackend(Protocol):
    def verify(self, public_key: bytes, message: bytes, signature: bytes) -> None: ...


class SignatureVerificationError(ValueError):
    """Raised when a signed checkpoint cannot be cryptographically verified."""


def _b64(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def _unb64(value: Any, field: str) -> bytes:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be base64 text")
    try:
        return base64.b64decode(value.encode("ascii"), validate=True)
    except Exception as exc:
        raise ValueError(f"invalid base64 in {field}") from exc


def _canonical(value: Mapping[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


@dataclass(frozen=True)
class TrustKey:
    key_id: str
    algorithm: str
    public_key: bytes
    state: TrustKeyState = TrustKeyState.ACTIVE
    epoch: int = 0
    version: str = TRUST_KEY_VERSION

    def __post_init__(self) -> None:
        if self.version != TRUST_KEY_VERSION:
            raise ValueError("unsupported trust-key version")
        if not self.key_id or "\x00" in self.key_id:
            raise ValueError("invalid trust key id")
        if self.algorithm != SUPPORTED_ALGORITHM:
            raise ValueError("unsupported trust-key algorithm")
        if len(self.public_key) != 32:
            raise ValueError("Ed25519 public key must be 32 bytes")
        if self.epoch < 0:
            raise ValueError("trust-key epoch must be non-negative")

    def to_record(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "key_id": self.key_id,
            "algorithm": self.algorithm,
            "public_key": _b64(self.public_key),
            "state": self.state.value,
            "epoch": self.epoch,
        }

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "TrustKey":
        return cls(
            key_id=record.get("key_id", ""),
            algorithm=record.get("algorithm", ""),
            public_key=_unb64(record.get("public_key"), "public_key"),
            state=TrustKeyState(record.get("state", "")),
            epoch=record.get("epoch", -1),
            version=record.get("version", ""),
        )


@dataclass(frozen=True)
class SignedCheckpoint:
    key_id: str
    sequence: int
    journal_digest: str
    generation: str
    signature: bytes
    algorithm: str = SUPPORTED_ALGORITHM
    version: str = SIGNED_CHECKPOINT_VERSION

    def __post_init__(self) -> None:
        if self.version != SIGNED_CHECKPOINT_VERSION:
            raise ValueError("unsupported signed-checkpoint version")
        if self.algorithm != SUPPORTED_ALGORITHM:
            raise ValueError("unsupported signature algorithm")
        if not self.key_id or self.sequence < 1:
            raise ValueError("invalid signed checkpoint identity")
        if len(self.journal_digest) != 64 or any(c not in "0123456789abcdef" for c in self.journal_digest):
            raise ValueError("invalid journal digest")

    def signing_record(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "algorithm": self.algorithm,
            "key_id": self.key_id,
            "sequence": self.sequence,
            "journal_digest": self.journal_digest,
            "generation": self.generation,
        }

    def signing_bytes(self) -> bytes:
        return _canonical(self.signing_record())

    def to_record(self) -> dict[str, Any]:
        return {**self.signing_record(), "signature": _b64(self.signature)}

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "SignedCheckpoint":
        return cls(
            key_id=record.get("key_id", ""),
            sequence=record.get("sequence", 0),
            journal_digest=record.get("journal_digest", ""),
            generation=record.get("generation", ""),
            signature=_unb64(record.get("signature"), "signature"),
            algorithm=record.get("algorithm", ""),
            version=record.get("version", ""),
        )

    @property
    def binding(self) -> str:
        return sha256(self.signing_bytes()).hexdigest()

    def as_anchor(self) -> JournalTrustAnchor:
        return JournalTrustAnchor(self.sequence, self.journal_digest, self.generation)


def sign_checkpoint(private_key: Any, *, key_id: str, sequence: int, journal_digest: str, generation: str) -> SignedCheckpoint:
    """Create a checkpoint using an externally held Ed25519 private-key object."""
    unsigned = SignedCheckpoint(key_id, sequence, journal_digest, generation, b"")
    signature = private_key.sign(unsigned.signing_bytes())
    return SignedCheckpoint(key_id, sequence, journal_digest, generation, signature)


class TrustStore:
    """Immutable-at-runtime view of externally provisioned trust keys."""

    def __init__(self, keys: tuple[TrustKey, ...], epoch: int) -> None:
        if epoch < 0:
            raise ValueError("trust-store epoch must be non-negative")
        ids = [key.key_id for key in keys]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate trust key id")
        if any(key.epoch > epoch for key in keys):
            raise ValueError("trust key belongs to a future epoch")
        self._keys = keys
        self.epoch = epoch

    @property
    def keys(self) -> tuple[TrustKey, ...]:
        return self._keys

    def key(self, key_id: str) -> TrustKey:
        for key in self._keys:
            if key.key_id == key_id:
                return key
        raise SignatureVerificationError("unknown trust key")

    def verify(self, checkpoint: SignedCheckpoint, backend: SignatureBackend) -> None:
        if checkpoint.algorithm != SUPPORTED_ALGORITHM:
            raise SignatureVerificationError("unknown signature algorithm")
        key = self.key(checkpoint.key_id)
        if key.state is TrustKeyState.REVOKED:
            raise SignatureVerificationError("trust key is revoked")
        backend.verify(key.public_key, checkpoint.signing_bytes(), checkpoint.signature)

    def with_rotation(self, new_key: TrustKey) -> "TrustStore":
        if new_key.key_id in {key.key_id for key in self._keys}:
            raise ValueError("trust key id already exists")
        if new_key.epoch != self.epoch + 1:
            raise ValueError("trust-key rotation must advance exactly one epoch")
        return TrustStore(self._keys + (new_key,), new_key.epoch)

    def with_state(self, key_id: str, state: TrustKeyState) -> "TrustStore":
        if state is TrustKeyState.ACTIVE:
            raise ValueError("activation requires an explicit rotation policy")
        found = False
        updated: list[TrustKey] = []
        for key in self._keys:
            if key.key_id == key_id:
                found = True
                updated.append(TrustKey(key.key_id, key.algorithm, key.public_key, state, key.epoch))
            else:
                updated.append(key)
        if not found:
            raise ValueError("unknown trust key")
        return TrustStore(tuple(updated), self.epoch)

    def to_record(self) -> dict[str, Any]:
        return {"version": TRUST_STORE_VERSION, "epoch": self.epoch, "keys": [key.to_record() for key in self._keys]}

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "TrustStore":
        if record.get("version") != TRUST_STORE_VERSION:
            raise ValueError("unsupported trust-store version")
        keys = tuple(TrustKey.from_record(item) for item in record.get("keys", []))
        return cls(keys, record.get("epoch", -1))
