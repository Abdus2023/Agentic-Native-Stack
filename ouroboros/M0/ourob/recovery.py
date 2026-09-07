"""Crash-safe reconstruction of runs with fail-closed authority replay."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .evidence import VerificationEvidence
from .journal import Journal
from .model import Run, RunState
from .state import InvalidTransition, transition


@dataclass(frozen=True)
class RecoveryResult:
    run: Run
    events_replayed: int
    evidence: VerificationEvidence | None = None


class RecoveryError(RuntimeError):
    """Raised when durable state cannot be safely reconstructed."""


def recover_run(journal: Journal, run_id: str) -> RecoveryResult:
    records = [record for record in journal.read() if record.get("run_id") == run_id]
    if not records:
        raise RecoveryError(f"no durable journal records for run: {run_id}")

    first = records[0]
    if first.get("event") != "RUN_CREATED":
        raise RecoveryError("RUN_CREATED must be the first durable event")
    if first.get("run_id") != run_id:
        raise RecoveryError("RUN_CREATED has the wrong run identity")

    task = first.get("task")
    generation = first.get("generation")
    if not isinstance(task, str) or not isinstance(generation, str):
        raise RecoveryError("RUN_CREATED is missing task or generation")

    run = Run(run_id, task)
    transition(run, RunState.INTAKE)
    run.generation = generation
    evidence: VerificationEvidence | None = None
    promotion_evidence_digest: str | None = None

    for record in records[1:]:
        evidence, promotion_evidence_digest = _replay(
            run, record, evidence, promotion_evidence_digest
        )

    if run.state in {RunState.VERIFIED, RunState.PROMOTABLE, RunState.PROMOTED} and evidence is None:
        raise RecoveryError("privileged state has no durable verification evidence")
    if run.state in {RunState.PROMOTABLE, RunState.PROMOTED} and promotion_evidence_digest != evidence.digest:
        raise RecoveryError("promotion state is not bound to recovered verification evidence")

    return RecoveryResult(run, len(records), evidence)


def _replay(
    run: Run,
    record: dict[str, Any],
    evidence: VerificationEvidence | None,
    promotion_evidence_digest: str | None,
) -> tuple[VerificationEvidence | None, str | None]:
    event = record.get("event")
    if not isinstance(event, str):
        raise RecoveryError("journal record has no valid event")
    if record.get("run_id") != run.id:
        raise RecoveryError(f"event {event} belongs to another run")

    generation = record.get("generation", run.generation)
    if not isinstance(generation, str):
        raise RecoveryError(f"invalid generation in event: {event}")

    if event == "PLAN_ACCEPTED":
        _transition(run, RunState.PLANNED, event)
    elif event == "AUTHORIZATION_GRANTED":
        if run.state is not RunState.PLANNED:
            raise RecoveryError("AUTHORIZATION_GRANTED requires durable PLANNED state")
        _transition(run, RunState.AUTHORIZED, event)
    elif event == "ACTION_PROPOSED":
        pass
    elif event == "ACTION_EXECUTED":
        if record.get("success"):
            if run.state is not RunState.AUTHORIZED:
                raise RecoveryError("successful ACTION_EXECUTED requires durable AUTHORIZED state")
            run.verification_epoch += 1
            _transition(run, RunState.OBSERVED, event)
        else:
            if run.state is not RunState.AUTHORIZED:
                raise RecoveryError("failed ACTION_EXECUTED requires durable AUTHORIZED state")
            _transition(run, RunState.FAILED, event)
    elif event == "POLICY_DENIED":
        _transition(run, RunState.BLOCKED, event)
    elif event == "VERIFICATION_STARTED":
        if run.state is not RunState.OBSERVED:
            raise RecoveryError("VERIFICATION_STARTED requires durable OBSERVED state")
        epoch = record.get("epoch")
        if not isinstance(epoch, int) or epoch != run.verification_epoch:
            raise RecoveryError("VERIFICATION_STARTED epoch does not match recovered run")
        _transition(run, RunState.VERIFYING, event)
    elif event == "GATE_RESULT":
        _replay_gate_result(run, record)
    elif event == "VERIFICATION_EVIDENCE_CAPTURED":
        if run.state is not RunState.VERIFYING:
            raise RecoveryError("verification evidence requires durable VERIFYING state")
        try:
            captured = VerificationEvidence.from_record(run.id, record)
        except ValueError as exc:
            raise RecoveryError(str(exc)) from exc
        if captured.generation != run.generation or captured.epoch != run.verification_epoch:
            raise RecoveryError("verification evidence is not bound to recovered generation/epoch")
        if not captured.passed:
            raise RecoveryError("durable verification evidence is not a complete PASS set")
        if tuple(result.gate for result in run.verifications) != tuple(result.gate for result in captured.results):
            raise RecoveryError("durable evidence does not match recovered gate results")
        _transition(run, RunState.VERIFIED, event)
        evidence = captured
    elif event == "PROMOTION_AUTHORIZED":
        if evidence is None:
            raise RecoveryError("PROMOTION_AUTHORIZED has no prior durable verification evidence")
        if run.state is not RunState.VERIFIED:
            raise RecoveryError("PROMOTION_AUTHORIZED requires durable VERIFIED state")
        digest = record.get("evidence_digest")
        if not isinstance(digest, str) or digest != evidence.digest:
            raise RecoveryError("promotion authorization is not bound to verification evidence")
        gate_set_digest = record.get("gate_set_digest")
        if gate_set_digest != evidence.gate_set_digest:
            raise RecoveryError("promotion authorization gate contract does not match evidence")
        _transition(run, RunState.PROMOTABLE, event)
        promotion_evidence_digest = digest
    elif event == "PROMOTED":
        if evidence is None or promotion_evidence_digest is None:
            raise RecoveryError("PROMOTED has no prior durable promotion authorization")
        if record.get("evidence_digest") != promotion_evidence_digest:
            raise RecoveryError("PROMOTED is not bound to promotion authorization")
        _transition(run, RunState.PROMOTED, event)
    else:
        raise RecoveryError(f"unknown journal event: {event}")

    if event != "RUN_CREATED" and generation != run.generation and event not in {"ACTION_EXECUTED", "VERIFICATION_STARTED", "GATE_RESULT", "VERIFICATION_EVIDENCE_CAPTURED", "PROMOTION_AUTHORIZED", "PROMOTED"}:
        raise RecoveryError(f"generation changed unexpectedly during {event}")
    run.generation = generation
    return evidence, promotion_evidence_digest


def _transition(run: Run, target: RunState, event: str) -> None:
    try:
        transition(run, target)
    except InvalidTransition as exc:
        raise RecoveryError(f"invalid durable transition for {event}: {exc}") from exc


def _replay_gate_result(run: Run, record: dict[str, Any]) -> None:
    if run.state is not RunState.VERIFYING:
        raise RecoveryError("GATE_RESULT requires durable VERIFYING state")
    required = ("gate", "status", "evidence_id", "epoch")
    if not all(key in record for key in required):
        raise RecoveryError("invalid GATE_RESULT record")
    from .model import VerificationResult, VerificationStatus

    gate = record.get("gate")
    status = record.get("status")
    evidence_id = record.get("evidence_id")
    epoch = record.get("epoch")
    message = record.get("message", "")
    generation = record.get("generation")
    if not all(isinstance(value, str) for value in (gate, status, evidence_id, message, generation)) or not isinstance(epoch, int):
        raise RecoveryError("invalid GATE_RESULT record")
    if epoch != run.verification_epoch or generation != run.generation:
        raise RecoveryError("GATE_RESULT is not bound to recovered generation/epoch")
    try:
        parsed_status = VerificationStatus(status)
    except ValueError as exc:
        raise RecoveryError(f"invalid verification status: {status}") from exc
    run.verifications.append(VerificationResult(gate, parsed_status, evidence_id, generation, epoch, message))
