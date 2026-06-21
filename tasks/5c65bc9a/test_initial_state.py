# test_initial_state.py
#
# Pytest suite to validate the operating-system / filesystem **before**
# the student makes any changes for the “DNS & Hostname Resolution Triage
# for an Internal Outage” exercise.
#
# Rules respected:
#   • Uses only stdlib + pytest.
#   • Does NOT refer to any of the required output artefacts
#     (/home/user/dns_report.log, the final state of /home/user/custom_hosts, etc.).
#   • Provides clear, actionable failure messages.

import os
from pathlib import Path

HOME = Path("/home/user")
CUSTOM_HOSTS = HOME / "custom_hosts"

EXPECTED_LINES = [
    "10.20.1.15 db.internal.example.com",
    "10.20.1.20 api.internal.example.com",
]
MISSING_MAPPING = "cache.internal.example.com"


def test_home_directory_exists():
    assert HOME.is_dir(), (
        f"Expected home directory {HOME} to exist and be a directory, "
        "but it was not found."
    )


def test_custom_hosts_exists():
    assert CUSTOM_HOSTS.is_file(), (
        "The per-user hosts override file "
        f"({CUSTOM_HOSTS}) is missing. This file must be present *before* "
        "the student starts the task."
    )


def test_custom_hosts_initial_content():
    """
    Validate that /home/user/custom_hosts starts with exactly the two expected
    mappings and has not yet been modified to include the cache entry.
    """
    contents = CUSTOM_HOSTS.read_text(encoding="utf-8").splitlines()
    assert contents, (
        f"{CUSTOM_HOSTS} exists but is empty. It should begin with two host "
        "mappings for the database and API services."
    )

    # The file must have exactly the two expected lines at the outset.
    assert contents == EXPECTED_LINES, (
        f"{CUSTOM_HOSTS} should initially contain ONLY the following two lines:\n"
        f"  1. {EXPECTED_LINES[0]}\n"
        f"  2. {EXPECTED_LINES[1]}\n"
        f"Found instead:\n"
        + "\n".join(f"  • {line}" for line in contents)
    )

    # Additional sanity: the missing mapping must NOT be present.
    assert not any(MISSING_MAPPING in line for line in contents), (
        f"{CUSTOM_HOSTS} already contains an entry for {MISSING_MAPPING}; "
        "the initial state should *not* include this mapping."
    )