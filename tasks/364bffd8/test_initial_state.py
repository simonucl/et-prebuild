# test_initial_state.py
#
# This test-suite validates the *starting* state of the operating system
# before the student carries out any instructions for the “disk_maintenance”
# exercise.  Nothing related to the solution should already exist.
#
# Expectations for the pristine environment:
#
# 1. The directory /home/user/disk_maintenance must NOT exist.
# 2. Consequently, /home/user/disk_maintenance/pip_cache_path.txt must NOT exist.
# 3. The Python package manager (pip) must already be usable and able to
#    report its cache directory; that directory must itself exist.
#
# Any failure here indicates that the environment is not in the expected
# initial state for students to begin the task.

import os
import sys
import subprocess
from pathlib import Path

DISK_MAINT_DIR = Path("/home/user/disk_maintenance")
PIP_CACHE_RECORD = DISK_MAINT_DIR / "pip_cache_path.txt"


def test_disk_maintenance_directory_absent():
    """
    The working directory for the exercise must not exist before the student
    starts the task.
    """
    assert not DISK_MAINT_DIR.exists(), (
        f"The directory {DISK_MAINT_DIR} should NOT exist before the task begins. "
        "Please remove it so the student can create it as part of the exercise."
    )


def test_output_file_absent():
    """
    The target output file must not be present initially.
    """
    assert not PIP_CACHE_RECORD.exists(), (
        f"The file {PIP_CACHE_RECORD} should NOT exist before the task begins. "
        "It will be created by the student's one-liner command."
    )


def test_pip_cache_directory_accessible():
    """
    Ensure `pip` is available and can reveal its cache directory
    (needed so the student can discover it).  Also verify that the reported
    path is absolute and currently exists on disk.
    """
    # Use the same interpreter running the tests; this avoids PATH issues.
    cmd = [sys.executable, "-m", "pip", "cache", "dir"]
    try:
        completed = subprocess.run(
            cmd,
            check=True,
            text=True,
            capture_output=True,
            timeout=15,
        )
    except FileNotFoundError as exc:
        pytest.fail(
            f"Unable to execute pip using the current interpreter: {exc}. "
            "pip must be available for the exercise."
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Running 'python -m pip cache dir' timed out; pip may be misconfigured.")

    cache_path = completed.stdout.strip()

    assert cache_path, "pip did not return a cache directory path."
    assert cache_path.startswith("/"), (
        f"pip reported a non-absolute path: {cache_path!r}. "
        "It should be an absolute path like '/home/user/.cache/pip'."
    )
    assert Path(cache_path).is_dir(), (
        f"The directory reported by pip does not exist on disk: {cache_path}"
    )