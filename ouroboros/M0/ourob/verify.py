from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import subprocess
import sys
from pathlib import Path

from .generation import repository_generation
from .model import VerificationResult, VerificationStatus


@dataclass(frozen=True)
class Gate:
    name: str
    command: tuple[str, ...]
    required: bool = True


@dataclass(frozen=True)
class VerificationReport:
    generation: str
    epoch: int
    results: tuple[VerificationResult, ...]

    @property
    def passed(self) -> bool:
        return bool(self.results) and all(r.status is VerificationStatus.PASS for r in self.results)


DEFAULT_GATES = (
    Gate("compileall", (sys.executable, "-m", "compileall", "-q", "ourob")),
)


class Verifier:
    """Deterministic gate runner whose evidence is bound to one repository generation."""

    def __init__(self, repo_root: Path, gates: tuple[Gate, ...] = DEFAULT_GATES) -> None:
        self.repo_root = repo_root.resolve()
        self.gates = gates

    def verify(self, epoch: int) -> VerificationReport:
        generation = repository_generation(self.repo_root).id
        results: list[VerificationResult] = []
        for gate in self.gates:
            try:
                completed = subprocess.run(gate.command, cwd=self.repo_root, capture_output=True, text=True, timeout=120, check=False)
            except FileNotFoundError as exc:
                status = VerificationStatus.BLOCKED if gate.required else VerificationStatus.NOT_RUN
                message = str(exc)
            except subprocess.TimeoutExpired as exc:
                status = VerificationStatus.FAIL
                message = f"timeout: {exc}"
            else:
                status = VerificationStatus.PASS if completed.returncode == 0 else VerificationStatus.FAIL
                message = (completed.stdout + completed.stderr).strip()
            evidence_id = sha256(f"{generation}\0{epoch}\0{gate.name}\0{status}\0{message}".encode()).hexdigest()
            results.append(VerificationResult(gate.name, status, evidence_id, generation, epoch, message))

        final_generation = repository_generation(self.repo_root).id
        if final_generation != generation:
            results = [VerificationResult(r.gate, VerificationStatus.STALE, r.evidence_id, generation, epoch, "repository changed during verification") for r in results]
        return VerificationReport(generation, epoch, tuple(results))
