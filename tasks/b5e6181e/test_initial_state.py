# test_initial_state.py
#
# This pytest suite validates that the **initial state** of the operating
# system / file-system is exactly as expected *before* the student starts
# working on the assignment.
#
# What we verify:
#   1. Presence of the input directory:        /home/user/data/traffic_logs/
#   2. Presence of the three required .log.gz files (full absolute paths).
#   3. That each file is a valid gzip file that can be decompressed.
#   4. Every decompressed line matches the expected “[YYYY-MM-DD HH:MM:SS] N”
#      format and there are exactly five lines per region as per specification.
#
# We deliberately do **not** test for any output artefacts – those belong to the
# student’s deliverables and will be checked later by a different test suite.

import gzip
import os
import re
from pathlib import Path

import pytest

# ---------- Constants ---------- #

INPUT_DIR = Path("/home/user/data/traffic_logs")
REGION_FILES = {
    "region1": INPUT_DIR / "region1.log.gz",
    "region2": INPUT_DIR / "region2.log.gz",
    "region3": INPUT_DIR / "region3.log.gz",
}

EXPECTED_LINE_COUNT = 5  # each region file must contain exactly 5 lines
LINE_REGEX = re.compile(
    rb"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] \d+\s*$"
)  # raw bytes, no trailing spaces other than optional newline


# ---------- Helper functions ---------- #


def _assert_is_valid_gzip(filepath: Path):
    """
    Open a gzip file and read its content to ensure it is not corrupted.
    Return the decompressed lines for further inspection.
    """
    try:
        with gzip.open(filepath, "rb") as fh:
            data = fh.readlines()
    except (OSError, EOFError) as exc:  # OSError for gzip bad magic & others
        pytest.fail(f"{filepath} cannot be opened as a valid gzip file: {exc}")

    # Basic sanity: file must not be empty
    if not data:
        pytest.fail(f"{filepath} is empty after decompression.")

    return data


# ---------- Tests ---------- #


def test_input_directory_exists():
    assert INPUT_DIR.is_dir(), (
        f"Required input directory {INPUT_DIR} is missing. "
        "Make sure the dataset is correctly staged."
    )


@pytest.mark.parametrize("region, path", sorted(REGION_FILES.items()))
def test_region_log_files_exist(region, path: Path):
    assert path.is_file(), (
        f"Missing log file for {region}: expected at {path}. "
        "Ensure all three .log.gz files are present."
    )
    # File should be non-empty
    assert path.stat().st_size > 0, f"{path} exists but is empty."


@pytest.mark.parametrize("region, path", sorted(REGION_FILES.items()))
def test_region_log_files_are_valid_gzip_and_format(region, path: Path):
    lines = _assert_is_valid_gzip(path)

    # Verify exact number of lines for this assignment.
    assert len(lines) == EXPECTED_LINE_COUNT, (
        f"{path} must contain exactly {EXPECTED_LINE_COUNT} log entries "
        f"(found {len(lines)})."
    )

    # Check every line matches the strict format.
    for idx, raw_line in enumerate(lines, start=1):
        if not LINE_REGEX.fullmatch(raw_line.rstrip(b"\n")):
            pytest.fail(
                f"Line {idx} in {path} does not match the required "
                "[YYYY-MM-DD HH:MM:SS] <latency_in_ms> format. "
                f"Offending line (repr): {raw_line!r}"
            )

        # Optional semantic sanity: latency should be an integer in a plausible range
        latency_str = raw_line.split()[-1]
        try:
            latency_val = int(latency_str)
        except ValueError:
            pytest.fail(
                f"Line {idx} in {path} contains non-integer latency value: {latency_str!r}"
            )
        assert 0 <= latency_val <= 100_000, (
            f"Latency value {latency_val} in {path} line {idx} "
            "is outside the expected range 0–100000 ms."
        )