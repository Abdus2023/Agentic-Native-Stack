from __future__ import annotations

from dataclasses import dataclass
import subprocess
import sys
from pathlib import Path

from .generation import repository_generation
from .model import VerificationResult


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
        return bool(self.results) and all(r.status == "PASS" for r in self.results)


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
                completed = subprocess.run(
                    gate.command,
                    cwd=self.repo_root,
                    capture_output=True,
                    text=True,
                    timeout=120,
                    check=False,
                )
            except FileNotFoundError as exc:
                status = "BLOCKED" if gate.required else "NOT_RUN"
                results.append(VerificationResult(gate.name, status, generation, epoch, str(exc)))
                continue
            except subprocess.TimeoutExpired as exc:
                results.append(VerificationResult(gate.name, "FAIL", generation, epoch, f"timeout: {exc}"))
                continue
            status = "PASS" if completed.returncode == 0 else "FAIL"
            detail = (completed.stdout + completed.stderr).strip()
            results.append(VerificationResult(gate.name, status, generation, epoch, detail))

        # Evidence is valid only if the repository did not mutate during verification.
        final_generation = repository_generation(self.repo_root).id
        if final_generation != generation:
            results = [VerificationResult(r.gate, "STALE", generation, epoch, "repository changed during verification") for r in results]
        return VerificationReport(generation, epoch, tuple(results))
