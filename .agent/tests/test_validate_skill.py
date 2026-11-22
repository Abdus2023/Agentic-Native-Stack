#!/usr/bin/env python3
"""Unit tests for validate_skill.py; standard library only."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "tools" / "validate_skill.py"
SPEC = importlib.util.spec_from_file_location("validator", SOURCE)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

VALID = """---
name: sample-skill
description: Test skill.
---
# Sample
## Purpose
A sufficiently detailed purpose.
## Trigger
Use in this test.
## Preconditions
A value.
## Audit procedure
1. Inspect.
## Output format
A result.
## Stop conditions
Stop on failure.
## Acceptance checklist
The test passes.
"""

class ValidatorTests(unittest.TestCase):
    def validate_body(self, folder, body):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / folder / "SKILL.md"
            path.parent.mkdir()
            path.write_text(body, encoding="utf-8")
            return MODULE.validate(path)

    def test_valid_skill_with_heading_aliases_passes(self):
        self.assertEqual([], self.validate_body("sample-skill", VALID))

    def test_directory_name_mismatch_fails(self):
        self.assertTrue(any("does not match directory" in e for e in self.validate_body("wrong-folder", VALID)))

    def test_missing_description_fails(self):
        bad = VALID.replace("description: Test skill.\n", "")
        self.assertTrue(any("description" in e for e in self.validate_body("sample-skill", bad)))

    def test_missing_required_section_fails(self):
        bad = VALID.replace("## Audit procedure\n1. Inspect.\n", "")
        self.assertTrue(any("missing required section: procedure" in e for e in self.validate_body("sample-skill", bad)))

    def test_missing_frontmatter_delimiter_fails(self):
        bad = VALID.replace("\n---\n", "\n", 1)
        self.assertTrue(any("closing delimiter" in e for e in self.validate_body("sample-skill", bad)))

    def test_duplicate_frontmatter_key_fails(self):
        bad = VALID.replace("description: Test skill.\n", "description: Test skill.\ndescription: Duplicate.\n")
        self.assertTrue(any("duplicate frontmatter key" in e for e in self.validate_body("sample-skill", bad)))

    def test_invalid_name_fails(self):
        bad = VALID.replace("name: sample-skill", "name: Sample_Skill")
        self.assertTrue(any("invalid skill name" in e for e in self.validate_body("Sample_Skill", bad)))

    def test_empty_directory_cli_reports_no_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(SOURCE), tmp], capture_output=True, text=True)
            self.assertEqual(1, result.returncode)
            self.assertIn("no SKILL.md files", result.stdout)

    def test_missing_file_returns_error(self):
        self.assertTrue(any("cannot read" in e for e in MODULE.validate(Path("/definitely/not/a/SKILL.md"))))

if __name__ == "__main__":
    unittest.main()
