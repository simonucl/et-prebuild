# test_initial_state.py
#
# This test-suite validates that the operating-system is in the expected
# *initial* state before the student performs any actions.  It checks only
# the pre-existing “/home/user/backup/source” tree and **does not** look for
# any artefacts that the student has yet to create (archives, logs, restore
# dirs, …).

import hashlib
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
SOURCE_ROOT = HOME / "backup" / "source"

# --------------------------------------------------------------------------- #
# Helper data: the files that must already exist and their exact contents
# --------------------------------------------------------------------------- #
EXPECTED_FILES = {
    SOURCE_ROOT / "documents" / "report.txt": (
        "Quarterly report Q1 2021\n"
        "All figures in USD.\n"
        "END\n"
    ),
    SOURCE_ROOT / "images" / "logo.png": "PNG_PLACEHOLDER\n",
    SOURCE_ROOT / "scripts" / "backup.sh": (
        "#!/usr/bin/env bash\n"
        "# Simple maintenance script\n"
        'echo "Backup completed."\n'
    ),
    SOURCE_ROOT / "data" / "sample.csv": (
        "id,name,score\n"
        "1,Alice,83\n"
        "2,Bob,91\n"
        "3,Charlie,78\n"
    ),
    SOURCE_ROOT / "notes" / "todo.md": (
        "# TODO\n"
        "- Verify backups\n"
        "- Document retention policy\n"
        "- Schedule incremental jobs\n"
    ),
}


# --------------------------------------------------------------------------- #
# Utility
# --------------------------------------------------------------------------- #
def sha256_of_string(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_source_root_exists_and_is_dir():
    assert SOURCE_ROOT.exists(), f"Required directory {SOURCE_ROOT} is missing."
    assert SOURCE_ROOT.is_dir(), f"{SOURCE_ROOT} exists but is not a directory."


@pytest.mark.parametrize("path,expected_content", EXPECTED_FILES.items())
def test_required_file_exists_with_correct_content(path: Path, expected_content: str):
    # 1. Path existence and type
    assert path.exists(), f"Required file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."

    # 2. Content integrity
    with path.open("r", encoding="utf-8") as fh:
        actual_content = fh.read()

    # Short-circuit to avoid spewing the entire file on failure; compare hashes.
    exp_hash, act_hash = sha256_of_string(expected_content), sha256_of_string(actual_content)
    assert act_hash == exp_hash, (
        f"File {path} exists but its contents differ from the expected initial "
        f"state.\nExpected SHA-256: {exp_hash}\nActual   SHA-256: {act_hash}"
    )