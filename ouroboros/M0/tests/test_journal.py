from pathlib import Path

import pytest

from ourob.journal import Journal, JournalIntegrityError


def test_journal_is_hash_chained(tmp_path: Path) -> None:
    journal = Journal(tmp_path / "journal.jsonl")
    first = journal.append("RUN_CREATED", run_id="r1", generation="g1", task="demo")
    second = journal.append("PLAN_ACCEPTED", run_id="r1", generation="g1")

    assert first["sequence"] == 1
    assert first["previous_digest"] == "0" * 64
    assert second["sequence"] == 2
    assert second["previous_digest"] == first["digest"]
    assert len(second["digest"]) == 64
    assert journal.read() == [first, second]


def test_journal_detects_tampering(tmp_path: Path) -> None:
    path = tmp_path / "journal.jsonl"
    journal = Journal(path)
    journal.append("RUN_CREATED", run_id="r1", generation="g1", task="demo")
    journal.append("PLAN_ACCEPTED", run_id="r1", generation="g1")
    lines = path.read_text(encoding="utf-8").splitlines()
    lines[0] = lines[0].replace('"task":"demo"', '"task":"tampered"')
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with pytest.raises(JournalIntegrityError, match="invalid journal digest"):
        journal.read()


def test_journal_detects_truncated_or_malformed_tail(tmp_path: Path) -> None:
    path = tmp_path / "journal.jsonl"
    journal = Journal(path)
    journal.append("RUN_CREATED", run_id="r1", generation="g1", task="demo")
    with path.open("a", encoding="utf-8") as handle:
        handle.write('{"event":"ACTION_EXECUTED"')

    with pytest.raises(JournalIntegrityError, match="invalid JSON"):
        journal.read()


def test_append_refuses_to_continue_after_corruption(tmp_path: Path) -> None:
    path = tmp_path / "journal.jsonl"
    journal = Journal(path)
    journal.append("RUN_CREATED", run_id="r1", generation="g1", task="demo")
    path.write_text(path.read_text(encoding="utf-8") + "not-json\n", encoding="utf-8")

    with pytest.raises(JournalIntegrityError):
        journal.append("PLAN_ACCEPTED", run_id="r1", generation="g1")
