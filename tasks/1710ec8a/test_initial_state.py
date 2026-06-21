# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state before the
# student’s backup script runs.  Only the pre-existing source data is
# inspected; no assertions are made about any of the files or directories
# that the student is expected to create later under /home/user/backups.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
DATA_DIR = HOME / "data"
FILE_A = DATA_DIR / "file_a.txt"
FILE_B = DATA_DIR / "file_b.txt"

EXPECTED_CONTENTS = {
    FILE_A: "Alpha\n",
    FILE_B: "Beta\n",
}


def _read_file(path: Path) -> str:
    """Return the *text* contents of a file, raising a helpful error if it
    cannot be read."""
    try:
        with path.open("r", encoding="utf-8") as fp:
            return fp.read()
    except FileNotFoundError:
        pytest.fail(f"Required file is missing: {path}")
    except PermissionError:
        pytest.fail(f"Required file exists but is not readable: {path}")


def test_data_directory_exists_and_is_directory():
    assert DATA_DIR.exists(), f"Directory {DATA_DIR} is missing."
    assert DATA_DIR.is_dir(), f"Expected {DATA_DIR} to be a directory."


@pytest.mark.parametrize("path", [FILE_A, FILE_B])
def test_required_files_exist(path: Path):
    assert path.exists(), f"Required file is missing: {path}"
    assert path.is_file(), f"Expected {path} to be a regular file."


def test_required_files_contents_and_size():
    for path, expected_text in EXPECTED_CONTENTS.items():
        actual_text = _read_file(path)
        assert (
            actual_text == expected_text
        ), f"Contents of {path} did not match the expected text."

        # Verify file size matches expected number of bytes.
        expected_size = len(expected_text.encode("utf-8"))
        actual_size = path.stat().st_size
        assert (
            actual_size == expected_size
        ), f"Size of {path} was {actual_size} bytes, expected {expected_size} bytes."


def test_data_directory_contains_only_expected_files():
    """Ensure no unexpected extra files are present in the data directory."""
    expected_names = {p.name for p in EXPECTED_CONTENTS.keys()}
    dir_listing = {p.name for p in DATA_DIR.iterdir() if p.is_file()}
    unexpected = dir_listing - expected_names
    assert (
        not unexpected
    ), f"Unexpected file(s) found in {DATA_DIR}: {', '.join(sorted(unexpected))}"