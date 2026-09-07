from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from ourob.bootstrap import Bootstrap
from ourob.journal import Journal
from ourob.kernel import Kernel
from ourob.model import Action, ActionKind
from ourob.policy import PolicyEngine
from ourob.skills import filesystem_skills


def test_self_extension_cold_bootstrap() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "policies").mkdir()
        (root / "verification").mkdir()
        (root / "skills").mkdir()
        (root / "policies" / "constitution.json").write_text(
            '{"schema":"ourob.constitution.v1","mode":"fail_closed","invariants":[]}', encoding="utf-8"
        )
        (root / "verification" / "gates.json").write_text(
            '{"schema":"ourob.gates.v1","gates":[]}', encoding="utf-8"
        )
        (root / "skills" / "__init__.py").write_text("", encoding="utf-8")
        (root / "skills" / "manifest.json").write_text('{"skills":[]}', encoding="utf-8")

        kernel = Kernel(root, PolicyEngine(), filesystem_skills(root), Journal(root / ".ourob" / "journal.jsonl"))
        run = kernel.create_run("Add greet capability")
        kernel.plan(run)
        kernel.authorize(run)

        source = '''from ourob.model import ActionKind\nfrom ourob.skills import Skill\n\ndef register(registry, name="greet"):\n    registry.register(Skill(name, frozenset({ActionKind.EXECUTE}), lambda action: f"Hello, {action.arguments['name']}!"))\n'''
        action = Action(uuid4().hex, ActionKind.WRITE, "filesystem.write", {"path": "skills/greet.py", "content": source})
        assert kernel.execute(run, action).ok

        (root / "skills" / "manifest.json").write_text(
            json.dumps({"skills": [{"name": "greet", "module": "skills.greet"}]}), encoding="utf-8"
        )

        boot = Bootstrap(root).load()
        assert boot.trusted
        assert "greet" in boot.skills
