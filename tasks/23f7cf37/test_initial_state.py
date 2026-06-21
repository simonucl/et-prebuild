# test_initial_state.py
"""
Pytest suite that validates the *initial* operating-system / filesystem state for
the “permission audit” exercise.

What we check (nothing about the eventual output file is tested):
1. The workspace directory `/home/user/audit_workspace` exists and is writable.
2. The input snapshot file `/home/user/audit_workspace/system_file_listing.txt`
   exists, is readable, and contains exactly eight lines.
3. Those eight lines appear in the documented order and each ends with the
   expected absolute path.
"""

import os
import stat
import pytest

WORKSPACE_DIR = "/home/user/audit_workspace"
SNAPSHOT_FILE = os.path.join(WORKSPACE_DIR, "system_file_listing.txt")

# The paths (in order) that must appear at the end of each line of the snapshot
EXPECTED_PATHS = [
    "/usr/local/bin/devtool",
    "/home/user/doc.txt",
    "/etc/passwd",
    "/usr/bin/su",
    "/tmp",
    "/var/www/html/index.php",
    "/usr/local/bin/gidtool",
    "/home/user/.ssh/id_rsa",
]


def test_workspace_directory_exists_and_is_writable():
    assert os.path.isdir(
        WORKSPACE_DIR
    ), f"Required directory `{WORKSPACE_DIR}` is missing or not a directory."
    assert os.access(
        WORKSPACE_DIR, os.W_OK
    ), f"Directory `{WORKSPACE_DIR}` exists but is not writable by the current user."


def test_snapshot_file_exists_and_is_readable():
    assert os.path.isfile(
        SNAPSHOT_FILE
    ), f"Required snapshot file `{SNAPSHOT_FILE}` is missing."
    assert os.access(
        SNAPSHOT_FILE, os.R_OK
    ), f"Snapshot file `{SNAPSHOT_FILE}` is not readable."


def test_snapshot_file_has_expected_content():
    with open(SNAPSHOT_FILE, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    # Ensure exactly eight lines (each line in the listing ends with '\n').
    assert (
        len(lines) == 8
    ), f"Snapshot file should contain exactly 8 lines, found {len(lines)}."

    # Strip the trailing newline for comparison, but leave interior whitespace intact.
    stripped_lines = [line.rstrip("\n") for line in lines]

    # Verify each line ends with the documented absolute path in the correct order.
    for idx, (line, expected_path) in enumerate(zip(stripped_lines, EXPECTED_PATHS), start=1):
        assert line.endswith(
            expected_path
        ), (
            f"Line {idx} of snapshot should end with '{expected_path}' but was:\n"
            f"    {line}"
        )