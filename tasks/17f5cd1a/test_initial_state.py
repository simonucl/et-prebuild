# test_initial_state.py
#
# This test-suite validates that the prerequisite directory tree and log files
# exist *before* the student runs their solution for creating
# reports/failure_summary.txt.  It deliberately avoids touching or asserting on
# the expected output directory or file.
#
# Assumptions taken from the task’s ground-truth section:
#
#   /home/user/api_tests
#       └── logs
#           ├── serviceA/2024-06-08.log
#           ├── serviceB/2024-06-08.log
#           └── serviceC
#               ├── 2024-06-07.log
#               └── archive/2024-05-30.log
#
# The content of each of the four log files is asserted verbatim so that later
# stages can rely on deterministic input data.

import os
import stat
import pytest

WORKSPACE = "/home/user/api_tests"

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _assert_is_readable_file(path: str):
    """Utility: fail with a clear message if `path` is not a world-readable file."""
    assert os.path.isfile(path), f"Expected file does not exist: {path}"
    mode = os.stat(path).st_mode
    is_world_readable = bool(mode & stat.S_IROTH)
    assert is_world_readable, f"File {path} is not world-readable (mode {oct(mode)})"

# --------------------------------------------------------------------------- #
# Directory structure
# --------------------------------------------------------------------------- #
def test_workspace_directory_exists():
    assert os.path.isdir(WORKSPACE), f"Workspace directory missing: {WORKSPACE}"

@pytest.mark.parametrize(
    "rel_path",
    [
        "logs",
        "logs/serviceA",
        "logs/serviceB",
        "logs/serviceC",
        "logs/serviceC/archive",
    ],
)
def test_required_directories_exist(rel_path):
    abs_path = os.path.join(WORKSPACE, rel_path)
    assert os.path.isdir(abs_path), f"Required directory missing: {abs_path}"

# --------------------------------------------------------------------------- #
# Expected log files and their exact contents
# --------------------------------------------------------------------------- #
EXPECTED_FILES = {
    "logs/serviceA/2024-06-08.log": [
        "OK: ping 200\n",
        "FAIL: /users endpoint returned 500\n",
        "OK: /orders endpoint returned 201\n",
    ],
    "logs/serviceB/2024-06-08.log": [
        "FAIL: token refresh failed\n",
        "FAIL: login API timeout\n",
        "OK: healthcheck 200\n",
    ],
    "logs/serviceC/2024-06-07.log": [
        "OK: initial handshake 200\n",
        "FAIL: search API 502\n",
        "OK: teardown 200\n",
    ],
    "logs/serviceC/archive/2024-05-30.log": [
        "FAIL: should not be included because old\n",
        "OK: cleanup complete\n",
    ],
}

@pytest.mark.parametrize("rel_path,expected_lines", EXPECTED_FILES.items())
def test_expected_log_files_exist_and_match(rel_path, expected_lines):
    """
    For each log file we expect:
      1. It exists at the exact absolute location.
      2. It is a regular, world-readable file.
      3. Its byte content matches the canonical list, including newlines.
    """
    abs_path = os.path.join(WORKSPACE, rel_path)

    # 1 & 2 — existence and permissions
    _assert_is_readable_file(abs_path)

    # 3 — exact byte-for-byte content
    with open(abs_path, "rb") as fh:
        content = fh.readlines()
    assert content == [line.encode() if isinstance(line, str) else line
                       for line in expected_lines], (
        f"Content mismatch for {abs_path}.\n"
        "If this file legitimately changed, update the EXPECTED_FILES mapping."
    )