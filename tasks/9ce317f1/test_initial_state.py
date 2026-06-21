# test_initial_state.py
#
# Pytest suite that validates the **pre-exercise** filesystem state for the
# “app-logs” observability task.
#
# What we expect to exist BEFORE the student’s solution runs:
#
# Directories
# ├─ /home/user/app_logs
# └─ /home/user/cache
#
# Files (and their exact sizes)
# ├─ /home/user/app_logs/api.log  –  123  bytes
# ├─ /home/user/app_logs/db.log   – 2048  bytes
# ├─ /home/user/cache/temp1.bin   – 4096  bytes
# └─ /home/user/cache/temp2.bin   – 1024  bytes
#
# Aggregate sizes (sum of file sizes only):
# ├─ /home/user/app_logs  → 2171 bytes
# └─ /home/user/cache     → 5120 bytes
#
# What MUST *not* exist yet:
#   /home/user/obs_metrics
#
# If any of these expectations are violated, the student’s environment is
# considered mis-configured *before* they even start.
#
# Only stdlib + pytest are used as required.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
APP_LOGS_DIR = HOME / "app_logs"
CACHE_DIR = HOME / "cache"
OBS_METRICS_DIR = HOME / "obs_metrics"
CSV_TARGET = OBS_METRICS_DIR / "disk_usage_20240115.csv"


def dir_size_bytes(directory: Path) -> int:
    """
    Return the cumulative size (in bytes) of all regular files contained
    anywhere under `directory`. Directory metadata sizes are ignored because
    the task’s “du -sb” instructions aim to count file contents only.
    """
    total = 0
    for root, _dirs, files in os.walk(directory):
        for f in files:
            fp = Path(root) / f
            # Follow the behavior of du -sb: if a file is a regular file, count
            # its size; skip device nodes, sockets, etc.  We still add link
            # targets only once because os.walk gives each path exactly once.
            if fp.is_file():
                total += fp.stat().st_size
    return total


# ---------------------------------------------------------------------------
# Generic directory existence tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "path_desc, path",
    [
        ("app_logs directory", APP_LOGS_DIR),
        ("cache directory", CACHE_DIR),
    ],
)
def test_expected_directories_exist(path_desc, path):
    assert path.exists(), f"Expected {path_desc} at {path!s} to exist, but it is missing"
    assert path.is_dir(), f"Expected {path_desc} at {path!s} to be a directory"


# ---------------------------------------------------------------------------
# File existence and exact size tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "file_path, expected_size",
    [
        (APP_LOGS_DIR / "api.log", 123),
        (APP_LOGS_DIR / "db.log", 2048),
        (CACHE_DIR / "temp1.bin", 4096),
        (CACHE_DIR / "temp2.bin", 1024),
    ],
)
def test_expected_files_and_sizes(file_path: Path, expected_size: int):
    assert file_path.exists(), f"Required file {file_path!s} is missing"
    assert file_path.is_file(), f"Expected {file_path!s} to be a regular file"
    actual_size = file_path.stat().st_size
    assert (
        actual_size == expected_size
    ), f"File {file_path!s} has size {actual_size} bytes; expected {expected_size} bytes"


# ---------------------------------------------------------------------------
# Aggregate directory-size checks
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "directory, expected_total",
    [
        (APP_LOGS_DIR, 123 + 2048),  # 2171
        (CACHE_DIR, 4096 + 1024),    # 5120
    ],
)
def test_directory_total_sizes(directory: Path, expected_total: int):
    actual_total = dir_size_bytes(directory)
    assert (
        actual_total == expected_total
    ), (
        f"Directory {directory!s} contains {actual_total} bytes in regular files; "
        f"expected exactly {expected_total} bytes"
    )


# ---------------------------------------------------------------------------
# Negative test: obs_metrics must NOT exist yet
# ---------------------------------------------------------------------------

def test_obs_metrics_not_present_initially():
    assert not OBS_METRICS_DIR.exists(), (
        f"{OBS_METRICS_DIR!s} should NOT exist before the student runs their "
        "solution, but it is already present"
    )
    assert not CSV_TARGET.exists(), (
        f"CSV report {CSV_TARGET!s} should NOT exist before the student runs "
        "their solution, but it is already present"
    )