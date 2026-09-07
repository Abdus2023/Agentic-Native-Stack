from pathlib import Path

from ourob.generation import repository_generation
from ourob.model import Run, RunState, VerificationResult, VerificationStatus
from ourob.promotion import PromotionAuthority


def test_promotion_rejects_stale_evidence(tmp_path: Path) -> None:
    run = Run("r1", "test", RunState.VERIFIED, verification_epoch=2)
    run.generation = repository_generation(tmp_path).id
    result = VerificationResult("gate", VerificationStatus.PASS, "e", run.generation, 1, "old epoch")
    decision = PromotionAuthority().authorize(run, (result,), tmp_path)
    assert not decision.allowed
    assert run.state is RunState.VERIFIED


def test_promotion_requires_current_verified_evidence(tmp_path: Path) -> None:
    generation = repository_generation(tmp_path).id
    run = Run("r1", "test", RunState.VERIFIED, generation=generation, verification_epoch=2)
    result = VerificationResult("gate", VerificationStatus.PASS, "e", generation, 2, "ok")
    decision = PromotionAuthority().authorize(run, (result,), tmp_path)
    assert decision.allowed
    assert run.state is RunState.PROMOTED
