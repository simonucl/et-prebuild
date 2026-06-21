# test_initial_state.py
#
# Pytest suite that validates the initial state of the operating system /
# filesystem *before* the student performs any actions for the “alert logs
# archive & restore” task.
#
# It checks ONLY the pre-existing resources and explicitly avoids looking for
# any artefacts that the student is supposed to create later
# (e.g. /home/user/alerts_archive.tar.gz or /home/user/alerts_restore).
#
# Requirements verified:
#   • /home/user/alerts exists and is a directory.
#   • The directory contains exactly three files: cpu.log, memory.log, disk.log.
#   • No other files or sub-directories are present inside /home/user/alerts.
#   • The size (in bytes) and the exact byte-for-byte content of each file
#     matches the specification.
#
# Only the Python standard library and pytest are used.


import os
from pathlib import Path

import pytest


ALERTS_DIR = Path("/home/user/alerts")

EXPECTED_FILES = {
    "cpu.log": b"CPU: all good\n",   # 14 bytes
    "memory.log": b"MEM: ok\n",      # 8 bytes
    "disk.log": b"DISK: 70%\n",      # 10 bytes
}


@pytest.fixture(scope="module")
def alerts_dir_contents():
    """
    Gather and return information about the /home/user/alerts directory
    in a single place so the filesystem is only accessed once per test run.
    """
    if not ALERTS_DIR.exists():
        pytest.fail(f"Required directory {ALERTS_DIR} is missing.")
    if not ALERTS_DIR.is_dir():
        pytest.fail(f"{ALERTS_DIR} exists but is not a directory.")

    entries = list(ALERTS_DIR.iterdir())
    return entries


def test_alerts_directory_exists():
    assert ALERTS_DIR.exists(), f"Directory {ALERTS_DIR} must exist."
    assert ALERTS_DIR.is_dir(), f"{ALERTS_DIR} exists but is not a directory."


def test_alerts_directory_contains_only_expected_files(alerts_dir_contents):
    actual_names = sorted(p.name for p in alerts_dir_contents)
    expected_names = sorted(EXPECTED_FILES.keys())
    assert actual_names == expected_names, (
        f"{ALERTS_DIR} is expected to contain exactly {expected_names}, "
        f"but found {actual_names}."
    )
    # Ensure there are no sub-directories.
    for p in alerts_dir_contents:
        assert p.is_file(), (
            f"Unexpected entry {p} inside {ALERTS_DIR}: only regular files "
            f"{list(EXPECTED_FILES)} are allowed."
        )


@pytest.mark.parametrize("filename, expected_bytes", EXPECTED_FILES.items())
def test_each_log_file_has_correct_size_and_contents(filename, expected_bytes):
    file_path = ALERTS_DIR / filename
    assert file_path.exists(), f"Missing required file {file_path}."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    actual_size = file_path.stat().st_size
    expected_size = len(expected_bytes)
    assert actual_size == expected_size, (
        f"{file_path} should be {expected_size} bytes, found {actual_size} bytes."
    )

    with file_path.open("rb") as fp:
        actual_contents = fp.read()

    assert actual_contents == expected_bytes, (
        f"Contents of {file_path} do not match the expected specification.\n"
        f"Expected bytes: {expected_bytes!r}\n"
        f"Actual bytes:   {actual_contents!r}"
    )