# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state **before**
# the student starts working on the assignment.  It checks only for the
# prerequisite files/directories that must already exist; it **must not**
# look for any artefacts that the student is expected to create later
# (archive, restore dir, checksum log, etc.).

import os
from pathlib import Path

PROJECT_ROOT = Path("/home/user/project")

EXPECTED_RELATIVE_FILE_PATHS = {
    Path("app.conf"),
    Path("db.conf"),
    Path("env/dev.env"),
    Path("env/prod.env"),
}

EXPECTED_FILE_CONTENTS = {
    Path("app.conf"): "version=1.0\n",
    Path("db.conf"): "host=localhost\nport=5432\n",
    Path("env/dev.env"): "DEBUG=true\n",
    Path("env/prod.env"): "DEBUG=false\n",
}


def _collect_relative_file_paths(root: Path):
    """
    Walk the directory tree starting at `root` and return a set of Paths
    that are **relative** to `root`.  Only regular files are included.
    """
    rel_paths = set()
    for dirpath, _, filenames in os.walk(root):
        dirpath_p = Path(dirpath)
        for fname in filenames:
            file_path = dirpath_p / fname
            rel_paths.add(file_path.relative_to(root))
    return rel_paths


def test_project_directory_exists():
    assert PROJECT_ROOT.exists(), f"Directory {PROJECT_ROOT} does not exist."
    assert PROJECT_ROOT.is_dir(), f"{PROJECT_ROOT} exists but is not a directory."


def test_required_files_exist():
    for rel_path in EXPECTED_RELATIVE_FILE_PATHS:
        full_path = PROJECT_ROOT / rel_path
        assert full_path.exists(), f"Required file {full_path} is missing."
        assert full_path.is_file(), f"{full_path} exists but is not a regular file."


def test_no_extra_files_present():
    """Ensure the project directory contains *exactly* the expected files."""
    actual_files = _collect_relative_file_paths(PROJECT_ROOT)
    assert actual_files == EXPECTED_RELATIVE_FILE_PATHS, (
        "The project directory should contain exactly the following files:\n"
        f"{sorted(str(p) for p in EXPECTED_RELATIVE_FILE_PATHS)}\n"
        f"Found instead:\n"
        f"{sorted(str(p) for p in actual_files)}"
    )


def test_file_contents_are_as_expected():
    """Validate that each file has the precise contents specified in the task."""
    for rel_path, expected_content in EXPECTED_FILE_CONTENTS.items():
        full_path = PROJECT_ROOT / rel_path
        with full_path.open("r", encoding="utf-8") as f:
            actual_content = f.read()
        assert actual_content == expected_content, (
            f"Content mismatch in {full_path}.\n"
            f"Expected:\n{expected_content!r}\n"
            f"Found:\n{actual_content!r}"
        )