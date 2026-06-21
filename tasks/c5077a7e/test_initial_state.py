# test_initial_state.py
#
# This pytest suite verifies the initial filesystem state *before* the student
# performs any actions for the “disabled accounts” task.

import os
import pytest

HOME = "/home/user"
ACCOUNTS_FILE = os.path.join(HOME, "user_accounts.txt")
DISABLED_LOG = os.path.join(HOME, "disabled_accounts.log")


@pytest.fixture(scope="module")
def accounts_content():
    """
    Read the whole accounts file once for all tests.
    """
    try:
        with open(ACCOUNTS_FILE, "rb") as f:
            return f.read()
    except FileNotFoundError:
        pytest.fail(
            f"Required file not found: {ACCOUNTS_FILE!r}. "
            "It must be present before the task starts."
        )


def test_accounts_file_exists():
    """
    The main user database must exist as a regular file.
    """
    assert os.path.isfile(
        ACCOUNTS_FILE
    ), f"The user accounts file {ACCOUNTS_FILE!r} is missing."


def test_accounts_file_contents(accounts_content):
    """
    Verify the exact initial contents (including final newline).
    """
    expected = (
        b"john ENABLED\n"
        b"mary DISABLED\n"
        b"peter ENABLED\n"
        b"susan DISABLED\n"
        b"david DISABLED\n"
    )

    assert accounts_content == expected, (
        f"The contents of {ACCOUNTS_FILE!r} do not match the expected initial "
        "dataset. They must be exactly:\n\n"
        "john ENABLED\n"
        "mary DISABLED\n"
        "peter ENABLED\n"
        "susan DISABLED\n"
        "david DISABLED\n"
    )


def test_disabled_log_absent():
    """
    The report file must NOT exist before the student runs their command.
    """
    assert not os.path.exists(
        DISABLED_LOG
    ), f"The file {DISABLED_LOG!r} should not exist before the task begins."