# test_initial_state.py
# Purpose: Assert that the initial filesystem state required by the exercise
# is present *before* the student writes any solution code or produces output
# artefacts.
#
# Rules enforced here:
#   • /home/user/provisioning/inventory.csv must exist and be a regular file.
#   • The file must be world-readable (at least user-readable).
#   • Its exact byte-for-byte contents must match the 12-line block published
#     in the task description, including the final trailing newline.
#
# NOTE:
#   We deliberately do NOT check for the presence of any directory or file
#   that the student is supposed to create as part of the task
#   (e.g. /home/user/provisioning/report or role_frequency.log).

import os
import stat
import pytest

INVENTORY_PATH = "/home/user/provisioning/inventory.csv"

# Expected inventory content (including final trailing newline)
EXPECTED_INVENTORY_CONTENT = (
    "web-01,web,prod\n"
    "web-02,web,prod\n"
    "db-01,db,prod\n"
    "cache-01,cache,prod\n"
    "db-02,db,staging\n"
    "web-03,web,staging\n"
    "cache-02,cache,staging\n"
    "queue-01,queue,prod\n"
    "queue-02,queue,staging\n"
    "queue-03,queue,dev\n"
    "web-04,web,dev\n"
    "db-03,db,dev\n"
)


def test_inventory_file_exists_and_is_file():
    """
    The inventory file must exist and be a regular file located exactly at
    /home/user/provisioning/inventory.csv.
    """
    assert os.path.exists(
        INVENTORY_PATH
    ), f"Required file not found: {INVENTORY_PATH}"
    assert os.path.isfile(
        INVENTORY_PATH
    ), f"Path exists but is not a regular file: {INVENTORY_PATH}"


def test_inventory_file_permissions():
    """
    The inventory file must be readable by the current user (mode 0o400 or more)
    so that the student can process it with standard Unix utilities.
    """
    st = os.stat(INVENTORY_PATH)
    # Build the combined read bits for user / group / others.
    read_bits = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
    assert (
        st.st_mode & read_bits
    ), f"File {INVENTORY_PATH} is not readable (insufficient permissions)"


def test_inventory_file_contents_exact_match():
    """
    The inventory file must contain exactly the 12 lines specified in the
    public task description, with a final trailing newline and no extra data.
    """
    with open(INVENTORY_PATH, "r", encoding="utf-8") as f:
        actual_content = f.read()

    # Check for byte-for-byte match (string comparison is fine in text mode).
    assert (
        actual_content == EXPECTED_INVENTORY_CONTENT
    ), (
        "Contents of inventory.csv do not match the expected 12-line block.\n\n"
        "Expected:\n"
        f"{EXPECTED_INVENTORY_CONTENT!r}\n\n"
        "Found:\n"
        f"{actual_content!r}"
    )