# test_initial_state.py
#
# This pytest file validates that the container has the *inputs*
# required for the benchmark task.  It intentionally avoids looking
# for—​or making any assumptions about—​the *outputs* that the student
# will create (e.g. /home/user/benchmark or the CSV file).
#
# The checks focus on:
#   1. Existence and executability of the three reference binaries.
#   2. Availability of the sha256sum utility that the task requires.
#   3. The shell’s POSIX-compliant “time -p” facility.
#
# If any of these pre-conditions are missing, the test suite fails
# early with a clear, actionable explanation.

import os
import shutil
import subprocess

import pytest

# Full paths to the tiny, always-present GNU coreutils binaries that
# will be used for timing.
REFERENCE_BINARIES = [
    "/usr/bin/ls",
    "/usr/bin/find",
    "/usr/bin/grep",
]

SHA256_PATH = "/usr/bin/sha256sum"


@pytest.mark.parametrize("binary_path", REFERENCE_BINARIES)
def test_reference_binaries_exist_and_are_executable(binary_path):
    """
    Ensure that each reference binary exists and is executable.
    The benchmark depends on these files being present.
    """
    assert os.path.exists(
        binary_path
    ), f"Expected binary not found: {binary_path}"
    assert os.path.isfile(
        binary_path
    ), f"Path exists but is not a regular file: {binary_path}"
    assert os.access(
        binary_path, os.X_OK
    ), f"Binary is not executable: {binary_path}"


def test_sha256sum_available():
    """
    Verify that the sha256sum utility is present and executable.
    The student will use it to generate SHA-256 checksums.
    """
    assert os.path.exists(
        SHA256_PATH
    ), f"sha256sum not found at expected path: {SHA256_PATH}"
    assert os.access(
        SHA256_PATH, os.X_OK
    ), f"sha256sum exists but is not executable: {SHA256_PATH}"


def test_time_p_option_is_supported():
    """
    Confirm that the POSIX-compliant timing facility (`time -p`) works.
    We invoke it through the default shell and check that its output
    contains the required three lines: real, user, sys.
    """
    cmd = ["bash", "-c", "time -p true"]
    # Run the command and capture stderr because `time` writes there.
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert proc.returncode == 0, "`time -p true` failed to execute successfully"

    stderr_lines = [line.strip() for line in proc.stderr.splitlines() if line.strip()]
    assert len(stderr_lines) == 3, (
        "Expected exactly three timing lines from `time -p`, got:\n"
        + "\n".join(stderr_lines)
    )
    expected_prefixes = ["real", "user", "sys"]
    for line, prefix in zip(stderr_lines, expected_prefixes):
        assert line.startswith(prefix), (
            f"`time -p` output is malformed; expected line starting with '{prefix}', "
            f"got: '{line}'"
        )