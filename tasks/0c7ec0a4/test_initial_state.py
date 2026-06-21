# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state *before* the learner begins the “disk-write dd benchmark” task.
#
# Expectations for the clean slate:
#
# 1. The working directory /home/user/deploy_benchmark MUST NOT exist yet.
#    (It will be created by the learner.)
# 2. Consequently, the file /home/user/deploy_benchmark/perf.json must also
#    be absent.
# 3. The system must, however, provide the tooling and special files that
#    the learner will need:
#       • a usable `dd` executable available on $PATH
#       • the character device /dev/zero
#
# Any failure here indicates that the exercise environment was not properly
# reset or that crucial tools are missing, which would render the assignment
# impossible to complete.

import os
import shutil
import stat
import pytest
from pathlib import Path

# Constants
HOME_DIR = Path("/home/user")
BENCH_DIR = HOME_DIR / "deploy_benchmark"
PERF_JSON = BENCH_DIR / "perf.json"

@pytest.fixture(scope="module")
def dd_path():
    """Locate the dd executable once for all tests."""
    return shutil.which("dd")

def test_dd_is_available(dd_path):
    assert dd_path is not None, (
        "The `dd` executable could not be found on the system PATH. "
        "It is required to perform the disk-write benchmark."
    )
    assert os.access(dd_path, os.X_OK), (
        f"The located `dd` executable ({dd_path}) is not marked as executable."
    )

def test_dev_zero_exists_and_is_char_device():
    dev_zero = Path("/dev/zero")
    assert dev_zero.exists(), "/dev/zero is missing; it is required as the input for dd."
    mode = dev_zero.stat().st_mode
    assert stat.S_ISCHR(mode), "/dev/zero exists but is not a character device."

def test_benchmark_directory_does_not_exist_yet():
    assert not BENCH_DIR.exists(), (
        f"The directory {BENCH_DIR} already exists, but it should not be present "
        "before the learner starts the task. Please ensure a clean environment."
    )

def test_perf_json_not_present():
    assert not PERF_JSON.exists(), (
        f"The file {PERF_JSON} already exists, but it must be absent "
        "at the beginning of the exercise."
    )