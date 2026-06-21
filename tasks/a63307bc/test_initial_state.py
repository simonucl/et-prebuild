# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must be in
# place **before** the student runs their shell command.  If any of these
# checks fail it means the starting environment is wrong, not that the
# student’s solution is incorrect.

import os
import stat
import pytest

HOME = "/home/user"
INCIDENT_DIR = os.path.join(HOME, "incident")
DOTENV_PATH = os.path.join(INCIDENT_DIR, ".env.incident")

# The dotenv file must contain exactly these four lines (each terminated by \n)
EXPECTED_DOTENV_LINES = [
    "DB_USER=central\n",
    "DB_PASS=R3sp0nder!\n",
    "INCIDENT_ID=ZA-8841\n",
    "API_TOKEN=762f4e86-9d48-4d6a-8e63-25f00ec3f3c9\n",
]


def _human_path(path: str) -> str:  # helper for clearer assertion messages
    return repr(path)


def test_incident_directory_exists_and_is_writable():
    """The /home/user/incident directory must exist and be writable."""
    assert os.path.isdir(INCIDENT_DIR), (
        f"Required directory {_human_path(INCIDENT_DIR)} does not exist "
        "or is not a directory."
    )

    # Check that the directory is writable by the current user.
    assert os.access(INCIDENT_DIR, os.W_OK), (
        f"Directory {_human_path(INCIDENT_DIR)} exists but is not writable "
        "by the current user."
    )


def test_dotenv_file_exists_with_correct_contents():
    """Validate the presence and exact contents of the .env.incident file."""
    assert os.path.isfile(DOTENV_PATH), (
        f"Required dotenv file {_human_path(DOTENV_PATH)} is missing."
    )

    # Read the file *exactly* as text with newline characters preserved.
    with open(DOTENV_PATH, "r", encoding="utf-8") as fp:
        lines = fp.readlines()

    # Check that we have exactly four lines.
    assert len(lines) == 4, (
        f"Expected exactly 4 lines in {_human_path(DOTENV_PATH)}, "
        f"found {len(lines)}.\nLines read: {lines}"
    )

    # Compare line-by-line with the expected content.
    for expected, actual in zip(EXPECTED_DOTENV_LINES, lines):
        assert actual == expected, (
            f"Mismatch in {_human_path(DOTENV_PATH)}.\n"
            f"Expected line: {expected!r}\n"
            f"Actual line:   {actual!r}"
        )