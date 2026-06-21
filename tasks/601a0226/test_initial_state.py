# test_initial_state.py
#
# This pytest file validates the initial state of the operating-system
# before the student performs any action.
#
# It checks:
#   1. Presence of /home/user/build directory.
#   2. Presence, executability and exact contents of the two shell scripts:
#        /home/user/build/build_android.sh
#        /home/user/build/cleanup_artifacts.sh
#   3. Absence of a user crontab (i.e. `crontab -l` should fail with a
#      non-zero exit status indicating “no crontab for <user>”).
#
# NOTE:  We intentionally do NOT check for any of the *output* artefacts
#        that will be produced by the student’s solution
#        (e.g. cron_setup.log or the crontab entries themselves),
#        per the grading specification.

import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest


BUILD_DIR = Path("/home/user/build")
ANDROID_SCRIPT = BUILD_DIR / "build_android.sh"
CLEANUP_SCRIPT = BUILD_DIR / "cleanup_artifacts.sh"


def _read_file_lines(path: Path):
    """
    Read a text file and return its lines WITHOUT trailing newlines.
    """
    with path.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh.readlines()]


@pytest.mark.parametrize(
    "path,expected_lines",
    [
        (
            ANDROID_SCRIPT,
            [
                "#!/usr/bin/env bash",
                'echo "Building Android..."',
            ],
        ),
        (
            CLEANUP_SCRIPT,
            [
                "#!/usr/bin/env bash",
                'echo "Cleaning up old artefacts..."',
            ],
        ),
    ],
)
def test_script_exists_and_content(path: Path, expected_lines):
    """
    Validate that each required shell script exists, is executable and has
    exactly the expected contents (ignoring an optional final newline).
    """
    assert path.exists(), f"Required script not found: {path}"
    assert path.is_file(), f"{path} exists but is not a regular file"

    st = path.stat()
    is_executable = bool(st.st_mode & stat.S_IXUSR)
    assert is_executable, f"{path} must be executable (mode 755)"

    # Check that permissions are at least 0755; we don't fail on stricter perms.
    expected_perm = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
    assert (st.st_mode & 0o777) == expected_perm, (
        f"{path} permissions should be 755 "
        f"(current: {oct(st.st_mode & 0o777)})"
    )

    actual_lines = _read_file_lines(path)
    assert actual_lines == expected_lines, (
        f"Contents of {path} do not match expected.\n"
        f"Expected lines:\n{expected_lines}\n"
        f"Found lines:\n{actual_lines}"
    )


def test_build_directory_exists():
    """The /home/user/build directory must already exist."""
    assert BUILD_DIR.exists(), f"Directory {BUILD_DIR} does not exist"
    assert BUILD_DIR.is_dir(), f"{BUILD_DIR} exists but is not a directory"


def test_no_user_crontab():
    """
    The initial state must NOT have a user crontab installed.
    `crontab -l` should exit with a non-zero status and emit
    the canonical 'no crontab for <user>' message.
    """
    result = subprocess.run(
        ["crontab", "-l"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    # On most systems `crontab -l` prints the message on stdout and exits 1
    # when no crontab is present, but some route it to stderr.
    assert result.returncode != 0, (
        "`crontab -l` unexpectedly succeeded; a user crontab is already "
        "installed but the exercise expects none."
    )

    combined_output = (result.stdout + result.stderr).lower()
    assert "no crontab for" in combined_output, (
        "Expected message 'no crontab for <user>' not found when running "
        "`crontab -l`. Combined output was:\n"
        f"{result.stdout}{result.stderr}"
    )