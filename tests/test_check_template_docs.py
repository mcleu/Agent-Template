from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class DocumentationValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.fixture_root = Path(self.temporary_directory.name) / "fixture"
        shutil.copytree(
            REPOSITORY_ROOT,
            self.fixture_root,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_validator(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "scripts/check_template_docs.py"],
            cwd=self.fixture_root,
            check=False,
            capture_output=True,
            text=True,
        )

    def replace_once(self, relative_path: str, old: str, new: str) -> None:
        path = self.fixture_root / relative_path
        content = path.read_text(encoding="utf-8")
        self.assertEqual(content.count(old), 1, f"expected one match for {old!r}")
        path.write_text(content.replace(old, new, 1), encoding="utf-8")

    def test_current_repository_passes(self) -> None:
        result = self.run_validator()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Latest supported schema version: 1", result.stdout)

    def test_rejects_incorrect_metadata_scalar_types(self) -> None:
        self.replace_once("AGENTS.template.md", "schema_version: 1", 'schema_version: "1"')
        self.replace_once(
            "AGENTS.template.md", 'document_version: "1.0"', "document_version: 1.0"
        )
        self.replace_once(
            "AGENTS.template.md", 'last_edited: "2026-08-05"', "last_edited: 2026-08-05"
        )

        result = self.run_validator()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema_version must be an unquoted integer", result.stderr)
        self.assertIn("document_version must be a quoted string", result.stderr)
        self.assertIn("last_edited must be a quoted date string", result.stderr)

    def test_rejects_duplicate_document_control_sections(self) -> None:
        path = self.fixture_root / "README.md"
        duplicate = (
            "## Document control\n\n"
            "**Last edited:** 1999-01-01\n\n"
            "**Current version:** 9.9\n\n"
            "| Version | Date | Change |\n"
            "| --- | --- | --- |\n"
            "| 9.9 | 1999-01-01 | Stale duplicate fixture. |\n\n"
        )
        path.write_text(duplicate + path.read_text(encoding="utf-8"), encoding="utf-8")

        result = self.run_validator()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must contain exactly one Document control section", result.stderr)

    def test_rejects_missing_repository_absolute_link(self) -> None:
        path = self.fixture_root / "README.md"
        content = path.read_text(encoding="utf-8")
        path.write_text(
            content.replace(
                "# Agent Template\n",
                "# Agent Template\n\n[Broken fixture](/definitely-missing.md)\n",
                1,
            ),
            encoding="utf-8",
        )

        result = self.run_validator()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("/definitely-missing.md: missing target component", result.stderr)

    def test_discovers_and_accepts_complete_v2_schema(self) -> None:
        source = self.fixture_root / "schemas" / "v1"
        destination = self.fixture_root / "schemas" / "v2"
        shutil.copytree(source, destination)
        for path in destination.glob("*.md"):
            content = path.read_text(encoding="utf-8")
            content = content.replace("schema_version: 1", "schema_version: 2")
            content = content.replace("schema-contract-v1", "schema-contract-v2")
            content = content.replace("schema v1", "schema v2")
            content = content.replace("Schema v1", "Schema v2")
            path.write_text(content, encoding="utf-8")

        result = self.run_validator()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Latest supported schema version: 2", result.stdout)


if __name__ == "__main__":
    unittest.main()
