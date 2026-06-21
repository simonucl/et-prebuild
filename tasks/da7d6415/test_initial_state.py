# test_initial_state.py
#
# This test-suite validates that the operating-system / filesystem is in the
# expected *initial* state ­— i.e. before the student has created the archive
# directory or the pip package snapshot file.
#
# Rules enforced:
# 1. The directory /home/user/archives may or may not exist.  Either state is
#    acceptable at the outset, but if it **does** already exist it must *not*
#    contain the target file `pip_packages_backup.txt`.
# 2. The file /home/user/archives/pip_packages_backup.txt must **not** exist.
# 3. `pip` (or `python -m pip`) must be available and able to execute
#    `pip freeze`, producing at least one line of output.  This guarantees the
#    student can finish the task in the next step.

import os
import subprocess
import sys
import pytest
from pathlib import Path

ARCHIVE_DIR = Path("/home/user/archives")
BACKUP_FILE = ARCHIVE_DIR / "pip_packages_backup.txt"


def _run(cmd):
    """
    Helper to run a subprocess and return (return_code, stdout, stderr),
    where stdout and stderr are decoded to str.
    """
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, stderr = proc.communicate()
    return proc.returncode, stdout, stderr


def test_pip_available_and_freeze_produces_output():
    """
    Ensure that `pip freeze` can be executed in the current environment and
    yields at least one line.  This confirms the student has the tooling
    required to complete the task.
    """
    # Use `python -m pip` to reduce risk of shell PATH issues.
    code, stdout, stderr = _run([sys.executable, "-m", "pip", "freeze"])
    assert code == 0, (
        "Unable to execute `pip freeze` — return code was non-zero.\n"
        f"stderr:\n{stderr}"
    )

    lines = [line for line in stdout.splitlines() if line.strip()]
    assert lines, (
        "`pip freeze` produced no output.  There should be at least one "
        "installed package so that auditors can reproduce the environment."
    )


def test_backup_file_does_not_exist_yet():
    """
    Validate that the snapshot file is **absent** prior to the student's work.
    If the archive directory exists already, it must not contain the file.
    """
    assert not BACKUP_FILE.exists(), (
        f"Found unexpected file at {BACKUP_FILE!s}. "
        "The backup file must not exist before the task is performed."
    )


def test_archive_directory_state_is_valid():
    """
    The archive directory is allowed to be absent at the outset.  If it does
    exist (perhaps created by a previous, unrelated exercise), that is fine as
    long as it does *not* already contain `pip_packages_backup.txt`.
    """
    if ARCHIVE_DIR.exists():
        assert ARCHIVE_DIR.is_dir(), (
            f"{ARCHIVE_DIR!s} exists but is not a directory.  "
            "It must either be a directory or absent entirely."
        )

        found = sorted(p.name for p in ARCHIVE_DIR.iterdir())
        assert "pip_packages_backup.txt" not in found, (
            f"{ARCHIVE_DIR!s} already contains 'pip_packages_backup.txt'.  "
            "The file should not be present before the student performs the "
            "backup operation."
        )