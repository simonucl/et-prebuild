# test_initial_state.py
"""
Pytest suite that validates the operating-system / filesystem *before* the
student performs any action.

This file checks that the cloned repository located at
    /home/user/my_project
has the expected initial layout and that the `file_manifest.log` file that the
student is supposed to create does **not** yet exist.

Only the Python standard library and pytest are used.
"""

import os
from pathlib import Path

ROOT = Path("/home/user/my_project").resolve()

# Expected directory names (absolute paths)
EXPECTED_DIRS = {
    ROOT,
    ROOT / "docs",
    ROOT / "src",
    ROOT / "tests",
}

# Expected regular files (absolute paths)
EXPECTED_FILES = {
    ROOT / "README.md",
    ROOT / "docs" / "usage.txt",
    ROOT / "src" / "app.py",
    ROOT / "src" / "helpers.py",
    ROOT / "tests" / "test_app.py",
    ROOT / "tests" / "test_helpers.py",
}

MANIFEST_PATH = ROOT / "file_manifest.log"


def test_repository_root_exists_and_is_directory():
    assert ROOT.exists(), f"Expected repository root {ROOT} to exist."
    assert ROOT.is_dir(), f"Expected {ROOT} to be a directory."


def test_expected_directories_exist_and_are_directories():
    for directory in EXPECTED_DIRS:
        assert directory.exists(), f"Expected directory {directory} to exist."
        assert directory.is_dir(), f"Expected {directory} to be a directory."
    # Ensure no unexpected symlink in place of a directory
    for directory in EXPECTED_DIRS:
        assert not directory.is_symlink(), f"{directory} should be a real directory, not a symlink."


def test_expected_files_exist_and_are_regular_files():
    for file_path in EXPECTED_FILES:
        assert file_path.exists(), f"Expected file {file_path} to exist."
        assert file_path.is_file(), f"Expected {file_path} to be a regular file."
        assert not file_path.is_symlink(), f"{file_path} should be a regular file, not a symlink."


def test_no_extra_regular_files_present():
    """
    Walk the repository tree and ensure that *exactly* the expected six regular
    files are present. This prevents accidental extra files from being checked
    into the repo before the task begins.
    """
    discovered_files = set()

    for dirpath, dirnames, filenames in os.walk(ROOT):
        for fname in filenames:
            fpath = Path(dirpath) / fname
            # Skip manifest file if someone accidentally created it already
            if fpath == MANIFEST_PATH:
                continue
            if fpath.is_file():
                discovered_files.add(fpath.resolve())

    missing = EXPECTED_FILES - discovered_files
    unexpected = discovered_files - EXPECTED_FILES

    assert not missing, (
        "The following expected files are missing from the repository:\n"
        + "\n".join(str(p) for p in sorted(missing))
    )
    assert not unexpected, (
        "The repository contains unexpected files that should not be present "
        "at the initial state:\n"
        + "\n".join(str(p) for p in sorted(unexpected))
    )
    assert len(discovered_files) == len(
        EXPECTED_FILES
    ), f"Expected exactly {len(EXPECTED_FILES)} regular files, found {len(discovered_files)}."


def test_manifest_does_not_exist_yet():
    assert not MANIFEST_PATH.exists(), (
        f"{MANIFEST_PATH} should NOT exist before the student performs the task. "
        "Please remove it if it was created accidentally."
    )