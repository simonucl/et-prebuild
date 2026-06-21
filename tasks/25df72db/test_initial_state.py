# test_initial_state.py
#
# Pytest suite to validate the *initial* operating-system / filesystem state
# before the student begins working on the “5xx monitoring routine” exercise.
#
# What we assert
# --------------
# 1. The compressed log archive   : /home/user/logs/webapp-2023-09-16.log.gz
#    • Exists and is a regular file.
#    • Can be decompressed without error.
#    • Contains exactly the 15 expected log lines.
#    • Each line follows the required “CLF-like” format.
#    • Contains the expected distribution of 5xx responses
#        – total 5xx count     : 8
#        – per-endpoint counts : /api/products → 4
#                               /api/users    → 2
#                               /api/login    → 1
#                               /api/orders   → 1
#
# 2. The decompressed log file    : /home/user/logs/webapp-2023-09-16.log
#    • Must *not* exist yet (the student has to create it).
#
# 3. Alert artefacts              : /home/user/alerts/sep16_500_summary.csv
#                                   /home/user/alerts/ALERT_SEP16.txt
#    • Must *not* exist yet.
#
# 4. Alerts directory             : /home/user/alerts
#    • May or may not exist, but if it does, it must be a directory.
#
# Any deviation from the above constitutes an invalid starting state and the
# test suite will fail with descriptive error messages.
#
# Only stdlib + pytest are used, per instructions.

import gzip
import re
from pathlib import Path

import pytest


LOGS_DIR = Path("/home/user/logs")
ALERTS_DIR = Path("/home/user/alerts")

GZ_LOG_PATH = LOGS_DIR / "webapp-2023-09-16.log.gz"
PLAIN_LOG_PATH = LOGS_DIR / "webapp-2023-09-16.log"

SUMMARY_CSV = ALERTS_DIR / "sep16_500_summary.csv"
ALERT_TXT = ALERTS_DIR / "ALERT_SEP16.txt"

# --------------------------------------------------------------------------- #
# Helper constants for verifying the provided artefact:                       #
# --------------------------------------------------------------------------- #
EXPECTED_TOTAL_5XX = 8
EXPECTED_PER_ENDPOINT = {
    "/api/products": 4,
    "/api/users": 2,
    "/api/login": 1,
    "/api/orders": 1,
}
EXPECTED_LINE_COUNT = 15

# Regular expression that matches one log line according to the spec.
LOG_LINE_RE = re.compile(
    r"^"
    r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\s+"         # ISO-8601 timestamp
    r"(GET|POST|PUT|DELETE|PATCH|OPTIONS|HEAD)\s+"        # HTTP verb
    r"(/[^ ]+)\s+"                                        # URI path
    r"(\d{3})\s+"                                         # Status code
    r"([A-Za-z_]+)\s+"                                    # Reason phrase
    r"(\d+)ms"                                            # Latency in ms
    r"$"
)

# --------------------------------------------------------------------------- #
#                               Test cases                                    #
# --------------------------------------------------------------------------- #

def test_compressed_log_exists_and_is_valid():
    """Ensure the .gz log file exists and can be decoded to the known content."""
    assert GZ_LOG_PATH.exists(), (
        f"Expected compressed log file {GZ_LOG_PATH} is missing."
    )
    assert GZ_LOG_PATH.is_file(), (
        f"{GZ_LOG_PATH} exists but is not a regular file."
    )

    # Read and decode
    try:
        with gzip.open(GZ_LOG_PATH, "rt", encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except (OSError, gzip.BadGzipFile) as exc:
        pytest.fail(f"Failed to decompress {GZ_LOG_PATH}: {exc}")

    # Validate line count
    assert len(lines) == EXPECTED_LINE_COUNT, (
        f"Expected {EXPECTED_LINE_COUNT} lines in the gz log file, "
        f"found {len(lines)}."
    )

    # Validate each line format and gather 5xx statistics
    total_5xx = 0
    per_endpoint = {}

    for idx, line in enumerate(lines, start=1):
        m = LOG_LINE_RE.match(line)
        assert m, (
            f"Line {idx} in the compressed log does not match the required "
            f"format:\n{line!r}"
        )

        status_code = int(m.group(4))
        uri_path = m.group(3)

        if 500 <= status_code <= 599:
            total_5xx += 1
            per_endpoint[uri_path] = per_endpoint.get(uri_path, 0) + 1

    # Verify 5xx statistics match what the rest of the exercise expects.
    assert total_5xx == EXPECTED_TOTAL_5XX, (
        f"Compressed log should contain {EXPECTED_TOTAL_5XX} total 5xx "
        f"responses, found {total_5xx}."
    )
    assert per_endpoint == EXPECTED_PER_ENDPOINT, (
        "Per-endpoint 5xx count in compressed log does not match the expected "
        "distribution.\n"
        f"Expected: {EXPECTED_PER_ENDPOINT}\nFound   : {per_endpoint}"
    )


def test_plain_log_file_not_present_yet():
    """The decompressed .log file should not exist before the student runs their code."""
    assert not PLAIN_LOG_PATH.exists(), (
        f"{PLAIN_LOG_PATH} already exists, but the student is expected to "
        "create it by decompressing the archive."
    )


def test_alerts_directory_state_and_absence_of_output_files():
    """
    The alerts directory may or may not exist initially.  
    Either way, summary CSV and alert txt must not exist before the student acts.
    """
    if ALERTS_DIR.exists():
        assert ALERTS_DIR.is_dir(), (
            f"{ALERTS_DIR} exists but is not a directory."
        )

    assert not SUMMARY_CSV.exists(), (
        f"Summary CSV {SUMMARY_CSV} should not exist yet."
    )
    assert not ALERT_TXT.exists(), (
        f"Alert file {ALERT_TXT} should not exist yet."
    )