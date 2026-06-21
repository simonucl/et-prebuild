# test_initial_state.py
#
# This test-suite verifies the initial state of the filesystem that must be
# present **before** the student runs their solution.  It deliberately does
# NOT look for any of the files or directories that the student has to
# create later (e.g. anything under /home/user/diagnostics).
#
# Only the “source” data under /home/user/support_data/ is validated here.

import os
from pathlib import Path
import pytest


SUPPORT_ROOT = Path("/home/user/support_data").resolve()

APP1_LOG_DIR = SUPPORT_ROOT / "app1" / "logs"
APP2_LOG_DIR = SUPPORT_ROOT / "app2" / "logs"

EXPECTED_FILES = {
    APP1_LOG_DIR / "application.log": [
        "2023-12-25 10:15:00 INFO Application started",
        "2023-12-25 10:15:05 ERROR Failed to connect to database",
    ],
    APP1_LOG_DIR / "error.log": [
        "[2023-12-25 10:15:05] ERROR Database connection failure",
    ],
    APP2_LOG_DIR / "server.log": [
        "2023-12-25 11:00:00 INFO Server initialized",
    ],
    APP2_LOG_DIR / "access.log": [
        '127.0.0.1 - - [25/Dec/2023:11:00:01 +0000] "GET /health HTTP/1.1" 200 2',
    ],
}


def _assert_directory(path: Path):
    """Helper that asserts a directory exists and is, in fact, a directory."""
    assert path.exists(), f"Required directory {path} is missing."
    assert path.is_dir(), f"Expected {path} to be a directory."


def _read_text_lines(path: Path):
    """Return a list of lines without their trailing newlines."""
    with path.open("r", encoding="utf-8") as fp:
        return [line.rstrip("\n") for line in fp.readlines()]


def test_support_root_directory_exists():
    """Top-level support_data directory must exist."""
    _assert_directory(SUPPORT_ROOT)


@pytest.mark.parametrize(
    "dir_path",
    [
        APP1_LOG_DIR,
        APP2_LOG_DIR,
    ],
)
def test_log_directories_exist(dir_path):
    """Both app1/logs and app2/logs directories must be present."""
    _assert_directory(dir_path)


@pytest.mark.parametrize("file_path, expected_lines", EXPECTED_FILES.items())
def test_required_log_files_exist_with_expected_contents(file_path: Path, expected_lines):
    """
    Each log file must exist and contain exactly the expected lines.
    The comparison is line-by-line after stripping trailing newlines.
    """
    assert file_path.exists(), f"Required log file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} is not a regular file."

    actual_lines = _read_text_lines(file_path)

    assert actual_lines == expected_lines, (
        f"Contents of {file_path} do not match the expected reference data.\n"
        f"Expected ({len(expected_lines)} lines): {expected_lines}\n"
        f"Actual   ({len(actual_lines)} lines): {actual_lines}"
    )