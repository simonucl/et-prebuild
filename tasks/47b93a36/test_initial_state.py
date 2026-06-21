# test_initial_state.py
#
# Pytest suite that verifies the PRE-exercise state of the filesystem.
# The checks confirm that the starting conditions are exactly as
# specified and that no work from the exercise has been done yet.
#
# Rules enforced:
#   1. /home/user/legacy_users.tmp must exist and contain the three
#      legacy usernames, each on its own line, terminated by a single
#      newline character (i.e., the file ends with '\n').
#   2. No directory called /home/user/account_management should exist
#      yet (neither a file nor a symlink of that name may exist).
#
# The goal is to give immediate, explanatory feedback if the baseline
# state of the operating system or filesystem deviates from the
# expected starting point.
#
# NOTE: These tests must be executed *before* the learner performs the
#       steps outlined in the task description.
import os
from pathlib import Path

import pytest


HOME = Path("/home/user")
LEGACY_FILE = HOME / "legacy_users.tmp"
ACCOUNT_MGMT_DIR = HOME / "account_management"


def test_legacy_file_exists_with_correct_contents():
    """
    Ensure /home/user/legacy_users.tmp exists and has the exact
    expected contents *including* the trailing newline.
    """
    assert LEGACY_FILE.is_file(), (
        f"Expected legacy file '{LEGACY_FILE}' to exist as a regular file "
        f"before any actions are taken, but it was not found."
    )

    expected_content = "old_alpha\nold_beta\nold_gamma\n"
    actual_content = LEGACY_FILE.read_text(encoding="utf-8")

    assert actual_content == expected_content, (
        f"The contents of '{LEGACY_FILE}' do not match the expected starting "
        f"state.\nExpected:\n{expected_content!r}\nGot:\n{actual_content!r}"
    )


def test_account_management_directory_absent():
    """
    Ensure /home/user/account_management does NOT exist yet.
    It must not be a directory, file, or symlink at this point.
    """
    assert not ACCOUNT_MGMT_DIR.exists(), (
        f"'{ACCOUNT_MGMT_DIR}' already exists, but it should be created "
        f"by the learner during the exercise—not beforehand."
    )