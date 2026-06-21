# test_initial_state.py
#
# This pytest suite verifies the initial state of the operating system
# before the student writes their solution.
#
# It checks that the helper file containing the IoT-gateway IPv4 address
# exists at the expected absolute path and that its contents match the
# expected value.  The output artifact (/home/user/iot_diag.log) is **not**
# examined, per the grading-system rules.

import os
import ipaddress
from pathlib import Path

HELPER_FILE = Path("/home/user/iot_gateway_ip.txt")
EXPECTED_IP_STR = "198.51.100.42"


def test_helper_file_exists():
    """
    The helper file that supplies the gateway's IP address must already
    be present.  If it is missing, the student's instructions are
    impossible to follow.
    """
    assert HELPER_FILE.is_file(), (
        f"Required helper file not found: {HELPER_FILE!s}\n"
        "Make sure the file exists at the absolute path shown above."
    )


def test_helper_file_contents_exact_match():
    """
    The helper file must contain exactly one IPv4 address that matches
    the truth value provided in the task description.
    """
    content = HELPER_FILE.read_text(encoding="utf-8")

    # Strip only trailing newline and any incidental whitespace
    stripped = content.strip()

    assert stripped == EXPECTED_IP_STR, (
        f"Unexpected contents in {HELPER_FILE!s}.\n"
        f"Expected: {EXPECTED_IP_STR!r}\n"
        f"Found:    {stripped!r}"
    )

    # Additionally confirm it is a syntactically valid IPv4 address.
    try:
        ipaddress.IPv4Address(stripped)
    except ipaddress.AddressValueError:
        assert False, (
            f"The contents of {HELPER_FILE!s} are not a valid IPv4 address: {stripped!r}"
        )