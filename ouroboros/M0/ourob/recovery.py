"""Crash-safe reconstruction of runs from the append-only journal."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .journal import Journal
from .model import Run, RunState, VerificationResult, VerificationStatus
from .state import InvalidTransition, transition


@dataclass(frozen=True)
class RecoveryResult:
    run: Run
    events_replayed: int


class RecoveryError(RuntimeError):
    """Raised when durable state cannot be safely reconstructed."""


def recover_run(journal: Journal, run_id: str) -> RecoveryResult:
    records = [r for r in journal.read() if r.get("run_id") == run_id]
    if not records:
        raise RecoveryError(f"no durable journal records for run: {run_id}")
    first = records[0]
    if first.get("event") != "RUN_CREATED":
        raise RecoveryError("RUN_CREATED must be the first durable event")
    task = first.get("task")
    generation = first.get("generation")
    if not isinstance(task, str) or not isinstance(generation, str):
        raise RecoveryError("RUN_CREATED is missing task or generation")
    run = Run(run_id, task)
    transition(run, RunState.INTAKE)
    run.generation = generation
    for record in records[1:]:
        _replay(run, record)
    return RecoveryResult(run, len(records))


def _replay(run: Run, record: dict[str, Any]) -> None:
    event = record.get("event")
    if not isinstance(event, str):
        raise RecoveryError("journal record has no valid event")
    targets = {
        "PLAN_ACCEPTED": RunState.PLANNED,
        "AUTHORIZATION_GRANTED": RunState.AUTHORIZED,
        "ACTION_EXECUTED": RunState.OBSERVED if record.get("success") else RunState.FAILED,
        "VERIFICATION_STARTED": RunState.VERIFYING,
        "PROMOTION_AUTHORIZED": RunState.PROMOTABLE,
        "PROMOTED": RunState.PROMOTED,
        "POLICY_DENIED": RunState.BLOCKED,
    }
    if event in {"ACTION_PROPOSED", "GATE_RESULT"}:
        target = None
    elif event in targets:
        target = targets[event]
    else:
        raise RecoveryError(f"unknown journal event: {event}")
    if target is not None:
        try:
            transition(run, target)
        except InvalidTransition as exc:
            raise RecoveryError(f"invalid durable transition for {event}: {exc}") from exc
    generation = record.get("generation", run.generation)
    if not isinstance(generation, str):
        raise RecoveryError(f"invalid generation in event: {event}")
    run.generation = generation
    if event == "ACTION_EXECUTED" and record.get("success"):
        run.verification_epoch += 1
    if event == "GATE_RESULT":
        run.verifications.append(_verification(record))


def _verification(record: dict[str, Any]) -> VerificationResult:
    gate, status, evidence_id, epoch = (
        record.get("gate"), record.get("status"), record.get("evidence_id"), record.get("epoch")
    )
    if not isinstance(gate, str) or not isinstance(status, str) or not isinstance(evidence_id, str) or not isinstance(epoch, int):
        raise RecoveryError("invalid GATE_RESULT record")
    try:
        parsed_status = VerificationStatus(status)
    except ValueError as exc:
        raise RecoveryError(f"invalid verification status: {status}") from exc
    return VerificationResult(gate, parsed_status, evidence_id, str(record.get("generation", "")), epoch)
