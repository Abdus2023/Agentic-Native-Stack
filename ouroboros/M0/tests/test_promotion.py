from pathlib import Path
import sys

from ourob.evidence import capture_evidence
from ourob.generation import repository_generation
from ourob.model import Run, RunState, VerificationResult, VerificationStatus
from ourob.promotion import PromotionAuthority
from ourob.verify import Gate, Verifier


def _evidence(tmp_path: Path, epoch: int, command=(sys.executable, "-c", "print('ok')")):
    generation = repository_generation(tmp_path).id
    run = Run("r1", "test", RunState.VERIFIED, generation=generation, verification_epoch=epoch)
    gate = Gate("gate", tuple(command))
    verifier = Verifier(tmp_path, (gate,))
    result = VerificationResult("gate", VerificationStatus.PASS, "e", generation, epoch, "ok")
    return run, verifier, capture_evidence(run, (result,), ("gate",), verifier.gate_set_digest)


def test_promotion_rejects_stale_evidence(tmp_path: Path) -> None:
    run, verifier, evidence = _evidence(tmp_path, 1)
    run.verification_epoch = 2
    decision = PromotionAuthority(tmp_path).authorize(run, evidence, tmp_path, verifier.gate_set_digest)
    assert not decision.allowed
    assert decision.reason == "evidence epoch is stale"
    assert run.state is RunState.VERIFIED


def test_promotion_requires_current_verified_evidence(tmp_path: Path) -> None:
    run, verifier, evidence = _evidence(tmp_path, 2)
    decision = PromotionAuthority(tmp_path).authorize(run, evidence, tmp_path, verifier.gate_set_digest)
    assert decision.allowed
    assert run.state is RunState.PROMOTED


def test_promotion_rejects_changed_gate_contract(tmp_path: Path) -> None:
    run, verifier, evidence = _evidence(tmp_path, 2)
    changed = Verifier(tmp_path, (Gate("gate", (sys.executable, "-c", "print('changed')")),))
    decision = PromotionAuthority(tmp_path).authorize(run, evidence, tmp_path, changed.gate_set_digest)
    assert not decision.allowed
    assert decision.reason == "verification gate contract changed"
    assert run.state is RunState.VERIFIED
