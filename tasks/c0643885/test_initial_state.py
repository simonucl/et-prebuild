# test_initial_state.py
#
# This pytest file validates the *initial* operating-system / filesystem
# state that must be present **before** the student performs any action.
#
# RULES (from the task description):
# • Only the initial CSV file and its parent directory must already exist.
# • No checks are made for any “output” or “logs” paths, as per instructions.

import os
import stat
import textwrap
import pytest

INPUT_DIR = "/home/user/audit/input"
CSV_PATH = os.path.join(INPUT_DIR, "user_permissions.csv")

EXPECTED_CSV_CONTENT = textwrap.dedent("""\
    username,uid,permission
    alice,1001,read
    bob,1002,write
    carol,1003,execute
    dave,1004,write
    erin,1005,read
    """)


def _read_file_bytes(path):
    """Utility that returns the exact bytes of a file."""
    with open(path, "rb") as f:
        return f.read()


def _read_file_text(path):
    """Utility that returns the exact text of a file using UTF-8."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_input_directory_exists_and_permissions():
    """/home/user/audit/input must exist, be a directory, and have 0755 perms."""
    assert os.path.isdir(INPUT_DIR), (
        f"Expected directory {INPUT_DIR!r} to exist but it does not."
    )

    # Verify permissions are exactly 0o755
    mode = stat.S_IMODE(os.stat(INPUT_DIR).st_mode)
    assert mode == 0o755, (
        f"{INPUT_DIR!r} exists but has permissions {oct(mode)}; "
        "expected 0o755."
    )


def test_csv_file_exists_and_permissions():
    """CSV file must exist, be a file, and have 0644 perms."""
    assert os.path.isfile(CSV_PATH), (
        f"Expected CSV file {CSV_PATH!r} to exist but it does not."
    )

    mode = stat.S_IMODE(os.stat(CSV_PATH).st_mode)
    assert mode == 0o644, (
        f"{CSV_PATH!r} exists but has permissions {oct(mode)}; "
        "expected 0o644."
    )


def test_csv_contents_are_exact():
    """CSV file must contain the exact expected content, byte-for-byte."""
    # Compare bytes to guard against hidden encoding artefacts.
    expected_bytes = EXPECTED_CSV_CONTENT.encode("utf-8")
    actual_bytes = _read_file_bytes(CSV_PATH)

    assert (
        actual_bytes == expected_bytes
    ), (
        f"The contents of {CSV_PATH!r} do not match the expected "
        f"pre-task contents.\n\n"
        "Expected:\n"
        f"{EXPECTED_CSV_CONTENT}\n"
        "Actual:\n"
        f"{_read_file_text(CSV_PATH)}"
    )