# test_initial_state.py
#
# Pytest suite to validate the *initial* operating-system / file-system
# state **before** the student performs any action for the “backup
# consolidation” task.
#
# The tests assert that:
#   • The expected source directories and log files already exist.
#   • Each log file contains the exact, space-separated lines described
#     in the specification (no more, no less, and in the right order).
#   • The /home/user/backups/summary/ directory and its output files
#     (backup_index.csv and stats.txt) are NOT present yet.
#
# Failing tests provide clear, actionable error messages so that the
# student immediately knows what pre-existing element is missing or
# different from the truth table.
#
# Only Python’s standard library and pytest are used, as required.

import os
import pytest
from pathlib import Path

HOME = Path("/home/user").resolve()
BACKUPS_DIR = HOME / "backups"
DAILY_DIR = BACKUPS_DIR / "daily"
SUMMARY_DIR = BACKUPS_DIR / "summary"

# --------------------------------------------------------------------------- #
# Expected daily log files and their *exact* contents.                        #
# --------------------------------------------------------------------------- #

EXPECTED_DAILY_FILES = {
    DAILY_DIR / "backup_report_2023-08-01.log": [
        "db.sql 20480 9f8b1e2d 2023-08-01",
        "home.tar 512000 c3d8fab1 2023-08-01",
        "etc.cfg 120 1a2b3c4d 2023-08-01",
    ],
    DAILY_DIR / "backup_report_2023-08-02.log": [
        "db.sql 20560 af4c9d11 2023-08-02",
        "home.tar 513024 0ddce8ef 2023-08-02",
        "etc.cfg 125 ee44aa55 2023-08-02",
    ],
    DAILY_DIR / "backup_report_2023-08-03.log": [
        "db.sql 20640 bb88cc77 2023-08-03",
        "home.tar 514048 2376abdc 2023-08-03",
        "etc.cfg 130 ddd77711 2023-08-03",
    ],
}


# --------------------------------------------------------------------------- #
# Helper functions                                                            #
# --------------------------------------------------------------------------- #
def _read_strip_newlines(path: Path):
    """
    Return a list of lines from *path* with trailing newline characters
    removed, preserving original order. The file is read using UTF-8
    (default) text mode.
    """
    with path.open("r", encoding="utf-8") as fp:
        return [line.rstrip("\n") for line in fp.readlines()]


# --------------------------------------------------------------------------- #
# Test cases                                                                  #
# --------------------------------------------------------------------------- #
def test_directories_exist_and_are_correct():
    """
    Verify that /home/user/backups/ and /home/user/backups/daily/ are
    present and are directories. Also verify that the summary directory
    does NOT yet exist.
    """
    assert BACKUPS_DIR.is_dir(), (
        f"Expected directory not found: {BACKUPS_DIR}. "
        "The initial backups directory must already exist."
    )

    assert DAILY_DIR.is_dir(), (
        f"Expected directory not found: {DAILY_DIR}. "
        "The initial 'daily' sub-directory must already exist."
    )

    # The summary directory should *not* exist before the student runs code.
    assert not SUMMARY_DIR.exists(), (
        f"Directory {SUMMARY_DIR} should NOT exist before the student starts. "
        "Your environment is not in the required initial state."
    )


@pytest.mark.parametrize("file_path", list(EXPECTED_DAILY_FILES.keys()))
def test_daily_log_files_exist(file_path: Path):
    """
    Each expected daily log file must be present and be a regular file.
    """
    assert file_path.is_file(), (
        f"Required log file missing: {file_path}. "
        "Ensure the initial dataset is complete."
    )


@pytest.mark.parametrize(
    "file_path, expected_lines", EXPECTED_DAILY_FILES.items()
)
def test_daily_log_file_contents_exact(file_path: Path, expected_lines):
    """
    Validate that each daily log file contains EXACTLY the expected lines,
    in the correct order, with the correct number of fields per line, and
    no extra/trailing data.
    """
    actual_lines = _read_strip_newlines(file_path)

    assert (
        actual_lines == expected_lines
    ), (
        f"Contents of {file_path} do not match the specification.\n\n"
        f"Expected ({len(expected_lines)} lines):\n"
        + "\n".join(expected_lines)
        + "\n\n"
        f"Actual ({len(actual_lines)} lines):\n"
        + "\n".join(actual_lines)
    )

    # Additional defensive checks: each line must have 4 space-separated fields
    for idx, line in enumerate(actual_lines, start=1):
        fields = line.split()
        assert len(fields) == 4, (
            f"Line {idx} in {file_path} should contain exactly 4 "
            f"space-separated fields, found {len(fields)}: {line!r}"
        )


def test_output_files_absent():
    """
    Ensure that the expected OUTPUT artefacts (created by the student's
    script later) are NOT present yet. This guarantees we are checking the
    *initial* state, not an already-modified environment.
    """
    index_csv = SUMMARY_DIR / "backup_index.csv"
    stats_txt = SUMMARY_DIR / "stats.txt"

    assert not index_csv.exists(), (
        f"{index_csv} already exists, but it must NOT be present before the "
        "task is attempted."
    )
    assert not stats_txt.exists(), (
        f"{stats_txt} already exists, but it must NOT be present before the "
        "task is attempted."
    )