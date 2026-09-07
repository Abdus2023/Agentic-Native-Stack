from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from .generation import repository_generation
from .model import Run, VerificationResult, VerificationStatus


def _canonical_results(results: tuple[VerificationResult, ...]) -> bytes:
    lines = []
    for result in results:
        lines.append(
            "\0".join(
                (
                    result.gate,
                    result.status.value,
                    result.evidence_id,
                    result.generation,
                    str(result.epoch),
                    result.message,
                )
            )
        )
    return ("\n".join(lines) + "\n").encode("utf-8") if lines else b""


@dataclass(frozen=True)
class VerificationEvidence:
    """Immutable verification evidence with a self-checking content digest."""

    run_id: str
    generation: str
    epoch: int
    results: tuple[VerificationResult, ...]
    digest: str

    @property
    def passed(self) -> bool:
        return bool(self.results) and all(
            result.status is VerificationStatus.PASS
            and result.generation == self.generation
            and result.epoch == self.epoch
            for result in self.results
        )

    def canonical_bytes(self) -> bytes:
        header = f"{self.run_id}\0{self.generation}\0{self.epoch}\0".encode("utf-8")
        return header + _canonical_results(self.results)

    def recompute_digest(self) -> str:
        return sha256(self.canonical_bytes()).hexdigest()

    def integrity_valid(self) -> bool:
        return self.digest == self.recompute_digest()

    def is_current(self, repo_root) -> bool:
        return repository_generation(repo_root).id == self.generation


def capture_evidence(run: Run, results: tuple[VerificationResult, ...]) -> VerificationEvidence:
    """Freeze verifier output and compute its canonical content digest."""
    evidence = VerificationEvidence(
        run_id=run.id,
        generation=run.generation,
        epoch=run.verification_epoch,
        results=tuple(results),
        digest="",
    )
    return VerificationEvidence(
        run_id=evidence.run_id,
        generation=evidence.generation,
        epoch=evidence.epoch,
        results=evidence.results,
        digest=evidence.recompute_digest(),
    )
