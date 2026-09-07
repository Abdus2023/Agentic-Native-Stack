from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

DEFAULT_EXCLUDED_NAMES = frozenset({".git", ".ourob", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"})


@dataclass(frozen=True)
class ManifestEntry:
    path: str
    digest: str
    size: int


@dataclass(frozen=True)
class RepositoryGeneration:
    id: str
    entries: tuple[ManifestEntry, ...]


def _included(path: Path, root: Path, excluded: frozenset[str]) -> bool:
    relative = path.relative_to(root)
    return not any(part in excluded for part in relative.parts)


def build_manifest(root: Path, excluded: frozenset[str] = DEFAULT_EXCLUDED_NAMES) -> tuple[ManifestEntry, ...]:
    root = root.resolve()
    entries: list[ManifestEntry] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or not _included(path, root, excluded):
            continue
        data = path.read_bytes()
        entries.append(ManifestEntry(path.relative_to(root).as_posix(), sha256(data).hexdigest(), len(data)))
    return tuple(entries)


def canonical_manifest(entries: tuple[ManifestEntry, ...]) -> bytes:
    lines = [f"{entry.path}\0{entry.digest}\0{entry.size}" for entry in entries]
    return ("\n".join(lines) + "\n").encode("utf-8") if lines else b""


def repository_generation(root: Path, excluded: frozenset[str] = DEFAULT_EXCLUDED_NAMES) -> RepositoryGeneration:
    entries = build_manifest(root, excluded)
    return RepositoryGeneration(sha256(canonical_manifest(entries)).hexdigest(), entries)
