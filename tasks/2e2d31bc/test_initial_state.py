# test_initial_state.py
#
# This test-suite validates that the operating system / filesystem is in the
# *initial* state expected *before* the student performs any actions for the
# “user-accounts” exercise.
#
# The suite checks only the pre-existing inputs and environment; it does NOT
# look for the output artefacts that the student is going to create.  In fact
# it explicitly asserts that those output files do **not** exist yet.
#
# Only the Python standard library + pytest are used, in accordance with the
# grading infrastructure requirements.

import json
import os
import stat
import subprocess
from shutil import which
import pytest
from pathlib import Path

# Constants
HOME = Path("/home/user")
ACCOUNTS_DIR = HOME / "accounts"

USERS_JSON = ACCOUNTS_DIR / "users.json"
SCHEMA_JSON = ACCOUNTS_DIR / "users_schema.json"

# Files that *must not* exist yet (they will be created by the student)
ACTIVE_USERS_TXT = ACCOUNTS_DIR / "active_users.txt"
VALIDATION_LOG   = ACCOUNTS_DIR / "validation.log"

EXPECTED_USERS = [
    {
        "username": "alice",
        "email": "alice@example.com",
        "active": True,
        "roles": ["admin", "editor"],
    },
    {
        "username": "bob",
        "email": "bob@example.com",
        "active": False,
        "roles": ["viewer"],
    },
    {
        "username": "carol",
        "email": "carol@example.com",
        "active": True,
        "roles": ["editor"],
    },
    {
        "username": "dave",
        "email": "dave@example.com",
        "active": True,
        "roles": ["viewer", "support"],
    },
    {
        "username": "eve",
        "email": "eve@example.com",
        "active": False,
        "roles": ["suspended"],
    },
]

###############################################################################
# Helper utilities
###############################################################################

def assert_file_readable(path: Path, msg: str):
    """
    Assert that `path` exists, is a regular file and is readable.
    """
    assert path.exists(), f"{msg}: {path} does not exist."
    assert path.is_file(), f"{msg}: {path} exists but is not a regular file."
    # Check read permission bits for user
    st_mode = path.stat().st_mode
    assert st_mode & stat.S_IRUSR, f"{msg}: {path} is not readable by the user."


###############################################################################
# Tests
###############################################################################

def test_accounts_directory_exists():
    assert ACCOUNTS_DIR.exists(), f"Directory {ACCOUNTS_DIR} is missing."
    assert ACCOUNTS_DIR.is_dir(), f"{ACCOUNTS_DIR} exists but is not a directory."


def test_input_files_exist_and_are_readable():
    assert_file_readable(USERS_JSON, "Input file missing or unreadable")
    assert_file_readable(SCHEMA_JSON, "Schema file missing or unreadable")


def test_users_json_content_matches_expected():
    """
    Ensure that the initial users.json file contains *exactly* the expected
    five records so that later tasks work with known data.
    """
    with USERS_JSON.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    assert isinstance(data, list), (
        f"{USERS_JSON} should contain a JSON array, found {type(data).__name__}."
    )
    assert len(data) == len(EXPECTED_USERS), (
        f"{USERS_JSON} should have {len(EXPECTED_USERS)} user records, "
        f"found {len(data)}."
    )

    # Compare each dict; order matters because the reference order is known.
    for idx, (actual, expected) in enumerate(zip(data, EXPECTED_USERS), start=1):
        assert actual == expected, (
            f"Mismatch in user record #{idx} inside {USERS_JSON}.\n"
            f"Expected: {expected}\nActual:   {actual}"
        )


def test_schema_json_is_valid_json():
    """
    The schema must at least be parseable JSON (full JSON-Schema validation is
    not performed here to keep the dependency footprint minimal).
    """
    with SCHEMA_JSON.open("r", encoding="utf-8") as fh:
        try:
            json.load(fh)
        except json.JSONDecodeError as err:
            pytest.fail(f"{SCHEMA_JSON} is not valid JSON: {err}")


def test_no_output_files_exist_yet():
    """
    The files that the student is required to create must *not* exist prior to
    starting the exercise.  Their premature presence would indicate that the
    environment is in the wrong state.
    """
    for path in (ACTIVE_USERS_TXT, VALIDATION_LOG):
        assert not path.exists(), (
            f"Output file {path} already exists but should not be present "
            f"in the initial state."
        )


def test_jq_is_installed_and_callable():
    """
    The exercise instructions allow the use of `jq`.  Ensure it is installed
    and executable so the student can rely on it.
    """
    jq_path = which("jq")
    assert jq_path is not None, (
        "The command‐line tool 'jq' is not available in PATH. "
        "It is required by the exercise instructions."
    )
    # Also ensure it runs without raising an OSError.
    try:
        subprocess.run(["jq", "--version"], check=True, capture_output=True, text=True)
    except Exception as exc:
        pytest.fail(f"'jq' exists at {jq_path} but could not be executed: {exc}")