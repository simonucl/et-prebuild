# test_initial_state.py
#
# Pytest suite to validate that the operating-system / filesystem state
# is exactly as expected *before* the student carries out any actions.
#
# Rules enforced:
#   • Verifies required directories exist.
#   • Verifies required files exist with the correct byte sizes.
#   • Ensures no unexpected regular files are present inside the base path.
#
# NOTE: We intentionally do *not* check for the output file
# (/home/user/observability/disk_usage_report.csv), because that file
# should not exist yet.

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Paths that must exist
# ---------------------------------------------------------------------------

BASE_DIR = Path("/home/user/observability")
LOGS_DIR = BASE_DIR / "logs"
METRICS_DIR = BASE_DIR / "metrics"

# Expected files and their exact sizes in bytes
EXPECTED_FILES = {
    LOGS_DIR / "api.log": 1024,
    LOGS_DIR / "web.log": 2048,
    METRICS_DIR / "metrics.json": 3072,
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _human(path: Path) -> str:
    """Return a human-readable absolute path for assertion messages."""
    return str(path.resolve())


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_base_directories_exist():
    """Base /logs and /metrics directories must exist and be directories."""
    assert BASE_DIR.is_dir(), f"Missing base directory: {_human(BASE_DIR)}"
    for subdir in (LOGS_DIR, METRICS_DIR):
        assert subdir.exists(), f"Required directory does not exist: {_human(subdir)}"
        assert subdir.is_dir(), f"Expected a directory but found something else: {_human(subdir)}"


@pytest.mark.parametrize("file_path,expected_size", sorted(EXPECTED_FILES.items(), key=lambda kv: kv[0]))
def test_expected_files_exist_with_correct_size(file_path: Path, expected_size: int):
    """Each required file must exist and have the exact size specified."""
    assert file_path.exists(), f"Required file is missing: {_human(file_path)}"
    assert file_path.is_file(), f"Path exists but is not a regular file: {_human(file_path)}"
    actual_size = file_path.stat().st_size
    assert actual_size == expected_size, (
        f"File {_human(file_path)} has size {actual_size} bytes; "
        f"expected exactly {expected_size} bytes."
    )


def test_no_unexpected_regular_files_under_observability():
    """
    There should be *exactly* the three specified regular files beneath
    /home/user/observability. Any additional regular file would indicate an
    unexpected initial state.
    """
    discovered_files = set()
    for root, _dirs, files in os.walk(BASE_DIR):
        for fname in files:
            discovered_files.add(Path(root) / fname)

    expected_set = set(EXPECTED_FILES.keys())

    # Helpful diff-style error message if sets differ.
    missing = expected_set - discovered_files
    extra = discovered_files - expected_set
    msg_lines = []
    if missing:
        msg_lines.append("Missing expected files:\n  " + "\n  ".join(map(_human, sorted(missing))))
    if extra:
        msg_lines.append("Unexpected extra files found:\n  " + "\n  ".join(map(_human, sorted(extra))))
    assert discovered_files == expected_set, "\n".join(msg_lines)