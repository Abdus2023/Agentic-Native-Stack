from __future__ import annotations

from dataclasses import dataclass

from .generation import repository_generation
from .model import Run, RunState, VerificationResult, VerificationStatus
from .state import transition


@dataclass(frozen=True)
class PromotionDecision:
    allowed: bool
    reason: str


class PromotionAuthority:
    """The only M0 component allowed to authorize PROMOTED."""

    def authorize(self, run: Run, verification: tuple[VerificationResult, ...], repo_root) -> PromotionDecision:
        current = repository_generation(repo_root).id
        if run.state is not RunState.VERIFIED:
            return PromotionDecision(False, f"run is not VERIFIED: {run.state}")
        if run.generation != current:
            return PromotionDecision(False, "run generation is stale")
        if not verification:
            return PromotionDecision(False, "no verification evidence")
        for result in verification:
            if result.status is not VerificationStatus.PASS:
                return PromotionDecision(False, f"gate {result.gate} is {result.status}")
            if result.generation != current or result.epoch != run.verification_epoch:
                return PromotionDecision(False, f"gate {result.gate} evidence is stale")
        transition(run, RunState.PROMOTABLE)
        transition(run, RunState.PROMOTED)
        return PromotionDecision(True, "current verification authorizes promotion")
