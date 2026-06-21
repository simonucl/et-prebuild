# test_initial_state.py
#
# Pytest suite that verifies the *initial* operating-system / file-system
# state before the student begins any work.
#
# The assertions intentionally **do not** look for the output artefacts
# mentioned in the assignment (§ pattern_report.log and error_traces.txt);
# instead, they make sure the raw evidence file is present, intact and
# unmodified, and that the analysis directory is still clean.
#
# Only Python’s standard library plus `pytest` is used.

import os
import re
import shutil
from collections import Counter

LOG_DIR = "/home/user/logs"
LOG_FILE = os.path.join(LOG_DIR, "webapp_access.log")
ANALYSIS_DIR = "/home/user/analysis"
PATTERN_REPORT = os.path.join(ANALYSIS_DIR, "pattern_report.log")
ERROR_TRACES = os.path.join(ANALYSIS_DIR, "error_traces.txt")

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
LOG_PATTERN = re.compile(
    r"""
    ^(?P<ip>\S+)                     # IP address
      \s+\S+\s+\S+\s+                # remote logname & user (ignored)
      \[(?P<timestamp>[^\]]+)]\s+    # [timestamp]
      "(?P<method>\S+)\s             # "HTTP method
      (?P<path>[^ ]+)\s              #   request path
      (?P<protocol>[^"]+)"\s+        #   protocol"
      (?P<status>\d{3})\s+           # status code
      (?P<size>\d+)\s+               # size
      ".*"\s+".*"                    # referrer + user-agent (ignored)
    $""",
    re.VERBOSE,
)


def parse_log():
    """
    Yields a tuple (ip, status) for each well-formed line in the log.
    Raises AssertionError immediately if a line does not match the
    canonical Apache ‘combined’ format.
    """
    if not os.path.isfile(LOG_FILE):
        pytest.fail(f"Expected log file not found: {LOG_FILE}")

    with open(LOG_FILE, "rt", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            raw = raw.rstrip("\n")
            m = LOG_PATTERN.match(raw)
            assert (
                m is not None
            ), f"Line {lineno} in {LOG_FILE!s} does not match the expected Apache 'combined' format.\nOffending line: {raw}"
            yield m.group("ip"), int(m.group("status"))


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_log_directory_and_file_exist():
    assert os.path.isdir(
        LOG_DIR
    ), f"Directory {LOG_DIR!s} is missing – it should contain the access log."
    assert os.path.isfile(
        LOG_FILE
    ), f"Log file {LOG_FILE!s} is missing – cannot continue without raw evidence."
    assert (
        os.path.getsize(LOG_FILE) > 0
    ), f"Log file {LOG_FILE!s} is empty – that would be unexpected."


def test_log_file_has_expected_line_count_and_status_distribution():
    lines = list(parse_log())
    expected_total = 25
    expected_status_counts = {200: 15, 404: 6, 500: 4}

    # Total line count
    assert (
        len(lines) == expected_total
    ), f"Expected {expected_total} log entries, found {len(lines)}."

    # Status-code distribution
    status_counter = Counter(status for _ip, status in lines)
    assert (
        status_counter == expected_status_counts
    ), f"Unexpected status-code distribution.\nExpected: {expected_status_counts}\nFound   : {dict(status_counter)}"


def test_top_three_ip_addresses_match_expected():
    lines = list(parse_log())
    ip_counter = Counter(ip for ip, _status in lines)
    top_three = ip_counter.most_common(3)

    expected = [("192.168.1.10", 7), ("10.0.0.2", 5), ("172.16.0.3", 4)]
    assert (
        top_three == expected
    ), f"Top-3 IP address distribution is wrong.\nExpected: {expected}\nFound   : {top_three}"


def test_analysis_directory_is_clean():
    """
    Prior to the student's work, the /home/user/analysis directory should
    either not exist or contain NONE of the two deliverable files.  This
    ensures that the assessment starts from a true 'before' state.
    """
    for artefact in (PATTERN_REPORT, ERROR_TRACES):
        assert not os.path.exists(
            artefact
        ), f"Output artefact {artefact!s} already exists – the student has not been asked to create it yet."

    # The directory itself may or may not exist; both states are acceptable.
    if os.path.exists(ANALYSIS_DIR):
        assert os.path.isdir(
            ANALYSIS_DIR
        ), f"{ANALYSIS_DIR!s} exists but is not a directory."


def test_required_cli_tools_are_available():
    """
    Confirm that indispensable GNU/Linux standard utilities required by the
    assignment (awk and sed) are on the PATH.  The student is expected to
    use them later, so they must be present up-front.
    """
    for tool in ("awk", "sed"):
        assert shutil.which(tool) is not None, f"Required CLI tool '{tool}' is not available on PATH."