# test_initial_state.py
#
# Pytest suite to validate the operating-system / filesystem state
# BEFORE the student performs any actions for the incident-response
# exercise.  Only the *pre-existing* artefacts are examined here.
#
# IMPORTANT:
#   • We do NOT look for any output files or directories that the
#     student will be creating later (per specification).
#   • Only stdlib and pytest are used.

import os
import re
from pathlib import Path

# Absolute path to the raw network log that must already exist
RAW_LOG_PATH = Path("/home/user/incidents/raw_logs/network_2023-03-17.log")

# The suspicious IP we expect to see in the raw capture summary
SUSPICIOUS_IP = "10.23.45.67"

# Regex to pick out ISO-8601 timestamps on 2023-03-17 between 03:00 and 05:59
WINDOW_RE = re.compile(
    r"^2023-03-17T0[3-5]:[0-5][0-9]:[0-5][0-9]Z\b"
)


def test_raw_log_file_exists():
    """
    The raw log file that the analyst must work from MUST already be
    present and be a regular file.
    """
    assert RAW_LOG_PATH.is_file(), (
        f"Required raw log file not found at exact path: {RAW_LOG_PATH}"
    )


def test_raw_log_file_is_non_empty():
    """
    The raw log file must not be empty; otherwise there is nothing to process.
    """
    size = RAW_LOG_PATH.stat().st_size
    assert size > 0, (
        f"Raw log file {RAW_LOG_PATH} is unexpectedly empty (0 bytes)."
    )


def test_raw_log_contains_suspicious_ip():
    """
    Sanity-check that the raw log actually mentions the suspicious host
    so that the forthcoming extraction step is meaningful.
    """
    with RAW_LOG_PATH.open("r", encoding="utf-8") as fh:
        contents = fh.read()

    assert SUSPICIOUS_IP in contents, (
        f"The IP address {SUSPICIOUS_IP} was not found in "
        f"{RAW_LOG_PATH}. Verify that the correct log file is in place."
    )


def test_raw_log_contains_data_within_time_window():
    """
    Ensure at least one log line falls within the target time window
    (03:00:00Z – 05:00:00Z inclusive on 17 Mar 2023).  This guarantees
    that the extraction procedure will yield output.
    """
    with RAW_LOG_PATH.open("r", encoding="utf-8") as fh:
        matching_lines = [
            line for line in fh if WINDOW_RE.match(line) and SUSPICIOUS_IP in line
        ]

    assert matching_lines, (
        f"No log lines in {RAW_LOG_PATH} simultaneously satisfy the "
        f"date-range (03:00–05:00Z on 2023-03-17) and involvement of "
        f"{SUSPICIOUS_IP}. Verify the fixture data."
    )