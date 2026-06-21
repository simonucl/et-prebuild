# test_initial_state.py
#
# This pytest suite validates the _initial_ condition of the operating-system
# and file-system **before** the student performs any action.  It ensures that
# the raw log files needed for the assignment are present and correct, and that
# no output artefacts from the student’s future work exist yet.
#
# Only the Python standard library and pytest are used.

import os
import re
from pathlib import Path

HOME = Path("/home/user")
SYSLOG_DIR = HOME / "syslogs"
LOG_FILES = [
    SYSLOG_DIR / "systemA.log",
    SYSLOG_DIR / "systemB.log",
    SYSLOG_DIR / "systemC.log",
]
ANALYSIS_DIR = HOME / "analysis"
OUTPUT_FILE = ANALYSIS_DIR / "top_ip_counts.log"

# Expected per-IP aggregate counts across **all three** log files.
EXPECTED_COUNTS = {
    "10.0.0.1": 10,
    "10.0.0.2":  6,
    "10.0.0.3":  5,
    "10.0.0.4":  5,
    "10.0.0.5":  4,
}


def test_syslog_directory_exists():
    """The /home/user/syslogs directory must exist and be a directory."""
    assert SYSLOG_DIR.exists(), f"Missing directory: {SYSLOG_DIR}"
    assert SYSLOG_DIR.is_dir(), f"Path exists but is not a directory: {SYSLOG_DIR}"


def test_log_files_exist_and_are_regular():
    """Each expected log file must exist, be regular, and have ≥1 byte."""
    for lf in LOG_FILES:
        assert lf.exists(), f"Missing log file: {lf}"
        assert lf.is_file(), f"Path exists but is not a regular file: {lf}"
        size = lf.stat().st_size
        assert size > 0, f"Log file is empty: {lf}"


_LOG_LINE_RE = re.compile(
    r"""
    ^\d{4}-\d{2}-\d{2}T            # YYYY-MM-DDT
    \d{2}:\d{2}:\d{2}Z\s           # HH:MM:SSZ␣
    SRC=(\d{1,3}(?:\.\d{1,3}){3})\s# SRC=<IPv4>␣   (captures the IPv4)
    STATUS=(FAIL|SUCCESS)$         # STATUS=<WORD>
    """,
    re.VERBOSE,
)


def _parse_logs_and_count_ips():
    """Helper that parses all log files, validates format, and returns a counter dict."""
    counts = {}
    for lf in LOG_FILES:
        with lf.open("r", encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        # Each log file is expected to have exactly 10 lines.
        assert len(lines) == 10, f"Unexpected number of lines in {lf}: expected 10, found {len(lines)}"

        for num, line in enumerate(lines, start=1):
            m = _LOG_LINE_RE.match(line)
            assert m, f"Line {num} in {lf} does not match the required pattern:\n{line}"
            ip = m.group(1)
            counts[ip] = counts.get(ip, 0) + 1
    return counts


def test_log_file_format_and_ip_counts():
    """
    Validate every line of every log file and ensure the aggregate per-IP counts
    match the ground truth.  This guarantees the student starts from the correct
    data.
    """
    counts = _parse_logs_and_count_ips()

    # Ensure we observed exactly the IPs we expect—no more, no less.
    assert set(counts) == set(EXPECTED_COUNTS), (
        "The set of source IPs in the log files does not match the expected "
        f"set.\nObserved: {sorted(counts)}\nExpected: {sorted(EXPECTED_COUNTS)}"
    )

    # Check the exact counts.
    for ip, expected_cnt in EXPECTED_COUNTS.items():
        assert counts[ip] == expected_cnt, (
            f"Unexpected count for {ip}: expected {expected_cnt}, found {counts[ip]}"
        )


def test_output_not_yet_present():
    """
    Before the student runs their solution, no analysis directory or output file
    should exist yet.  Their presence would indicate that the initial state has
    been polluted.
    """
    assert not ANALYSIS_DIR.exists(), (
        f"The directory {ANALYSIS_DIR} already exists, but it should not be "
        "present before the student runs their code."
    )
    assert not OUTPUT_FILE.exists(), (
        f"The file {OUTPUT_FILE} already exists, but it should not be present "
        "before the student runs their code."
    )