# test_initial_state.py
#
# Pytest suite that validates the initial state of the filesystem
# before the student performs any action for the “server patch
# compliance” exercise.
#
# NOTE:
# * This test purposefully does NOT look for the compliance
#   artefact (/home/user/compliance/non_compliant_servers.log)
#   because that file should not exist yet.
# * Only the pre-populated status file and its contents are verified.

import os
import pathlib
import re

STATUS_FILE = pathlib.Path("/home/user/systems/patch_status.txt")

_EXPECTED_LINES = [
    "serverA,current",
    "serverB,outdated",
    "serverC,current",
    "serverD,outdated",
    "serverE,current",
]

_HOSTNAME_REGEX = re.compile(r"^[A-Za-z0-9]+$")
_PATCH_LEVELS = {"current", "outdated"}


def test_status_file_exists_and_is_regular():
    """The status file must exist and be a regular file."""
    assert STATUS_FILE.exists(), (
        f"Expected status file {STATUS_FILE} to exist, but it is missing."
    )
    assert STATUS_FILE.is_file(), (
        f"Expected {STATUS_FILE} to be a regular file, "
        f"but it is not (maybe a directory or symlink?)."
    )


def test_status_file_permissions_readable():
    """The file must be at least readable by the current user."""
    # Mode bits are platform-dependent; we only require readability.
    assert os.access(STATUS_FILE, os.R_OK), (
        f"Status file {STATUS_FILE} is not readable by the current user."
    )


def test_status_file_contents_exact_match():
    """
    The file must have exactly the five expected lines, in order,
    each terminated by a single newline character, and no additional data.
    """
    raw_bytes = STATUS_FILE.read_bytes()

    # Ensure the file ends with a single trailing newline
    assert raw_bytes.endswith(b"\n"), (
        "Status file must end with exactly one trailing newline."
    )

    # Split preserving empty tail (will drop the terminal empty string after split)
    lines = raw_bytes.decode().splitlines()
    assert lines == _EXPECTED_LINES, (
        "Status file contents do not match the expected 5 lines.\n"
        f"Expected:\n{_EXPECTED_LINES!r}\n"
        f"Found:\n{lines!r}"
    )


def test_each_line_has_valid_format():
    """
    Additional sanity check: every line must be 'hostname,patch_level'
    with allowed characters and patch levels.
    """
    text = STATUS_FILE.read_text().rstrip("\n")
    for idx, line in enumerate(text.split("\n"), start=1):
        parts = line.split(",")
        assert len(parts) == 2, (
            f"Line {idx!r} in {STATUS_FILE} is malformed: "
            f"expected exactly one comma but found {parts}."
        )
        hostname, patch_level = parts
        assert _HOSTNAME_REGEX.fullmatch(hostname), (
            f"Line {idx!r}: hostname '{hostname}' contains invalid characters."
        )
        assert patch_level in _PATCH_LEVELS, (
            f"Line {idx!r}: patch level '{patch_level}' is not one of "
            f"{sorted(_PATCH_LEVELS)}."
        )