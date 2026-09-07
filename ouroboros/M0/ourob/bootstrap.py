from __future__ import annotations

from dataclasses import dataclass
import importlib
import json
from pathlib import Path

from .generation import repository_generation
from .journal import Journal
from .policy import PolicyEngine
from .skills import SkillRegistry, filesystem_skills


@dataclass(frozen=True)
class BootstrapResult:
    generation: str
    trusted: bool
    skills: tuple[str, ...]
    reason: str


class Bootstrap:
    """Reconstruct runtime capabilities from repository state without self-attesting trust."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root.resolve()

    def load(self) -> BootstrapResult:
        generation = repository_generation(self.repo_root).id
        constitution = self.repo_root / "policies" / "constitution.json"
        gates = self.repo_root / "verification" / "gates.json"
        if not constitution.exists() or not gates.exists():
            return BootstrapResult(generation, False, (), "bootstrap trust inputs are missing")
        try:
            json.loads(constitution.read_text(encoding="utf-8"))
            json.loads(gates.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return BootstrapResult(generation, False, (), f"invalid bootstrap trust input: {exc}")

        registry = filesystem_skills(self.repo_root)
        manifest = self.repo_root / "skills" / "manifest.json"
        if manifest.exists():
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
                for entry in data.get("skills", []):
                    module = str(entry["module"])
                    name = str(entry["name"])
                    imported = importlib.import_module(module)
                    register = getattr(imported, "register")
                    register(registry, name=name)
            except (OSError, KeyError, TypeError, ValueError, ImportError, AttributeError, json.JSONDecodeError) as exc:
                return BootstrapResult(generation, False, (), f"skill bootstrap failed: {exc}")
        return BootstrapResult(generation, True, registry.names(), "repository-declared runtime reconstructed")
