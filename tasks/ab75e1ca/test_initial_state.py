# test_initial_state.py
#
# This test-suite asserts the *initial* filesystem state—before the
# student has executed any command.  It guarantees that:
#
# 1. The reports directory exists and is writable.
# 2. The change_history.log file exists and its contents are *exactly*
#    the seven expected lines (each terminated by '\n').
# 3. The target output file image_modifications.log does *not* yet exist.
#
# If any assertion fails, the accompanying message pin-points what is
# missing or incorrect so the student (or course author) can fix the
# initial set-up.

import os
import stat
import pytest

REPORTS_DIR = "/home/user/workspace/reports"
CHANGE_HISTORY = os.path.join(REPORTS_DIR, "change_history.log")
IMAGE_MODS = os.path.join(REPORTS_DIR, "image_modifications.log")

EXPECTED_CHANGE_HISTORY_CONTENT = (
    "[2023-11-01 09:12:45] ADD src/components/Header.js\n"
    "[2023-11-01 09:12:46] MODIFY assets/logo.png\n"
    "[2023-11-01 09:12:47] DELETE src/utils/helpers.py\n"
    "[2023-11-01 09:12:48] MODIFY assets/banner.jpg\n"
    "[2023-11-01 09:12:49] ADD README.md\n"
    "[2023-11-01 09:12:50] MODIFY assets/icons/menu.svg\n"
    "[2023-11-01 09:12:51] DELETE docs/old_manual.pdf\n"
)


def test_reports_directory_exists_and_writable():
    assert os.path.isdir(REPORTS_DIR), (
        f"Required directory {REPORTS_DIR!r} is missing. "
        "Create it before running the exercise."
    )

    # Verify the directory is user-writable (or more permissive).
    mode = os.stat(REPORTS_DIR).st_mode
    is_writable = bool(mode & stat.S_IWUSR)
    assert is_writable, (
        f"Directory {REPORTS_DIR!r} exists but is not user-writable. "
        "Adjust its permissions to allow file creation."
    )


def test_change_history_log_exists():
    assert os.path.isfile(CHANGE_HISTORY), (
        f"Required log file {CHANGE_HISTORY!r} does not exist."
    )


def test_change_history_log_contents_exact():
    with open(CHANGE_HISTORY, "r", encoding="utf-8", newline="") as fh:
        actual = fh.read()
    assert actual == EXPECTED_CHANGE_HISTORY_CONTENT, (
        f"{CHANGE_HISTORY!r} contents do not match the expected initial "
        "history. Ensure the file has the exact seven lines provided in the "
        "specification, each ending with a single '\\n'."
    )


def test_image_modifications_log_not_present_yet():
    assert not os.path.exists(IMAGE_MODS), (
        f"Output file {IMAGE_MODS!r} already exists, but it should not be "
        "present before the student runs their command."
    )