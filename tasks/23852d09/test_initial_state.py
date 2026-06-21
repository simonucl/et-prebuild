# test_initial_state.py
#
# This pytest suite verifies the *initial* environment before the student
# performs any action.  It checks that:
#   • /home/user/support_source exists and contains exactly the three expected
#     diagnostic files with the prescribed byte-for-byte contents.
#   • /home/user/support_collect and /home/user/diagnostic_sync do *not* yet
#     exist.
#
# Only stdlib and pytest are used.

from pathlib import Path
import stat
import pytest

HOME = Path("/home/user")
SRC_DIR = HOME / "support_source"
DST_DIR = HOME / "support_collect"
LOG_DIR = HOME / "diagnostic_sync"
LOG_FILE = LOG_DIR / "sync.log"

EXPECTED_FILES = {
    "config.conf": (
        "max_connections=200\n"
        "log_level=debug\n"
    ),
    "status.json": (
        "{\n"
        '  "service": "web-api",\n'
        '  "status": "running",\n'
        '  "uptime": 43200\n'
        "}\n"
    ),
    "system.log": (
        "2024-01-01 00:00:01 INFO System boot\n"
        "2024-01-01 00:00:05 INFO Diagnostics initialized\n"
        "2024-01-01 00:10:12 WARN High memory usage detected\n"
    ),
}


def test_support_source_directory_exists_and_is_readable():
    assert SRC_DIR.exists(), f"Expected source directory {SRC_DIR} to exist."
    assert SRC_DIR.is_dir(), f"{SRC_DIR} exists but is not a directory."


def test_support_source_contains_exact_files():
    present_files = sorted(p.name for p in SRC_DIR.iterdir() if p.is_file())
    expected_files = sorted(EXPECTED_FILES.keys())
    assert present_files == expected_files, (
        "Source directory does not contain the expected files.\n"
        f"Expected: {expected_files}\n"
        f"Found:    {present_files}"
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_FILES.items())
def test_each_source_file_content_matches(filename, expected_content):
    file_path = SRC_DIR / filename
    assert file_path.exists(), f"Expected file {file_path} to exist."
    assert file_path.is_file(), f"{file_path} is not a regular file."
    content = file_path.read_text(encoding="utf-8")
    assert content == expected_content, (
        f"Contents of {file_path} do not match the expected reference."
    )


def test_support_collect_does_not_exist_yet():
    assert not DST_DIR.exists(), (
        f"Destination directory {DST_DIR} should NOT exist at the initial state."
    )


def test_diagnostic_sync_directory_and_log_do_not_exist_yet():
    assert not LOG_DIR.exists(), (
        f"Log directory {LOG_DIR} should NOT exist at the initial state."
    )
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} should NOT exist at the initial state."
    )