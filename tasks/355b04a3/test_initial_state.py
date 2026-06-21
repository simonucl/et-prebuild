# test_initial_state.py
#
# This pytest suite verifies that the workstation is in a clean state
# BEFORE the student begins the exercise.  Nothing that the student is
# expected to create during the assignment should *already* exist, so
# the tests mainly check for absence (with a few sanity checks on the
# home directory itself).
#
# What must *NOT* exist yet:
#
#   /home/user/benchmark/perf_test.img   (the 1 GiB test file)
#   /home/user/benchmark/disk_speed.log  (the 5-line results log)
#
# The directory /home/user/benchmark may or may not exist beforehand
# (the instructions explicitly allow the student to “create it if it
# does not exist”).  If it *does* exist at this point, it must be a
# directory that the current user can write to, and it must **not**
# already contain either of the two files above.
#
# Only the Python standard library and pytest are used.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
BENCHMARK_DIR = HOME / "benchmark"
TEST_FILE = BENCHMARK_DIR / "perf_test.img"
LOG_FILE = BENCHMARK_DIR / "disk_speed.log"


def _is_writable_directory(path: Path) -> bool:
    """
    Return True if `path` is a writable directory for the current user.
    """
    if not path.is_dir():
        return False
    mode = path.stat().st_mode
    uid = os.getuid()
    gid = os.getgid()
    st = path.stat()
    # Owner writable?
    if st.st_uid == uid and mode & stat.S_IWUSR:
        return True
    # Group writable?
    if st.st_gid == gid and mode & stat.S_IWGRP:
        return True
    # World writable?
    if mode & stat.S_IWOTH:
        return True
    return False


def test_home_directory_exists_and_is_accessible():
    assert HOME.exists(), f"Expected home directory {HOME} to exist."
    assert HOME.is_dir(), f"Expected {HOME} to be a directory."
    assert os.access(HOME, os.W_OK), f"Home directory {HOME} must be writable."


def test_benchmark_directory_state():
    """
    The benchmark directory may or may not exist yet.

    • If it **does not** exist, that is fine.

    • If it **does** exist, it must be:
        – a directory,
        – writable by the current user,
        – **not** already containing the test artefacts
          (perf_test.img or disk_speed.log).
    """
    if BENCHMARK_DIR.exists():
        assert BENCHMARK_DIR.is_dir(), (
            f"{BENCHMARK_DIR} exists but is not a directory; "
            "remove or rename it before starting the exercise."
        )
        assert _is_writable_directory(BENCHMARK_DIR), (
            f"{BENCHMARK_DIR} exists but is not writable by the current user."
        )

    # In *all* cases (whether the directory exists or not), the artefacts
    # must NOT be present yet.
    assert not TEST_FILE.exists(), (
        f"Found unexpected file {TEST_FILE}. "
        "The 1 GiB test file should not exist before the exercise starts."
    )
    assert not LOG_FILE.exists(), (
        f"Found unexpected file {LOG_FILE}. "
        "The log file must be created by the student's solution, "
        "so it should not exist beforehand."
    )


@pytest.mark.parametrize(
    "path",
    [TEST_FILE, LOG_FILE],
)
def test_artifacts_do_not_exist_individually(path):
    """
    Parameterised duplicate of the artefact-absence checks so that pytest
    will report *which* specific path is in violation, should one exist.
    """
    assert not path.exists(), f"Unexpected pre-existing artefact: {path}"