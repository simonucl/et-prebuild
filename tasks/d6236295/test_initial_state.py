# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem
# before the student’s solution is executed.  It makes sure that the
# predefined workspace and its files are present and unmodified.
#
# IMPORTANT:  Do **not** add checks for the file that the student is
# supposed to create (`disk_usage_report.txt`).  At this point that
# file must not exist yet.

import os
import stat
import pytest

WORKSPACE_DIR = "/home/user/utils_workspace"

# Expected files and their *apparent* (byte-for-byte) sizes.
EXPECTED_FILES = {
    "script1.sh": 36,
    "script2.sh": 36,
    "README.md": 22,
}


def _full(path_fragment: str) -> str:
    """
    Helper that returns an absolute path inside the workspace.
    """
    return os.path.join(WORKSPACE_DIR, path_fragment)


def test_workspace_directory_exists_and_is_directory():
    """
    The workspace directory must be present and be a directory.
    """
    assert os.path.exists(WORKSPACE_DIR), (
        f"Required directory {WORKSPACE_DIR!r} is missing."
    )
    assert os.path.isdir(WORKSPACE_DIR), (
        f"{WORKSPACE_DIR!r} exists but is not a directory."
    )


@pytest.mark.parametrize("filename,expected_size", EXPECTED_FILES.items())
def test_required_files_present_with_correct_size(filename, expected_size):
    """
    Each required file must exist, be a regular file, and have the
    exact byte size specified in EXPECTED_FILES.
    """
    full_path = _full(filename)

    # Existence and type.
    assert os.path.exists(full_path), (
        f"Required file {full_path!r} is missing."
    )
    mode = os.stat(full_path).st_mode
    assert stat.S_ISREG(mode), (
        f"{full_path!r} exists but is not a regular file."
    )

    # Byte-for-byte size.
    actual_size = os.path.getsize(full_path)
    assert actual_size == expected_size, (
        f"{full_path!r} has size {actual_size} bytes, "
        f"but {expected_size} bytes were expected. "
        "The file’s contents must not be altered."
    )


def test_no_extra_files_yet():
    """
    Before the student runs their code, the workspace must only contain
    the predefined files.  This check ensures that no unexpected files
    or sub-directories are present **yet**.
    """
    present_entries = sorted(os.listdir(WORKSPACE_DIR))
    expected_entries = sorted(EXPECTED_FILES.keys())

    # If the assertion fails, show the full directory listing to
    # simplify debugging.
    assert present_entries == expected_entries, (
        "The workspace directory contains unexpected files or is missing "
        "required ones.\n"
        f"Expected entries: {expected_entries}\n"
        f"Present  entries: {present_entries}\n\n"
        "Note: The student’s solution must later create "
        "'disk_usage_report.txt', which is *not* expected at this stage."
    )