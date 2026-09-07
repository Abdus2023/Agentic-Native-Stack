from pathlib import Path

import pytest

from ourob.journal import Journal, JournalIntegrityError
from ourob.trust import JournalTrustAnchor, verify_trust_anchor


def _journal(tmp_path: Path) -> Journal:
    journal = Journal(tmp_path / "journal.jsonl")
    journal.append("RUN_CREATED", run_id="r1", generation="g1", task="demo")
    journal.append("PLAN_ACCEPTED", run_id="r1", generation="g1")
    return journal


def test_trust_anchor_round_trips_and_verifies(tmp_path: Path) -> None:
    journal = _journal(tmp_path)
    records = journal.read()
    anchor = JournalTrustAnchor(2, records[1]["digest"], "g1")

    assert JournalTrustAnchor.from_record(anchor.to_record()) == anchor
    assert journal.read_trusted(anchor) == records
    assert len(anchor.record_binding) == 64


def test_trust_anchor_rejects_whole_history_rewrite(tmp_path: Path) -> None:
    journal = _journal(tmp_path)
    records = journal.read()
    anchor = JournalTrustAnchor(2, records[1]["digest"], "g1")

    # Rebuild a self-consistent chain with different content. Ordinary hash
    # validation accepts it; the external checkpoint must reject it.
    replacement = Journal(tmp_path / "rewritten.jsonl")
    replacement.append("RUN_CREATED", run_id="attacker", generation="g1", task="rewritten")
    replacement.append("PLAN_ACCEPTED", run_id="attacker", generation="g1")

    with pytest.raises(JournalIntegrityError, match="trusted checkpoint digest mismatch"):
        replacement.read_trusted(anchor)


def test_trust_anchor_rejects_truncation_before_checkpoint(tmp_path: Path) -> None:
    journal = _journal(tmp_path)
    records = journal.read()
    anchor = JournalTrustAnchor(2, records[1]["digest"], "g1")

    path = journal.path
    path.write_text(path.read_text(encoding="utf-8").splitlines()[0] + "\n", encoding="utf-8")

    with pytest.raises(JournalIntegrityError, match="journal is shorter than trusted checkpoint"):
        journal.read_trusted(anchor)


def test_trust_anchor_generation_binding_is_optional_but_enforceable(tmp_path: Path) -> None:
    journal = _journal(tmp_path)
    records = journal.read()
    anchor = JournalTrustAnchor(1, records[0]["digest"], "wrong-generation")

    with pytest.raises(JournalIntegrityError, match="trusted checkpoint generation mismatch"):
        verify_trust_anchor(records, anchor)
