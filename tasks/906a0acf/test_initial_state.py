# test_initial_state.py
#
# This pytest suite validates that the operating-system / file-system
# is in the expected *initial* state before the student runs any
# commands.  If something is missing or different from the reference
# description, the tests will fail with a clear, actionable message.
#
# NOTE:
# • We never check for the existence of the future output file
#   /home/user/app/debug/weekly_error_report.log
#   because it must *not* be present yet.
# • Only the standard library and pytest are used.

import os
import gzip
from pathlib import Path

import pytest


HOME = Path("/home/user")
APP_DIR = HOME / "app"
LOGS_DIR = APP_DIR / "logs"
DEBUG_DIR = APP_DIR / "debug"


@pytest.fixture(scope="module")
def expected_log_contents():
    """
    Returns a mapping of <filename> → [list_of_expected_lines].

    Line endings in the real files are ignored; we compare logical lines only.
    """
    return {
        "service-a_2024-03-25.log": [
            "2024-03-25 10:02:15 INFO  Starting service",
            "2024-03-25 10:15:02 ERROR Connection timeout",
            "2024-03-25 10:18:47 WARN  Retrying",
            "2024-03-25 11:07:11 ERROR Failed to reconnect",
        ],
        "service-b_2024-03-24.log": [
            "2024-03-24 09:45:00 INFO  Scheduled task",
            "2024-03-24 09:46:21 INFO  Task running",
            "2024-03-24 09:47:33 ERROR Task failed",
        ],
        "service-a_2024-03-14.log": [
            "2024-03-14 13:01:09 INFO  Old record",
            "2024-03-14 13:05:17 WARN  Still fine",
            "2024-03-14 13:06:45 ERROR Historical issue",
        ],
    }


# ---------------------------------------------------------------------------
# Generic structure tests
# ---------------------------------------------------------------------------

def test_app_directory_structure():
    assert APP_DIR.is_dir(), f"Expected directory {APP_DIR} to exist."

    assert LOGS_DIR.is_dir(), (
        f"Expected logs directory {LOGS_DIR} to exist under {APP_DIR}."
    )

    assert DEBUG_DIR.is_dir(), (
        f"Expected debug directory {DEBUG_DIR} to exist under {APP_DIR}."
    )


def test_specific_files_exist(expected_log_contents):
    # Uncompressed *.log files
    for fname in expected_log_contents:
        fpath = LOGS_DIR / fname
        assert fpath.is_file(), f"Missing log file {fpath}."

    # readme.txt
    readme = LOGS_DIR / "readme.txt"
    assert readme.is_file(), f"Missing helper file {readme}."

    # archived directory and gzip file
    archived_dir = LOGS_DIR / "archived"
    gz_file = archived_dir / "archived_2024-03-20.log.gz"

    assert archived_dir.is_dir(), f"Expected archived directory {archived_dir}."
    assert gz_file.is_file(), f"Missing compressed log file {gz_file}."


def test_debug_directory_is_empty():
    """
    The debug directory should start out empty so the student can create
    weekly_error_report.log inside it.
    """
    contents = list(DEBUG_DIR.iterdir())
    # Allow dot-files (e.g. .gitkeep) but disallow regular files/sub-dirs
    non_hidden = [p for p in contents if p.name and not p.name.startswith(".")]

    assert not non_hidden, (
        f"Expected {DEBUG_DIR} to be empty (no non-hidden files/dirs), "
        f"found: {', '.join(p.name for p in non_hidden)}"
    )


# ---------------------------------------------------------------------------
# Content-specific tests
# ---------------------------------------------------------------------------

def test_log_file_contents(expected_log_contents):
    """
    Verify that each uncompressed *.log file contains exactly the expected
    lines in the documented order.
    """
    for fname, expected_lines in expected_log_contents.items():
        fpath = LOGS_DIR / fname
        actual_lines = fpath.read_text(encoding="utf-8").splitlines()

        assert actual_lines == expected_lines, (
            f"Contents of {fpath} differ from specification.\n"
            f"Expected:\n{expected_lines!r}\n\nGot:\n{actual_lines!r}"
        )


def test_archived_log_is_valid_gzip():
    """
    Ensure that the archived file really is gzip-compressed and can be opened.
    The *content* is irrelevant for our purposes, only that it is a valid
    gzip file (so it can safely be ignored by the student's command).
    """
    gz_path = LOGS_DIR / "archived" / "archived_2024-03-20.log.gz"
    try:
        with gzip.open(gz_path, "rt", encoding="utf-8") as fh:
            # Read a small chunk just to trigger decompression
            fh.read(1)
    except (OSError, EOFError) as exc:
        pytest.fail(
            f"File {gz_path} is not a valid gzip archive or is corrupted: {exc}"
        )