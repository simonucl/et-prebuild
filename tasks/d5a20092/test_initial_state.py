# test_initial_state.py
"""
Pytest suite that validates the **initial** state of the operating‐system
filesystem for the “January 2023 capacity-report” exercise.

These tests assert that:
    • The expected directory hierarchy and raw log files already exist.
    • The raw log files are the *only* January-2023 logs present, and their
      contents match the specification.
    • The arithmetic means that a correct solution must produce are
      CPU=50, MEM=72, DISK=60 (floor of the average of the two raw files).
    • No summary file for 2023-01 has yet been published.
    • Any pre-existing “latest” link must **not** already point to the
      January-2023 summary.
    • operations.log does *not* yet contain the required completion line.

The goal is to guarantee that students start from a clean, predictable state.
"""

import os
import glob
import math
import re
from pathlib import Path

RAW_DIR = Path("/home/user/capacity/raw")
REPORTS_DIR = Path("/home/user/capacity/reports")
SUMMARY_FILE = REPORTS_DIR / "summary_202301.log"
LATEST_LINK = Path("/home/user/capacity/latest")
OPERATIONS_LOG = Path("/home/user/capacity/operations.log")

EXPECTED_RAW_FILES = {
    RAW_DIR / "server1_202301.log",
    RAW_DIR / "server2_202301.log",
}

# Expected metric values from the specification
EXPECTED_VALUES = {
    RAW_DIR / "server1_202301.log": dict(CPU=42, MEM=76, DISK=63),
    RAW_DIR / "server2_202301.log": dict(CPU=58, MEM=68, DISK=57),
}

EXPECTED_AVERAGES = dict(CPU=50, MEM=72, DISK=60)


def test_directory_structure():
    """Verify that the required directory hierarchy exists."""
    assert Path("/home/user/capacity").is_dir(), (
        "Missing directory: /home/user/capacity"
    )
    assert RAW_DIR.is_dir(), f"Missing directory: {RAW_DIR}"
    assert REPORTS_DIR.is_dir(), f"Missing directory: {REPORTS_DIR}"


def test_raw_file_set_is_complete_and_exclusive():
    """
    Ensure that:
        • Exactly two *_202301.log files exist.
        • Their paths match the required server1_202301.log and server2_202301.log.
    """
    january_files = {Path(p) for p in glob.glob(str(RAW_DIR / "*_202301.log"))}
    assert january_files == EXPECTED_RAW_FILES, (
        "January 2023 raw files do not match the expected set.\n"
        f"Expected: {sorted(EXPECTED_RAW_FILES)}\n"
        f"Found   : {sorted(january_files)}"
    )


def _parse_metrics(filename: Path):
    """
    Helper that reads a raw log file and returns a dict with integer metrics.
    Validates format in the process.
    """
    with filename.open() as fh:
        lines = fh.read().splitlines()

    # Exact 3 lines, no extra blank lines
    assert len(lines) == 3, (
        f"{filename} should contain exactly 3 non-blank lines, found {len(lines)}."
    )

    pattern_map = {
        0: r"CPU_USED=(\d{1,3})$",
        1: r"MEM_USED=(\d{1,3})$",
        2: r"DISK_USED=(\d{1,3})$",
    }
    metrics = {}
    for idx, pat in pattern_map.items():
        m = re.fullmatch(pat, lines[idx])
        assert m, (
            f"Line {idx+1} of {filename} is malformed: {lines[idx]!r}"
        )
        value = int(m.group(1))
        assert 0 <= value <= 100, (
            f"Value out of range 0-100 in {filename}: {value}"
        )
        if idx == 0:
            metrics["CPU"] = value
        elif idx == 1:
            metrics["MEM"] = value
        else:
            metrics["DISK"] = value
    return metrics


def test_raw_file_contents_and_expected_values():
    """Validate the exact contents of each raw log file."""
    for filepath in EXPECTED_RAW_FILES:
        metrics = _parse_metrics(filepath)
        expected = EXPECTED_VALUES[filepath]
        assert metrics == expected, (
            f"Metrics in {filepath} do not match specification.\n"
            f"Expected: {expected}\n"
            f"Found   : {metrics}"
        )


def test_computed_averages_match_expected():
    """Compute arithmetic means from raw files and verify they match the spec."""
    totals = dict(CPU=0, MEM=0, DISK=0)
    count = 0
    for filepath in EXPECTED_RAW_FILES:
        data = _parse_metrics(filepath)
        for k in totals:
            totals[k] += data[k]
        count += 1

    averages = {k: math.floor(v / count) for k, v in totals.items()}
    assert averages == EXPECTED_AVERAGES, (
        "Averages computed from raw files do not match expected values.\n"
        f"Expected: {EXPECTED_AVERAGES}\n"
        f"Found   : {averages}"
    )


def test_summary_file_absent():
    """No January-2023 summary should exist yet."""
    assert not SUMMARY_FILE.exists(), (
        f"Pre-existing summary file detected: {SUMMARY_FILE}. "
        "The student task must create this file."
    )


def test_latest_symlink_not_yet_pointing_to_new_summary():
    """
    The /home/user/capacity/latest symlink may or may not exist, but
    it must *not* already resolve to the January-2023 summary.
    """
    if LATEST_LINK.is_symlink():
        target = os.readlink(LATEST_LINK)
        assert Path(target).resolve() != SUMMARY_FILE, (
            f"latest symlink already points to {SUMMARY_FILE}; "
            "it should be updated only after the student solution runs."
        )


def test_operations_log_not_yet_finalised():
    """
    operations.log may or may not exist, but its *final* line must not
    yet indicate ‘2023-01 publication completed’.
    """
    if not OPERATIONS_LOG.exists():
        # Absence is acceptable for the initial state.
        return

    with OPERATIONS_LOG.open() as fh:
        lines = fh.read().splitlines()

    if not lines:
        return  # Empty file is also acceptable.

    last_line = lines[-1]
    completed_re = re.compile(
        r"^2023-01 publication completed → 20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
    )
    assert not completed_re.fullmatch(last_line), (
        "operations.log already contains the January-2023 completion entry.\n"
        "The student task is expected to append this entry."
    )