from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import pytest

from ourob.signed_trust import (
    SignedCheckpoint,
    SignatureVerificationError,
    TrustKey,
    TrustKeyState,
    TrustStore,
    sign_checkpoint,
)


class Ed25519Backend:
    def verify(self, public_key: bytes, message: bytes, signature: bytes) -> None:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

        try:
            Ed25519PublicKey.from_public_bytes(public_key).verify(signature, message)
        except InvalidSignature as exc:
            raise SignatureVerificationError("invalid checkpoint signature") from exc


def _store(private_key: Ed25519PrivateKey) -> TrustStore:
    public = private_key.public_key().public_bytes_raw()
    return TrustStore((TrustKey("root-1", "Ed25519", public, TrustKeyState.ACTIVE, 0),), 0)


def test_signed_checkpoint_round_trip_and_verification() -> None:
    private = Ed25519PrivateKey.generate()
    store = _store(private)
    checkpoint = sign_checkpoint(private, key_id="root-1", sequence=3, journal_digest="a" * 64, generation="g3")

    assert SignedCheckpoint.from_record(checkpoint.to_record()) == checkpoint
    store.verify(checkpoint, Ed25519Backend())
    assert checkpoint.binding


def test_signature_covers_generation_and_digest() -> None:
    private = Ed25519PrivateKey.generate()
    store = _store(private)
    checkpoint = sign_checkpoint(private, key_id="root-1", sequence=3, journal_digest="a" * 64, generation="g3")
    forged = SignedCheckpoint("root-1", 3, "b" * 64, "g3", checkpoint.signature)

    with pytest.raises(SignatureVerificationError, match="invalid checkpoint signature"):
        store.verify(forged, Ed25519Backend())


def test_revoked_key_cannot_verify() -> None:
    private = Ed25519PrivateKey.generate()
    store = _store(private).with_state("root-1", TrustKeyState.REVOKED)
    checkpoint = sign_checkpoint(private, key_id="root-1", sequence=1, journal_digest="a" * 64, generation="g1")

    with pytest.raises(SignatureVerificationError, match="revoked"):
        store.verify(checkpoint, Ed25519Backend())


def test_rotation_requires_next_epoch_and_new_key_id() -> None:
    first = Ed25519PrivateKey.generate()
    store = _store(first)
    second = Ed25519PrivateKey.generate()
    key = TrustKey("root-2", "Ed25519", second.public_key().public_bytes_raw(), TrustKeyState.ACTIVE, 1)

    rotated = store.with_rotation(key)
    assert rotated.epoch == 1
    assert rotated.key("root-2") == key

    with pytest.raises(ValueError, match="exactly one epoch"):
        store.with_rotation(TrustKey("root-3", "Ed25519", second.public_key().public_bytes_raw(), TrustKeyState.ACTIVE, 3))


def test_unknown_key_fails_closed() -> None:
    private = Ed25519PrivateKey.generate()
    store = _store(private)
    other = Ed25519PrivateKey.generate()
    checkpoint = sign_checkpoint(other, key_id="unknown", sequence=1, journal_digest="a" * 64, generation="g1")

    with pytest.raises(SignatureVerificationError, match="unknown trust key"):
        store.verify(checkpoint, Ed25519Backend())
