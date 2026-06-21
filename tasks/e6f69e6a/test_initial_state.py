# test_initial_state.py
#
# This test-suite verifies the **initial** condition of the operating-system /
# file-system before the student begins working on the “log-archiving” task.
# It confirms that the expected raw log files are present and that none of the
# artefacts the student is supposed to create exist yet.  Any failure message
# is meant to be explicit so that missing (or unexpectedly present) material is
# immediately clear.
#
# ONLY stdlib + pytest are used, as requested.

import os
from pathlib import Path
import pytest

# ---------
# Constants
# ---------
HOME = Path("/home/user")
RAW_DIR = HOME / "logs" / "raw"
RAW_FILES = [
    RAW_DIR / "access-2023-06-01.log",
    RAW_DIR / "access-2023-06-02.log",
    RAW_DIR / "access-2023-06-03.log",
]

ARCHIVE = HOME / "archives" / "web-logs-2023.tar.gz"
ANALYSIS_WEBLOGS_DIR = HOME / "analysis" / "weblogs"
REPORT_FILE = ANALYSIS_WEBLOGS_DIR / "404_report.txt"


# --------------------------
# Helpers for clearer asserts
# --------------------------
def assert_path_is_dir(path: Path):
    assert path.exists(), f"Expected directory at '{path}', but it does not exist."
    assert path.is_dir(), f"Expected '{path}' to be a directory."


def assert_path_is_file(path: Path):
    assert path.exists(), f"Expected file at '{path}', but it does not exist."
    assert path.is_file(), f"Expected '{path}' to be a regular file."


# ---------------
# Actual test set
# ---------------
def test_raw_logs_directory_exists():
    """The raw logs directory must exist *and* be a directory."""
    assert_path_is_dir(RAW_DIR)


@pytest.mark.parametrize("log_file", RAW_FILES, ids=[p.name for p in RAW_FILES])
def test_individual_raw_log_exists_and_readable(log_file: Path):
    """
    Each of the three raw log files must exist and be readable.
    (Readability is important for subsequent processing.)
    """
    assert_path_is_file(log_file)
    # Check readability by opening the file.
    try:
        with log_file.open("r", encoding="utf-8") as fp:
            _ = fp.readline()  # reading a single line is enough
    except Exception as exc:
        pytest.fail(f"File '{log_file}' exists but could not be read: {exc}")


def test_archive_not_yet_present():
    """
    The compressed archive should **not** exist before the student runs their
    commands.
    """
    assert not ARCHIVE.exists(), (
        f"Archive '{ARCHIVE}' already exists, but it should not be present "
        "before the exercise is completed."
    )


def test_analysis_weblogs_dir_absent_or_empty():
    """
    The working directory into which the student will extract the logs should
    not exist yet.  If it does happen to exist, it must be empty so that the
    student's extraction step has a clean target.
    """
    if ANALYSIS_WEBLOGS_DIR.exists():
        assert ANALYSIS_WEBLOGS_DIR.is_dir(), (
            f"Path '{ANALYSIS_WEBLOGS_DIR}' exists but is not a directory."
        )
        contents = list(ANALYSIS_WEBLOGS_DIR.iterdir())
        assert (
            len(contents) == 0
        ), f"Directory '{ANALYSIS_WEBLOGS_DIR}' is expected to be empty, but contains: {', '.join(map(str, contents))}"


def test_report_file_not_present():
    """
    The 404_report.txt file must not exist at the start of the exercise.
    """
    assert not REPORT_FILE.exists(), (
        f"Report file '{REPORT_FILE}' already exists, but it should be created "
        "by the student."
    )