import json
from pathlib import Path

from ourob.bootstrap import Bootstrap


def test_bootstrap_requires_trust_inputs(tmp_path: Path) -> None:
    result = Bootstrap(tmp_path).load()
    assert not result.trusted


def test_bootstrap_reconstructs_filesystem_capability(tmp_path: Path) -> None:
    policies = tmp_path / "policies"
    verification = tmp_path / "verification"
    policies.mkdir()
    verification.mkdir()
    (policies / "constitution.json").write_text(json.dumps({"schema": "test"}), encoding="utf-8")
    (verification / "gates.json").write_text(json.dumps({"schema": "test"}), encoding="utf-8")
    result = Bootstrap(tmp_path).load()
    assert result.trusted
    assert "filesystem.read" in result.skills
    assert "filesystem.write" in result.skills
