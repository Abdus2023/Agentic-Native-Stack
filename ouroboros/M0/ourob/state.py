"""Fail-closed run state machine."""

from .model import Run, RunState


class InvalidTransition(RuntimeError):
    """Raised when a run attempts an undeclared state transition."""


ALLOWED_TRANSITIONS: dict[RunState, frozenset[RunState]] = {
    RunState.NO_TASK: frozenset({RunState.INTAKE}),
    RunState.INTAKE: frozenset({RunState.PLANNED, RunState.BLOCKED}),
    RunState.PLANNED: frozenset({RunState.AUTHORIZED, RunState.BLOCKED}),
    RunState.AUTHORIZED: frozenset({RunState.EXECUTING, RunState.BLOCKED}),
    RunState.EXECUTING: frozenset({RunState.OBSERVED, RunState.FAILED, RunState.BLOCKED}),
    RunState.OBSERVED: frozenset({RunState.AUTHORIZED, RunState.VERIFYING}),
    RunState.VERIFYING: frozenset({RunState.VERIFIED, RunState.FAILED, RunState.BLOCKED}),
    RunState.VERIFIED: frozenset({RunState.PROMOTABLE}),
    RunState.PROMOTABLE: frozenset({RunState.PROMOTED}),
    RunState.PROMOTED: frozenset(),
    RunState.BLOCKED: frozenset(),
    RunState.FAILED: frozenset(),
}


def transition(run: Run, target: RunState) -> None:
    """Apply exactly one declared transition; never infer or skip states."""
    allowed = ALLOWED_TRANSITIONS[run.state]
    if target not in allowed:
        raise InvalidTransition(f"{run.state} -> {target} is not permitted")
    run.state = target
