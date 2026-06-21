# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem state
# before the student performs any actions for the “connection-health report”
# task.
#
# What we check:
#   1.  /home/user/network/logs/            exists and is writable.
#   2.  /home/user/network/logs/connection_report_utf16le.txt
#          • exists
#          • permissions are 0644 (or stricter)
#          • begins with UTF-16 LE BOM (FF FE)
#          • decodes as UTF-16 LE into exactly four lines, each ending in CRLF
#          • text content matches the expected initial report.
#
# We deliberately DO NOT look for any of the output files the student
# will create later (e.g. *_utf8.txt, failed_connections.log).

import os
import stat
import pytest


DIR_PATH = "/home/user/network/logs"
INPUT_FILE = os.path.join(DIR_PATH, "connection_report_utf16le.txt")

_EXPECTED_LINES = [
    "2023-07-21 10:12:05 192.168.1.10 OK\r\n",
    "2023-07-21 10:14:27 192.168.1.11 FAILED\r\n",
    "2023-07-21 10:15:32 192.168.1.12 OK\r\n",
    "2023-07-21 10:17:43 192.168.1.13 FAILED\r\n",
]


def _mode_is_no_more_permissive_than(path: str, reference: int) -> bool:
    """
    Return True if the file/dir at *path* has permissions that are the same
    as, or stricter than, *reference* (octal).
    Example: 0600 is stricter than 0644.
    """
    st_mode = os.stat(path).st_mode
    return (st_mode & 0o777) <= reference


def test_logs_directory_exists_and_writable():
    assert os.path.isdir(DIR_PATH), (
        f"Required directory {DIR_PATH!r} is missing. "
        "Create it before running your solution."
    )
    assert os.access(DIR_PATH, os.W_OK), (
        f"Directory {DIR_PATH!r} is not writable by the current user."
    )


def test_input_file_exists_and_permissions():
    assert os.path.isfile(INPUT_FILE), (
        f"Input report file {INPUT_FILE!r} is missing. "
        "It must be present before conversion."
    )

    assert _mode_is_no_more_permissive_than(INPUT_FILE, 0o644), (
        f"File {INPUT_FILE!r} permissions are too permissive. "
        "They should be 0644 or stricter."
    )


def test_input_file_is_utf16le_with_bom_and_correct_content():
    # 1. Verify BOM.
    with open(INPUT_FILE, "rb") as fb:
        raw = fb.read()

    assert raw.startswith(b"\xff\xfe"), (
        f"File {INPUT_FILE!r} must start with a UTF-16 LE BOM (FF FE)."
    )

    # 2. Decode (skip BOM) and split lines.
    decoded = raw[2:].decode("utf-16-le")
    lines = decoded.splitlines(keepends=True)

    assert len(lines) == 4, (
        f"Expected 4 lines in {INPUT_FILE!r}; found {len(lines)}."
    )

    # 3. Ensure each line ends with CRLF and matches expected content.
    for idx, (actual, expected) in enumerate(zip(lines, _EXPECTED_LINES), start=1):
        assert actual.endswith("\r\n"), (
            f"Line {idx} in {INPUT_FILE!r} does not end with CRLF."
        )
        assert actual == expected, (
            f"Line {idx} content mismatch.\n"
            f"Expected: {expected!r}\n"
            f"Found:    {actual!r}"
        )