from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from .journal import Journal
from .model import Action, Event, Observation, Run, RunState
from .policy import PolicyEngine
from .skills import SkillRegistry
from .state import transition


@dataclass
class Kernel:
    repo_root: Path
    policy: PolicyEngine
    skills: SkillRegistry
    journal: Journal

    def create_run(self, task: str) -> Run:
        run = Run(id=uuid4().hex, task=task)
        transition(run, RunState.INTAKE)
        self.journal.append(Event("RUN_CREATED", run.id, None, run.generation, {"task": task}))
        return run

    def execute(self, run: Run, action: Action) -> Observation:
        if run.state is not RunState.AUTHORIZED:
            raise RuntimeError(f"mutation gateway requires AUTHORIZED run, got {run.state}")

        self.journal.append(Event("ACTION_PROPOSED", run.id, action.id, run.generation, {"kind": action.kind, "skill": action.skill}))
        decision = self.policy.evaluate(action)
        if not decision.allowed:
            self.journal.append(Event("POLICY_DENIED", run.id, action.id, run.generation, {"reason": decision.reason}))
            transition(run, RunState.BLOCKED)
            return Observation(action.id, False, None, decision.reason)

        self.journal.append(Event("POLICY_ALLOWED", run.id, action.id, run.generation, {"reason": decision.reason}))
        transition(run, RunState.EXECUTING)
        observation = self.skills.execute(action)
        self.journal.append(Event("ACTION_EXECUTED", run.id, action.id, run.generation, {"success": observation.success}))
        self.journal.append(Event("OBSERVATION", run.id, action.id, run.generation, {"success": observation.success, "error": observation.error}))
        if observation.success:
            transition(run, RunState.OBSERVED)
        else:
            transition(run, RunState.FAILED)
        return observation
