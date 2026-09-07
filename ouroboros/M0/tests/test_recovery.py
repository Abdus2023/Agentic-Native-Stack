from pathlib import Path

import pytest

from ourob.evidence import capture_evidence
from ourob.journal import Journal
from ourob.model import Event, Run, VerificationResult, VerificationStatus
from ourob.recovery import RecoveryError, recover_run


def _journal(path: Path) -> Journal:
    return Journal(path / "journal.jsonl")


def _created(journal: Journal, run_id: str = "r1", generation: str = "g1") -> None:
    journal.append(Event("RUN_CREATED", run_id, None, generation, {"task": "demo"}))


def test_recovery_replays_ordinary_non_privileged_run(tmp_path: Path) -> None:
    journal = _journal(tmp_path)
    _created(journal)
    journal.append(Event("PLAN_ACCEPTED", "r1", None, "g1", {}))

    recovered = recover_run(journal, "r1")

    assert recovered.run.state.value == "PLANNED"
    assert recovered.evidence is None
    assert recovered.events_replayed == 2


def test_recovery_rejects_authorization_without_durable_plan(tmp_path: Path) -> None:
    journal = _journal(tmp_path)
    _created(journal)
    journal.append(Event("AUTHORIZATION_GRANTED", "r1", None, "g1", {"scope": "run"}))

    with pytest.raises(RecoveryError, match="durable PLANNED"):
        recover_run(journal, "r1")


def test_gate_results_without_evidence_capture_never_become_verified(tmp_path: Path) -> None:
    journal = _journal(tmp_path)
    _created(journal)
    journal.append(Event("PLAN_ACCEPTED", "r1", None, "g1", {}))
    journal.append(Event("AUTHORIZATION_GRANTED", "r1", None, "g1", {"scope": "run"}))
    journal.append(Event("ACTION_EXECUTED", "r1", "a1", "g2", {"success": True}))
    journal.append(Event("VERIFICATION_STARTED", "r1", None, "g2", {"epoch": 1}))
    journal.append(Event("GATE_RESULT", "r1", None, "g2", {"gate": "tests", "status": "PASS", "evidence_id": "e1", "epoch": 1, "message": ""}))

    recovered = recover_run(journal, "r1")

    assert recovered.run.state.value == "VERIFYING"
    assert recovered.evidence is None


def test_tampered_evidence_digest_is_rejected(tmp_path: Path) -> None:
    journal = _journal(tmp_path)
    _created(journal)
    journal.append(Event("PLAN_ACCEPTED", "r1", None, "g1", {}))
    journal.append(Event("AUTHORIZATION_GRANTED", "r1", None, "g1", {"scope": "run"}))
    journal.append(Event("ACTION_EXECUTED", "r1", "a1", "g2", {"success": True}))
    journal.append(Event("VERIFICATION_STARTED", "r1", None, "g2", {"epoch": 1}))
    result = VerificationResult("tests", VerificationStatus.PASS, "e1", "g2", 1)
    journal.append(Event("GATE_RESULT", "r1", None, "g2", {"gate": "tests", "status": "PASS", "evidence_id": "e1", "epoch": 1, "message": ""}))
    evidence = capture_evidence(Run("r1", "demo", generation="g2", verification_epoch=1), (result,), ("tests",), "gate-v1")
    payload = evidence.to_record()
    payload["evidence_digest"] = "f" * 64
    journal.append(Event("VERIFICATION_EVIDENCE_CAPTURED", "r1", None, "g2", payload))

    with pytest.raises(RecoveryError, match="digest is invalid"):
        recover_run(journal, "r1")


def test_promotion_without_durable_evidence_is_rejected(tmp_path: Path) -> None:
    journal = _journal(tmp_path)
    _created(journal)
    journal.append(Event("PLAN_ACCEPTED", "r1", None, "g1", {}))
    journal.append(Event("AUTHORIZATION_GRANTED", "r1", None, "g1", {"scope": "run"}))
    journal.append(Event("ACTION_EXECUTED", "r1", "a1", "g2", {"success": True}))
    journal.append(Event("VERIFICATION_STARTED", "r1", None, "g2", {"epoch": 1}))
    journal.append(Event("PROMOTION_AUTHORIZED", "r1", None, "g2", {"evidence_digest": "e" * 64, "gate_set_digest": "gate-v1"}))

    with pytest.raises(RecoveryError, match="no prior durable verification evidence"):
        recover_run(journal, "r1")


def test_valid_durable_authority_chain_reconstructs_exact_promotion_state(tmp_path: Path) -> None:
    journal = _journal(tmp_path)
    _created(journal)
    journal.append(Event("PLAN_ACCEPTED", "r1", None, "g1", {}))
    journal.append(Event("AUTHORIZATION_GRANTED", "r1", None, "g1", {"scope": "run"}))
    journal.append(Event("ACTION_EXECUTED", "r1", "a1", "g2", {"success": True}))
    journal.append(Event("VERIFICATION_STARTED", "r1", None, "g2", {"epoch": 1}))
    result = VerificationResult("tests", VerificationStatus.PASS, "e1", "g2", 1)
    journal.append(Event("GATE_RESULT", "r1", None, "g2", {"gate": "tests", "status": "PASS", "evidence_id": "e1", "epoch": 1, "message": ""}))
    evidence = capture_evidence(Run("r1", "demo", generation="g2", verification_epoch=1), (result,), ("tests",), "gate-v1")
    journal.append(Event("VERIFICATION_EVIDENCE_CAPTURED", "r1", None, "g2", evidence.to_record()))
    journal.append(Event("PROMOTION_AUTHORIZED", "r1", None, "g2", {"evidence_digest": evidence.digest, "gate_set_digest": evidence.gate_set_digest, "reason": "ok"}))
    journal.append(Event("PROMOTED", "r1", None, "g2", {"evidence_digest": evidence.digest}))

    recovered = recover_run(journal, "r1")

    assert recovered.run.state.value == "PROMOTED"
    assert recovered.run.generation == "g2"
    assert recovered.run.verification_epoch == 1
    assert recovered.evidence == evidence
