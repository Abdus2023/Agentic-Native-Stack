#!/usr/bin/env python3
"""Structural lint for HARĒNA SKILL.md files; standard library only.

This checks identity/frontmatter and the minimum content contract. It does not
validate YAML fully, semantic correctness, security, workflow behavior, links,
runtime discovery, or domain claims.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SECTION_ALIASES = {
    "purpose": {"purpose"},
    "activation": {"activation", "trigger", "triggers", "when to use"},
    "inputs": {"inputs", "input", "preconditions", "inputs and preconditions", "required evidence", "intake"},
    "procedure": {"procedure", "audit procedure", "required workflow", "workflow", "steps"},
    "outputs": {"outputs", "output", "output format", "completion report format", "final report", "deliverables"},
    "failure handling": {"failure handling", "failure handling and stop conditions", "stop conditions", "error handling", "failure modes"},
    "acceptance criteria": {"acceptance criteria", "acceptance checklist", "acceptance", "verification checklist"},
}

def parse_frontmatter(text: str):
    errors = []
    if not text.startswith("---\n"):
        return {}, ["missing YAML frontmatter opening delimiter"]
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, ["missing YAML frontmatter closing delimiter"]
    fields = {}
    for line_no, line in enumerate(text[4:end].splitlines(), 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"frontmatter line {line_no}: expected key: value")
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if not key:
            errors.append(f"frontmatter line {line_no}: empty key")
            continue
        if key in fields:
            errors.append(f"duplicate frontmatter key: {key}")
        fields[key] = value.strip(chr(34) + chr(39))
    return fields, errors

def validate(path: Path):
    errors = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"cannot read UTF-8 skill file: {exc}"]
    fields, fm_errors = parse_frontmatter(text)
    errors.extend(fm_errors)
    name, description = fields.get("name", ""), fields.get("description", "")
    if not name:
        errors.append("frontmatter missing name")
    elif not NAME_RE.fullmatch(name):
        errors.append(f"invalid skill name: {name!r}")
    elif path.parent.name != name:
        errors.append(f"skill name {name!r} does not match directory {path.parent.name!r}")
    if not description:
        errors.append("frontmatter missing description")
    headings = {re.sub(r"\s+", " ", m.group(1).strip().lower())
                for m in re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, re.M)}
    for section, aliases in SECTION_ALIASES.items():
        if not headings.intersection(aliases):
            errors.append(f"missing required section: {section} (accepted: {', '.join(sorted(aliases))})")
    if len(text.strip()) < 250:
        errors.append("skill is unusually short; review completeness")
    return errors

def main():
    if len(sys.argv) != 2:
        print("Usage: validate_skill.py <skill-file-or-directory>", file=sys.stderr)
        return 2
    target = Path(sys.argv[1])
    if not target.exists():
        print(f"ERROR: path does not exist: {target}")
        return 1
    paths = [target] if target.is_file() else sorted(target.rglob("SKILL.md"))
    if not paths:
        print(f"ERROR: no SKILL.md files found under {target}")
        return 1
    failed = False
    for path in paths:
        errors = validate(path)
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path}")
    print(f"RESULT: {'FAIL' if failed else 'PASS'} ({len(paths)} skill file(s))")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
