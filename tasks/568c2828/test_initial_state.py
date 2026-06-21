# test_initial_state.py
#
# This test-suite verifies that the *initial* filesystem state that ships
# with the exercise is exactly what the assignment description promises.
# It deliberately checks *before* the student has had a chance to create
# the validation directory or any report artefacts.
#
# Only the Python stdlib and pytest are used.

import json
import os
import re
from pathlib import Path

import pytest

HOME = Path("/home/user")
BASE_DIR = HOME / "backup_sim"
BACKUPS_DIR = BASE_DIR / "backups"
SCHEMA_DIR = BASE_DIR / "schema"
VALIDATION_DIR = BASE_DIR / "validation"

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def is_hex32(s: str) -> bool:
    """Return True iff *s* is exactly 32 hex chars (upper/lower mixed)."""
    return bool(re.fullmatch(r"[a-fA-F0-9]{32}", s))


def load_json(path: Path):
    """Load JSON from *path* with a readable error if it fails."""
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as e:
        pytest.fail(
            f"File '{path}' is expected to be valid JSON at test-time but "
            f"failed to parse: {e}"
        )


# --------------------------------------------------------------------------- #
# Structural tests (directories / files present)
# --------------------------------------------------------------------------- #

def test_directory_tree_present():
    # Top-level directory
    assert BASE_DIR.is_dir(), f"Missing directory {BASE_DIR}"
    # backups/ sub-directory
    assert BACKUPS_DIR.is_dir(), f"Missing directory {BACKUPS_DIR}"
    # schema/ sub-directory
    assert SCHEMA_DIR.is_dir(), f"Missing directory {SCHEMA_DIR}"


@pytest.mark.parametrize(
    "filename",
    [
        "backup_2023-11-01.json",
        "backup_2023-12-06.json",
        "backup_2023-12-20.json",
    ],
)
def test_each_backup_file_exists(filename):
    path = BACKUPS_DIR / filename
    assert path.is_file(), f"Expected backup file '{path}' to exist"


def test_schema_file_exists():
    schema_path = SCHEMA_DIR / "backup_schema.json"
    assert schema_path.is_file(), f"Expected schema file '{schema_path}' to exist"


def test_validation_directory_absent_initially():
    assert not VALIDATION_DIR.exists(), (
        f"The directory {VALIDATION_DIR} should NOT exist before the student "
        "runs their solution"
    )


# --------------------------------------------------------------------------- #
# Content tests for the three shipped backup files
# --------------------------------------------------------------------------- #

REQUIRED_TOP_LEVEL_KEYS = {"backupDate", "hostname", "files"}
REQUIRED_FILE_KEYS = {"path", "sha256"}


def _basic_schema_checks(data, source_path: Path):
    """A *very* small subset of the full JSON schema, sufficient for tests."""
    missing = REQUIRED_TOP_LEVEL_KEYS - data.keys()
    assert not missing, (
        f"{source_path.name} is missing top-level keys: {', '.join(sorted(missing))}"
    )

    # files -> array of objects
    files = data["files"]
    assert isinstance(files, list), f"{source_path.name}: 'files' must be a list"
    assert files, f"{source_path.name}: 'files' list must not be empty"

    for idx, item in enumerate(files):
        assert isinstance(item, dict), (
            f"{source_path.name}: item #{idx} in 'files' is not an object"
        )
        miss_item = REQUIRED_FILE_KEYS - item.keys()
        assert not miss_item, (
            f"{source_path.name}: item #{idx} missing keys "
            f"{', '.join(sorted(miss_item))}"
        )
        sha = item["sha256"]
        assert is_hex32(sha), (
            f"{source_path.name}: item #{idx} has invalid sha256 '{sha}' "
            "(must be 32 hex chars)"
        )


def test_backup_2023_11_01_valid():
    path = BACKUPS_DIR / "backup_2023-11-01.json"
    data = load_json(path)
    _basic_schema_checks(data, path)


def test_backup_2023_12_20_valid():
    path = BACKUPS_DIR / "backup_2023-12-20.json"
    data = load_json(path)
    _basic_schema_checks(data, path)


def test_backup_2023_12_06_is_invalid_json():
    """
    The exercise purposefully ships this file with an embedded C-style comment,
    which violates the JSON spec.  Parsing must therefore raise
    json.JSONDecodeError.  We assert that here so that the start-state is
    exactly as documented.
    """
    path = BACKUPS_DIR / "backup_2023-12-06.json"

    with path.open("r", encoding="utf-8") as fh:
        content = fh.read()

    # Quick sanity-check that we're indeed looking at the right file
    assert "/*" in content, (
        f"Expected an inline comment in {path.name} but none was found; "
        "the file may have been modified."
    )

    # Attempt to parse and expect a JSONDecodeError
    with pytest.raises(json.JSONDecodeError):
        json.loads(content)