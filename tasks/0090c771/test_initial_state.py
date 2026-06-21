# test_initial_state.py
#
# Pytest suite that validates the on-disk state *before* the student carries
# out any actions.  It confirms that the pre-populated working directory
# (/home/user/production_data) exists exactly as specified and contains the
# correct files with the precise content expected.  It intentionally *does not*
# test for the presence or absence of any output artefacts the student is
# supposed to create later (e.g. backups, tarballs, integrity reports).

import os
from pathlib import Path

import pytest

# Absolute base path to the directory that must already exist
BASE_DIR = Path("/home/user/production_data").resolve()

# Expected directory tree and file contents (relative path -> exact text content)
EXPECTED_FILES = {
    "docs/report.txt": "Daily sales report\n",
    "images/logo.png": "PNG_PLACEHOLDER\n",
    "config/app.conf": "env=prod\nversion=1.2.0\n",
    "config/db.conf": "host=localhost\nport=5432\n",
}


def _collect_actual_files(base: Path):
    """
    Recursively collect all regular files under `base` and return a
    dictionary mapping RELATIVE paths (POSIX style) to absolute Path
    objects.
    """
    actual = {}
    for path in base.rglob("*"):
        if path.is_file():
            rel = path.relative_to(base).as_posix()
            actual[rel] = path
    return actual


def test_base_directory_exists_and_is_dir():
    assert BASE_DIR.exists(), f"Required directory '{BASE_DIR}' is missing."
    assert BASE_DIR.is_dir(), f"'{BASE_DIR}' exists but is not a directory."


def test_expected_files_exist_with_correct_content():
    """
    Verify that every expected file exists with exactly the required content.
    """
    for rel_path, expected_content in EXPECTED_FILES.items():
        abs_path = BASE_DIR / rel_path
        assert abs_path.exists(), f"Missing expected file: '{abs_path}'."
        assert abs_path.is_file(), f"'{abs_path}' exists but is not a regular file."
        # Read in binary, then decode via utf-8 to catch encoding issues exactly.
        actual_content = abs_path.read_bytes().decode("utf-8", errors="strict")
        assert (
            actual_content == expected_content
        ), (
            f"Content mismatch for '{abs_path}'.\n"
            f"Expected ({len(expected_content)} bytes): {repr(expected_content)}\n"
            f"Found    ({len(actual_content)} bytes): {repr(actual_content)}"
        )


def test_no_extra_or_missing_files():
    """
    Ensure there are *exactly* the four expected files (no more, no less)
    anywhere under /home/user/production_data.
    """
    actual_files = _collect_actual_files(BASE_DIR)

    missing = set(EXPECTED_FILES) - set(actual_files)
    extra = set(actual_files) - set(EXPECTED_FILES)

    # Provide detailed diagnostics in assertion messages
    messages = []
    if missing:
        messages.append(f"Missing file(s): {', '.join(sorted(missing))}")
    if extra:
        messages.append(f"Unexpected extra file(s): {', '.join(sorted(extra))}")

    assert not (missing or extra), " ; ".join(messages) or "File set mismatch detected."