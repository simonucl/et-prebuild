# test_initial_state.py
#
# Pytest suite that verifies the *initial* operating-system / filesystem
# state before the student performs any action for the “disk_demo” task.
#
# The checks assert that:
#   • The expected directory tree exists exactly as described.
#   • File sizes match the specification.
#   • No extra files, directories, symlinks, sockets, etc. are present.
#   • The report file that the student must later create does **not** yet
#     exist.
#
# Only the Python standard library and pytest are used.

import os
import stat
from pathlib import Path

import pytest

# ----------------------------------------------------------------------
# Constants describing the expected pre-existing structure
# ----------------------------------------------------------------------

HOME                   = Path("/home/user")
ROOT_DIR               = HOME / "projects" / "disk_demo"
REPORT_FILE            = HOME / "disk_usage_report.log"

EXPECTED_IMMEDIATE = {
    ROOT_DIR / "file1.txt",
    ROOT_DIR / "file2.log",
    ROOT_DIR / "subdir",
}

EXPECTED_RECURSIVE_FILES = {
    ROOT_DIR / "file1.txt",
    ROOT_DIR / "file2.log",
    ROOT_DIR / "subdir" / "data.bin",
}

EXPECTED_RECURSIVE_DIRS = {
    ROOT_DIR,
    ROOT_DIR / "subdir",
}

EXPECTED_SIZES = {
    ROOT_DIR / "file1.txt": 1024,
    ROOT_DIR / "file2.log": 2048,
    ROOT_DIR / "subdir" / "data.bin": 3072,
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------

def _collect_paths(base: Path):
    """
    Walk *base* recursively and return two sets containing:
      • all directories  (including *base*)
      • all regular files
    Everything else (symlinks, sockets, etc.) is collected in `others`.
    """
    dirs, files, others = set(), set(), set()

    for dirpath, dirnames, filenames in os.walk(base, followlinks=False):
        dp = Path(dirpath)
        dirs.add(dp)

        # Sort lists deterministically (not strictly required but nice)
        dirnames.sort()
        filenames.sort()

        # Inspect directories (ensure they are real directories)
        for d in dirnames:
            p = dp / d
            mode = p.lstat().st_mode
            if stat.S_ISDIR(mode):
                dirs.add(p)
            else:
                others.add(p)

        # Inspect files
        for f in filenames:
            p = dp / f
            mode = p.lstat().st_mode
            if stat.S_ISREG(mode):
                files.add(p)
            else:
                others.add(p)

    return dirs, files, others


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_root_directory_exists_and_is_directory():
    assert ROOT_DIR.exists(), f"Required directory {ROOT_DIR} is missing."
    assert ROOT_DIR.is_dir(), f"{ROOT_DIR} exists but is not a directory."


def test_expected_immediate_children_present_and_no_extras():
    children = {p for p in ROOT_DIR.iterdir()}
    missing = EXPECTED_IMMEDIATE - children
    extras  = children - EXPECTED_IMMEDIATE

    assert not missing, (
        "Missing expected immediate children inside "
        f"{ROOT_DIR} : {sorted(str(m) for m in missing)}"
    )
    assert not extras, (
        "Unexpected extra items found directly inside "
        f"{ROOT_DIR} : {sorted(str(e) for e in extras)}"
    )


@pytest.mark.parametrize("path", sorted(EXPECTED_RECURSIVE_FILES, key=str))
def test_expected_files_exist_with_correct_size(path: Path):
    assert path.exists(), f"Expected file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."
    actual_size = path.stat().st_size
    expected_size = EXPECTED_SIZES[path]
    assert actual_size == expected_size, (
        f"File {path} has size {actual_size} bytes; "
        f"expected {expected_size} bytes."
    )


def test_no_unexpected_content_anywhere():
    """
    Ensures:
      • Only the declared files and directories exist under ROOT_DIR.
      • No symlinks, sockets, FIFOs, or other special files exist.
    """
    dirs, files, others = _collect_paths(ROOT_DIR)

    expected_dirs  = EXPECTED_RECURSIVE_DIRS
    expected_files = EXPECTED_RECURSIVE_FILES

    # Directories ----------------------------------------------------------------
    missing_dirs = expected_dirs - dirs
    extra_dirs   = dirs - expected_dirs
    assert not missing_dirs, (
        "Missing directories under disk_demo: "
        f"{sorted(str(d) for d in missing_dirs)}"
    )
    assert not extra_dirs, (
        "Unexpected directories under disk_demo: "
        f"{sorted(str(d) for d in extra_dirs)}"
    )

    # Files ----------------------------------------------------------------------
    missing_files = expected_files - files
    extra_files   = files - expected_files
    assert not missing_files, (
        "Missing files under disk_demo: "
        f"{sorted(str(f) for f in missing_files)}"
    )
    assert not extra_files, (
        "Unexpected extra files under disk_demo: "
        f"{sorted(str(f) for f in extra_files)}"
    )

    # Others (symlinks, sockets, etc.) -------------------------------------------
    assert not others, (
        "Found items that are not regular files or directories under "
        f"{ROOT_DIR}: {sorted(str(o) for o in others)}"
    )


def test_report_file_does_not_yet_exist():
    assert not REPORT_FILE.exists(), (
        f"The report file {REPORT_FILE} already exists, but it should NOT "
        "be present before the student runs their solution."
    )