# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the OS / filesystem
# for the “IoT logs” exercise _before_ the student performs any action.
#
# The tests make sure that
#   • /home/user/iot_logs/ exists and is a directory
#   • the three expected *.log files are present
#   • each file is a regular readable file (0644 perms)
#   • the contents of the files match what the grading harness promises
#     (specifically, the ERROR lines and their error-codes)
#
# No test is performed for the output file error_summary.tsv; that belongs
# to the student-generated artefacts, which are **not** part of the initial
# state.

import os
import stat
import re
from pathlib import Path
from collections import Counter

import pytest

IOT_LOG_DIR = Path("/home/user/iot_logs")
EXPECTED_FILES = {
    "device01.log": {
        # Minimal substrings we expect to find in the file
        "ERROR SENSOR_TIMEOUT E105",
        "ERROR LOW_BATTERY E201",
    },
    "device02.log": {
        "ERROR SENSOR_TIMEOUT E105",
        "ERROR OVERHEAT E301",
    },
    "device03.log": {
        "ERROR LOW_BATTERY E201",
        "ERROR OVERHEAT E301",
    },
}

# Expected aggregated error-code counts across **all** log files.
EXPECTED_ERROR_COUNTS = Counter({"E105": 3, "E201": 3, "E301": 2})


@pytest.fixture(scope="module")
def log_files():
    """
    Return a mapping of filename -> Path object for the expected log files.
    The fixture itself asserts that the directory and files exist.
    """
    # 1. Directory must exist and be a directory.
    assert IOT_LOG_DIR.exists(), (
        f"Required directory {IOT_LOG_DIR} is missing."
    )
    assert IOT_LOG_DIR.is_dir(), (
        f"{IOT_LOG_DIR} exists but is not a directory."
    )

    files = {}
    for fname in EXPECTED_FILES:
        fpath = IOT_LOG_DIR / fname
        assert fpath.exists(), (
            f"Expected log file {fpath} is missing."
        )
        assert fpath.is_file(), (
            f"{fpath} exists but is not a regular file."
        )
        files[fname] = fpath

    return files


def test_permissions(log_files):
    """
    The provided log files must be world-readable (mode 0644).
    We only validate the permission bits, not ownership (UID/GID may vary).
    """
    for fname, fpath in log_files.items():
        mode = stat.S_IMODE(os.stat(fpath).st_mode)
        expected_mode = 0o644
        assert mode == expected_mode, (
            f"File {fpath} has permissions {oct(mode)}, "
            f"expected {oct(expected_mode)}."
        )


def test_contains_expected_substrings(log_files):
    """
    Each log file should contain the ERROR lines advertised in the spec.
    We verify that *at least* the given substrings are present so that
    later tests relying on the same contents make sense.
    """
    for fname, expected_snippets in EXPECTED_FILES.items():
        with open(log_files[fname], "r", encoding="utf-8") as fh:
            content = fh.read()

        for snippet in expected_snippets:
            assert snippet in content, (
                f"File {log_files[fname]} is missing expected text:\n"
                f'    "{snippet}"'
            )


def _extract_error_codes(path: Path):
    """
    Helper: yield error-codes (tokens that look like 'E' followed by digits)
    from lines that contain the literal string 'ERROR'.
    """
    pattern = re.compile(r"\bE\d+\b")
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if "ERROR" in line:
                match = pattern.search(line)
                if match:
                    yield match.group(0)


def test_aggregated_error_code_counts(log_files):
    """
    Parse all *.log files, extract error-codes from lines containing 'ERROR',
    and make sure the aggregated counts match the specification.
    """
    counts = Counter()
    for fpath in log_files.values():
        counts.update(_extract_error_codes(fpath))

    assert counts == EXPECTED_ERROR_COUNTS, (
        "Aggregated error-code counts do not match the expected initial "
        "state.\n"
        f"  Expected: {dict(EXPECTED_ERROR_COUNTS)}\n"
        f"  Found:    {dict(counts)}"
    )