# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state required for the “host count” exercise.  These tests run *before*
# the student performs any action.

import os
import stat
import pytest

HOME = "/home/user"
SERVERS_DIR = os.path.join(HOME, "servers")
HOSTS_LST = os.path.join(SERVERS_DIR, "hosts.lst")
HOSTS_COUNT = os.path.join(SERVERS_DIR, "hosts.count")

EXPECTED_HOST_LINES = [
    "host-a",
    "host-b",
    "host-c",
    "host-d",
    "host-e",
    "host-f",
    "host-g",
]


def test_servers_directory_exists_and_is_writable():
    """
    The directory /home/user/servers must exist and be writable by the current user.
    """
    assert os.path.isdir(
        SERVERS_DIR
    ), f"Required directory {SERVERS_DIR!r} does not exist or is not a directory."

    # The directory must be writable (current user has write permission).
    assert os.access(
        SERVERS_DIR, os.W_OK
    ), f"Directory {SERVERS_DIR!r} is not writable by the current user."


def test_hosts_lst_exists_with_exact_expected_content():
    """
    /home/user/servers/hosts.lst must exist and contain exactly the expected
    hostnames, one per line, each terminated by a single LF.
    """
    assert os.path.isfile(
        HOSTS_LST
    ), f"Required file {HOSTS_LST!r} does not exist."

    with open(HOSTS_LST, "r", encoding="utf-8") as f:
        content = f.read()

    expected_content = "\n".join(EXPECTED_HOST_LINES) + "\n"

    assert (
        content == expected_content
    ), (
        f"{HOSTS_LST!r} contents are incorrect.\n"
        f"Expected exactly:\n{expected_content!r}\n\n"
        f"Found:\n{content!r}"
    )

    # Also confirm the file has exactly 7 lines
    assert (
        len(content.strip().split("\n")) == 7
    ), f"{HOSTS_LST!r} should contain exactly 7 hostnames, found {len(content.strip().split())}."


def test_hosts_count_does_not_exist_yet():
    """
    The tally file /home/user/servers/hosts.count should NOT exist before the
    student runs their command.
    """
    assert not os.path.exists(
        HOSTS_COUNT
    ), (
        f"{HOSTS_COUNT!r} already exists, but it should be created only after "
        "the student runs the required one-liner."
    )