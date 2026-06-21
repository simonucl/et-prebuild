# test_initial_state.py
#
# This pytest suite verifies **only** the pre-task (initial) state of the
# filesystem.  It checks that the provided “remote” storage area already
# exists with the correct files and contents, and that nothing extra is
# present.  It deliberately does **not** look for—or complain about—the
# yet-to-be-created /home/user/ml_project workspace, because that is part
# of the student’s forthcoming work.

import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants describing the expected initial state
# --------------------------------------------------------------------------- #

REMOTE_BASE = Path("/home/user/remote_storage")

EXPECTED_RELATIVE_PATHS = [
    "images/cats/cat1.jpg",
    "images/dogs/dog1.jpg",
    "images/dogs/dog2.jpg",
    "labels/dog_labels.csv",
    "labels/cat_labels.csv",
]

# Expected *byte-exact* contents for each placeholder file
EXPECTED_CONTENTS = {
    "images/cats/cat1.jpg": b"CAT1_PLACEHOLDER\n",
    "images/dogs/dog1.jpg": b"DOG1_PLACEHOLDER\n",
    "images/dogs/dog2.jpg": b"DOG2_PLACEHOLDER\n",
    "labels/dog_labels.csv": b"id,label\n1,bulldog\n2,poodle\n",
    "labels/cat_labels.csv": b"id,label\n1,siamese\n2,maine_coon\n",
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def list_all_files_under(base_dir: Path):
    """
    Return a set of POSIX-style paths (relative to `base_dir`) for every
    regular file found under `base_dir`.
    """
    files = set()
    for root, _, filenames in os.walk(base_dir):
        for fname in filenames:
            full_path = Path(root) / fname
            rel_path = full_path.relative_to(base_dir).as_posix()
            files.add(rel_path)
    return files


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_remote_storage_directory_exists():
    assert REMOTE_BASE.exists(), (
        f"Expected directory {REMOTE_BASE} does not exist.  The initial "
        "filesystem should contain the remote storage area before the "
        "student runs any commands."
    )
    assert REMOTE_BASE.is_dir(), f"{REMOTE_BASE} exists but is not a directory."


@pytest.mark.parametrize("relative_path", EXPECTED_RELATIVE_PATHS)
def test_expected_files_exist(relative_path):
    file_path = REMOTE_BASE / relative_path
    assert file_path.exists(), f"Missing expected file: {file_path}"
    assert file_path.is_file(), f"Path exists but is not a file: {file_path}"


def test_no_extra_files_present():
    actual_files = list_all_files_under(REMOTE_BASE)
    expected_files = set(EXPECTED_RELATIVE_PATHS)

    missing = expected_files - actual_files
    extra = actual_files - expected_files

    msg_parts = []
    if missing:
        msg_parts.append(
            "Missing files:\n  " + "\n  ".join(sorted(missing))
        )
    if extra:
        msg_parts.append(
            "Unexpected extra files:\n  " + "\n  ".join(sorted(extra))
        )

    assert not missing and not extra, (
        "The contents of /home/user/remote_storage do not match the expected "
        "initial state.\n" + "\n".join(msg_parts)
    )


@pytest.mark.parametrize("relative_path,expected_bytes", EXPECTED_CONTENTS.items())
def test_file_contents_match(relative_path, expected_bytes):
    file_path = REMOTE_BASE / relative_path
    actual_bytes = file_path.read_bytes()
    assert (
        actual_bytes == expected_bytes
    ), f"Content mismatch in {file_path}. Expected {expected_bytes!r}, got {actual_bytes!r}"