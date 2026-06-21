# test_initial_state.py
#
# This pytest suite validates that the starting filesystem state is
# exactly what the assignment description promises *before* the student
# begins any work.  If any assertion here fails, either the environment
# was not provisioned correctly or someone has already modified it.
#
# Only the standard library and pytest are used, per the project rules.

import os
from pathlib import Path
import stat
import pytest

CREDS_DIR = Path("/home/user/creds")
CURRENT_FILE = CREDS_DIR / "current_creds.csv"
NEW_FILE = CREDS_DIR / "new_creds.csv"
ROTATED_FILE = CREDS_DIR / "rotated_creds.csv"
REPORT_FILE = CREDS_DIR / "rotation_report.log"


@pytest.fixture(scope="module")
def expected_current_lines():
    return [
        "username,service,old_key,expiry,notes",
        "alice,db,AKIAOLDALICE,2023-12-31,rotate soon",
        "bob,web,AKIABOBOLD,2023-10-31,-",
        "carol,cache,AKIACACHEOLD,2023-11-30,urgent",
    ]


@pytest.fixture(scope="module")
def expected_new_lines():
    return [
        "username,service,new_key,issued,valid_until",
        "alice,db,AKIANEWALICE,2023-09-01,2024-09-01",
        "bob,web,AKIANEWB0B,2023-08-15,2024-08-15",
        "carol,cache,AKIANEWCACHE,2023-09-10,2024-09-10",
    ]


def test_creds_directory_exists():
    assert CREDS_DIR.is_dir(), f"Required directory {CREDS_DIR} is missing."


def test_current_creds_exists_and_contents(expected_current_lines):
    assert CURRENT_FILE.is_file(), f"{CURRENT_FILE} is missing."

    with CURRENT_FILE.open("r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    assert lines == expected_current_lines, (
        f"Contents of {CURRENT_FILE} do not match the expected initial state.\n"
        f"Expected lines:\n{expected_current_lines}\n\nActual lines:\n{lines}"
    )


def test_new_creds_exists_and_contents(expected_new_lines):
    assert NEW_FILE.is_file(), f"{NEW_FILE} is missing."

    with NEW_FILE.open("r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    assert lines == expected_new_lines, (
        f"Contents of {NEW_FILE} do not match the expected initial state.\n"
        f"Expected lines:\n{expected_new_lines}\n\nActual lines:\n{lines}"
    )


def test_rotated_creds_not_yet_present():
    assert not ROTATED_FILE.exists(), (
        f"{ROTATED_FILE} already exists—but it should be created *after* "
        "the student runs their solution."
    )


def test_rotation_report_not_yet_present():
    assert not REPORT_FILE.exists(), (
        f"{REPORT_FILE} already exists—but it should be produced *after* "
        "the student runs their solution."
    )


def test_sample_files_are_world_inaccessible():
    """
    The starter CSVs do not need to be world-readable or writable.
    They should at minimum prevent world write (the assignment does not
    specify a precise mode, but 600 or 644 are both acceptable here).
    """
    for path in (CURRENT_FILE, NEW_FILE):
        mode = path.stat().st_mode
        assert not (mode & stat.S_IWOTH), f"{path} is world-writable, which is unsafe."
        assert not (mode & stat.S_IXOTH), f"{path} has the world execute bit set unexpectedly."