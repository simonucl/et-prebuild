# test_initial_state.py
#
# Pytest suite that verifies the *initial* state of the workspace located at
# /home/user/dev_pipeline/ **before** the student runs any commands.
#
# The tests intentionally avoid checking for any files that are supposed to be
# created by the student’s solution (e.g., processed.log, error.log).  They only
# assert the required starting conditions.

from pathlib import Path
import os
import pytest

BASE_DIR = Path("/home/user/dev_pipeline")
INCOMING_DIR = BASE_DIR / "incoming"
ARCHIVE_DIR = BASE_DIR / "archive"
MANIFEST_FILE = BASE_DIR / "file_manifest.txt"

@pytest.mark.parametrize(
    "path, is_dir",
    [
        (BASE_DIR, True),
        (INCOMING_DIR, True),
        (ARCHIVE_DIR, True),
        (MANIFEST_FILE, False),
    ],
)
def test_required_paths_exist(path: Path, is_dir: bool):
    """
    Ensure that the core workspace paths exist and are of the expected type.
    """
    assert path.exists(), f"Expected path {path} to exist, but it is missing."
    if is_dir:
        assert path.is_dir(), f"Expected {path} to be a directory."
    else:
        assert path.is_file(), f"Expected {path} to be a regular file."


def test_incoming_contains_expected_files_only():
    """
    The incoming/ directory must contain exactly two CSV files:
    data_alpha.csv and data_beta.csv.  data_gamma.csv must *not* be present.
    """
    expected = {"data_alpha.csv", "data_beta.csv"}
    present = {p.name for p in INCOMING_DIR.iterdir() if p.is_file()}
    missing = expected - present
    unexpected = present - expected
    assert not missing, (
        f"The following expected files are missing from {INCOMING_DIR}: {', '.join(missing)}"
    )
    assert not unexpected, (
        f"The following unexpected files are present in {INCOMING_DIR}: {', '.join(unexpected)}"
    )
    assert not (INCOMING_DIR / "data_gamma.csv").exists(), (
        "data_gamma.csv must NOT exist in the incoming/ directory at the start."
    )


@pytest.mark.parametrize("csv_name", ["data_alpha.csv", "data_beta.csv"])
def test_csv_files_are_non_empty(csv_name):
    """
    Ensure that the CSV files present in incoming/ are non-empty.
    """
    csv_path = INCOMING_DIR / csv_name
    size = csv_path.stat().st_size
    assert size > 0, f"{csv_path} is empty; it should contain dummy data."


def test_archive_initially_empty():
    """
    The archive/ directory should start out empty (no CSV files in place yet).
    """
    archive_contents = [p for p in ARCHIVE_DIR.iterdir() if p.is_file()]
    assert not archive_contents, (
        f"archive/ should be empty before processing, "
        f"but found: {', '.join(p.name for p in archive_contents)}"
    )


def test_manifest_file_contents_exact():
    """
    file_manifest.txt must contain exactly the three filenames in order,
    each terminated by a single newline character, and no extra whitespace.
    """
    expected_content = "data_alpha.csv\ndata_beta.csv\ndata_gamma.csv\n"
    actual_content = MANIFEST_FILE.read_text(encoding="utf-8")
    assert actual_content == expected_content, (
        "file_manifest.txt does not contain the expected content.\n"
        f"Expected (repr): {repr(expected_content)}\n"
        f"Actual   (repr): {repr(actual_content)}"
    )