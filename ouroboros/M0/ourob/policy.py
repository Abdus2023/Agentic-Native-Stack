from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath

from .model import Action, ActionKind


class MutationClass(StrEnum):
    ORDINARY = "ORDINARY"
    CAPABILITY = "CAPABILITY"
    POLICY = "POLICY"
    VERIFIER = "VERIFIER"
    KERNEL = "KERNEL"
    BOOTSTRAP = "BOOTSTRAP"


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str
    mutation_class: MutationClass


PROTECTED_PREFIXES: dict[MutationClass, tuple[str, ...]] = {
    MutationClass.KERNEL: ("ourob/kernel/", "ourob/kernel.py"),
    MutationClass.BOOTSTRAP: ("bootstrap/", "ourob/bootstrap.py"),
    MutationClass.POLICY: ("policies/", "ourob/policy.py"),
    MutationClass.VERIFIER: ("verification/", "ourob/verify.py"),
}


class PolicyEngine:
    """Small deterministic policy interpreter; repository policy data is not executable authority."""

    def classify(self, path: str) -> MutationClass:
        normalized = PurePosixPath(path).as_posix().lstrip("./")
        for mutation_class, prefixes in PROTECTED_PREFIXES.items():
            if any(normalized == prefix.rstrip("/") or normalized.startswith(prefix) for prefix in prefixes):
                return mutation_class
        if normalized.startswith("skills/") or normalized.startswith("ourob/skills/"):
            return MutationClass.CAPABILITY
        return MutationClass.ORDINARY

    def evaluate(self, action: Action) -> PolicyDecision:
        if action.kind not in {ActionKind.WRITE, ActionKind.EDIT}:
            return PolicyDecision(True, "non-mutating action", MutationClass.ORDINARY)

        path = str(action.arguments.get("path", ""))
        if not path:
            return PolicyDecision(False, "mutation requires a repository-relative path", MutationClass.ORDINARY)

        mutation_class = self.classify(path)
        if mutation_class is MutationClass.ORDINARY:
            return PolicyDecision(True, "ordinary repository mutation allowed", mutation_class)

        return PolicyDecision(
            False,
            f"elevated authorization required for {mutation_class} mutation: {path}",
            mutation_class,
        )
