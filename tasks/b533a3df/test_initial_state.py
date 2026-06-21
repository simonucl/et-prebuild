# test_initial_state.py
#
# Pytest test-suite that verifies the workstation’s filesystem
# *before* the learner performs the backup task.  These tests confirm
# that only the “raw” dataset is present and that no archive / log
# artefacts exist yet.

import hashlib
import os
from pathlib import Path

RAW_DIR = Path("/home/user/ml_data/raw")
ML_DATA_DIR = RAW_DIR.parent
ARCHIVE_DIR = ML_DATA_DIR / "archive"


def test_raw_directory_exists():
    """
    The raw dataset directory must exist exactly where expected.
    """
    assert RAW_DIR.is_dir(), f"Required directory {RAW_DIR} is missing."


def test_raw_directory_contains_only_expected_files():
    """
    raw/ must contain exactly three files with the given names.
    """
    expected = {
        RAW_DIR / "images_train.csv",
        RAW_DIR / "images_val.csv",
        RAW_DIR / "labels.json",
    }
    found = {p for p in RAW_DIR.iterdir() if p.is_file()}

    missing = expected - found
    extra = found - expected

    assert not missing, f"Missing expected file(s) in {RAW_DIR}: {', '.join(str(p) for p in missing)}"
    assert not extra, (
        f"Unexpected extra file(s) found in {RAW_DIR}: {', '.join(str(p) for p in extra)}"
    )


def _read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


def test_raw_files_have_expected_contents():
    """
    Verify byte-for-byte contents of each initial dataset file.
    """
    expected_contents = {
        RAW_DIR / "images_train.csv": "id,label\n1,cat\n2,dog\n",
        RAW_DIR / "images_val.csv": "id,label\n3,cat\n4,dog\n",
        RAW_DIR / "labels.json": '{"cat": 0, "dog": 1}\n',
    }

    for path, expected_text in expected_contents.items():
        assert path.exists(), f"Expected file {path} is missing."
        actual_text = _read_text(path)
        assert (
            actual_text == expected_text
        ), f"Contents of {path} do not match the specification."


def test_no_archive_directory_yet():
    """
    The archive directory and its artefacts must *not* exist before
    the learner runs their commands.
    """
    assert not ARCHIVE_DIR.exists(), (
        f"{ARCHIVE_DIR} already exists, but it should be created by the learner."
    )

    tar_path = ARCHIVE_DIR / "raw_data_20240115.tar"
    sha_path = ARCHIVE_DIR / "raw_data_20240115.sha256"

    # Using exists() instead of is_file() because the directory itself is absent.
    assert not tar_path.exists(), f"Tar archive {tar_path} should not exist yet."
    assert not sha_path.exists(), f"Checksum file {sha_path} should not exist yet."


def test_no_backup_log_yet():
    """
    /home/user/ml_data/backup_log.txt must *not* exist initially.
    """
    log_path = ML_DATA_DIR / "backup_log.txt"
    assert not log_path.exists(), f"Log file {log_path} should not exist before the task is done."