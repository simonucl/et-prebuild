# test_initial_state.py
#
# Pytest suite that validates the starting filesystem state **before**
# the student runs any commands.  It checks that the remote dataset is
# present and intact, and that the local project workspace starts with
# only the placeholder file that will later be removed.  It deliberately
# avoids touching any files that the student is expected to create
# (e.g., last_sync.log).

import os
from pathlib import Path

import pytest

# ---- Constants ----------------------------------------------------------------

REMOTE_DIR = Path("/home/user/remote_dataset")
LOCAL_DATA_DIR = Path("/home/user/ml_project/data")
LOCAL_LOGS_DIR = Path("/home/user/ml_project/logs")

REMOTE_FILES_EXPECTED = {
    # filename : expected byte-size
    "train.csv": 55,
    "test.csv": 32,
    "README.md": 79,
}

PLACEHOLDER_NAME = "OLD_FILES_DO_NOT_USE.txt"
PLACEHOLDER_SIZE = 27


# ---- Helper -------------------------------------------------------------------

def _read_bytes(path: Path) -> bytes:
    """
    Read and return the full contents of *path* as bytes.
    """
    with path.open("rb") as fh:
        return fh.read()


# ---- Tests --------------------------------------------------------------------

@pytest.mark.describe("Remote dataset directory is present and correct")
def test_remote_dataset_files_exist_and_sizes():
    assert REMOTE_DIR.is_dir(), (
        f"Expected remote dataset directory '{REMOTE_DIR}' to exist "
        "and be a directory, but it is missing or the wrong type."
    )

    for fname, expected_size in REMOTE_FILES_EXPECTED.items():
        file_path = REMOTE_DIR / fname
        assert file_path.is_file(), (
            f"Missing required file in remote dataset: {file_path}"
        )
        actual_size = file_path.stat().st_size
        assert actual_size == expected_size, (
            f"Remote file '{file_path}' has size {actual_size} bytes; "
            f"expected {expected_size} bytes."
        )


@pytest.mark.describe("Local workspace starts with the placeholder file only")
def test_local_workspace_placeholder_and_no_dataset_files_present():
    # Data directory must exist.
    assert LOCAL_DATA_DIR.is_dir(), (
        f"Local data directory '{LOCAL_DATA_DIR}' is missing or not a directory."
    )

    # Placeholder MUST exist and have the correct size.
    placeholder_path = LOCAL_DATA_DIR / PLACEHOLDER_NAME
    assert placeholder_path.is_file(), (
        f"Expected placeholder file '{placeholder_path}' to exist "
        "before synchronisation, but it is missing."
    )
    actual_size = placeholder_path.stat().st_size
    assert actual_size == PLACEHOLDER_SIZE, (
        f"Placeholder file '{placeholder_path}' has size {actual_size} bytes; "
        f"expected {PLACEHOLDER_SIZE} bytes."
    )

    # None of the dataset files should be present yet.
    for fname in REMOTE_FILES_EXPECTED:
        unexpected_path = LOCAL_DATA_DIR / fname
        assert not unexpected_path.exists(), (
            f"File '{unexpected_path}' should NOT exist before synchronisation."
        )


@pytest.mark.describe("Logs directory exists but contains no sync log yet")
def test_logs_directory_exists():
    assert LOCAL_LOGS_DIR.is_dir(), (
        f"Logs directory '{LOCAL_LOGS_DIR}' is missing or not a directory."
    )
    # Do NOT check for the presence/absence of 'last_sync.log' because that
    # file is an output artefact that will be created later.