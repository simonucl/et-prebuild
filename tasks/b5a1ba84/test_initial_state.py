# test_initial_state.py
#
# This test-suite validates the **pre-existing** state of the filesystem
# before the student runs any commands.  It intentionally does *not* test
# for the archive produced by the student’s task; it only checks that the
# initial directories and log files are in place and contain the expected
# sample text.

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
CI_DIR = HOME / "mobile_ci"
PIPELINE_DIR = CI_DIR / "pipeline_reports"
ARCHIVES_DIR = CI_DIR / "archives"

EXPECTED_DIRS = [
    CI_DIR,
    PIPELINE_DIR,
    ARCHIVES_DIR,
]

EXPECTED_FILES = {
    PIPELINE_DIR / "compile.log": "Compilation completed successfully.\n",
    PIPELINE_DIR / "unit_test.log": "All 128 unit tests passed.\n",
    PIPELINE_DIR / "integration_test.log": "Integration suite finished OK.\n",
}


def _is_regular_file(path: Path) -> bool:
    try:
        return stat.S_ISREG(path.stat().st_mode)
    except FileNotFoundError:
        return False


@pytest.mark.parametrize("directory", EXPECTED_DIRS)
def test_required_directories_exist(directory: Path):
    """All required directories must exist before the task starts."""
    assert directory.exists(), f"Missing required directory: {directory}"
    assert directory.is_dir(), f"Expected {directory} to be a directory."


@pytest.mark.parametrize("file_path,expected_contents", EXPECTED_FILES.items())
def test_log_files_exist_and_are_regular(file_path: Path, expected_contents: str):
    """Verify that each expected log file exists and is a regular file."""
    assert file_path.exists(), f"Missing required log file: {file_path}"
    assert _is_regular_file(file_path), f"{file_path} exists but is not a regular file"


@pytest.mark.parametrize("file_path,expected_contents", EXPECTED_FILES.items())
def test_log_file_contents_exact(file_path: Path, expected_contents: str):
    """
    Ensure each log file contains the exact one-line sample text ending with a newline.
    The student task must *not* modify these files, so their initial contents matter.
    """
    with open(file_path, "r", encoding="utf-8") as fp:
        actual = fp.read()
    assert (
        actual == expected_contents
    ), f"Unexpected contents in {file_path!s}.\nExpected: {expected_contents!r}\nGot:      {actual!r}"