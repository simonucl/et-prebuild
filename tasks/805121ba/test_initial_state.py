# test_initial_state.py
#
# Pytest suite that verifies the initial state of the OS / filesystem
# BEFORE the student starts working on the assignment.  It checks only
# the resources that must already exist (and nothing about the files the
# student will be asked to create later).

import os
import stat
from pathlib import Path

MONITORING_DIR = Path("/home/user/monitoring")
CHECK_DISK = MONITORING_DIR / "check_disk.sh"
CHECK_MEMORY = MONITORING_DIR / "check_memory.sh"

EXPECTED_DISK_CONTENT = "#!/usr/bin/env bash\necho \"DISK OK\"\n"
EXPECTED_MEMORY_CONTENT = "#!/usr/bin/env bash\necho \"MEMORY OK\"\n"


def _assert_executable(path: Path):
    """
    Helper that asserts a file exists, is regular, and has the executable bit
    set for the owner.  Yields a clear assertion message if not.
    """
    assert path.exists(), f"Expected file {path} to exist."
    assert path.is_file(), f"Expected {path} to be a regular file."
    st = path.stat()
    assert bool(st.st_mode & stat.S_IXUSR), (
        f"Expected {path} to be executable by owner (mode 0o755 recommended). "
        f"Current mode: {oct(st.st_mode & 0o777)}"
    )


def test_monitoring_directory_exists():
    assert MONITORING_DIR.exists(), (
        f"Directory {MONITORING_DIR} is missing. "
        "The monitoring specialist keeps their scripts here."
    )
    assert MONITORING_DIR.is_dir(), (
        f"{MONITORING_DIR} exists but is not a directory."
    )


def test_check_disk_script_present_with_correct_content_and_permissions():
    _assert_executable(CHECK_DISK)

    content = CHECK_DISK.read_text(encoding="utf-8")
    assert (
        content == EXPECTED_DISK_CONTENT
    ), (
        f"{CHECK_DISK} content mismatch.\n"
        f"Expected exactly:\n{EXPECTED_DISK_CONTENT!r}\n"
        f"Got:\n{content!r}"
    )


def test_check_memory_script_present_with_correct_content_and_permissions():
    _assert_executable(CHECK_MEMORY)

    content = CHECK_MEMORY.read_text(encoding="utf-8")
    assert (
        content == EXPECTED_MEMORY_CONTENT
    ), (
        f"{CHECK_MEMORY} content mismatch.\n"
        f"Expected exactly:\n{EXPECTED_MEMORY_CONTENT!r}\n"
        f"Got:\n{content!r}"
    )