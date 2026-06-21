# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating system
# before the student starts working.  It makes sure that the required input
# artifact exists with the exact, byte-for-byte content expected and that the
# workspace directory is writable.  No assertions are made about any output
# files the student will create later.

import os
import textwrap

import pytest

WORKSPACE_DIR = "/home/user/audit_workspace"
INPUT_FILE = os.path.join(WORKSPACE_DIR, "permissions_dump.txt")

# Exact content that must already be present in permissions_dump.txt.
# NOTE:  All spaces, new-lines, and other bytes are significant.
EXPECTED_CONTENT = textwrap.dedent(
    """\
    -rw-r--r-- 1 alice auditors 1337 Jun 10 10:24 config.yml
    -rwxr-xr-x 1 bob auditors 4096 Jun  5 09:12 run.sh
    -rw-rw-r-- 1 carol auditors 2048 May 30 14:00 notes.txt
    -rw-r--r-- 1 dave auditors 5120 Apr 21 08:45 backup.tar
    -rwxrwxrwx 1 eve auditors   64 Jun 11 11:11 dangerous.sh
    """
).encode()  # turned into bytes so we compare exactly what is on disk


def test_workspace_directory_exists_and_is_writable():
    """
    The workspace directory must already exist and be writable by the
    non-root user running the tests.  If it does not exist or is not writable,
    the forthcoming tasks cannot be completed.
    """
    assert os.path.isdir(
        WORKSPACE_DIR
    ), f"Required directory '{WORKSPACE_DIR}' is missing."

    assert os.access(
        WORKSPACE_DIR, os.W_OK
    ), f"Directory '{WORKSPACE_DIR}' is not writable. " \
       "The user needs write permission inside it to create output files."


def test_permissions_dump_exists_with_exact_content(tmp_path):
    """
    Verifies that permissions_dump.txt exists and that its content matches the
    specification *exactly* (byte-for-byte).  Any discrepancy means the test
    environment is wrong, which must be fixed before the student code runs.
    """
    assert os.path.isfile(
        INPUT_FILE
    ), f"Input listing '{INPUT_FILE}' is missing."

    with open(INPUT_FILE, "rb") as fh:
        actual = fh.read()

    # Show a helpful diff-like output if there is a mismatch.
    if actual != EXPECTED_CONTENT:
        # Limit output length so pytest error message stays readable.
        max_preview = 500
        preview_actual = actual.decode(errors="replace")[:max_preview]
        preview_expected = EXPECTED_CONTENT.decode()[:max_preview]
        raise AssertionError(
            "Content of 'permissions_dump.txt' does not match the expected "
            "template.\n\n--- Expected (first 500 bytes) ---\n"
            f"{preview_expected}\n"
            "--- Actual (first 500 bytes) ---\n"
            f"{preview_actual}\n"
            "Please ensure the file is present and unmodified."
        )