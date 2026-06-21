# test_initial_state.py
#
# This PyTest suite validates the *initial* operating-system / file-system
# state **before** the student attempts the exercise.  It deliberately
# avoids checking for any artefacts that are supposed to be created by the
# student (e.g. the audit log).  All failures include clear explanations so
# that a student immediately knows what is missing or incorrect.
#
# Requirements verified:
#   1. Presence, permissions and contents of the source directory
#      /home/user/compliance_reports/ and its two expected files.
#   2. Presence and emptiness of the destination directory
#      /home/user/remote_mount/compliance_staging/.
#   3. Absence of the audit-log directory /home/user/compliance_audit_logs/
#      at start-up (it must be created later by the student).

import os
from pathlib import Path
import stat
import pytest

# ---------- Constants used throughout the tests ---------- #

HOME = Path("/home/user").resolve()

SRC_DIR = HOME / "compliance_reports"
SRC_FILES = {
    "report_Q1.txt": "Quarter 1 compliance results – draft\n",
    "report_Q2.txt": "Quarter 2 compliance results – draft\n",
}

DEST_DIR = HOME / "remote_mount" / "compliance_staging"

AUDIT_DIR = HOME / "compliance_audit_logs"


# ---------- Helper utilities ---------- #

def _assert_min_permissions(path: Path, expected_octal: int):
    """
    Assert that `path` has *at least* the requested permission bits when
    masked against 0o777 (i.e. rwx for user/group/other).  Group/other may
    have additional permissions.
    """
    mode = path.stat().st_mode & 0o777
    missing = expected_octal & ~mode
    assert missing == 0, (
        f"{path} exists but permissions {oct(mode)} are too restrictive; "
        f"expected at least {oct(expected_octal)}"
    )


# ---------- Tests ---------- #

def test_source_directory_exists_and_permissions():
    assert SRC_DIR.is_dir(), (
        f"Required source directory {SRC_DIR} is missing or not a directory."
    )
    _assert_min_permissions(SRC_DIR, 0o755)


@pytest.mark.parametrize("filename,expected_content", SRC_FILES.items())
def test_source_files_exist_permissions_and_contents(filename, expected_content):
    file_path = SRC_DIR / filename
    assert file_path.is_file(), (
        f"Expected file {file_path} is missing."
    )
    _assert_min_permissions(file_path, 0o644)

    with file_path.open("r", encoding="utf-8") as fp:
        data = fp.read()
    assert data == expected_content, (
        f"Contents of {file_path} do not match expected.\n"
        f"Expected: {repr(expected_content)}\nGot     : {repr(data)}"
    )


def test_no_extra_files_in_source_directory():
    """
    Ensure there are *exactly* the expected files (no mystery extras) in the
    source directory.  Hidden files (dotfiles) are also flagged as extras.
    """
    present = sorted(p.name for p in SRC_DIR.iterdir())
    expected = sorted(SRC_FILES.keys())
    assert present == expected, (
        f"Source directory {SRC_DIR} should contain only {expected} but "
        f"currently contains {present}."
    )


def test_destination_directory_exists_and_empty():
    assert DEST_DIR.is_dir(), (
        f"Destination directory {DEST_DIR} is missing or not a directory."
    )
    _assert_min_permissions(DEST_DIR, 0o755)

    # The directory should be empty before the student runs rsync.
    contents = [p.name for p in DEST_DIR.iterdir()]
    assert contents == [], (
        f"Destination directory {DEST_DIR} must start out empty, "
        f"but currently contains: {contents}"
    )


def test_audit_directory_does_not_exist_yet():
    assert not AUDIT_DIR.exists(), (
        f"The directory {AUDIT_DIR} should NOT exist before the student "
        f"runs their solution."
    )