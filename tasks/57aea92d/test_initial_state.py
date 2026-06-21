# test_initial_state.py
#
# This test-suite validates ONLY the *initial* filesystem state that must
# exist **before** the student starts working on the two support tickets.
#
# IMPORTANT:
#   • Per instructions, we deliberately avoid testing for any artefacts that
#     will be created or modified by the student (those items are listed in
#     the public task description under “Required artefacts”).
#   • Therefore we do *not* touch:
#         /home/user/support-sim/releases/v3
#         /home/user/support-sim/current        (will be repointed later)
#         /home/user/support-sim/admin/previous_release.txt
#         /home/user/support-sim/logs/latest.log
#         /home/user/support-sim/admin/link_update_YYYYMMDD.log
#
# Only the pre-existing filesystem layout is checked here.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
BASE = HOME / "support-sim"

RELEASES = BASE / "releases"
LOGS = BASE / "logs"
ADMIN = BASE / "admin"

@pytest.fixture(scope="module")
def base_dirs():
    """Return the key Path objects for convenience."""
    return {
        "BASE": BASE,
        "RELEASES": RELEASES,
        "LOGS": LOGS,
        "ADMIN": ADMIN,
    }

def _assert_dir(path: Path):
    assert path.exists(), f"Expected directory {path} is missing."
    assert path.is_dir(), f"{path} exists but is not a directory."

def _assert_file_with_content(path: Path, expected: bytes):
    assert path.exists(), f"Expected file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."
    actual = path.read_bytes()
    assert (
        actual == expected
    ), (
        f"File {path} has unexpected content.\n"
        f"Expected bytes: {expected!r}\nActual bytes:   {actual!r}"
    )

def test_directory_tree_exists(base_dirs):
    """Top-level directories must be in place before any work starts."""
    for name, path in base_dirs.items():
        _assert_dir(path)

def test_releases_v1_and_v2_exist_with_correct_app_conf():
    """Both legacy releases v1 and v2 must be present and intact."""
    # v1
    v1_dir = RELEASES / "v1"
    _assert_dir(v1_dir)
    _assert_file_with_content(v1_dir / "app.conf", b"version=v1\n")

    # v2
    v2_dir = RELEASES / "v2"
    _assert_dir(v2_dir)
    _assert_file_with_content(v2_dir / "app.conf", b"version=v2\n")

def test_logs_contain_required_daily_log_files():
    """The three daily log files required by the task must already exist."""
    for fname in ["2023-07-28.log", "2023-08-01.log", "2023-08-15.log"]:
        path = LOGS / fname
        assert path.exists(), f"Log file {path} is missing."
        assert path.is_file(), f"{path} exists but is not a regular file."