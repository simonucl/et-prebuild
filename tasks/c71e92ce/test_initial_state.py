# test_initial_state.py
#
# This pytest suite validates that the *initial* operating-system state
# is suitable for a junior operator to carry out the task of creating a
# virtual environment and producing a verification log.  It deliberately
# avoids checking for (or against) any files or directories that the
# student is expected to create later, in accordance with the grading
# rules.

import os
import subprocess
import sys
from pathlib import Path
import re
import pytest


HOME_DIR = Path("/home/user")


def run(cmd):
    """
    Helper that executes *cmd* (a list of strings) and returns the completed
    subprocess object.  It raises pytest.fail with a clear, actionable
    message if the command cannot be run.
    """
    try:
        completed = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        pytest.fail(f"Required executable not found while running {cmd!r}: {exc}")

    return completed


def test_home_directory_exists_and_is_writable():
    """
    The reference home directory (/home/user) must exist, be a directory,
    and be writable—otherwise the student will be unable to create the
    required workspace.
    """
    assert HOME_DIR.exists(), f"Expected home directory {HOME_DIR} is missing."
    assert HOME_DIR.is_dir(), f"{HOME_DIR} exists but is not a directory."
    # Check writability by verifying the directory has the write bit set *for the owner*.
    # os.access is used here purely for a quick permission check.
    assert os.access(HOME_DIR, os.W_OK), f"{HOME_DIR} is not writable."


def test_python3_command_available():
    """
    The system must have `python3` on the PATH and it must report a
    semantic-version string such as 'Python 3.10.12'.
    """
    completed = run(["python3", "-V"])
    assert completed.returncode == 0, (
        "`python3 -V` returned a non-zero exit status:\n" + completed.stdout
    )

    output = completed.stdout.strip()
    assert output.startswith("Python "), (
        "Unexpected output from `python3 -V` "
        f"(expected it to start with 'Python '): {output!r}"
    )

    # Basic semantic-version sanity check: Python X.Y.Z
    version_part = output.split(maxsplit=1)[1] if " " in output else ""
    version_re = r"^\d+\.\d+\.\d+$"
    assert re.match(version_re, version_part), (
        f"`python3 -V` output ({output!r}) does not contain a valid X.Y.Z "
        "version string."
    )


def test_builtin_venv_module_is_available():
    """
    The student's instructions require the built-in `venv` module.  Ensure
    that it can be invoked via `python3 -m venv -h` without errors.
    """
    completed = run(["python3", "-m", "venv", "-h"])

    # Some Python versions send help text to stderr, others to stdout; we
    # capture both in stdout for simplicity.  A zero exit code is what we
    # care about.
    assert completed.returncode == 0, (
        "The built-in `venv` module is not available or failed to run:\n"
        f"{completed.stdout}"
    )

    # A brief sanity check that the help text at least *mentions* "venv".
    assert "venv" in completed.stdout.lower(), (
        "`python3 -m venv -h` did not output expected help text."
    )