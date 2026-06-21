# test_initial_state.py
#
# Pytest suite to verify the *initial* (pre-task) state of the
# operating-system / filesystem for the “flat-file user database”
# exercise.
#
# These checks make sure that the final, required artefacts do *not*
# already exist (or do not yet contain their expected final state).
# The student must bring the system from this initial state to the
# final state described in the assignment.

import os
from pathlib import Path

import pytest

HOME_DIR = Path("/home/user")
SITE_ADMIN_DIR = HOME_DIR / "site_admin"

USERS_CSV = SITE_ADMIN_DIR / "users.csv"
SUMMARY_LOG = SITE_ADMIN_DIR / "user_summary.log"
OPS_LOG = SITE_ADMIN_DIR / "ops.log"

# Final, target contents — used to ensure the files do **not** already
# contain the finished result.
_final_users_csv = (
    "username,email,role\n"
    "alice,alice@example.com,admin\n"
    "bob,bob@example.com,editor\n"
    "carol,carol@example.com,viewer\n"
    "dave,dave@example.com,editor\n"
)

_final_summary_log = "Total Users: 4\n"

_final_ops_log = (
    "STEP 1: Created directory site_admin\n"
    "STEP 2: Initialized users.csv with default users\n"
    "STEP 3: Added user carol\n"
    "STEP 4: Added user dave\n"
    "STEP 5: Generated user_summary.log\n"
)


def _file_has_final_contents(path: Path, expected: str) -> bool:
    """
    Helper that returns True if ‘path’ exists *and* its exact byte
    content matches ‘expected’.
    """
    if not path.is_file():
        return False
    try:
        data = path.read_bytes()
    except OSError:
        # If the file cannot be read for some reason, treat it as not
        # containing the final, correct contents.
        return False

    # All required files are text files with LF endings and UTF-8
    # encoding.  We compare bytes to avoid any ambiguity.
    return data == expected.encode()


def test_home_directory_exists_and_is_directory():
    assert HOME_DIR.exists(), f"Expected home directory {HOME_DIR} to exist."
    assert HOME_DIR.is_dir(), f"{HOME_DIR} exists but is not a directory."


def test_site_admin_directory_may_exist_but_is_not_finalised():
    """
    The site_admin directory may or may not exist before the student
    starts.  If it exists, we merely assert that it does **not** yet
    contain all three finished artefacts with their final, correct
    contents.
    """
    if not SITE_ADMIN_DIR.exists():
        # Perfectly acceptable starting state.
        pytest.skip(f"{SITE_ADMIN_DIR} does not exist yet — OK for initial state")

    assert SITE_ADMIN_DIR.is_dir(), (
        f"{SITE_ADMIN_DIR} exists but is not a directory. "
        "Please remove or rename it before beginning the exercise."
    )

    # Check that none of the three required files already contain their
    # final, correct contents.
    assert not _file_has_final_contents(
        USERS_CSV, _final_users_csv
    ), (
        "users.csv is already present with the final, expected contents.\n"
        "It should not exist (or should have different contents) before "
        "the student performs the required steps."
    )

    assert not _file_has_final_contents(
        SUMMARY_LOG, _final_summary_log
    ), (
        "user_summary.log already contains the final, expected contents. "
        "It should not be finalised before the student runs their commands."
    )

    assert not _file_has_final_contents(
        OPS_LOG, _final_ops_log
    ), (
        "ops.log already contains the final, expected contents. "
        "It should not be finalised before the student runs their commands."
    )


@pytest.mark.parametrize(
    "path,expected_content",
    [
        (USERS_CSV, _final_users_csv),
        (SUMMARY_LOG, _final_summary_log),
        (OPS_LOG, _final_ops_log),
    ],
)
def test_required_files_do_not_yet_have_final_contents(path: Path, expected_content: str):
    """
    For each of the three required files:
      • If the file does not exist yet → pass.
      • If the file exists, ensure it does *not* already match the final
        required content.
    """
    if not path.exists():
        # File not present yet — acceptable initial state.
        pytest.skip(f"{path} does not exist yet — OK for initial state")

    assert not _file_has_final_contents(
        path, expected_content
    ), (
        f"{path} already has the final, expected content.\n"
        "This file should be generated/updated by the student's commands, "
        "not be pre-populated."
    )