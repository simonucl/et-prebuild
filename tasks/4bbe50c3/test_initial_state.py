# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student performs any actions for the “checksum” task.
# Only the Python standard library and pytest are used.

import hashlib
import os
import stat
import pytest

DIAG_DIR = "/home/user/diagnostics"
APP_LOG = os.path.join(DIAG_DIR, "app.log")
EXPECTED_CONTENT = b"abc"
EXPECTED_SHA256 = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_diagnostics_directory_exists():
    """The diagnostics directory that will hold logs must already exist."""
    assert os.path.isdir(DIAG_DIR), (
        f"Required directory {DIAG_DIR} is missing. "
        "Create it before running the exercise."
    )


def test_app_log_exists_and_is_regular_file():
    """Verify that /home/user/diagnostics/app.log exists and is a regular file."""
    assert os.path.exists(APP_LOG), f"Required log file {APP_LOG} is missing."
    assert os.path.isfile(APP_LOG) and stat.S_ISREG(os.stat(APP_LOG).st_mode), (
        f"{APP_LOG} exists but is not a regular file."
    )


def test_app_log_content_and_checksum():
    """
    The log file must contain exactly the bytes 'abc' (no trailing newline)
    and its SHA-256 checksum must match the known value.
    """
    with open(APP_LOG, "rb") as fh:
        data = fh.read()

    assert data == EXPECTED_CONTENT, (
        f"{APP_LOG} content mismatch.\n"
        f"Expected: {EXPECTED_CONTENT!r}\n"
        f"Found:    {data!r}"
    )

    computed_sha256 = hashlib.sha256(data).hexdigest()
    assert computed_sha256 == EXPECTED_SHA256, (
        f"SHA-256 mismatch for {APP_LOG}.\n"
        f"Expected: {EXPECTED_SHA256}\n"
        f"Found:    {computed_sha256}"
    )


def test_checksums_log_absent_initially():
    """
    The output file (checksums.log) must NOT exist at the start.
    The student’s solution will create or overwrite it.
    """
    checksums_log = os.path.join(DIAG_DIR, "checksums.log")
    assert not os.path.exists(checksums_log), (
        f"Output file {checksums_log} should not pre-exist. "
        "It must be created by the student's script."
    )