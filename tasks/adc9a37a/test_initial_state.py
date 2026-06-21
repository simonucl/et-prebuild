# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state
# before the learner creates the required backup artefacts.
#
# Rules verified:
#   • Required source directory and files exist.
#   • File contents and exact byte‐sizes match the specification.
#   • /home/user/backups/ directory exists and is empty
#     (the exercise will later create files inside it).
#
# NOTE:  The tests **do not** check for the presence (or absence) of the
#        final output artefacts `train_data_backup.tar.gz` or
#        `train_data_backup.log`, complying with the grading rules.

import os
import stat

HOME = "/home/user"
TRAIN_DIR = os.path.join(HOME, "ml_data", "train")
BACKUPS_DIR = os.path.join(HOME, "backups")

FEATURES_PATH = os.path.join(TRAIN_DIR, "features.csv")
TARGETS_PATH = os.path.join(TRAIN_DIR, "targets.csv")

EXPECTED_FEATURES_BYTES = b"f1,f2,f3\n1,2,3\n4,5,6\n"  # 21 bytes
EXPECTED_TARGETS_BYTES = b"t\n0\n1\n"                  # 6 bytes


def _read_bytes(path: str) -> bytes:
    """Utility: read file as raw bytes."""
    with open(path, "rb") as fh:
        return fh.read()


def test_train_directory_exists():
    assert os.path.isdir(TRAIN_DIR), (
        f"Required directory {TRAIN_DIR!r} is missing."
    )
    # Also check read permissions for robustness.
    mode = os.stat(TRAIN_DIR).st_mode
    assert bool(mode & stat.S_IRUSR), (
        f"Directory {TRAIN_DIR!r} is not readable."
    )


def test_source_files_exist():
    for path in (FEATURES_PATH, TARGETS_PATH):
        assert os.path.isfile(path), (
            f"Expected source file {path!r} does not exist."
        )


def test_features_file_content_and_size():
    data = _read_bytes(FEATURES_PATH)
    expected = EXPECTED_FEATURES_BYTES
    assert data == expected, (
        f"Content of {FEATURES_PATH!r} does not match the specification."
    )
    assert len(data) == 21, (
        f"Size of {FEATURES_PATH!r} expected to be 21 bytes, "
        f"found {len(data)} bytes."
    )


def test_targets_file_content_and_size():
    data = _read_bytes(TARGETS_PATH)
    expected = EXPECTED_TARGETS_BYTES
    assert data == expected, (
        f"Content of {TARGETS_PATH!r} does not match the specification."
    )
    assert len(data) == 6, (
        f"Size of {TARGETS_PATH!r} expected to be 6 bytes, "
        f"found {len(data)} bytes."
    )


def test_backups_directory_exists_and_is_empty():
    assert os.path.isdir(BACKUPS_DIR), (
        f"Directory {BACKUPS_DIR!r} expected to exist."
    )
    # Ensure the directory is writable (so the learner can create files there).
    assert os.access(BACKUPS_DIR, os.W_OK), (
        f"Directory {BACKUPS_DIR!r} is not writable."
    )
    # Only consider visible entries (ignore '.' & '..').
    visible_entries = [
        entry for entry in os.listdir(BACKUPS_DIR)
        if entry not in (".", "..")
    ]
    assert visible_entries == [], (
        f"{BACKUPS_DIR!r} should be empty before the task starts; "
        f"found: {visible_entries}"
    )