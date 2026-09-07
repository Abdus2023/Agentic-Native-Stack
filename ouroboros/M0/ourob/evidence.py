from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from .generation import repository_generation
from .model import Run, VerificationResult, VerificationStatus


def _canonical_results(results: tuple[VerificationResult, ...]) -> bytes:
    lines = []
    for result in sorted(results, key=lambda item: item.gate):
        lines.append("\0".join((result.gate, result.status.value, result.evidence_id, result.generation, str(result.epoch), result.message)))
    return ("\n".join(lines) + "\n").encode("utf-8") if lines else b""


@dataclass(frozen=True)
class VerificationEvidence:
    """Immutable, complete, and self-checking verification evidence."""

    run_id: str
    generation: str
    epoch: int
    results: tuple[VerificationResult, ...]
    required_gates: tuple[str, ...]
    digest: str
    gate_set_digest: str = ""

    @property
    def passed(self) -> bool:
        required = tuple(sorted(set(self.required_gates)))
        actual = tuple(sorted(result.gate for result in self.results))
        return (
            bool(required)
            and actual == required
            and len(actual) == len(set(actual))
            and all(
                result.status is VerificationStatus.PASS
                and result.generation == self.generation
                and result.epoch == self.epoch
                for result in self.results
            )
        )

    def canonical_bytes(self) -> bytes:
        gates = "\0".join(sorted(self.required_gates))
        header = f"{self.run_id}\0{self.generation}\0{self.epoch}\0{gates}\0{self.gate_set_digest}\0".encode("utf-8")
        return header + _canonical_results(self.results)

    def recompute_digest(self) -> str:
        return sha256(self.canonical_bytes()).hexdigest()

    def integrity_valid(self) -> bool:
        return bool(self.gate_set_digest) and self.digest == self.recompute_digest()

    def is_current(self, repo_root) -> bool:
        return repository_generation(repo_root).id == self.generation


def capture_evidence(
    run: Run,
    results: tuple[VerificationResult, ...],
    required_gates: tuple[str, ...],
    gate_contract_digest: str,
) -> VerificationEvidence:
    """Freeze verifier output against its already-canonicalized gate identity."""
    if not gate_contract_digest:
        raise ValueError("gate contract digest is required")
    evidence = VerificationEvidence(
        run.id,
        run.generation,
        run.verification_epoch,
        tuple(results),
        tuple(required_gates),
        "",
        gate_contract_digest,
    )
    return VerificationEvidence(
        evidence.run_id,
        evidence.generation,
        evidence.epoch,
        evidence.results,
        evidence.required_gates,
        evidence.recompute_digest(),
        evidence.gate_set_digest,
    )
