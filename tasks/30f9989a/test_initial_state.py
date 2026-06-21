# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state that must be
# present *before* the student starts working on the “DNS audit harness”
# exercise.  It checks:
#   1. Required directory exists.
#   2. Required files exist with exact, canonical content.
#   3. The run_check.sh script is present and executable.
#
# If any check fails, the assertion message pin-points the exact problem so the
# student can correct it quickly.
#
# Only the Python standard library and pytest are used, in accordance with the
# rules.

import os
import stat
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Canonical paths & expected contents
# ---------------------------------------------------------------------------

BASE_DIR = Path("/home/user/dba_dns_check")
HOST_LIST = BASE_DIR / "host_targets.lst"
REPORT_LOG = BASE_DIR / "dns_check_report.log"
RUN_SCRIPT = BASE_DIR / "run_check.sh"

EXPECTED_HOST_LINES = [
    "db-primary.internal",
    "db-replica.internal",
    "analytics-db.internal",
]

EXPECTED_REPORT_LINES = [
    "2023-01-01T00:00:00Z db-primary.internal UNRESOLVED",
    "2023-01-01T00:00:00Z db-replica.internal UNRESOLVED",
    "2023-01-01T00:00:00Z analytics-db.internal UNRESOLVED",
]

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def _assert_lines(path: Path, expected_lines: list[str]) -> None:
    """
    Assert that the file at *path* contains exactly *expected_lines* in order,
    with no extra blank lines or trailing whitespace.
    """
    assert path.exists(), f"Required file is missing: {path}"
    assert path.is_file(), f"Expected a file but found something else: {path}"

    raw_content = path.read_text(encoding="utf-8")

    # Preserve exact line endings; splitlines(keepends=False) is deterministic.
    actual_lines = raw_content.splitlines()

    # Helpful diagnostics if mismatch occurs
    expected_joined = "\n".join(expected_lines)
    actual_joined = "\n".join(actual_lines)

    assert (
        actual_lines == expected_lines
    ), (
        f"Contents of {path} are incorrect.\n"
        f"--- Expected (exactly) ---\n{expected_joined}\n"
        f"--- Actual ---\n{actual_joined}\n"
        "Ensure lines are in the correct order with single spaces "
        "and no extra blank lines or trailing whitespace."
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_directory_exists():
    """The base directory /home/user/dba_dns_check must exist."""
    assert BASE_DIR.exists(), f"Required directory is missing: {BASE_DIR}"
    assert BASE_DIR.is_dir(), f"{BASE_DIR} exists but is not a directory."


def test_host_targets_lst_contents():
    """host_targets.lst must exist and contain the canonical three hostnames."""
    _assert_lines(HOST_LIST, EXPECTED_HOST_LINES)


def test_dns_check_report_log_contents():
    """dns_check_report.log must exist and match the expected, fixed content."""
    _assert_lines(REPORT_LOG, EXPECTED_REPORT_LINES)


def test_run_check_sh_is_executable():
    """
    run_check.sh must exist and be executable by the current user
    (no need to run it here; execution will be handled by downstream grader).
    """
    assert RUN_SCRIPT.exists(), f"Required script is missing: {RUN_SCRIPT}"
    assert RUN_SCRIPT.is_file(), f"{RUN_SCRIPT} exists but is not a regular file."

    # Check the user-execute bit
    mode = RUN_SCRIPT.stat().st_mode
    is_executable = bool(mode & stat.S_IXUSR)
    assert is_executable, (
        f"{RUN_SCRIPT} is not executable. "
        "Run: chmod +x /home/user/dba_dns_check/run_check.sh"
    )