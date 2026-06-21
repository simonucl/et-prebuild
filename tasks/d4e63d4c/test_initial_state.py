# test_initial_state.py
#
# This test-suite validates the **initial** workstation state **before**
# the student executes their one-liner.  It ensures that:
#
# 1.  The working directory `/home/user/pentest` already exists.
# 2.  The dotenv file `/home/user/pentest/.targets.env` exists and
#     contains the *exact* three required variables with the correct
#     new-line termination (LF) and ordering.
# 3.  The output file that the student is expected to create
#     (`/home/user/pentest/scan_plan.txt`) does **not** exist yet.
#
# No third-party libraries are used; only stdlib and pytest are imported.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
PENTEST_DIR = HOME / "pentest"
DOTENV_PATH = PENTEST_DIR / ".targets.env"
SCAN_PLAN_PATH = PENTEST_DIR / "scan_plan.txt"

EXPECTED_DOTENV_CONTENT = (
    b"TARGET_A=192.168.1.10\n"
    b"TARGET_B=10.0.0.5\n"
    b"PORTS=22,80,443\n"
)


def test_pentest_directory_exists():
    """/home/user/pentest must exist and be a directory."""
    assert PENTEST_DIR.exists(), (
        f"Required directory {PENTEST_DIR} is missing. "
        "Create it so subsequent files can be placed there."
    )
    assert PENTEST_DIR.is_dir(), f"{PENTEST_DIR} exists but is not a directory."


def test_targets_env_exists_with_correct_content(tmp_path):
    """
    Verify that .targets.env exists and its bytes match the expected
    three-line content exactly (including final LF and no extra lines).
    """
    assert DOTENV_PATH.exists(), (
        f"Expected dotenv file {DOTENV_PATH} is missing. "
        "Make sure it is present before proceeding."
    )
    assert DOTENV_PATH.is_file(), f"{DOTENV_PATH} exists but is not a regular file."

    # Read as raw bytes to perform a byte-for-byte comparison,
    # preserving line endings.
    content = DOTENV_PATH.read_bytes()
    assert (
        content == EXPECTED_DOTENV_CONTENT
    ), (
        f"{DOTENV_PATH} does not contain the expected contents.\n\n"
        "Expected (repr shown):\n"
        f"{EXPECTED_DOTENV_CONTENT!r}\n\n"
        "Found (repr shown):\n"
        f"{content!r}"
    )


def test_scan_plan_does_not_exist_yet():
    """
    The file that the student will create must *not* exist beforehand.
    Its presence would undermine the validity of the exercise.
    """
    assert not SCAN_PLAN_PATH.exists(), (
        f"{SCAN_PLAN_PATH} already exists. The student should create this file "
        "with their one-liner; remove it before starting the task."
    )