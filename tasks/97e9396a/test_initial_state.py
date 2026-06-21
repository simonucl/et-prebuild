# test_initial_state.py
"""
Pytest suite to validate the initial filesystem state *before* the student
performs the synchronization task.

This file checks:
1. Presence and exact contents of the source experiment artifacts.
2. Absence of any pre-existing data in the remote store.
3. Correct emptiness of the logs directory.

The tests purposefully do **not** look for any output artifacts that the
student is expected to create (e.g., the destination exp42 directory or the
exp42_sync.log file).
"""
from pathlib import Path
import pytest

# Base paths
HOME = Path("/home/user")
SRC_DIR = HOME / "mlops" / "experiments" / "exp42"
REMOTE_STORE_DIR = HOME / "remote_store"
LOGS_DIR = HOME / "mlops" / "logs"

@pytest.fixture(scope="module")
def src_files():
    """
    Return a mapping of expected filenames to their exact expected contents
    (including trailing newlines).
    """
    return {
        "model.pkl": "DUMMY MODEL DATA\n",
        "metrics.json": (
            "{\n"
            '  "accuracy": 0.93,\n'
            '  "loss": 0.12\n'
            "}\n"
        ),
    }

def test_source_directory_exists_and_only_expected_files_present(src_files):
    assert SRC_DIR.is_dir(), (
        f"Required source directory {SRC_DIR} is missing or not a directory."
    )

    actual_files = sorted(p.name for p in SRC_DIR.iterdir() if p.is_file())
    expected_files = sorted(src_files.keys())

    assert actual_files == expected_files, (
        f"Source directory {SRC_DIR} must contain exactly these files: "
        f"{expected_files}, but found: {actual_files}"
    )

def test_source_files_contents(src_files):
    for filename, expected_content in src_files.items():
        file_path = SRC_DIR / filename
        assert file_path.is_file(), f"Expected file {file_path} is missing."

        actual_content = file_path.read_text(encoding="utf-8")
        assert actual_content == expected_content, (
            f"Contents of {file_path} do not match the expected template.\n"
            f"Expected:\n{expected_content!r}\nActual:\n{actual_content!r}"
        )

def test_remote_store_is_present_and_empty():
    assert REMOTE_STORE_DIR.is_dir(), (
        f"Remote store directory {REMOTE_STORE_DIR} is missing or not a directory."
    )

    # The remote store must be completely empty: no files, no subdirectories.
    entries = list(REMOTE_STORE_DIR.iterdir())
    assert len(entries) == 0, (
        f"Remote store {REMOTE_STORE_DIR} must be empty before synchronization, "
        f"but found: {[p.name for p in entries]}"
    )

def test_logs_directory_is_present_and_empty():
    assert LOGS_DIR.is_dir(), (
        f"Logs directory {LOGS_DIR} is missing or not a directory."
    )

    log_entries = list(LOGS_DIR.iterdir())
    assert len(log_entries) == 0, (
        f"Logs directory {LOGS_DIR} must be empty initially, "
        f"but contains: {[p.name for p in log_entries]}"
    )