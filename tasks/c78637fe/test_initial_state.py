# test_initial_state.py
#
# This pytest suite verifies the *initial* operating-system / filesystem
# state **before** the student’s solution runs.
#
# It intentionally *does not* look for any of the artefacts that the
# student is supposed to create (e.g. /home/user/logs or any log files),
# because those belong to the *output* side of the task and must not be
# present yet.

import os
import stat
import re
import pytest

INVENTORY_PATH = "/home/user/iot_targets.csv"

######################################################################
# Helper utilities
######################################################################


def read_non_comment_lines(path):
    """
    Read non-empty, non-comment lines (lines that are *not* starting with ‘#’)
    from the given file. Lines are stripped of their trailing newline.
    """
    with open(path, "r", encoding="utf-8") as fh:
        lines = [
            line.rstrip("\n")
            for line in fh
            if line.strip() and not line.lstrip().startswith("#")
        ]
    return lines


######################################################################
# Tests
######################################################################


def test_inventory_file_exists_and_is_regular():
    """
    The inventory CSV must exist and be a regular file that is readable.
    """
    assert os.path.exists(
        INVENTORY_PATH
    ), f"Required inventory file {INVENTORY_PATH} does not exist."
    file_stat = os.stat(INVENTORY_PATH)
    assert stat.S_ISREG(
        file_stat.st_mode
    ), f"{INVENTORY_PATH} exists but is not a regular file."
    assert os.access(
        INVENTORY_PATH, os.R_OK
    ), f"{INVENTORY_PATH} exists but is not readable."


def test_inventory_file_content_is_exact():
    """
    The inventory file must contain exactly the two expected device lines
    (excluding blank and comment lines) and nothing else. Lines must be
    comma-separated with *no* embedded spaces.
    """
    lines = read_non_comment_lines(INVENTORY_PATH)

    # Expected canonical content
    expected_lines = [
        "device01,127.0.0.1",
        "device02,10.255.255.1",
    ]

    assert (
        lines == expected_lines
    ), f"{INVENTORY_PATH} must contain exactly the two lines {expected_lines!r} (no spaces). Found: {lines!r}"


def test_each_inventory_line_is_valid_csv_pair():
    """
    Each non-comment line must:
      * have exactly one comma (thus two fields),
      * contain no spaces at all,
      * have a non-empty device_id,
      * have a syntactically valid IPv4 address.
    """
    ipv4_re = re.compile(
        r"^(?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}"
        r"(?:25[0-5]|2[0-4]\d|1?\d{1,2})$"
    )

    for lineno, line in enumerate(read_non_comment_lines(INVENTORY_PATH), start=1):
        assert (
            " " not in line
        ), f"Line {lineno} in {INVENTORY_PATH} contains spaces which are not allowed: {line!r}"

        parts = line.split(",")
        assert (
            len(parts) == 2
        ), f"Line {lineno} in {INVENTORY_PATH} must have exactly one comma separating two fields: {line!r}"

        device_id, ip = parts
        assert device_id, f"Line {lineno}: device_id component is empty."
        assert ipv4_re.match(
            ip
        ), f"Line {lineno}: IP component {ip!r} is not a valid IPv4 address."


def test_inventory_file_ends_with_newline():
    """
    POSIX text files conventionally end with a trailing newline. Confirm
    that the last byte in the inventory file is '\\n' so that downstream
    tooling that relies on line-buffered input behaves as expected.
    """
    with open(INVENTORY_PATH, "rb") as fh:
        fh.seek(-1, os.SEEK_END)
        last_byte = fh.read(1)
    assert (
        last_byte == b"\n"
    ), f"{INVENTORY_PATH} should end with a newline character, but it does not."