from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .model import Action, ActionKind, Observation


@dataclass(frozen=True)
class Skill:
    name: str
    kinds: frozenset[ActionKind]
    handler: Callable[[Action], Any]


class SkillRegistry:
    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        if skill.name in self._skills:
            raise ValueError(f"skill already registered: {skill.name}")
        self._skills[skill.name] = skill

    def has(self, name: str) -> bool:
        return name in self._skills

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._skills))

    def execute(self, action: Action) -> Observation:
        skill = self._skills.get(action.skill)
        if skill is None:
            return Observation(action.id, False, "", None, f"unknown skill: {action.skill}")
        if action.kind not in skill.kinds:
            return Observation(action.id, False, "", None, f"skill does not support {action.kind}")
        try:
            return Observation(action.id, True, "", skill.handler(action), None)
        except Exception as exc:
            return Observation(action.id, False, "", None, f"{type(exc).__name__}: {exc}")


def filesystem_skills(repo_root: Path) -> SkillRegistry:
    root = repo_root.resolve()
    registry = SkillRegistry()

    def safe_target(action: Action) -> tuple[Path, Path]:
        relative = Path(str(action.arguments["path"]))
        target = (root / relative).resolve()
        try:
            relative_resolved = target.relative_to(root)
        except ValueError as exc:
            raise ValueError("path escapes repository root") from exc
        return target, relative_resolved

    def read(action: Action) -> str:
        target, _ = safe_target(action)
        return target.read_text(encoding="utf-8")

    def write(action: Action) -> str:
        target, relative = safe_target(action)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(str(action.arguments.get("content", "")), encoding="utf-8")
        return relative.as_posix()

    registry.register(Skill("filesystem.read", frozenset({ActionKind.READ}), read))
    registry.register(Skill("filesystem.write", frozenset({ActionKind.WRITE, ActionKind.EDIT}), write))
    return registry
