# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state *before* the
# student runs any commands for the “rsync + log” exercise.
#
# The tests verify that:
#   • The source dataset tree exists with the expected five files and exact
#     byte-for-byte contents.
#   • The remote-staging tree exists but is *out-of-date*, i.e. it contains
#     only the two “OLD_” files with their expected (older) contents and **no
#     other files** are present anywhere under
#         /home/user/remote_host/staging/
#
# Nothing related to the expected *output* of the exercise (e.g. /home/user/
# sync_logs or the final remote mirror) is tested here, in accordance with the
# grading rules.

from pathlib import Path
import pytest

# --------------------------------------------------------------------------- #
# Helper data                                                                 #
# --------------------------------------------------------------------------- #

LOCAL_BASE = Path("/home/user/ml_data/raw_dataset")
REMOTE_BASE = Path("/home/user/remote_host/staging")
REMOTE_DATASET = REMOTE_BASE / "dataset"

# Expected local files and their exact byte content
LOCAL_EXPECTED = {
    "train/images/img1.jpg": b"IMG1\n",
    "train/images/img2.jpg": b"IMG2\n",
    "train/labels/img1.txt": b"label1\n",
    "val/images/img3.jpg":   b"IMG3\n",
    "val/labels/img3.txt":   b"label3\n",
}

# Expected *outdated* files that should exist on the remote host **before**
# the student performs synchronisation.
REMOTE_EXPECTED_OLD = {
    "train/images/img1.jpg": b"OLD_IMG1\n",
    "train/labels/img1.txt": b"oldlbl1\n",
}

# --------------------------------------------------------------------------- #
# Utility functions                                                           #
# --------------------------------------------------------------------------- #

def _collect_files(root: Path):
    """
    Return a set of POSIX-style relative paths (str) for *all* regular files
    under the given root, as well as a mapping of relative path -> bytes.
    """
    files_set = set()
    bytes_map = {}
    for path in root.rglob("*"):
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            files_set.add(rel)
            bytes_map[rel] = path.read_bytes()
    return files_set, bytes_map


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_local_dataset_files_exist_and_content():
    """Local raw-dataset tree must contain exactly the five expected files."""
    assert LOCAL_BASE.is_dir(), (
        f"Expected directory {LOCAL_BASE} does not exist."
    )

    files_seen, bytes_map = _collect_files(LOCAL_BASE)

    # 1) Check that the set of files is *exactly* as expected.
    expected_set = set(LOCAL_EXPECTED.keys())
    assert files_seen == expected_set, (
        "Local dataset does not match the expected file list.\n"
        f"Expected: {sorted(expected_set)}\n"
        f"Found   : {sorted(files_seen)}"
    )

    # 2) Check the byte-for-byte contents.
    mismatches = [
        rel for rel, expected_bytes in LOCAL_EXPECTED.items()
        if bytes_map.get(rel) != expected_bytes
    ]
    assert not mismatches, (
        "One or more local files have incorrect content:\n"
        + "\n".join(mismatches)
    )


def test_remote_staging_has_only_old_files_with_expected_content():
    """
    The remote staging tree must *currently* contain only the two outdated
    files (nothing more, nothing less) and each must have the exact expected
    bytes.
    """
    # Ensure required directories exist.
    assert REMOTE_DATASET.is_dir(), (
        f"Expected directory {REMOTE_DATASET} does not exist."
    )

    files_seen, bytes_map = _collect_files(REMOTE_BASE)

    # The grader specifies that *no other files* are present under
    # /home/user/remote_host/staging/ at the start.
    expected_set = {f"dataset/{rel}" for rel in REMOTE_EXPECTED_OLD.keys()}
    assert files_seen == expected_set, (
        "Remote staging directory does not have the expected initial files.\n"
        f"Expected (relative to {REMOTE_BASE}): {sorted(expected_set)}\n"
        f"Found                                : {sorted(files_seen)}"
    )

    # Verify content of the two outdated files.
    mismatches = [
        rel for rel, expected_bytes in REMOTE_EXPECTED_OLD.items()
        if bytes_map.get(f"dataset/{rel}") != expected_bytes
    ]
    assert not mismatches, (
        "One or more remote files contain unexpected content:\n"
        + "\n".join(mismatches)
    )