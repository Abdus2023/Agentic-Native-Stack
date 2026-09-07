from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from .generation import repository_generation
from .journal import Journal
from .model import Action, Event, Observation, Run, RunState, VerificationResult, VerificationStatus
from .policy import PolicyEngine
from .promotion import PromotionAuthority
from .skills import SkillRegistry
from .state import transition
from .verify import Verifier


@dataclass
class Kernel:
    repo_root: Path
    policy: PolicyEngine
    skills: SkillRegistry
    journal: Journal
    verifier: Verifier | None = None
    promoter: PromotionAuthority | None = None

    def __post_init__(self) -> None:
        self.repo_root = self.repo_root.resolve()
        self.verifier = self.verifier or Verifier(self.repo_root)
        self.promoter = self.promoter or PromotionAuthority(self.repo_root)

    def create_run(self, task: str) -> Run:
        run = Run(id=uuid4().hex, task=task)
        transition(run, RunState.INTAKE)
        run.generation = repository_generation(self.repo_root).id
        self.journal.append(Event("RUN_CREATED", run.id, None, run.generation, {"task": task}))
        return run

    def plan(self, run: Run) -> None:
        if run.state is not RunState.INTAKE:
            raise RuntimeError(f"planning requires INTAKE, got {run.state}")
        transition(run, RunState.PLANNED)
        self.journal.append(Event("PLAN_ACCEPTED", run.id, None, run.generation, {}))

    def authorize(self, run: Run) -> None:
        if run.state is not RunState.PLANNED:
            raise RuntimeError(f"authorization requires PLANNED, got {run.state}")
        current = repository_generation(self.repo_root).id
        if current != run.generation:
            transition(run, RunState.BLOCKED)
            raise RuntimeError("run generation changed before authorization")
        transition(run, RunState.AUTHORIZED)
        self.journal.append(Event("AUTHORIZATION_GRANTED", run.id, None, run.generation, {}))

    def execute(self, run: Run, action: Action) -> Observation:
        if run.state is not RunState.AUTHORIZED:
            raise RuntimeError(f"mutation gateway requires AUTHORIZED run, got {run.state}")
        self.journal.append(Event("ACTION_PROPOSED", run.id, action.id, run.generation, {"kind": action.kind, "skill": action.skill}))
        decision = self.policy.evaluate(action)
        if not decision.allowed:
            self.journal.append(Event("POLICY_DENIED", run.id, action.id, run.generation, {"reason": decision.reason}))
            transition(run, RunState.BLOCKED)
            return Observation(action.id, False, run.generation, None, decision.reason)
        transition(run, RunState.EXECUTING)
        observation = self.skills.execute(action)
        current = repository_generation(self.repo_root).id
        if observation.ok:
            run.verification_epoch += 1
            run.generation = current
            self.journal.append(Event("ACTION_EXECUTED", run.id, action.id, current, {"success": True}))
            transition(run, RunState.OBSERVED)
        else:
            self.journal.append(Event("ACTION_EXECUTED", run.id, action.id, run.generation, {"success": False, "error": observation.error}))
            transition(run, RunState.FAILED)
        return observation

    def verify(self, run: Run) -> tuple[VerificationResult, ...]:
        if run.state is not RunState.OBSERVED:
            raise RuntimeError(f"verification requires OBSERVED, got {run.state}")
        transition(run, RunState.VERIFYING)
        assert self.verifier is not None
        report = self.verifier.verify(run.verification_epoch)
        run.verifications.extend(report.results)
        self.journal.append(Event("VERIFICATION_STARTED", run.id, None, report.generation, {"epoch": report.epoch}))
        for result in report.results:
            self.journal.append(Event("GATE_RESULT", run.id, None, result.generation, {"gate": result.gate, "status": result.status, "evidence_id": result.evidence_id, "epoch": result.epoch}))
        if report.generation != run.generation or not report.passed:
            transition(run, RunState.FAILED)
        else:
            transition(run, RunState.VERIFIED)
        return report.results

    def promote(self, run: Run) -> None:
        if self.promoter is None:
            raise RuntimeError("promotion authority unavailable")
        decision = self.promoter.authorize(run, tuple(run.verifications), self.repo_root)
        if not decision.allowed:
            raise RuntimeError(decision.reason)
        self.journal.append(Event("PROMOTION_AUTHORIZED", run.id, None, run.generation, {"reason": decision.reason}))
        self.journal.append(Event("PROMOTED", run.id, None, run.generation, {}))
