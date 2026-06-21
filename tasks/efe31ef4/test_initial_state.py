# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state *before* the student performs any action.
#
# It checks ONLY the pre-existing data that the student’s solution must work
# with.  It intentionally does **not** look for any of the files that the
# student is expected to create later (e.g. the tar.gz archive or the log
# file), in accordance with the grading-infrastructure rules.

import os
from pathlib import Path

# Base paths used throughout the tests
HOME = Path("/home/user")
TICKETS_DIR = HOME / "tickets"
ISSUE_DIR = TICKETS_DIR / "issue_20230815"
BACKUPS_DIR = HOME / "backups"


def readable_path(p: Path) -> str:
    """
    Helper that returns a str-version of a Path suitable for assertion
    messages.  (Ensures consistent, easily readable failure text.)
    """
    return str(p.resolve())


def test_required_directories_exist():
    """
    Verify that all prerequisite directories are present *and* are of the
    correct type (directory, not file, symlink, etc.).
    """
    for directory in (TICKETS_DIR, ISSUE_DIR, BACKUPS_DIR):
        assert directory.exists(), (
            f"Required directory {readable_path(directory)} is missing."
        )
        assert directory.is_dir(), (
            f"Expected {readable_path(directory)} to be a directory, "
            "but it is not."
        )


def test_backups_directory_is_writable():
    """
    The /home/user/backups directory must be writable so the student can place
    the archive and log file there.
    """
    assert os.access(BACKUPS_DIR, os.W_OK), (
        f"Directory {readable_path(BACKUPS_DIR)} is not writable by the user."
    )


def test_notes_txt_content():
    """
    Validate that notes.txt exists and contains the exact expected text (with
    trailing newline).
    """
    notes_file = ISSUE_DIR / "notes.txt"
    expected = "User unable to connect to VPN.\n"
    assert notes_file.exists(), (
        f"Missing file: {readable_path(notes_file)}"
    )
    assert notes_file.is_file(), (
        f"{readable_path(notes_file)} exists but is not a regular file."
    )
    actual = notes_file.read_text(encoding="utf-8")
    assert actual == expected, (
        f"Content of {readable_path(notes_file)} is incorrect.\n"
        f"Expected: {repr(expected)}\n"
        f"Actual:   {repr(actual)}"
    )


def test_diagnostics_log_content():
    """
    Validate that diagnostics.log exists and contains the exact expected text
    (with trailing newline).
    """
    diag_file = ISSUE_DIR / "diagnostics.log"
    expected = "[2023-08-15 10:03] Ping to vpn.company.com failed.\n"
    assert diag_file.exists(), (
        f"Missing file: {readable_path(diag_file)}"
    )
    assert diag_file.is_file(), (
        f"{readable_path(diag_file)} exists but is not a regular file."
    )
    actual = diag_file.read_text(encoding="utf-8")
    assert actual == expected, (
        f"Content of {readable_path(diag_file)} is incorrect.\n"
        f"Expected: {repr(expected)}\n"
        f"Actual:   {repr(actual)}"
    )


def test_screenshot_png_is_non_empty():
    """
    The placeholder screenshot.png must exist and contain some data (non-empty
    file).  Exact bytes are not important; only that it is not empty.
    """
    png_file = ISSUE_DIR / "screenshot.png"
    assert png_file.exists(), (
        f"Missing file: {readable_path(png_file)}"
    )
    assert png_file.is_file(), (
        f"{readable_path(png_file)} exists but is not a regular file."
    )
    size = png_file.stat().st_size
    assert size > 0, (
        f"{readable_path(png_file)} is empty; expected it to contain binary "
        "data."
    )