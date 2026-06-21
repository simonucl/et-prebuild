# test_initial_state.py
#
# Pytest suite that validates the initial filesystem / OS state *before*
# the student performs any action for the “security hardening” task.
#
# This file checks only the prerequisite artifacts.  It intentionally
# avoids looking for any expected *output* of the student’s work.
#
# Requirements validated here (taken from the task description):
#   • /home/user/security/services.csv must exist
#   • File permissions must be 0644
#   • The file must contain exactly the lines specified in the prompt
#     (including final trailing newline)
#   • Status values must be only “enable” or “disable”
#
# If any of these pre-conditions are not met, the tests will fail with
# clear, actionable error messages.

import os
import stat
import pytest

CSV_PATH = "/home/user/security/services.csv"

# Expected, *canonical* content (including final newline)
EXPECTED_CSV_CONTENT = (
    "service,status\n"
    "cups,disable\n"
    "ssh,enable\n"
    "avahi-daemon,disable\n"
    "bluetooth,disable\n"
    "ntp,enable\n"
)

EXPECTED_LINES = EXPECTED_CSV_CONTENT.splitlines()


def test_services_csv_exists_and_is_regular_file():
    """Verify that /home/user/security/services.csv exists and is a regular file."""
    assert os.path.exists(CSV_PATH), (
        f"Required file {CSV_PATH} is missing."
    )
    assert os.path.isfile(CSV_PATH), (
        f"{CSV_PATH} exists but is not a regular file."
    )


def test_services_csv_permissions():
    """Ensure the file permissions are exactly 0644."""
    st = os.stat(CSV_PATH)
    perm = stat.S_IMODE(st.st_mode)
    expected_perm = 0o644
    assert perm == expected_perm, (
        f"{CSV_PATH} permissions are {oct(perm)}, expected {oct(expected_perm)}."
    )


def test_services_csv_content_exact_match():
    """
    Confirm that the file content matches the specification byte-for-byte,
    including the terminating newline.
    """
    with open(CSV_PATH, "r", encoding="utf-8", newline="") as fh:
        content = fh.read()

    assert content == EXPECTED_CSV_CONTENT, (
        f"{CSV_PATH} content does not match the required initial state.\n"
        "Expected:\n"
        f"{EXPECTED_CSV_CONTENT!r}\n"
        "Found:\n"
        f"{content!r}"
    )

    # Additional sanity checks in case the file content is modified in the future.
    lines = content.splitlines()
    assert lines[0] == "service,status", (
        "First line must be exactly the header 'service,status'."
    )

    for line in lines[1:]:
        parts = line.split(",", 1)
        assert len(parts) == 2, (
            f"Line '{line}' is malformed; expected two comma-separated values."
        )
        service, status = parts
        assert status in {"enable", "disable"}, (
            f"Invalid status '{status}' in line '{line}'. Expected 'enable' or 'disable'."
        )