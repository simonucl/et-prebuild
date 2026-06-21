# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating-system /
# filesystem *before* the student performs any action for the deployment task.
#
# Run with:  pytest -q
#
# The tests intentionally fail with clear, actionable messages whenever the
# required preconditions are not met.

import os
import stat
import pytest

HOME = "/home/user"
DP_ROOT = f"{HOME}/data-pipeline"
RELEASES = f"{DP_ROOT}/releases"
V1_DIR = f"{RELEASES}/v1.9"
V2_DIR = f"{RELEASES}/v2.0"
SYMLINK_CURRENT = f"{DP_ROOT}/current"
LOG_FILE = f"{HOME}/rollout.log"

###############################################################################
# Helper utilities
###############################################################################


def _is_symlink_to(path: str, target: str) -> bool:
    """Return True iff *path* is a symlink that ultimately resolves to *target*."""
    if not os.path.islink(path):
        return False
    # os.path.realpath() follows the symlink chain to the final target.
    return os.path.realpath(path) == target


###############################################################################
# Tests
###############################################################################


@pytest.mark.parametrize(
    "dir_path",
    [
        DP_ROOT,
        RELEASES,
        V1_DIR,
        V2_DIR,
    ],
)
def test_required_directories_exist(dir_path):
    assert os.path.isdir(
        dir_path
    ), f"Required directory missing or not a directory: {dir_path}"


@pytest.mark.parametrize(
    "ver_dir,expected_content",
    [
        (V1_DIR, "1.9\n"),
        (V2_DIR, "2.0\n"),
    ],
)
def test_version_files_exist_and_correct(ver_dir, expected_content):
    version_file = os.path.join(ver_dir, "VERSION")
    assert os.path.isfile(
        version_file
    ), f"VERSION file is missing: {version_file}"
    with open(version_file, "r", encoding="utf-8") as fh:
        content = fh.read()
    assert (
        content == expected_content
    ), f"VERSION file {version_file} contains {repr(content)}; expected {repr(expected_content)}"


def test_symlink_current_points_to_v1_9():
    assert os.path.lexists(
        SYMLINK_CURRENT
    ), f"Symlink {SYMLINK_CURRENT} does not exist"
    assert os.path.islink(
        SYMLINK_CURRENT
    ), f"{SYMLINK_CURRENT} exists but is not a symlink"
    assert _is_symlink_to(
        SYMLINK_CURRENT, V1_DIR
    ), f"{SYMLINK_CURRENT} should resolve to {V1_DIR}, got {os.path.realpath(SYMLINK_CURRENT)}"


def test_rollout_log_contains_only_header_line():
    assert os.path.isfile(
        LOG_FILE
    ), f"Log file is missing: {LOG_FILE}"
    with open(LOG_FILE, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    header = "timestamp,from,to,status\n"
    assert (
        lines == [header]
    ), (
        f"{LOG_FILE} must contain exactly one line with the header.\n"
        f"Expected: {repr(header)}\n"
        f"Actual  : {''.join(lines)!r}"
    )