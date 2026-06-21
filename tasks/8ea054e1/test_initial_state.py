# test_initial_state.py
#
# This pytest suite validates the initial filesystem state **before**
# the student starts working on the assignment.  Only the **given**
# resources are checked; nothing about the expected *output* artifacts
# is validated here (as per the specification).
#
# What we verify:
#   • /home/user/logs            – must exist and be a directory
#   • /home/user/logs/dns_traffic.log
#       – must exist, be a regular file, and contain exactly the
#         prescribed DNS-traffic sample (including the final newline)

import os
from pathlib import Path
import pytest

LOG_DIR = Path("/home/user/logs")
DNS_LOG = LOG_DIR / "dns_traffic.log"

EXPECTED_LINES = [
    "2023-03-01T12:00:01Z example.com 93.184.216.34\n",
    "2023-03-01T12:00:02Z example.com 93.184.216.34\n",
    "2023-03-01T12:00:03Z localhost 127.0.0.1\n",
    "2023-03-01T12:00:04Z example.net 93.184.216.34\n",
    "2023-03-01T12:00:05Z example.com 93.184.216.35\n",
    "2023-03-01T12:00:06Z example.net 93.184.216.34\n",
]


def test_log_directory_exists():
    """The /home/user/logs directory must be present."""
    assert LOG_DIR.exists(), f"Required directory missing: {LOG_DIR}"
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory"


def test_dns_traffic_log_exists_and_contents():
    """
    /home/user/logs/dns_traffic.log must exist and contain the exact
    sample data, line-by-line, including the terminating newline on the
    final line.
    """
    # --- existence & type checks ------------------------------------------------
    assert DNS_LOG.exists(), f"Required file missing: {DNS_LOG}"
    assert DNS_LOG.is_file(), f"{DNS_LOG} exists but is not a regular file"

    # --- content check ---------------------------------------------------------
    with DNS_LOG.open("r", encoding="utf-8", newline="") as fp:
        actual_lines = fp.readlines()

    # Verify number of lines first to get a helpful diff if it fails.
    assert (
        len(actual_lines) == len(EXPECTED_LINES)
    ), (
        f"{DNS_LOG} has {len(actual_lines)} lines; expected {len(EXPECTED_LINES)} "
        f"lines.\nActual lines:\n{actual_lines}"
    )

    # Check each line exactly.
    for idx, (exp, act) in enumerate(zip(EXPECTED_LINES, actual_lines), start=1):
        assert (
            act == exp
        ), (
            f"Mismatch on line {idx} of {DNS_LOG}.\n"
            f"Expected: {exp!r}\n"
            f"Found   : {act!r}"
        )

    # Extra safety: ensure file ends with a newline (already enforced above, but explicit is better)
    assert actual_lines[-1].endswith(
        "\n"
    ), f"The last line of {DNS_LOG} must end with a newline character"