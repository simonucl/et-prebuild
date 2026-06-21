# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state before the
# student starts solving the penetration-testing pipeline task.
#
# What we check for:
#   1. The working directory /home/user/pen_test exists and is a directory.
#   2. The file /home/user/pen_test/targets.txt exists.
#   3. The file contains EXACTLY the three expected IP addresses, in the
#      correct order, with no extra blank or comment lines.
#
# We intentionally do NOT look for any of the output artefacts that the
# student is supposed to create later (scans/, logs/, summary/, etc.),
# per the grading-framework instructions.

import os
import stat
import pytest

PEN_TEST_DIR = "/home/user/pen_test"
TARGETS_TXT = os.path.join(PEN_TEST_DIR, "targets.txt")
EXPECTED_IPS = [
    "192.168.0.10",
    "192.168.0.11",
    "192.168.0.12",
]


def test_pen_test_directory_exists():
    """Verify that the working directory /home/user/pen_test exists."""
    assert os.path.isdir(
        PEN_TEST_DIR
    ), f"Required directory {PEN_TEST_DIR!r} is missing or is not a directory."


def test_targets_txt_exists():
    """Verify that targets.txt exists inside the working directory."""
    assert os.path.isfile(
        TARGETS_TXT
    ), f"Required file {TARGETS_TXT!r} is missing."


def test_targets_txt_contents_exact():
    """
    Verify that targets.txt contains exactly the expected three IP addresses,
    one per line, with no additional content.
    """
    with open(TARGETS_TXT, "r", encoding="utf-8") as fh:
        raw_lines = fh.readlines()

    # Strip newline characters but preserve ordering.
    lines = [ln.rstrip("\n") for ln in raw_lines]

    assert (
        lines == EXPECTED_IPS
    ), (
        f"{TARGETS_TXT!r} does not contain the expected IP list.\n"
        f"Expected lines:\n  {EXPECTED_IPS}\n"
        f"Actual lines:\n  {lines}"
    )


def test_targets_txt_is_world_readable():
    """
    Verify that targets.txt is world-readable (other read bit set), so subsequent
    scripts can access it without permission issues.
    """
    mode = os.stat(TARGETS_TXT).st_mode
    assert mode & stat.S_IROTH, (
        f"{TARGETS_TXT!r} is not world-readable; "
        "expected permissions to include 'other read' (chmod o+r)."
    )