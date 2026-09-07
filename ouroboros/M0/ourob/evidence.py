from __future__ import annotations

from dataclasses import dataclass

from .generation import repository_generation
from .model import Run, VerificationResult, VerificationStatus


@dataclass(frozen=True)
class VerificationEvidence:
    """Immutable in-memory verification evidence bound to one run generation."""

    run_id: str
    generation: str
    epoch: int
    results: tuple[VerificationResult, ...]

    @property
    def passed(self) -> bool:
        return bool(self.results) and all(
            result.status is VerificationStatus.PASS
            and result.generation == self.generation
            and result.epoch == self.epoch
            for result in self.results
        )

    def is_current(self, repo_root) -> bool:
        return repository_generation(repo_root).id == self.generation


def capture_evidence(run: Run, results: tuple[VerificationResult, ...]) -> VerificationEvidence:
    """Freeze verifier output; no later Run mutation can alter the evidence."""
    return VerificationEvidence(
        run_id=run.id,
        generation=run.generation,
        epoch=run.verification_epoch,
        results=tuple(results),
    )
