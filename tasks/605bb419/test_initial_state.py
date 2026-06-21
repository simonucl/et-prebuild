# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state **before** the student runs any code.  These tests codify the
# “ground truth” described in the task narrative so that any deviation
# will be flagged immediately and with a clear error message.
#
# The checks performed:
#   • Presence of the /home/user/capacity_planner/logs directory.
#   • Absence (yet) of /home/user/capacity_planner/output.
#   • Presence of the expected five *.log files **and only those**.
#   • Exact byte size, line count and modification epoch of every log.
#
# Only Python’s stdlib and pytest are used.

import os
from pathlib import Path
import stat
import pytest

HOME = Path("/home/user")
BASE_DIR = HOME / "capacity_planner"
LOG_DIR = BASE_DIR / "logs"
OUTPUT_DIR = BASE_DIR / "output"

# Canonical truth map:  path → (size_bytes, line_count, mtime_epoch)
EXPECTED_FILES = {
    LOG_DIR / "app1.log": (112, 3, 1680000000),
    LOG_DIR / "app2.log": (45, 2, 1680003600),
    LOG_DIR / "app3.log": (16, 1, 1680007200),
    LOG_DIR / "app4.log": (117, 4, 1680010800),
    LOG_DIR / "app5.log": (10, 5, 1680014400),
}


def _read_bytes(path: Path) -> bytes:
    """Utility: read the full file into memory (binary)."""
    with path.open("rb") as fh:
        return fh.read()


@pytest.fixture(scope="module")
def actual_files():
    """
    Collect information about all *.log FILES directly under LOG_DIR.
    Returns a dict: path → (size, line_count, mtime)
    """
    files = {}
    for child in LOG_DIR.iterdir():
        if child.is_file() and child.suffix == ".log":
            content = _read_bytes(child)
            size = len(content)
            line_count = content.count(b"\n")
            mtime = int(child.stat().st_mtime)
            files[child] = (size, line_count, mtime)
    return files


def test_logs_directory_exists():
    assert LOG_DIR.is_dir(), (
        f"Required directory {LOG_DIR} is missing. "
        "The initial state must contain the logs folder."
    )


def test_output_directory_absent():
    assert not OUTPUT_DIR.exists(), (
        f"Directory {OUTPUT_DIR} should NOT exist before the student script runs."
    )


def test_exact_log_file_set_present(actual_files):
    expected_set = set(EXPECTED_FILES)
    actual_set = set(actual_files)
    missing = expected_set - actual_set
    extra = actual_set - expected_set
    assert not missing, (
        "The following expected *.log files are missing:\n  " +
        "\n  ".join(str(p) for p in sorted(missing))
    )
    assert not extra, (
        "Unexpected *.log files found in the initial state:\n  " +
        "\n  ".join(str(p) for p in sorted(extra))
    )


@pytest.mark.parametrize("path,expected", sorted(EXPECTED_FILES.items()))
def test_log_file_stats(path: Path, expected, actual_files):
    assert path in actual_files, (
        f"File {path} is missing in the collected actual_files dict—"
        "this should have been caught earlier."
    )

    actual_size, actual_lines, actual_mtime = actual_files[path]
    exp_size, exp_lines, exp_mtime = expected

    assert actual_size == exp_size, (
        f"Byte size mismatch for {path} "
        f"(expected {exp_size}, found {actual_size})."
    )
    assert actual_lines == exp_lines, (
        f"Line-count mismatch for {path} "
        f"(expected {exp_lines}, found {actual_lines})."
    )
    assert actual_mtime == exp_mtime, (
        f"Modification-time (epoch) mismatch for {path} "
        f"(expected {exp_mtime}, found {actual_mtime})."
    )


def test_files_are_regular_files():
    for path in EXPECTED_FILES:
        st = path.stat()
        assert stat.S_ISREG(st.st_mode), f"{path} is not a regular file"