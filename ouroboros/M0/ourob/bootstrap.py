from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import json
from pathlib import Path

from .generation import repository_generation
from .policy import PolicyEngine
from .skills import SkillRegistry, filesystem_skills


@dataclass(frozen=True)
class BootstrapResult:
    generation: str
    trusted: bool
    skills: tuple[str, ...]
    reason: str
    registry: SkillRegistry | None = None


class Bootstrap:
    """Reconstruct capabilities from repository-declared state, fail closed."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root.resolve()

    def _module_path(self, module: str) -> Path:
        if not module or module.startswith(".") or "/" in module or "\\" in module:
            raise ValueError("module must be a repository-relative dotted name")
        parts = module.split(".")
        if any(not part.isidentifier() for part in parts):
            raise ValueError("invalid module name")
        candidate = (self.repo_root / Path(*parts)).with_suffix(".py").resolve()
        try:
            candidate.relative_to(self.repo_root)
        except ValueError as exc:
            raise ValueError("module escapes repository root") from exc
        if not candidate.is_file():
            raise FileNotFoundError(candidate)
        return candidate

    def load(self) -> BootstrapResult:
        generation = repository_generation(self.repo_root).id
        constitution = self.repo_root / "policies" / "constitution.json"
        gates = self.repo_root / "verification" / "gates.json"
        if not constitution.exists() or not gates.exists():
            return BootstrapResult(generation, False, (), "bootstrap trust inputs are missing")
        try:
            constitution_data = json.loads(constitution.read_text(encoding="utf-8"))
            gates_data = json.loads(gates.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return BootstrapResult(generation, False, (), f"invalid bootstrap trust input: {exc}")
        if not isinstance(constitution_data, dict) or constitution_data.get("schema") != "ourob.constitution.v1":
            return BootstrapResult(generation, False, (), "unsupported constitution schema")
        if constitution_data.get("mode") != "fail_closed":
            return BootstrapResult(generation, False, (), "constitution is not fail_closed")
        if not isinstance(gates_data, dict) or gates_data.get("schema") != "ourob.gates.v1":
            return BootstrapResult(generation, False, (), "unsupported gate schema")
        if not isinstance(gates_data.get("gates"), list) or not gates_data["gates"]:
            return BootstrapResult(generation, False, (), "no verification gates declared")

        registry: SkillRegistry = filesystem_skills(self.repo_root)
        PolicyEngine()
        manifest = self.repo_root / "skills" / "manifest.json"
        if not manifest.exists():
            return BootstrapResult(generation, True, registry.names(), "repository-declared runtime reconstructed", registry)
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            entries = data["skills"]
            if not isinstance(entries, list):
                raise ValueError("skills manifest must contain a list")
            for entry in entries:
                if not isinstance(entry, dict) or set(entry) != {"name", "module"}:
                    raise ValueError("each skill entry must contain exactly name and module")
                name = entry["name"]
                module = entry["module"]
                if not isinstance(name, str) or not name or not isinstance(module, str):
                    raise ValueError("skill name and module must be non-empty strings")
                if registry.has(name):
                    raise ValueError(f"skill already registered: {name}")
                path = self._module_path(module)
                spec = importlib.util.spec_from_file_location(f"_ourob_skill_{name}", path)
                if spec is None or spec.loader is None:
                    raise ImportError(f"cannot load skill module: {module}")
                loaded = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(loaded)
                register = getattr(loaded, "register", None)
                if not callable(register):
                    raise AttributeError(f"skill module has no register(): {module}")
                before = registry.names()
                register(registry, name=name)
                after = registry.names()
                if len(after) != len(before) + 1 or not registry.has(name):
                    raise ValueError(f"skill registration contract violated: {name}")
        except (OSError, KeyError, TypeError, ValueError, ImportError, AttributeError, json.JSONDecodeError) as exc:
            return BootstrapResult(generation, False, (), f"skill bootstrap failed: {exc}")

        return BootstrapResult(generation, True, registry.names(), "repository-declared runtime reconstructed", registry)
