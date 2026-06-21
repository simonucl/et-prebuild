# test_initial_state.py
#
# This pytest suite validates the **initial** operating-system / filesystem
# state before the learner performs any action for the “legacy utility” task.
#
# Requirements being checked:
#   1. The directory /home/user/legacy_utils exists.
#   2. The file /home/user/legacy_utils/greet.sh exists and is a regular file.
#   3. greet.sh is **not** yet executable (mode 0644 is expected).
#   4. greet.sh contains the exact three lines that came with the image:
#        Line-1: #!/bin/bash
#        Line-2: echo "greet.sh version 1.0"
#        Line-3: echo "Hello, $1!"
#   5. The directory /home/user/logs does **not** yet exist.
#   6. The file   /home/user/logs/greet_run.log does **not** yet exist.
#
# If any assertion fails, the accompanying message explains precisely what is
# missing or unexpected so the learner can correct the environment before
# attempting the task.

import os
import stat
import pytest

LEGACY_DIR = "/home/user/legacy_utils"
SCRIPT_PATH = os.path.join(LEGACY_DIR, "greet.sh")
LOG_DIR = "/home/user/logs"
LOG_FILE = os.path.join(LOG_DIR, "greet_run.log")


def test_legacy_directory_exists():
    assert os.path.isdir(LEGACY_DIR), (
        f"Required directory '{LEGACY_DIR}' is missing. The legacy utility "
        "should already be present in this location."
    )


def test_greet_sh_exists_and_has_expected_content_and_permissions():
    # ---- existence & type --------------------------------------------------
    assert os.path.exists(SCRIPT_PATH), (
        f"Required file '{SCRIPT_PATH}' is missing."
    )
    assert os.path.isfile(SCRIPT_PATH), (
        f"'{SCRIPT_PATH}' exists but is not a regular file."
    )

    # ---- permissions: not executable yet (mode 0644 expected) -------------
    st_mode = os.stat(SCRIPT_PATH).st_mode
    is_exec_owner = bool(st_mode & stat.S_IXUSR)
    is_exec_group = bool(st_mode & stat.S_IXGRP)
    is_exec_other = bool(st_mode & stat.S_IXOTH)
    assert not (is_exec_owner or is_exec_group or is_exec_other), (
        f"'{SCRIPT_PATH}' should start as non-executable (mode 0644). "
        "It appears to have executable bits set."
    )

    # ---- content -----------------------------------------------------------
    with open(SCRIPT_PATH, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    expected_lines = [
        "#!/bin/bash",
        'echo "greet.sh version 1.0"',
        'echo "Hello, $1!"',
    ]

    assert lines == expected_lines, (
        f"'{SCRIPT_PATH}' does not contain the expected lines.\n"
        f"Expected:\n{expected_lines}\n\nFound:\n{lines}"
    )


def test_logs_directory_and_log_file_absent_initially():
    # The logs directory should *not* exist before the learner runs anything.
    assert not os.path.exists(LOG_DIR), (
        f"Directory '{LOG_DIR}' should NOT exist yet. It must be created by "
        "the learner's solution."
    )

    # Likewise for the target log file.
    assert not os.path.exists(LOG_FILE), (
        f"File '{LOG_FILE}' should NOT exist yet. It must be created by "
        "the learner's solution."
    )