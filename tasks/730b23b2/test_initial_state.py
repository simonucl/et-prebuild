# test_initial_state.py
#
# Pytest suite that validates the initial file-system state for the
# “backup administrator” exercise *before* the student carries out any
# actions.  It purposefully ignores the future artefacts that the student
# must create under /home/user/archives, because those are considered
# output and must **not** be asserted here.
#
# Requirements verified:
#   * The directory tree /home/user/projects exists.
#   * All expected sub-directories exist and are of mode 0755.
#   * All expected regular files exist, have the exact byte size and the
#     expected contents.
#   * No additional files or directories are present below
#     /home/user/projects (helps catch polluted environments).

import os
import stat
from pathlib import Path

PROJECT_ROOT = Path("/home/user/projects").resolve()

EXPECTED_DIRS = {
    PROJECT_ROOT,
    PROJECT_ROOT / "site1",
    PROJECT_ROOT / "site2",
    PROJECT_ROOT / "site2" / "data",
}

# Mapping of absolute path -> (expected_size, expected_contents)
EXPECTED_FILES = {
    PROJECT_ROOT / "site1" / "index.html": (19, "<html>Site1</html>\n"),
    PROJECT_ROOT / "site1" / "config.yml": (15, "theme: minimal\n"),
    PROJECT_ROOT / "site2" / "README.md": (8, "# Site2\n"),
    PROJECT_ROOT / "site2" / "data" / "info.txt": (5, "Info\n"),
}


def _mode(path: Path) -> int:
    """Return the permission bits (e.g. 0o755) for a path."""
    return stat.S_IMODE(os.stat(path, follow_symlinks=False).st_mode)


def test_projects_directory_exists_and_permissions():
    assert PROJECT_ROOT.exists(), (
        f"Expected directory '{PROJECT_ROOT}' is missing. "
        "The exercise begins with a populated /home/user/projects tree."
    )
    assert PROJECT_ROOT.is_dir(), f"'{PROJECT_ROOT}' exists but is not a directory."
    # Check every expected directory exists with mode 0755
    for dpath in EXPECTED_DIRS:
        assert dpath.exists(), f"Required directory '{dpath}' is missing."
        assert dpath.is_dir(), f"'{dpath}' is expected to be a directory."
        assert _mode(dpath) == 0o755, (
            f"Directory '{dpath}' should have mode 0755 "
            f"(drwxr-xr-x) but has {_mode(dpath):#o}."
        )


def test_expected_files_exist_and_contents_match():
    for fpath, (expected_size, expected_contents) in EXPECTED_FILES.items():
        assert fpath.exists(), f"Required file '{fpath}' is missing."
        assert fpath.is_file(), f"'{fpath}' exists but is not a regular file."
        actual_size = fpath.stat().st_size
        assert actual_size == expected_size, (
            f"File '{fpath}' has size {actual_size} bytes; "
            f"expected {expected_size} bytes."
        )

        # Read as text; all sample files are UTF-8 friendly.
        with fpath.open("r", encoding="utf-8") as fh:
            data = fh.read()
        assert data == expected_contents, (
            f"Contents of '{fpath}' do not match the required initial "
            "state for the exercise."
        )


def test_no_extra_files_or_directories_present():
    """
    The supplied environment must not contain any additional files or
    directories beneath /home/user/projects.  This guards against a dirty
    workspace that could interfere with later grading of the student's
    manifest and tarball.
    """
    actual_dirs = set()
    actual_files = set()

    for dirpath, dirnames, filenames in os.walk(PROJECT_ROOT, topdown=True, followlinks=False):
        dpath = Path(dirpath)
        actual_dirs.add(dpath.resolve())
        # Collect files
        for fname in filenames:
            actual_files.add((dpath / fname).resolve())

    # Directories
    missing_dirs = EXPECTED_DIRS - actual_dirs
    extra_dirs = actual_dirs - EXPECTED_DIRS
    assert not missing_dirs, f"Missing expected directories: {', '.join(map(str, missing_dirs))}"
    assert not extra_dirs, f"Unexpected extra directories found: {', '.join(map(str, extra_dirs))}"

    # Files
    expected_file_paths = set(EXPECTED_FILES.keys())
    missing_files = expected_file_paths - actual_files
    extra_files = actual_files - expected_file_paths
    assert not missing_files, f"Missing expected files: {', '.join(map(str, missing_files))}"
    assert not extra_files, f"Unexpected extra files found: {', '.join(map(str, extra_files))}"