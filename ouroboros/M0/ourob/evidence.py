from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Any

from .generation import repository_generation
from .model import Run, VerificationResult, VerificationStatus


def _canonical_results(results: tuple[VerificationResult, ...]) -> bytes:
    lines = []
    for result in sorted(results, key=lambda item: item.gate):
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
    """Immutable, complete, self-checking verification evidence."""

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
        header = (
            f"{self.run_id}\0{self.generation}\0{self.epoch}\0"
            f"{gates}\0{self.gate_set_digest}\0"
        ).encode("utf-8")
        return header + _canonical_results(self.results)

    def recompute_digest(self) -> str:
        return sha256(self.canonical_bytes()).hexdigest()

    def integrity_valid(self) -> bool:
        return bool(self.gate_set_digest) and self.digest == self.recompute_digest()

    def is_current(self, repo_root) -> bool:
        return repository_generation(repo_root).id == self.generation

    def to_record(self) -> dict[str, Any]:
        """Return the complete immutable payload needed for crash recovery."""
        return {
            "evidence_digest": self.digest,
            "gate_set_digest": self.gate_set_digest,
            "required_gates": list(self.required_gates),
            "epoch": self.epoch,
            "generation": self.generation,
            "results": [
                {
                    "gate": result.gate,
                    "status": result.status.value,
                    "evidence_id": result.evidence_id,
                    "generation": result.generation,
                    "epoch": result.epoch,
                    "message": result.message,
                }
                for result in self.results
            ],
        }

    @classmethod
    def from_record(cls, run_id: str, record: dict[str, Any]) -> "VerificationEvidence":
        digest = record.get("evidence_digest")
        gate_set_digest = record.get("gate_set_digest")
        required = record.get("required_gates")
        generation = record.get("generation")
        epoch = record.get("epoch")
        raw_results = record.get("results")
        if (
            not isinstance(digest, str)
            or not isinstance(gate_set_digest, str)
            or not isinstance(required, list)
            or not all(isinstance(gate, str) for gate in required)
            or not isinstance(generation, str)
            or not isinstance(epoch, int)
            or not isinstance(raw_results, list)
        ):
            raise ValueError("invalid verification evidence record")

        results: list[VerificationResult] = []
        for raw in raw_results:
            if not isinstance(raw, dict):
                raise ValueError("invalid verification evidence result")
            gate = raw.get("gate")
            status = raw.get("status")
            evidence_id = raw.get("evidence_id")
            result_generation = raw.get("generation")
            result_epoch = raw.get("epoch")
            message = raw.get("message", "")
            if (
                not isinstance(gate, str)
                or not isinstance(status, str)
                or not isinstance(evidence_id, str)
                or not isinstance(result_generation, str)
                or not isinstance(result_epoch, int)
                or not isinstance(message, str)
            ):
                raise ValueError("invalid verification evidence result")
            try:
                parsed_status = VerificationStatus(status)
            except ValueError as exc:
                raise ValueError(f"invalid verification status: {status}") from exc
            results.append(
                VerificationResult(
                    gate,
                    parsed_status,
                    evidence_id,
                    result_generation,
                    result_epoch,
                    message,
                )
            )

        evidence = cls(
            run_id,
            generation,
            epoch,
            tuple(results),
            tuple(required),
            digest,
            gate_set_digest,
        )
        if not evidence.integrity_valid():
            raise ValueError("verification evidence digest is invalid")
        return evidence


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
