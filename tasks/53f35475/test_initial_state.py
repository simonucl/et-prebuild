# test_initial_state.py
#
# This test-suite validates that the operating-system and filesystem
# are in a clean, ready-to-work condition *before* the student begins
# the exercise.  It purposefully avoids checking for any of the
# deliverables that the student is expected to create later.

import os
import shutil
import subprocess
import time
from pathlib import Path

HOME = Path("/home/user")
EXPERIMENTS_ROOT = HOME / "experiments"


def _assert(condition: bool, message: str) -> None:
    """
    Tiny helper so we can keep assert-messages consistently explicit.
    """
    if not condition:
        raise AssertionError(message)


def test_home_directory_exists():
    """
    The canonical home directory /home/user must already exist and be a directory.
    """
    _assert(HOME.exists(), f"Expected home directory {HOME} to exist.")
    _assert(
        HOME.is_dir(), f"Expected {HOME} to be a directory, but it is not."
    )


def test_experiments_root_exists_and_is_writable():
    """
   The parent directory /home/user/experiments (NOT the exp001 subdir)
   must already exist and be writable so that the student can create
   their experiment folder inside it.
    """
    _assert(
        EXPERIMENTS_ROOT.exists(),
        f"Directory {EXPERIMENTS_ROOT} is missing; please create it so experiments can be stored there.",
    )
    _assert(
        EXPERIMENTS_ROOT.is_dir(),
        f"Expected {EXPERIMENTS_ROOT} to be a directory.",
    )
    _assert(
        os.access(EXPERIMENTS_ROOT, os.W_OK),
        f"Directory {EXPERIMENTS_ROOT} is not writable; student will need write permission to create experiment data.",
    )


def test_python3_is_available():
    """
    The exercise assumes Python 3 is present for running a small
    training simulation; verify that it can be located via $PATH.
    """
    python_bin = shutil.which("python3")
    _assert(
        python_bin is not None,
        "python3 not found in PATH; it is required to run the training job.",
    )
    _assert(
        os.access(python_bin, os.X_OK),
        f"Located python3 at {python_bin}, but it is not executable.",
    )


def test_can_spawn_and_wait_for_short_background_process():
    """
    Make sure the environment allows starting and monitoring a short-lived
    background process—a core requirement for the upcoming task.
    The test starts `sleep 0.1` and checks it exits with status 0.
    """
    proc = subprocess.Popen(["sleep", "0.1"])
    # Wait at most 2 seconds to stay well within CI timeouts
    try:
        proc.wait(timeout=2.0)
    except subprocess.TimeoutExpired:
        proc.kill()
        raise AssertionError(
            "Subprocess 'sleep 0.1' did not finish in the expected time window."
        )

    _assert(
        proc.returncode == 0,
        f"Subprocess 'sleep 0.1' exited with non-zero status {proc.returncode}.",
    )


def test_ps_command_exists():
    """
    Students will likely use `ps` to capture the PID of their background job.
    Ensure it is available and executable.
    """
    ps_bin = shutil.which("ps")
    _assert(ps_bin, "`ps` command not found in PATH; it is required to inspect processes.")
    _assert(os.access(ps_bin, os.X_OK), f"`ps` found at {ps_bin} but it is not executable.")