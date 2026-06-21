# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system
# before the student runs any commands.  It deliberately avoids checking for
# any artifacts that the student is expected to create (e.g.,
# /home/user/support or collected_files.txt).  Instead, it verifies the
# presence and basic readability of the prerequisite diagnostic files that
# the assignment references.  If any of these assertions fail, the student’s
# starting environment is incorrect and the grading harness should stop
# before continuing.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")


@pytest.fixture(scope="module")
def expected_paths():
    """
    The essential diagnostic files that must be reachable on a healthy Linux
    system for this assignment.
    """
    return [
        Path("/etc/os-release"),
        Path("/etc/hosts"),
        Path("/proc/cpuinfo"),
    ]


def test_home_directory_exists_and_is_directory():
    assert HOME.exists(), f"Expected home directory {HOME!s} to exist."
    assert HOME.is_dir(), f"Expected {HOME!s} to be a directory, but it is not."


@pytest.mark.parametrize("path_idx", range(3))
def test_diagnostic_files_exist_and_are_readable(expected_paths, path_idx):
    """
    For each required diagnostic file, ensure that:
      • It exists.
      • It is a regular file (or a procfs pseudo-file in the case of /proc/*).
      • It can be opened for reading without raising an exception.
    """
    target_path = expected_paths[path_idx]
    assert target_path.exists(), (
        f"Required diagnostic file {target_path!s} does not exist. "
        "The initial system state is invalid."
    )

    # In /proc, many entries are not reported as regular files.  We simply
    # assert that it is *not* a directory.
    assert not target_path.is_dir(), (
        f"Expected {target_path!s} to be a file-like object, but found a directory."
    )

    # Attempt to open and read a single byte to confirm readability.
    try:
        with target_path.open("rb") as fh:
            fh.read(1)
    except Exception as exc:  # pylint: disable=broad-except
        pytest.fail(
            f"Could not read from {target_path!s}. "
            f"This file must be readable.  Error: {exc}"
        )