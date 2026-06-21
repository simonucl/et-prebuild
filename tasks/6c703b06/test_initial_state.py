# test_initial_state.py
#
# This test-suite validates the **initial** on-disk state *before* the student
# runs any command.  If any of these tests fail, the exercise environment is
# corrupted and the student cannot possibly succeed.
#
# Requirements checked:
#   • The log directory tree exists exactly as described.
#   • All expected “.tmp” files are present.
#   • No unexpected “.tmp” files are present.
#   • All expected non-“.tmp” files are present.
#   • The file /home/user/deleted_tmp.log does NOT yet exist.

import os
from pathlib import Path

ROOT_DIR = Path("/home/user/storage/logs")

# Directories that must exist
EXPECTED_DIRS = {
    ROOT_DIR,
    ROOT_DIR / "app1",
    ROOT_DIR / "app2",
    ROOT_DIR / "app2" / "archive",
}

# “.tmp” files that must exist *and* will later be deleted
EXPECTED_TMP_FILES = {
    ROOT_DIR / "root.tmp",
    ROOT_DIR / "app1" / "upload.tmp",
    ROOT_DIR / "app1" / "session.tmp",
    ROOT_DIR / "app2" / "archive" / "cache.tmp",
    ROOT_DIR / "app2" / "archive" / "old_2021.tmp",
}

# Non-“.tmp” files that must stay intact for the entire exercise
EXPECTED_NON_TMP_FILES = {
    ROOT_DIR / "keep.log",
    ROOT_DIR / "app1" / "info.log",
    ROOT_DIR / "app2" / "error.log",
}

LOG_FILE = Path("/home/user/deleted_tmp.log")


def _pretty(paths):
    """Return a sorted, newline-joined representation of a set of paths."""
    return "\n".join(sorted(str(p) for p in paths))


def test_required_directories_exist():
    """All directories that the grader relies on must be present."""
    missing_dirs = {d for d in EXPECTED_DIRS if not d.is_dir()}
    assert not missing_dirs, (
        "The following required directories are missing:\n"
        f"{_pretty(missing_dirs)}"
    )


def test_expected_tmp_files_exist():
    """Every .tmp file listed in the task description must exist."""
    missing_files = {f for f in EXPECTED_TMP_FILES if not f.is_file()}
    assert not missing_files, (
        "The following required .tmp files are missing:\n"
        f"{_pretty(missing_files)}"
    )


def test_no_unexpected_tmp_files_exist():
    """
    There must be **exactly** the five .tmp files specified—no more, no less.
    Extra .tmp files could cause the student’s deletion command to fail
    validation later on.
    """
    # Walk the tree and collect every *.tmp file that currently exists.
    current_tmp_files = {
        Path(root) / name
        for root, _, files in os.walk(ROOT_DIR)
        for name in files
        if name.endswith(".tmp")
    }

    unexpected = current_tmp_files - EXPECTED_TMP_FILES
    missing     = EXPECTED_TMP_FILES - current_tmp_files

    assert not unexpected and not missing, (
        "Mismatch between expected and found .tmp files.\n"
        f"Missing:\n{_pretty(missing) or '  (none)'}\n\n"
        f"Unexpected:\n{_pretty(unexpected) or '  (none)'}"
    )


def test_expected_non_tmp_files_exist():
    """Non-.tmp files that should remain untouched must be present."""
    missing_files = {f for f in EXPECTED_NON_TMP_FILES if not f.is_file()}
    assert not missing_files, (
        "The following required non-.tmp files are missing:\n"
        f"{_pretty(missing_files)}"
    )


def test_deleted_tmp_log_absent_initially():
    """
    The log file that the student is supposed to create must **not** exist yet.
    Its presence would indicate that the task has already been attempted or
    the environment is contaminated.
    """
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} already exists, but it should be created only after the "
        "student runs their single-line command."
    )