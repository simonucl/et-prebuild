# test_initial_state.py
"""
PyTest suite that verifies the *initial* filesystem state before the student
runs any commands.  It asserts that only the original log file exists and that
its contents match the specification.  It also makes sure that the expected
output artefacts are *absent*, so the subsequent exercise can create them.

Location conventions (all absolute):
    /home/user/project/app.log
    /home/user/project/error_lines.log
    /home/user/project/error_summary.txt
"""
import os
import stat
from pathlib import Path

import pytest


PROJECT_DIR = Path("/home/user/project")
APP_LOG = PROJECT_DIR / "app.log"
ERROR_LINES = PROJECT_DIR / "error_lines.log"
ERROR_SUMMARY = PROJECT_DIR / "error_summary.txt"

# Expected contents of app.log (each line includes its trailing newline).
EXPECTED_APP_LOG_LINES = [
    "2024-01-01 10:00:00 INFO  [INIT] - Application started\n",
    "2024-01-01 10:00:01 WARN  [CONFIG] - Missing optional field 'foo'\n",
    "2024-01-01 10:00:02 ERROR [AUTH] - ERR42 - Authentication failed for user 'alice'\n",
    "2024-01-01 10:00:03 ERROR [DB] - ERR13 - Database connection lost\n",
    "2024-01-01 10:00:04 INFO  [AUTH] - User 'alice' retry\n",
    "2024-01-01 10:00:05 ERROR [AUTH] - ERR42 - Authentication failed for user 'alice'\n",
    "2024-01-01 10:00:06 ERROR [AUTH] - ERR42 - Authentication failed for user 'bob'\n",
    "2024-01-01 10:00:07 WARN  [NET] - Network latency above threshold\n",
    "2024-01-01 10:00:08 ERROR [DB] - ERR13 - Database connection lost\n",
    "2024-01-01 10:00:09 ERROR [AUTH] - ERR99 - Token expired for user 'carol'\n",
    "2024-01-01 10:00:10 INFO  [SHUTDOWN] - Application stopped\n",
]


@pytest.fixture(scope="module")
def app_log_contents():
    """
    Read /home/user/project/app.log and return its list of lines.
    Raises an explicit assertion if the file cannot be read.
    """
    assert PROJECT_DIR.is_dir(), (
        f"Required directory {PROJECT_DIR} is missing. "
        "Create it before proceeding."
    )

    assert APP_LOG.is_file(), (
        f"Required log file {APP_LOG} is missing. "
        "It must exist before running the solution."
    )

    try:
        with APP_LOG.open("r", encoding="utf-8") as fh:
            contents = fh.readlines()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {APP_LOG}: {exc}")

    return contents


def test_app_log_permissions():
    """
    app.log must be readable by the current user.
    """
    st = APP_LOG.stat()
    mode = stat.S_IMODE(st.st_mode)
    # World-readable implies 0o444 at minimum; check the owner-read bit.
    assert mode & stat.S_IRUSR, f"{APP_LOG} is not readable (mode {oct(mode)})"


def test_app_log_contents_match(app_log_contents):
    """
    Ensure that app.log contains exactly the expected 11 lines.
    """
    assert app_log_contents == EXPECTED_APP_LOG_LINES, (
        "The contents of app.log do not match the expected initial state.\n"
        "Differences:\n"
        + _unified_diff(EXPECTED_APP_LOG_LINES, app_log_contents)
    )


def test_no_error_files_yet():
    """
    Neither error_lines.log nor error_summary.txt should exist
    before the student runs their commands.
    """
    assert not ERROR_LINES.exists(), (
        f"{ERROR_LINES} should NOT exist yet. "
        "The student must create it as part of the task."
    )
    assert not ERROR_SUMMARY.exists(), (
        f"{ERROR_SUMMARY} should NOT exist yet. "
        "The student must create it as part of the task."
    )


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
import difflib
from typing import List


def _unified_diff(a: List[str], b: List[str]) -> str:
    """
    Return a unified diff of two lists of strings for nicer assertion messages.
    """
    diff = difflib.unified_diff(
        a,
        b,
        fromfile="expected",
        tofile="actual",
        lineterm=""
    )
    return "\n".join(diff)