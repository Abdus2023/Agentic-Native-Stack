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
