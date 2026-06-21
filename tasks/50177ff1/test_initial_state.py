# test_initial_state.py
#
# Pytest suite that validates the starting state *before* the student
# performs the task described in the prompt.
#
# The checks intentionally verify only the pre-existing layout and DO NOT
# look for any artefacts that the student has yet to create.
#
# Requirements validated here
# ---------------------------
# 1. Legacy helper script exists, is executable, and has the expected
#    she-bang line.
# 2. The accounts database exists, is readable, and contains the specific
#    records referenced in the specification.
# 3. The reports directory and the final report file are *absent*.
# 4. The helper script, when invoked with the database file, produces the
#    unsorted list of disabled users exactly as described.
#
# Only stdlib + pytest are used.

import os
import stat
import subprocess
from textwrap import dedent
import pytest

# --------------------------------------------------------------------------- #
# Constant paths used throughout the test-suite
# --------------------------------------------------------------------------- #
HOME = "/home/user"
LEGACY_SCRIPT = os.path.join(HOME, "legacy_scripts", "find_disabled_accounts.sh")
DATABASE_FILE = os.path.join(HOME, "legacy_data", "accounts.txt")
REPORTS_DIR = os.path.join(HOME, "reports")
REPORT_FILE = os.path.join(REPORTS_DIR, "disabled_users_report.log")


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def file_mode(path):
    """
    Return the octal permission bits of ``path`` (e.g. 0o755).
    """
    return stat.S_IMODE(os.stat(path).st_mode)


# --------------------------------------------------------------------------- #
# Tests that validate the initial state
# --------------------------------------------------------------------------- #
def test_legacy_script_exists_and_executable():
    assert os.path.isfile(LEGACY_SCRIPT), (
        f"Legacy script expected at {LEGACY_SCRIPT} but is missing."
    )
    # Must be executable by *someone* (user/group/other)
    assert os.access(LEGACY_SCRIPT, os.X_OK), (
        f"Legacy script {LEGACY_SCRIPT} exists but is not executable."
    )
    # Optional: check mode is at least 0o755 (but allow looser perms)
    mode = file_mode(LEGACY_SCRIPT)
    assert mode & 0o111, (
        f"Legacy script {LEGACY_SCRIPT} is present but lacks execute bits; "
        f"current mode is {oct(mode)}."
    )


def test_legacy_script_starts_with_shebang():
    with open(LEGACY_SCRIPT, "r", encoding="utf-8") as fh:
        first_line = fh.readline().strip()
    expected = "#!/usr/bin/env bash"
    assert first_line == expected, (
        f"Legacy script {LEGACY_SCRIPT} must start with '{expected}', "
        f"but starts with '{first_line}'."
    )


def test_database_file_exists_and_readable():
    assert os.path.isfile(DATABASE_FILE), (
        f"Accounts DB expected at {DATABASE_FILE} but is missing."
    )
    assert os.access(DATABASE_FILE, os.R_OK), (
        f"Accounts DB {DATABASE_FILE} exists but is not readable."
    )


@pytest.mark.parametrize(
    "user,status",
    [
        ("john", "active"),
        ("alice", "disabled"),
        ("bob", "disabled"),
        ("zoe", "active"),
        ("charlie", "disabled"),
        ("dave", "active"),
    ],
)
def test_database_contains_expected_records(user, status):
    """
    Verify that each of the six exemplar records is present in the DB.

    This guards against accidental tampering so that later tests (and the
    student’s solution) have a consistent starting point.
    """
    with open(DATABASE_FILE, "r", encoding="utf-8") as fh:
        data = fh.read().splitlines()

    entry = f"{user}:{status}"
    assert (
        entry in data
    ), f"Expected record '{entry}' not found in {DATABASE_FILE}."


def test_reports_directory_absent():
    """
    Before the student runs any commands, /home/user/reports must NOT exist.
    """
    assert not os.path.exists(REPORTS_DIR), (
        f"{REPORTS_DIR} should NOT exist at the start of the exercise."
    )


def test_report_file_absent():
    """
    Similarly, the final report file must not pre-exist.
    """
    assert not os.path.exists(REPORT_FILE), (
        f"{REPORT_FILE} should NOT exist before the exercise is attempted."
    )


def test_legacy_script_raw_output():
    """
    Running the legacy script directly on the accounts DB should emit the
    unsorted list of disabled users in the order they appear in the DB.
    """
    completed = subprocess.run(
        [LEGACY_SCRIPT, DATABASE_FILE],
        check=True,
        text=True,
        capture_output=True,
    )
    expected_output = dedent(
        """\
        alice
        bob
        charlie
        """
    )
    assert (
        completed.stdout == expected_output
    ), (
        "Legacy script output did not match expectation.\n"
        f"Expected:\n{expected_output!r}\nGot:\n{completed.stdout!r}"
    )