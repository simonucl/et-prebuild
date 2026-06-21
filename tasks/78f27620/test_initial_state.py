# test_initial_state.py
#
# Pytest suite to validate the filesystem *before* the student performs the
# required shell commands for the “legacy policy scan” task.

import os
import stat
import textwrap
import pytest

# ---------------------------------------------------------------------------
# Constants that describe the expected initial state
# ---------------------------------------------------------------------------

HOME = "/home/user"
TOOLING_DIR = os.path.join(HOME, "devsecops_tooling")
SCRIPT_PATH = os.path.join(TOOLING_DIR, "legacy_policy_scan.sh")
RUN_LOGS_DIR = os.path.join(TOOLING_DIR, "run_logs")
LOG_FILE = os.path.join(RUN_LOGS_DIR, "2023-legacy-scan.log")

EXPECTED_SCRIPT_CONTENT = textwrap.dedent("""\
    #!/usr/bin/env bash
    echo "Legacy Policy Scanner v0.2"
    echo "Checking files..."
    echo "PASS: .gitignore - Compliant"
    echo "FAIL: Dockerfile - Missing USER directive"
    echo "PASS: main.tf - No hard-coded credentials"
    echo "Scan complete. 3 files inspected, 1 failure detected."
""").splitlines(keepends=False)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _mode_bits(path):
    """
    Return the file-mode bits for ``path`` as an integer.
    """
    return stat.S_IMODE(os.stat(path).st_mode)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_devsecops_tooling_directory_exists_and_is_directory():
    assert os.path.isdir(TOOLING_DIR), (
        f"Expected directory {TOOLING_DIR!r} to exist, "
        "but it was not found or is not a directory."
    )


def test_legacy_policy_scan_script_exists_and_is_executable():
    # Existence & type
    assert os.path.isfile(SCRIPT_PATH), (
        f"Expected script {SCRIPT_PATH!r} to exist, "
        "but it was not found or is not a regular file."
    )

    # Executable bit for the owner (at minimum)
    mode = _mode_bits(SCRIPT_PATH)
    assert mode & stat.S_IXUSR, (
        f"Script {SCRIPT_PATH!r} exists but is not executable by the user. "
        "Expected at least the user-execute bit to be set."
    )

    # (Optional) additionally verify group/world execute for a full 755 style
    expected_exec_bits = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    missing = expected_exec_bits & ~mode
    assert not missing, (
        f"Script {SCRIPT_PATH!r} should be executable for user/group/others "
        f"(mode 755). Missing execute bits: {oct(missing)}"
    )


def test_legacy_policy_scan_script_has_expected_contents():
    with open(SCRIPT_PATH, "r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh]

    # Compare up to the number of expected lines to allow for potential comments
    # after the known payload. This makes the test strict for the functional
    # lines but tolerant of extra headers.
    assert lines[: len(EXPECTED_SCRIPT_CONTENT)] == EXPECTED_SCRIPT_CONTENT, (
        "The contents of legacy_policy_scan.sh do not match the expected "
        "six echo statements.\n\n"
        "Expected first lines:\n"
        + "\n".join(EXPECTED_SCRIPT_CONTENT)
    )


def test_run_logs_directory_does_not_exist_yet():
    assert not os.path.exists(RUN_LOGS_DIR), (
        f"The directory {RUN_LOGS_DIR!r} should NOT exist yet. "
        "It must be created by the student’s shell commands."
    )


def test_log_file_does_not_exist_yet():
    assert not os.path.exists(LOG_FILE), (
        f"The file {LOG_FILE!r} should NOT exist yet. "
        "It will be generated when the task is performed."
    )