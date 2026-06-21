# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem
# before the student performs any work.  It checks only the resources
# that must already be present and explicitly avoids touching anything
# that will be produced later by the student (/home/user/backups/**).

import hashlib
from pathlib import Path

import pytest


PROJECT_ROOT = Path("/home/user/project_files").resolve()

EXPECTED_FILES = {
    "file1.txt": b"Hello Backup\n",
    "file2.txt": b"Data Integrity Test\n",
}


def test_project_directory_exists_and_is_directory():
    """
    /home/user/project_files must exist and be a directory.
    """
    assert PROJECT_ROOT.exists(), (
        f"Expected directory {PROJECT_ROOT} does not exist. "
        "Create it with the required files before proceeding."
    )
    assert PROJECT_ROOT.is_dir(), (
        f"{PROJECT_ROOT} exists but is not a directory. "
        "It must be a directory containing the project files."
    )


def test_expected_files_present_with_correct_contents():
    """
    The project directory must contain exactly the two expected files,
    and their contents must match the specification *byte-for-byte*.
    """
    # Collect actual regular files in PROJECT_ROOT (ignore sub-dirs, if any)
    actual_files = {p.name: p for p in PROJECT_ROOT.iterdir() if p.is_file()}

    # 1. Presence check
    missing = sorted(set(EXPECTED_FILES) - set(actual_files))
    extra   = sorted(set(actual_files) - set(EXPECTED_FILES))

    assert not missing, (
        "The following required file(s) are missing from "
        f"{PROJECT_ROOT}: {', '.join(missing)}"
    )
    assert not extra, (
        "Unexpected file(s) found in "
        f"{PROJECT_ROOT}: {', '.join(extra)}. "
        "Only file1.txt and file2.txt should be present initially."
    )

    # 2. Content check
    for filename, expected_bytes in EXPECTED_FILES.items():
        path = actual_files[filename]
        actual_bytes = path.read_bytes()
        if actual_bytes != expected_bytes:
            # Show a helpful diff without dumping whole file
            exp_hash = hashlib.sha256(expected_bytes).hexdigest()
            act_hash = hashlib.sha256(actual_bytes).hexdigest()
            pytest.fail(
                f"Contents of {path} do not match the expected specification.\n"
                f"Expected SHA-256: {exp_hash}\n"
                f"Actual   SHA-256: {act_hash}\n"
                "Ensure the file has exactly the required bytes "
                "including the newline."
            )