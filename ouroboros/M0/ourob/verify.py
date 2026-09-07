from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import subprocess
import sys
from pathlib import Path

from .generation import repository_generation
from .model import VerificationResult, VerificationStatus


GATE_CONTRACT_VERSION = "ouroboros.gate-contract.v1"


@dataclass(frozen=True)
class Gate:
    name: str
    command: tuple[str, ...]
    required: bool = True

    def canonical(self) -> bytes:
        """Return the normative, unambiguous gate contract bytes."""
        if not self.name or "\0" in self.name or "\n" in self.name:
            raise ValueError("gate names must be non-empty and free of NUL/newline")
        if not self.command or any(not isinstance(part, str) for part in self.command):
            raise ValueError(f"invalid command for gate: {self.name}")
        if any("\0" in part or "\n" in part for part in self.command):
            raise ValueError(f"invalid command token for gate: {self.name}")
        payload = {
            "command": list(self.command),
            "name": self.name,
            "required": self.required,
        }
        return json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")


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


def _validate_gate_set(gates: tuple[Gate, ...]) -> None:
    names = [gate.name for gate in gates]
    if any(not name or "\0" in name or "\n" in name for name in names):
        raise ValueError("gate names must be non-empty and free of NUL/newline")
    if len(names) != len(set(names)):
        raise ValueError("duplicate gate names are not permitted")
    for gate in gates:
        gate.canonical()


def gate_set_digest(gates: tuple[Gate, ...]) -> str:
    """SHA-256 identity of the complete gate contract set."""
    _validate_gate_set(gates)
    canonical = GATE_CONTRACT_VERSION.encode("ascii") + b"\0"
    canonical += b"\n".join(gate.canonical() for gate in sorted(gates, key=lambda item: item.name))
    canonical += b"\n" if gates else b""
    return sha256(canonical).hexdigest()


class Verifier:
    """Deterministic gate runner bound to one generation and gate contract."""

    def __init__(self, repo_root: Path, gates: tuple[Gate, ...] = DEFAULT_GATES) -> None:
        self.repo_root = repo_root.resolve()
        self.gates = tuple(gates)
        _validate_gate_set(self.gates)

    @property
    def gate_set_digest(self) -> str:
        return gate_set_digest(self.gates)

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
                status = VerificationStatus.BLOCKED if gate.required else VerificationStatus.NOT_RUN
                message = str(exc)
            except subprocess.TimeoutExpired as exc:
                status = VerificationStatus.FAIL
                message = f"timeout: {exc}"
            else:
                status = VerificationStatus.PASS if completed.returncode == 0 else VerificationStatus.FAIL
                message = (completed.stdout + completed.stderr).strip()
            evidence_id = sha256(
                f"{generation}\0{epoch}\0{gate.name}\0{status}\0{message}".encode()
            ).hexdigest()
            results.append(VerificationResult(gate.name, status, evidence_id, generation, epoch, message))

        final_generation = repository_generation(self.repo_root).id
        if final_generation != generation:
            results = [
                VerificationResult(
                    r.gate,
                    VerificationStatus.STALE,
                    r.evidence_id,
                    generation,
                    epoch,
                    "repository changed during verification",
                )
                for r in results
            ]
        return VerificationReport(generation, epoch, tuple(results))
