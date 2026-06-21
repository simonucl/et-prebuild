# test_initial_state.py
#
# Pytest suite that validates the _initial_ state of the filesystem
# before the student performs any actions for the “latency delta report”
# exercise.  It asserts that the two raw log files are present with the
# expected content, that no output CSV is present yet, and that no stray
# files are in /home/user/logs.

import os
import re
from pathlib import Path

LOG_DIR = Path("/home/user/logs")
LOG_A = LOG_DIR / "serviceA_2023-09-15.log"
LOG_B = LOG_DIR / "serviceB_2023-09-15.log"
DELTA_CSV = LOG_DIR / "incident_0915_latency_delta.csv"

EXPECTED_A_LINES = [
    "2023-09-15T08:00:01Z|req-1001|u-501|120",
    "2023-09-15T08:00:02Z|req-1002|u-502|95",
    "2023-09-15T08:00:03Z|req-1003|u-503|230",
    "2023-09-15T08:00:04Z|req-1004|u-504|110",
    "2023-09-15T08:00:05Z|req-1005|u-505|150",
]

EXPECTED_B_LINES = [
    "2023-09-15T08:00:01Z|req-1001|u-501|80",
    "2023-09-15T08:00:02Z|req-1002|u-502|60",
    "2023-09-15T08:00:03Z|req-1006|u-506|200",
    "2023-09-15T08:00:04Z|req-1004|u-504|90",
    "2023-09-15T08:00:05Z|req-1005|u-505|100",
]

LINE_REGEX = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\|[^|]+\|[^|]+\|[0-9]+$"
)


def _read_lines(path: Path):
    """Read a text file, strip the trailing newline (if any), and
    return a list of lines without the trailing newline characters."""
    with path.open("r", encoding="utf-8") as fh:
        # .splitlines() discards trailing newline characters safely
        return fh.read().splitlines()


def test_logs_directory_exists():
    assert LOG_DIR.exists(), f"Expected directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


def test_log_files_exist_with_expected_content():
    # --- Service A ---
    assert LOG_A.exists(), f"Missing log file: {LOG_A}"
    assert LOG_A.is_file(), f"{LOG_A} exists but is not a regular file."
    lines_a = _read_lines(LOG_A)
    assert lines_a == EXPECTED_A_LINES, (
        f"Contents of {LOG_A} do not match the expected seed data.\n"
        f"Expected:\n{EXPECTED_A_LINES}\nFound:\n{lines_a}"
    )

    # --- Service B ---
    assert LOG_B.exists(), f"Missing log file: {LOG_B}"
    assert LOG_B.is_file(), f"{LOG_B} exists but is not a regular file."
    lines_b = _read_lines(LOG_B)
    assert lines_b == EXPECTED_B_LINES, (
        f"Contents of {LOG_B} do not match the expected seed data.\n"
        f"Expected:\n{EXPECTED_B_LINES}\nFound:\n{lines_b}"
    )

    # Validate format of every line against the 4-field pipe pattern
    for path, lines in [(LOG_A, lines_a), (LOG_B, lines_b)]:
        for i, line in enumerate(lines, start=1):
            assert LINE_REGEX.match(line), (
                f"Line {i} in {path} has an invalid format:\n{line}"
            )


def test_delta_csv_not_present_yet():
    assert not DELTA_CSV.exists(), (
        f"{DELTA_CSV} should NOT exist before the student has generated "
        "the latency-delta report."
    )


def test_no_extra_files_in_logs_dir():
    # Only the two seed log files should exist initially.
    expected_files = {LOG_A.name, LOG_B.name}
    found_files = {p.name for p in LOG_DIR.iterdir() if p.is_file()}
    extra_files = found_files - expected_files
    missing_files = expected_files - found_files

    assert not missing_files, (
        f"The following expected log files are missing from {LOG_DIR}: "
        f"{', '.join(sorted(missing_files))}"
    )
    assert not extra_files, (
        f"Unexpected files found in {LOG_DIR} before the task begins: "
        f"{', '.join(sorted(extra_files))}"
    )