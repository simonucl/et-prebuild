# test_initial_state.py
#
# This pytest suite validates the *initial* on-disk state **before**
# the student starts working on the backup task.  It checks that the
# required source data are present and that no deliverables already
# exist.  All paths are absolute and refer to the user’s home
# directory (/home/user).

import os
import stat
import hashlib
import pytest

HOME = "/home/user"
DATA_DIR = os.path.join(HOME, "data")
PROJECT_A = os.path.join(DATA_DIR, "projectA")
PROJECT_B = os.path.join(DATA_DIR, "projectB")
BACKUPS_DIR = os.path.join(HOME, "backups")

FILES_EXPECTED = {
    os.path.join(PROJECT_A, "report.txt"): "Annual Report 2023 final version\n",
    os.path.join(PROJECT_A, "draft.tmp"): "temporary data\n",
    os.path.join(PROJECT_B, "config.cfg"): (
        "# sample configuration\n"
        "version = 1.0\n"
        "enabled = true\n"
    ),
    os.path.join(PROJECT_B, "notes.txt"): (
        "Meeting notes for upcoming release\n"
        "Remember to update changelog.\n"
    ),
}

ARCHIVE      = os.path.join(BACKUPS_DIR, "data_backup.tar.gz")
CHECKSUM     = ARCHIVE + ".sha256"
LOGFILE      = os.path.join(BACKUPS_DIR, "backup.log")


@pytest.mark.parametrize(
    "path",
    [DATA_DIR, PROJECT_A, PROJECT_B],
)
def test_required_directories_exist(path):
    assert os.path.isdir(path), f"Required directory missing: {path}"


def test_expected_subdirectories_only():
    """/home/user/data/ must contain exactly the two project directories."""
    subdirs = sorted(
        d for d in os.listdir(DATA_DIR)
        if os.path.isdir(os.path.join(DATA_DIR, d))
    )
    assert subdirs == ["projectA", "projectB"], (
        f"/home/user/data/ should contain only 'projectA' and 'projectB' "
        f"but has: {subdirs}"
    )


@pytest.mark.parametrize("filepath,expected_content", FILES_EXPECTED.items())
def test_required_files_exist_with_correct_content(filepath, expected_content):
    assert os.path.isfile(filepath), f"Required file missing: {filepath}"

    # Ensure it is a regular file (not symlink, device, etc.)
    st_mode = os.stat(filepath).st_mode
    assert stat.S_ISREG(st_mode), f"{filepath} is not a regular file."

    with open(filepath, "r", encoding="utf-8") as fh:
        content = fh.read()
    assert content == expected_content, (
        f"Content of {filepath!r} does not match the expected reference."
    )


def test_no_extra_files_in_source_tree():
    """The data tree must not contain additional unexpected files."""
    expected_paths = set(FILES_EXPECTED.keys())
    for root, _, files in os.walk(DATA_DIR):
        for fname in files:
            path = os.path.join(root, fname)
            assert path in expected_paths, (
                f"Unexpected file found in data directory: {path}"
            )


@pytest.mark.parametrize("deliverable", [ARCHIVE, CHECKSUM, LOGFILE])
def test_deliverables_do_not_exist_yet(deliverable):
    assert not os.path.exists(deliverable), (
        f"Deliverable {deliverable} already exists before student action; "
        "the directory should start empty."
    )


def test_backups_directory_absent_initially():
    assert not os.path.exists(BACKUPS_DIR), (
        f"The backups directory {BACKUPS_DIR} must not exist at start."
    )