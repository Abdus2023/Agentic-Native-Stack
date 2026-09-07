from pathlib import Path

from ourob.generation import repository_generation


def test_generation_is_deterministic(tmp_path: Path) -> None:
    (tmp_path / "b.txt").write_text("b", encoding="utf-8")
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    first = repository_generation(tmp_path)
    second = repository_generation(tmp_path)
    assert first.id == second.id
    assert [entry.path for entry in first.entries] == ["a.txt", "b.txt"]


def test_excluded_runtime_state_does_not_change_generation(tmp_path: Path) -> None:
    (tmp_path / "x.txt").write_text("x", encoding="utf-8")
    (tmp_path / ".ourob").mkdir()
    before = repository_generation(tmp_path).id
    (tmp_path / ".ourob" / "journal.jsonl").write_text("event", encoding="utf-8")
    assert repository_generation(tmp_path).id == before
