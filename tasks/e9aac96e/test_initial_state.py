# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating-system /
# filesystem **before** the student starts working on the MLOps task.
#
# What we purposefully do *not* test for:
#   • /home/user/experiments/dummy_training_exp (and anything inside it)
#   • /home/user/experiments/index.csv
#
# Those paths are considered *outputs* that the student will create; checking
# them here would violate the “no-output-file” rule.
#
# We only make sure that all *inputs* required for the exercise are present and
# that no stray training process is already running.

import os
import stat
import pytest

TRAIN_SCRIPT = "/home/user/train_dummy.sh"
EXPERIMENTS_DIR = "/home/user/experiments"


def test_training_script_exists_and_is_executable():
    """
    Verify that the dummy training shell script is present, is a regular file,
    has non-zero size, and is executable.  These conditions must hold before
    the student attempts to launch it.
    """
    assert os.path.exists(TRAIN_SCRIPT), (
        f"Required script not found at exact path: {TRAIN_SCRIPT}"
    )

    assert os.path.isfile(TRAIN_SCRIPT), (
        f"Expected a regular file at {TRAIN_SCRIPT}, but something else exists."
    )

    assert os.path.getsize(TRAIN_SCRIPT) > 0, (
        f"The script {TRAIN_SCRIPT} is empty; it should contain shell code."
    )

    mode = os.stat(TRAIN_SCRIPT).st_mode
    is_executable = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, (
        f"The script {TRAIN_SCRIPT} is not marked executable. "
        "Make sure it has the proper execute permission bits set."
    )


def test_experiments_directory_exists_and_is_writable():
    """
    The parent directory into which the experiment subfolder will be created
    must already exist and be writable by the current user.
    """
    assert os.path.exists(EXPERIMENTS_DIR), (
        f"The experiments directory {EXPERIMENTS_DIR} does not exist."
    )

    assert os.path.isdir(EXPERIMENTS_DIR), (
        f"Expected {EXPERIMENTS_DIR} to be a directory."
    )

    # Check writability by actually attempting to create and delete a temp file
    try:
        test_path = os.path.join(EXPERIMENTS_DIR, ".write_test_tmp")
        with open(test_path, "w") as fp:
            fp.write("ok")
    except Exception as exc:  # pragma: no cover
        pytest.fail(
            f"The current user does not have write permission in "
            f"{EXPERIMENTS_DIR}: {exc}"
        )
    finally:
        try:
            os.remove(test_path)
        except FileNotFoundError:
            pass


def _iter_cmdlines():
    """
    Helper generator iterating over all cmdlines (list of str) of running
    processes by reading /proc/<pid>/cmdline.  We stay strictly within the
    Python stdlib and avoid external dependencies such as psutil.
    """
    proc_root = "/proc"
    for pid in os.listdir(proc_root):
        if not pid.isdigit():
            continue
        cmdline_path = os.path.join(proc_root, pid, "cmdline")
        try:
            with open(cmdline_path, "rb") as fh:
                raw = fh.read()
            if not raw:
                continue
            # /proc/<pid>/cmdline is NUL-separated
            parts = raw.split(b"\0")
            # Filter out empty parts and decode to str (fallback to replace errors)
            yield [p.decode(errors="replace") for p in parts if p]
        except (FileNotFoundError, PermissionError):
            # Process might have ended, or we might lack permission; skip it.
            continue


def test_training_process_not_already_running():
    """
    Ensure there is no already-running dummy training process.  The exercise
    requires the student to launch the script themselves; if it is already
    running, something is wrong with the initial state.
    """
    for cmdline in _iter_cmdlines():
        # We check the *full* path match to avoid false positives.
        if cmdline and cmdline[0] == TRAIN_SCRIPT:
            pytest.fail(
                f"A process for {TRAIN_SCRIPT} is already running "
                f"(cmdline: {' '.join(cmdline)}). "
                "The initial state must be clean."
            )