# test_initial_state.py
#
# Pytest suite that verifies the pre-exercise filesystem state for the
# “slow SQL query” task.
#
# WHAT IS VERIFIED
# ----------------
# 1. Directories
#    • /home/user/app/logs  (must exist, be a directory, mode 0755)
#    • /home/user/output    (must exist, be a directory, mode 0755, EMPTY)
#
# 2. File /home/user/app/logs/perf.log
#    • Must exist, be a regular file, mode 0644
#    • Must contain EXACTLY six lines (UNIX LF endings)
#    • Content of each line must match the specification—no extra
#      whitespace before/after, no additional lines.
#
#     2023-08-17 10:15:01 INFO Query A Execution time: 123 ms\n
#     2023-08-17 10:15:02 INFO Query B Execution time: 567 ms\n
#     2023-08-17 10:15:03 INFO Query C Execution time: 754 ms\n
#     2023-08-17 10:15:04 INFO Query D Execution time: 31 ms\n
#     2023-08-17 10:15:05 INFO Query E Execution time: 499 ms\n
#     2023-08-17 10:15:06 INFO Query F Execution time: 820 ms\n
#
# 3. ABSENCE of output artefacts
#    • /home/user/output MUST NOT yet contain slow_queries.log or any
#      other file/sub-directory.
#
# Any deviation from the above will cause the tests to fail with a clear,
# explanatory message.
#
# NOTE: Only stdlib + pytest are used.

import os
from pathlib import Path
import stat
import pytest

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

APP_LOG_DIR   = Path("/home/user/app/logs")
OUTPUT_DIR    = Path("/home/user/output")
LOG_FILE      = APP_LOG_DIR / "perf.log"

EXPECTED_LINES = [
    "2023-08-17 10:15:01 INFO Query A Execution time: 123 ms\n",
    "2023-08-17 10:15:02 INFO Query B Execution time: 567 ms\n",
    "2023-08-17 10:15:03 INFO Query C Execution time: 754 ms\n",
    "2023-08-17 10:15:04 INFO Query D Execution time: 31 ms\n",
    "2023-08-17 10:15:05 INFO Query E Execution time: 499 ms\n",
    "2023-08-17 10:15:06 INFO Query F Execution time: 820 ms\n",
]

def _mode(path: Path):
    "Return the permission bits (e.g. 0o644) for the given path."
    return path.stat().st_mode & 0o777

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "directory, expected_mode",
    [
        (APP_LOG_DIR, 0o755),
        (OUTPUT_DIR,  0o755),
    ],
)
def test_required_directories_exist(directory: Path, expected_mode: int):
    assert directory.exists(), f"Required directory {directory} is missing."
    assert directory.is_dir(), f"{directory} exists but is not a directory."
    actual_mode = _mode(directory)
    assert actual_mode == expected_mode, (
        f"{directory} permissions are {oct(actual_mode)}, "
        f"expected {oct(expected_mode)}."
    )

def test_output_directory_is_empty():
    contents = list(OUTPUT_DIR.iterdir())
    assert contents == [], (
        f"{OUTPUT_DIR} is expected to be empty before the exercise starts, "
        f"but it contains: {[p.name for p in contents]}"
    )

def test_perf_log_file_exists_and_has_correct_mode():
    assert LOG_FILE.exists(), f"Required log file {LOG_FILE} is missing."
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."
    actual_mode = _mode(LOG_FILE)
    expected_mode = 0o644
    assert actual_mode == expected_mode, (
        f"{LOG_FILE} permissions are {oct(actual_mode)}, "
        f"expected {oct(expected_mode)}."
    )

def test_perf_log_file_content_exact_match():
    # Read the file in binary mode first to ensure UNIX LF endings
    raw_bytes = LOG_FILE.read_bytes()
    assert b"\r\n" not in raw_bytes, (
        f"{LOG_FILE} must use UNIX LF line endings, but CRLF was detected."
    )

    # Now read as text for content validation
    with LOG_FILE.open(encoding="utf-8") as fp:
        lines = fp.readlines()

    assert len(lines) == 6, (
        f"{LOG_FILE} must contain exactly 6 lines, found {len(lines)}."
    )

    for idx, (actual, expected) in enumerate(zip(lines, EXPECTED_LINES), start=1):
        assert actual == expected, (
            f"Line {idx} of {LOG_FILE!s} is incorrect.\n"
            f"Expected: {expected!r}\n"
            f"Found   : {actual!r}"
        )