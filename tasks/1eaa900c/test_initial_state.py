# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student’s synchronisation script is executed.
#
# It asserts that:
# 1. The expected source / destination / log directories exist.
# 2. The source directory contains exactly the three specified files with the
#    correct byte-sizes.
# 3. The destination directory exists but is completely empty.
# 4. The sync-log directory exists and is empty.
#
# Any deviation causes a clear, descriptive test failure so that the student
# immediately knows what prerequisite is missing or incorrect.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME = Path("/home/user")

SOURCE_DIR = HOME / "build_server"
DEST_DIR   = HOME / "deploy_server"
LOG_DIR    = HOME / "sync_logs"

EXPECTED_SOURCE_FILES = {
    "app-core-1.0.jar": 1024,
    "app-web-1.0.war":  2048,
    "readme.txt":         25,
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _directory_contents(path: Path):
    """
    Return a list of (name, Path) for all immediate children in *path*.
    Follows the order of Path.iterdir() but is converted to a list so it can
    be inspected multiple times.
    """
    return [(p.name, p) for p in path.iterdir()]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_directories_exist_and_are_directories():
    """
    Validate that the three main directories exist and are directories.
    """
    for dir_path, label in [
        (SOURCE_DIR, "source directory (/home/user/build_server)"),
        (DEST_DIR,   "destination directory (/home/user/deploy_server)"),
        (LOG_DIR,    "log directory (/home/user/sync_logs)"),
    ]:
        assert dir_path.exists(), f"Required {label} is missing: {dir_path}"
        assert dir_path.is_dir(), f"{label} exists but is not a directory: {dir_path}"


def test_source_directory_contents_and_sizes():
    """
    The source directory must contain exactly the three expected files with
    the precise byte-sizes given in the task description.
    """
    contents = dict(_directory_contents(SOURCE_DIR))

    # 1. No extra or missing files
    missing = set(EXPECTED_SOURCE_FILES) - set(contents)
    extra   = set(contents) - set(EXPECTED_SOURCE_FILES)

    assert not missing, (
        "Source directory is missing required file(s): "
        + ", ".join(sorted(missing))
    )
    assert not extra, (
        "Source directory contains unexpected extra file(s): "
        + ", ".join(sorted(extra))
    )

    # 2. Correct file sizes
    for filename, expected_size in EXPECTED_SOURCE_FILES.items():
        file_path = contents[filename]
        assert file_path.is_file(), f"{file_path} exists but is not a regular file."
        actual_size = file_path.stat().st_size
        assert actual_size == expected_size, (
            f"Size mismatch for {file_path}: expected {expected_size} bytes, "
            f"found {actual_size} bytes."
        )


def test_destination_directory_is_initially_empty():
    """
    The destination directory must start completely empty.
    """
    dest_contents = list(DEST_DIR.iterdir())
    assert not dest_contents, (
        "Destination directory must be empty before sync starts, "
        f"but contains: {', '.join(p.name for p in dest_contents)}"
    )


def test_log_directory_is_initially_empty():
    """
    The sync-logs directory must start empty (no previous run has happened).
    """
    log_contents = list(LOG_DIR.iterdir())
    assert not log_contents, (
        "Log directory must be empty before the first sync, "
        f"but contains: {', '.join(p.name for p in log_contents)}"
    )