# test_initial_state.py
#
# This pytest suite validates the operating-system / file-system *before*
# the student begins to build the “artifact-manager sandbox”.
#
# IMPORTANT CONSTRAINTS
# ---------------------
# • We intentionally do **NOT** touch or even *mention* any of the files /
#   directories that the student is expected to create later on.
# • Only fundamental prerequisites are checked:  the home directory, write
#   permissions, availability of standard tools, free disk space, etc.
#
# If any test here fails, the machine is not in a clean state for the
# assignment and the student should *not* start working.

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


HOME = Path("/home/user")


def _is_executable(cmd: str) -> bool:
    """
    Return True if *cmd* can be found in $PATH and is executable.
    """
    return shutil.which(cmd) is not None


@pytest.mark.parametrize(
    "path,kind",
    [
        (HOME, "directory"),
        (HOME / ".bashrc", "file"),
    ],
)
def test_basic_paths_exist(path: Path, kind: str):
    """
    • /home/user        must exist and be a directory.
    • /home/user/.bashrc must already be present so that the student can append
      the required environment-variable exports.
    """
    assert path.exists(), f"Expected {kind} {path} to exist."
    if kind == "directory":
        assert path.is_dir(), f"Expected {path} to be a directory."
    else:
        assert path.is_file(), f"Expected {path} to be a regular file."


def test_home_is_writable():
    """
    The student must be able to create files / directories inside /home/user.
    """
    test_file = HOME / ".write_test_pytest_tmp"
    try:
        with open(test_file, "w") as fh:
            fh.write("ping")
        assert test_file.exists(), "Unable to create files in /home/user – check permissions."
    finally:
        try:
            test_file.unlink(missing_ok=True)
        except Exception as exc:  # pragma: no cover
            # We do not want the test to fail just because cleanup did.
            print(f"Warning: cleanup of {test_file} failed: {exc}", file=sys.stderr)


def test_free_disk_space():
    """
    Ensure that at least 10 MiB of free space is available in the home
    filesystem; otherwise the student might run out of space while creating
    binaries or logs.
    """
    statvfs = os.statvfs(str(HOME))
    free_bytes = statvfs.f_bavail * statvfs.f_frsize
    min_required = 10 * 1024 * 1024  # 10 MiB
    assert (
        free_bytes >= min_required
    ), f"Less than 10 MiB free space in {HOME}. Required: {min_required}, available: {free_bytes}."


@pytest.mark.parametrize(
    "cmd",
    [
        "mkdir",
        "cp",
        "printf",
        "xargs",
        "/bin/bash",
    ],
)
def test_required_commands_available(cmd):
    """
    The assignment’s instructions rely on a handful of standard Unix tools.
    We check that they are discoverable in the current PATH.
    """
    assert _is_executable(cmd), f"Required command '{cmd}' is not available in the PATH."


def test_parallelisation_tool_present():
    """
    The task explicitly asks the student to perform at least one operation in
    parallel (e.g. using '&', GNU parallel, or xargs -P).
    While /bin/sh backgrounding is always available, the presence of either
    GNU 'parallel' *or* BSD/BusyBox 'parallel' greatly simplifies the task.
    We therefore check for it but do *not* make it a hard requirement.
    Instead, we provide a *warning* if it is missing.
    """
    if not _is_executable("parallel"):
        pytest.skip("GNU/BSD 'parallel' is not installed – student can still fall back to 'xargs -P'.")


def test_no_background_jobs_running():
    """
    Sanity check: there should be no stray 'cp' or 'parallel' jobs left over
    from previous runs.  This protects grading environments that execute the
    initial-state tests multiple times.
    """
    try:
        # Use 'ps -eo comm' to list only the command names; this is portable.
        output = subprocess.check_output(["ps", "-eo", "comm"], text=True)
    except Exception as exc:  # pragma: no cover
        pytest.skip(f"Could not invoke 'ps': {exc}")

    unwanted = {"cp", "parallel"}
    running = {line.strip() for line in output.splitlines()}
    leftovers = unwanted & running
    assert not leftovers, f"Stray background processes detected: {', '.join(leftovers)}"