# test_initial_state.py
#
# This test-suite verifies the **initial** filesystem state *before* the
# student starts working on the “backup automation” assignment.
#
# It checks that only the seed data set is present and that none of the
# artefacts the Makefile is supposed to create (Makefile itself, backups/,
# logs/, …) exist yet.
#
# The tests purposefully fail with clear, instructive messages when the
# expected pristine state is not found.

from pathlib import Path
import pytest

# Base paths used throughout the suite
HOME = Path("/home/user")
PROJECT = HOME / "project"

DATA_DIR = PROJECT / "data"
DATA_FILE = DATA_DIR / "file1.txt"

MAKEFILE = PROJECT / "Makefile"

BACKUPS_DIR = PROJECT / "backups"
LOGS_DIR = PROJECT / "logs"


@pytest.fixture(scope="module")
def data_file_contents():
    """Return the expected single line that must be in data/file1.txt."""
    return "Sample data for backup.\n"


def test_data_directory_present():
    assert DATA_DIR.exists(), (
        f"Expected data directory missing: {DATA_DIR}"
    )
    assert DATA_DIR.is_dir(), (
        f"{DATA_DIR} exists but is not a directory."
    )


def test_data_file_present_and_correct(data_file_contents):
    assert DATA_FILE.exists(), (
        f"Expected data file missing: {DATA_FILE}"
    )
    assert DATA_FILE.is_file(), (
        f"{DATA_FILE} exists but is not a regular file."
    )

    content = DATA_FILE.read_text(encoding="utf-8")
    assert content == data_file_contents, (
        "Unexpected content in data file.\n"
        f"Expected: {repr(data_file_contents)}\n"
        f"Found:    {repr(content)}"
    )


def test_makefile_absent_initially():
    assert not MAKEFILE.exists(), (
        f"A Makefile already exists at {MAKEFILE}; "
        "the assignment specifies it should be created by the student."
    )


@pytest.mark.parametrize("path", [BACKUPS_DIR, LOGS_DIR])
def test_output_directories_absent_initially(path: Path):
    assert not path.exists(), (
        f"Directory {path} already exists. "
        "The student’s Makefile should create it when appropriate."
    )