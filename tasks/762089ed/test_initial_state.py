# test_initial_state.py
#
# Pytest suite that validates the **initial** operating‐system / filesystem
# state before the student runs the “single compound shell command”.
#
# IMPORTANT:  The requirements explicitly forbid testing for the presence
#             (or absence) of any artefacts that the student is supposed
#             to create later (/home/user/firewall, *.rule, setup.log, …).
#             Consequently, the tests below restrict themselves to checking
#             ONLY the baseline environment that must already be in place.

import os
import re
import shutil
import stat
import subprocess
from pathlib import Path

import pytest


HOME_DIR = Path("/home/user")


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _expect(condition: bool, message: str):
    """
    Mini helper that raises an assertion with a clear, single-line message.
    This keeps the test bodies readable and failure output concise.
    """
    assert condition, message


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_user_home_directory_exists_and_is_writable():
    """
    The container must contain a user-level home directory at /home/user and
    the test runner must have write permissions there.  Without this, the
    student cannot create the required artefacts.
    """
    _expect(HOME_DIR.exists(), "Required directory /home/user is missing.")
    _expect(HOME_DIR.is_dir(), "/home/user exists but is not a directory.")

    # Check write permission by consulting the effective process credentials.
    _expect(
        os.access(HOME_DIR, os.W_OK),
        "Current user has no write permission on /home/user.",
    )

    # A sanity check that the directory has at least basic POSIX permissions
    # (the execute bit is needed to traverse into it).
    mode = HOME_DIR.stat().st_mode
    _expect(
        bool(mode & stat.S_IXUSR),
        "/home/user lacks user-execute permission (cannot be traversed).",
    )


def test_date_command_available_and_correct_format():
    """
    The provisioning instructions rely on `date +%F` to produce an ISO
    calendar date (YYYY-MM-DD).  Verify that the binary exists in PATH and
    that it outputs the expected format in the current locale/timezone.
    """
    date_path = shutil.which("date")
    _expect(date_path is not None, "`date` command not found in PATH.")

    # Run `date +%F` and grab stdout.
    try:
        output = subprocess.check_output(["date", "+%F"], text=True).strip()
    except subprocess.CalledProcessError as exc:  # pragma: no cover
        pytest.fail(f"`date +%F` failed to execute: {exc}")

    # Validate the format strictly: 4 digits, dash, 2 digits, dash, 2 digits.
    iso_regex = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    _expect(
        iso_regex.match(output) is not None,
        f"`date +%F` returned '{output}', expected YYYY-MM-DD format.",
    )


def test_bash_or_posix_shell_available():
    """
    The task specification refers to running a *single* compound shell
    command.  At minimum, `/bin/sh` must exist; practically, `/bin/bash`
    is available on most teaching containers.  Check that at least one of
    these shells exists and is executable.
    """
    candidate_shells = ["/bin/bash", "/bin/sh"]
    found_shells = [s for s in candidate_shells if Path(s).is_file() and os.access(s, os.X_OK)]

    _expect(
        found_shells,
        "No suitable shell found. Expected at least one of: /bin/bash, /bin/sh",
    )