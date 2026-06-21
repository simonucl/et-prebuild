# test_initial_state.py
#
# This test-suite validates ONLY the pre-exercise filesystem state.
# It purposefully ignores every output path that the student is
# expected to create (/home/user/backup_test/output/**).
#
# The checks focus on:
#   1. Presence of the required input directory hierarchy.
#   2. Presence, readability and permissions of the manifest file.
#   3. Byte-for-byte correctness of the manifest’s contents.
#
# If any assertion fails, the accompanying message pinpoints exactly
# what is missing or incorrect so the student (or course staff) can
# fix the base image before grading begins.
#
# NOTE: Uses only the Python standard library + pytest.

import os
import stat
import pytest

HOME = "/home/user"
BASE_DIR = os.path.join(HOME, "backup_test")
INPUT_DIR = os.path.join(BASE_DIR, "input")
MANIFEST = os.path.join(INPUT_DIR, "manifest.log")

EXPECTED_MANIFEST_LINES = [
    "2024-06-01 01:00:00 /var/www/html/index.html 2048 OK\n",
    "2024-06-01 01:00:05 /var/log/syslog 1048576 OK\n",
    "2024-06-01 01:00:10 /etc/passwd 4096 FAILED\n",
    "2024-06-01 01:00:15 /home/user/data/report.pdf 8192 OK\n",
    "2024-06-01 01:00:20 /home/user/secret/notes.txt 1234 FAILED\n",
]


def test_base_directory_exists():
    assert os.path.isdir(BASE_DIR), (
        f"Required base directory missing: {BASE_DIR}"
    )


def test_input_directory_exists():
    assert os.path.isdir(INPUT_DIR), (
        f"Required input directory missing: {INPUT_DIR}"
    )


def test_manifest_exists_and_is_readable():
    assert os.path.isfile(MANIFEST), (
        f"Required manifest file missing: {MANIFEST}"
    )

    # Check world-readable permissions (mode 0644 exactly).
    mode = stat.S_IMODE(os.stat(MANIFEST).st_mode)
    expected_mode = 0o644
    assert mode == expected_mode, (
        f"Manifest permissions should be {oct(expected_mode)}, "
        f"but are {oct(mode)}"
    )

    # Check that we can actually read the file.
    try:
        with open(MANIFEST, "r", encoding="utf-8") as fh:
            fh.read(1)
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read manifest file: {exc}")


def test_manifest_content_exact_match():
    with open(MANIFEST, "r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    assert actual_lines == EXPECTED_MANIFEST_LINES, (
        "Manifest content does not match the expected template.\n"
        "---- Expected ----\n"
        + "".join(EXPECTED_MANIFEST_LINES)
        + "\n---- Actual ----\n"
        + "".join(actual_lines)
    )