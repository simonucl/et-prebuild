# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the filesystem
# before the student performs any backup operations.
#
# The checks conform to the task description:
#   • /home/user/monitoring must already exist.
#   • Exactly two CSV files, with the prescribed names and byte-sizes,
#     must be present in that directory.
#   • No backup artefacts (directory, tarball, manifest, or log) should
#     exist yet.
#
# Only Python’s stdlib and pytest are used.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
MONITORING_DIR = HOME / "monitoring"
BACKUPS_DIR = HOME / "backups"

CSV_FILES = {
    "service1-uptime-2023-09.csv": 74,
    "service2-uptime-2023-09.csv": 74,
}

TARBALL = BACKUPS_DIR / "uptime-logs-2023-09.tar.gz"
MANIFEST = BACKUPS_DIR / "uptime-logs-2023-09.manifest"
LOGFILE = BACKUPS_DIR / "backup-2023-09.log"


@pytest.fixture(scope="module")
def monitoring_contents():
    """
    Return the list of files (names only) found in /home/user/monitoring.
    """
    assert MONITORING_DIR.exists(), (
        f"Required directory {MONITORING_DIR} does not exist. "
        "It must be present before any backup work starts."
    )
    assert MONITORING_DIR.is_dir(), (
        f"{MONITORING_DIR} exists but is not a directory."
    )
    return sorted(p.name for p in MONITORING_DIR.iterdir() if p.is_file())


def test_monitoring_has_only_expected_csv_files(monitoring_contents):
    # There must be exactly the CSV files given in the task description.
    assert sorted(CSV_FILES.keys()) == monitoring_contents, (
        f"/home/user/monitoring should contain exactly these files: "
        f"{sorted(CSV_FILES.keys())!r}, but actually contains: {monitoring_contents!r}"
    )


@pytest.mark.parametrize("filename,expected_size", CSV_FILES.items())
def test_each_csv_file_has_correct_size(filename, expected_size):
    file_path = MONITORING_DIR / filename
    assert file_path.exists(), f"Expected file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."
    actual_size = os.path.getsize(file_path)
    assert actual_size == expected_size, (
        f"{file_path} should be {expected_size} bytes, but is {actual_size} bytes."
    )


def test_backups_directory_does_not_exist_yet():
    # Before the student runs their commands, /home/user/backups
    # (and anything inside it) must not exist.
    assert not BACKUPS_DIR.exists(), (
        f"{BACKUPS_DIR} already exists before backup begins; "
        "the initial state should NOT contain this directory."
    )


@pytest.mark.parametrize("artefact", [TARBALL, MANIFEST, LOGFILE])
def test_no_backup_artefacts_exist_yet(artefact):
    assert not artefact.exists(), (
        f"Found unexpected file {artefact}; "
        "no backup artefacts should exist in the initial state."
    )