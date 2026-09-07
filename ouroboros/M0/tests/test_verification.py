from pathlib import Path
import sys

from ourob.model import VerificationStatus
from ourob.verify import Gate, Verifier


def test_verification_pass_is_generation_bound(tmp_path: Path) -> None:
    (tmp_path / "ourob").mkdir()
    (tmp_path / "ourob" / "ok.py").write_text("x = 1\n", encoding="utf-8")
    report = Verifier(tmp_path, (Gate("compile", (sys.executable, "-m", "compileall", "-q", "ourob")),)).verify(3)
    assert report.passed
    result = report.results[0]
    assert result.status is VerificationStatus.PASS
    assert result.generation == report.generation
    assert result.epoch == 3
    assert result.evidence_id


def test_missing_required_gate_is_blocked(tmp_path: Path) -> None:
    report = Verifier(tmp_path, (Gate("missing", ("definitely-not-a-real-command",)),)).verify(1)
    assert report.results[0].status is VerificationStatus.BLOCKED


def test_gate_contract_is_order_independent(tmp_path: Path) -> None:
    a = Gate("a", ("python", "-c", "print(1)"), True)
    b = Gate("b", ("python", "-c", "print(2)"), False)
    assert Verifier(tmp_path, (a, b)).gate_set_digest == Verifier(tmp_path, (b, a)).gate_set_digest


def test_gate_contract_changes_for_required_or_command(tmp_path: Path) -> None:
    base = Gate("gate", ("python", "-c", "print(1)"), True)
    optional = Gate("gate", base.command, False)
    changed = Gate("gate", ("python", "-c", "print(2)"), True)
    assert Verifier(tmp_path, (base,)).gate_set_digest != Verifier(tmp_path, (optional,)).gate_set_digest
    assert Verifier(tmp_path, (base,)).gate_set_digest != Verifier(tmp_path, (changed,)).gate_set_digest


def test_gate_contract_preserves_argument_boundaries(tmp_path: Path) -> None:
    first = Gate("gate", ("tool", "arg with spaces"))
    second = Gate("gate", ("tool", "arg", "with spaces"))
    assert Verifier(tmp_path, (first,)).gate_set_digest != Verifier(tmp_path, (second,)).gate_set_digest
