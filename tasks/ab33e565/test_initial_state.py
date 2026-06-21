# test_initial_state.py
#
# This pytest suite verifies that the *initial* operating-system / filesystem
# state matches the specification **before** the student performs any action.
#
# It checks:
#   • /home/user/releases  exists and is a directory (mode 755).
#   • /home/user/releases/release_log.csv exists, is a regular file
#     (mode 644), is readable, ends with a newline, and contains exactly the
#     eight expected CSV rows.

import os
import stat
import textwrap
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

RELEASES_DIR = Path("/home/user/releases")
CSV_FILE = RELEASES_DIR / "release_log.csv"

# Expected CSV lines *without* their trailing newline characters.
EXPECTED_CSV_LINES = [
    "ID,Version,Commit,Date,Environment",
    "1,2.3.0,5ad88f9,2023-04-17,staging",
    "2,2.3.0,5ad88f9,2023-04-18,production",
    "3,2.3.1,a71e3dd,2023-05-01,staging",
    "4,2.3.1,a71e3dd,2023-05-02,production",
    "5,2.2.5,cd891ee,2023-03-10,production",
    "6,2.4.0,ab123df,2023-06-11,staging",
    "7,2.4.0,ab123df,2023-06-12,production",
    "8,2.5.0-beta,bad1337,2023-07-01,staging",
]


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _mode(path: Path) -> int:
    """
    Return the permission bits of *path* (e.g. 0o644).

    We mask with 0o777 to ignore higher-order bits that are not permissions.
    """
    return stat.S_IMODE(path.stat().st_mode)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_releases_directory_exists_and_has_correct_mode():
    assert RELEASES_DIR.exists(), (
        f"The directory {RELEASES_DIR} does not exist. "
        "It must be present before you start the task."
    )
    assert RELEASES_DIR.is_dir(), (
        f"{RELEASES_DIR} exists but is not a directory."
    )

    expected_mode = 0o755
    actual_mode = _mode(RELEASES_DIR)
    assert actual_mode == expected_mode, (
        f"{RELEASES_DIR} should have mode 755 "
        f"(rwxr-xr-x), but its mode is {oct(actual_mode)}."
    )


def test_release_log_csv_exists_mode_and_contents():
    assert CSV_FILE.exists(), f"The file {CSV_FILE} does not exist."
    assert CSV_FILE.is_file(), f"{CSV_FILE} exists but is not a regular file."

    expected_mode = 0o644
    actual_mode = _mode(CSV_FILE)
    assert actual_mode == expected_mode, (
        f"{CSV_FILE} should have mode 644 "
        f"(rw-r--r--), but its mode is {oct(actual_mode)}."
    )

    # Read as binary first to ensure the file ends with a newline.
    with CSV_FILE.open("rb") as fh:
        data = fh.read()
    assert data.endswith(b"\n"), (
        f"{CSV_FILE} must end with a single trailing newline character."
    )

    # Decode and compare line-by-line content.
    text = data.decode("utf-8")
    lines = text.rstrip("\n").split("\n")  # drop only the *final* newline
    assert lines == EXPECTED_CSV_LINES, textwrap.dedent(
        f"""
        {CSV_FILE} contents do not match the expected specification.

        Expected {len(EXPECTED_CSV_LINES)} lines:
        {EXPECTED_CSV_LINES}

        Found {len(lines)} lines:
        {lines}
        """
    )