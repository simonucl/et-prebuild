# test_initial_state.py
#
# This test-suite verifies the *initial* operating-system / filesystem
# state that must be present **before** the student runs any commands.
#
# DO NOT add tests for the files / directories that the student is
# supposed to create (e.g. /home/user/cloud_reports, the symlink,
# or the audit log).  We only assert the existence and correctness of
# the resources that are guaranteed to be pre-existing.

import os
import stat
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial resources
# ---------------------------------------------------------------------------

TEMP_DIR = Path("/home/user/temp")
CSV_PATH = TEMP_DIR / "cost_report_Q42023.csv"

EXPECTED_TEMP_MODE = 0o755
EXPECTED_CSV_MODE = 0o644

EXPECTED_CSV_CONTENT = (
    "month,total_spend_usd\n"
    "Oct,12345.67\n"
    "Nov,11001.22\n"
    "Dec,12999.00\n"
)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _mode(path: Path) -> int:
    """Return the permission bits (e.g. 0o755) for the given path."""
    return stat.S_IMODE(path.stat().st_mode)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_temp_directory_exists_and_has_correct_mode():
    """
    /home/user/temp must exist, be a directory, and have mode 755.
    """
    assert TEMP_DIR.exists(), (
        f"Required directory missing: {TEMP_DIR}"
    )
    assert TEMP_DIR.is_dir(), (
        f"Expected {TEMP_DIR} to be a directory."
    )

    mode = _mode(TEMP_DIR)
    assert mode == EXPECTED_TEMP_MODE, (
        f"{TEMP_DIR} should have permissions {oct(EXPECTED_TEMP_MODE)}, "
        f"found {oct(mode)} instead."
    )


def test_cost_report_file_exists_mode_and_contents_are_correct():
    """
    /home/user/temp/cost_report_Q42023.csv must exist, be a regular file with
    mode 644, and contain the exact expected CSV data.
    """
    assert CSV_PATH.exists(), (
        f"Required file missing: {CSV_PATH}"
    )
    assert CSV_PATH.is_file(), (
        f"Expected {CSV_PATH} to be a regular file."
    )

    mode = _mode(CSV_PATH)
    assert mode == EXPECTED_CSV_MODE, (
        f"{CSV_PATH} should have permissions {oct(EXPECTED_CSV_MODE)}, "
        f"found {oct(mode)} instead."
    )

    # Verify file contents exactly, byte-for-byte
    contents = CSV_PATH.read_text(encoding="utf-8")
    assert contents == EXPECTED_CSV_CONTENT, (
        f"{CSV_PATH} does not contain the expected CSV data.\n"
        "If this file was modified, replace it with the original content."
    )