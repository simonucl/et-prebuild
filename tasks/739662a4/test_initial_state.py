# test_initial_state.py
#
# This pytest suite validates that the *initial* operating-system / filesystem
# state is sane and ready **before** the student performs any actions for the
# “environment hardening as code” exercise.
#
# IMPORTANT – Design constraints for these pre-checks
#   • DO NOT reference any of the files / directories the student is expected
#     to create (e.g. /home/user/policy-as-code or anything within it).
#   • Use only the Python standard library + pytest.
#   • All failures must clearly explain what prerequisite is missing or broken
#     so that troubleshooting is straightforward.
#
# The checks below focus on three pragmatic pre-requisites:
#   1. The home directory /home/user exists and is writable.
#   2. /tmp is writable (many build scripts rely on this).
#   3. A usable Bash interpreter is available in the PATH.
#
# These conditions guarantee that a student can create files, write logs,
# and execute shell scripts—without them, the main assignment would be
# impossible regardless of the student’s correctness.

import os
import pathlib
import subprocess
import tempfile

HOME = pathlib.Path("/home/user")
TMP_DIR = pathlib.Path("/tmp")


def _is_writable(p: pathlib.Path) -> bool:
    """
    Helper: return True if the current process can create and delete a file
    inside the given path.
    """
    try:
        with tempfile.NamedTemporaryFile(dir=p, delete=True):
            pass
        return True
    except (OSError, PermissionError):
        return False


def test_home_directory_exists_and_writable():
    """
    The canonical user directory must exist *and* be writable; otherwise the
    student cannot place their policy-as-code hierarchy in the required
    location.
    """
    assert HOME.exists(), f"Required home directory {HOME} does not exist."
    assert HOME.is_dir(), f"{HOME} exists but is not a directory."
    assert _is_writable(HOME), f"{HOME} is not writable—cannot proceed."


def test_tmp_directory_writable():
    """
    Many tools (including pytest and shell scripts) rely on /tmp being
    writable.  Confirm that assumption up-front.
    """
    assert TMP_DIR.exists(), "/tmp does not exist—unexpected base image."
    assert TMP_DIR.is_dir(), "/tmp exists but is not a directory."
    assert _is_writable(TMP_DIR), "/tmp is not writable—sandbox mis-configured."


def test_bash_available():
    """
    The assignment explicitly requires a Bash script (apply_policy.sh).
    Ensure that a functioning Bash interpreter is reachable via PATH.
    """
    try:
        completed = subprocess.run(
            ["bash", "-c", "echo -n OK"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
        )
    except FileNotFoundError:  # bash binary not found
        assert False, (
            "No 'bash' executable found in PATH. "
            "The student will be unable to run the required shell script."
        )
    except subprocess.SubprocessError as exc:
        assert False, f"Bash exists but failed a simple command: {exc}"

    assert (
        completed.stdout.decode() == "OK"
    ), "Bash did not return expected output—possible corruption."