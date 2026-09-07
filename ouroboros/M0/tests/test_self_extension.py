from __future__ import annotations

import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from uuid import uuid4

from ourob.bootstrap import Bootstrap
from ourob.journal import Journal
from ourob.kernel import Kernel
from ourob.model import Action, ActionKind
from ourob.policy import PolicyEngine
from ourob.skills import filesystem_skills
from ourob.verify import Gate, Verifier


def test_self_extension_full_closed_loop() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "policies").mkdir()
        (root / "verification").mkdir()
        (root / "skills").mkdir()
        (root / "policies" / "constitution.json").write_text(
            '{"schema":"ourob.constitution.v1","mode":"fail_closed","invariants":[]}', encoding="utf-8"
        )
        (root / "verification" / "gates.json").write_text(
            '{"schema":"ourob.gates.v1","gates":[{"name":"compile-skills","command":["python","-m","compileall","-q","skills"],"required":true}]}', encoding="utf-8"
        )
        (root / "skills" / "__init__.py").write_text("", encoding="utf-8")
        (root / "skills" / "manifest.json").write_text('{"skills":[]}', encoding="utf-8")

        kernel = Kernel(
            root, PolicyEngine(), filesystem_skills(root), Journal(root / ".ourob" / "journal.jsonl"),
            verifier=Verifier(root, (Gate("compile-skills", (sys.executable, "-m", "compileall", "-q", "skills")),)),
        )
        run = kernel.create_run("Add greet capability")
        kernel.plan(run)
        kernel.authorize(run)

        source = '''from ourob.model import ActionKind\nfrom ourob.skills import Skill\n\ndef register(registry, name="greet"):\n    registry.register(Skill(name, frozenset({ActionKind.EXECUTE}), lambda action: f"Hello, {action.arguments['name']}!"))\n'''
        assert kernel.execute(run, Action(uuid4().hex, ActionKind.WRITE, "filesystem.write", {"path": "skills/greet.py", "content": source})).ok
        manifest = json.dumps({"skills": [{"name": "greet", "module": "skills.greet"}]})
        assert kernel.execute(run, Action(uuid4().hex, ActionKind.WRITE, "filesystem.write", {"path": "skills/manifest.json", "content": manifest})).ok

        results = kernel.verify(run)
        assert results and all(result.status.value == "PASS" for result in results)
        kernel.promote(run)

        boot = Bootstrap(root).load()
        assert boot.trusted
        assert "greet" in boot.skills

        # Prove the reconstructed capability executes after cold bootstrap.
        registry = filesystem_skills(root)
        import importlib
        sys.path.insert(0, str(root))
        try:
            importlib.import_module("skills.greet").register(registry, name="greet")
        finally:
            sys.path.remove(str(root))
        observation = registry.execute(Action(uuid4().hex, ActionKind.EXECUTE, "greet", {"name": "World"}))
        assert observation.ok
        assert observation.result == "Hello, World!"


def test_protected_surface_is_denied_by_policy() -> None:
    policy = PolicyEngine()
    action = Action(uuid4().hex, ActionKind.WRITE, "filesystem.write", {"path": "ourob/kernel.py", "content": "# attack"})
    decision = policy.evaluate(action)
    assert not decision.allowed
