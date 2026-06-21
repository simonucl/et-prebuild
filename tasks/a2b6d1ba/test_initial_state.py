# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state before the
# student performs any work on the “daily log-rotation” task.
#
# The tests confirm that:
#   • The required directories already exist.
#   • The two existing security.log files are present, are regular files,
#     and contain the expected text.
#   • No symlinks (“latest” or top-level security.log) exist yet.
#   • No audit file (symlink_audit.txt) exists yet.
#
# Only stdlib + pytest are used.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
COMPLIANCE_DIR = HOME / "compliance"
LOGS_DIR = COMPLIANCE_DIR / "logs"

# Expected pre-existing directories
PREEXISTING_DIRS = [
    COMPLIANCE_DIR,
    LOGS_DIR,
    LOGS_DIR / "2024-02-01",
    LOGS_DIR / "2024-02-02",
]

# Expected pre-existing files and their exact content (with a trailing newline)
PREEXISTING_FILES = {
    LOGS_DIR / "2024-02-01" / "security.log": "SECURITY LOG 2024-02-01\n",
    LOGS_DIR / "2024-02-02" / "security.log": "SECURITY LOG 2024-02-02\n",
}

# Paths that should *not* exist prior to the student’s actions
SHOULD_NOT_EXIST = [
    LOGS_DIR / "latest",
    COMPLIANCE_DIR / "security.log",
    COMPLIANCE_DIR / "symlink_audit.txt",
]


@pytest.mark.parametrize("path", PREEXISTING_DIRS)
def test_required_directories_exist(path: Path):
    assert path.exists(), f"Required directory does not exist: {path}"
    assert path.is_dir(), f"Expected directory but found something else: {path}"


@pytest.mark.parametrize("file_path, expected_contents", PREEXISTING_FILES.items())
def test_security_logs_exist_with_correct_content(file_path: Path, expected_contents: str):
    assert file_path.exists(), f"Required file does not exist: {file_path}"
    assert file_path.is_file(), f"Expected a regular file at {file_path}, but found something else."
    assert not file_path.is_symlink(), f"{file_path} should be a regular file, not a symlink."

    # Read file and compare contents (allowing for trailing newlines / EOF variance)
    with file_path.open("r", encoding="utf-8") as fh:
        contents = fh.read()
    assert contents == expected_contents, (
        f"Contents of {file_path} are incorrect.\n"
        f"Expected: {repr(expected_contents)}\n"
        f"Found:    {repr(contents)}"
    )


@pytest.mark.parametrize("path", SHOULD_NOT_EXIST)
def test_symlinks_and_audit_file_do_not_exist_yet(path: Path):
    assert not path.exists(), (
        f"{path} should NOT exist before the student performs any actions, "
        "but it already exists."
    )
    # Additionally, catch the rare case of a dangling symlink
    if path.is_symlink():
        raise AssertionError(f"{path} is an unexpected symlink that should not be present.")