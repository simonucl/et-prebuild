# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem / OS state for the
# “slow-endpoints” exercise _before_ the student writes any solution code.
#
# Only stdlib + pytest are used.

import gzip
import os
import stat
from collections import defaultdict

import pytest

HOME = "/home/user"
OBS_ROOT = os.path.join(HOME, "observability")
LOG_DIR = os.path.join(OBS_ROOT, "logs")
REPORT_DIR = os.path.join(OBS_ROOT, "report")
LOG_FILE = os.path.join(LOG_DIR, "app-2023-09-21.log.gz")


@pytest.fixture(scope="session")
def decompressed_lines():
    """
    Return a list of UTF-8 decoded log lines from the gzip file.
    """
    assert os.path.isfile(LOG_FILE), f"Expected log file {LOG_FILE} to exist."
    try:
        with gzip.open(LOG_FILE, "rt", encoding="utf-8") as fh:
            data = fh.read()
    except OSError as exc:  # happens if the file is not a valid gzip
        pytest.fail(f"Could not decompress {LOG_FILE}: {exc}")

    lines = data.splitlines()
    # Sanity check: a log file should never be empty
    assert lines, f"{LOG_FILE} appears to be empty after decompression."
    return lines


def _check_mode(path, expected_mode):
    """
    Verify that `path` exists and its mode bits match `expected_mode`
    (only the permission part, i.e. the lowest 3 octal digits).
    """
    st = os.stat(path)
    actual = stat.S_IMODE(st.st_mode)
    assert (
        actual == expected_mode
    ), f"Expected {oct(expected_mode)} permissions on {path}, found {oct(actual)}."


def test_directories_exist_and_permissions():
    # /home/user/observability
    assert os.path.isdir(OBS_ROOT), f"Directory {OBS_ROOT} is missing."
    _check_mode(OBS_ROOT, 0o755)

    # …/logs
    assert os.path.isdir(LOG_DIR), f"Directory {LOG_DIR} is missing."
    _check_mode(LOG_DIR, 0o755)

    # …/report
    assert os.path.isdir(REPORT_DIR), f"Directory {REPORT_DIR} is missing."
    _check_mode(REPORT_DIR, 0o755)


def test_report_directory_is_empty():
    files = os.listdir(REPORT_DIR)
    assert (
        not files
    ), f"Expected {REPORT_DIR} to be empty, but it already contains: {files}"


def test_log_file_contains_expected_statistics(decompressed_lines):
    """
    Parse the log and make sure that for the day 2023-09-21 the five
    expected endpoints exist with the exact arithmetic mean latencies
    stated in the task description.
    """
    stats = defaultdict(list)

    for line in decompressed_lines:
        # Each line is “timestamp verb path status latency”
        parts = line.strip().split()
        # Guard against malformed lines (5 columns expected)
        if len(parts) != 5:
            continue

        timestamp, _verb, path, _status, latency = parts

        # Only keep records for the day of interest
        if not timestamp.startswith("2023-09-21"):
            continue

        # Remove the trailing "ms" and convert to int
        if not latency.endswith("ms"):
            pytest.fail(f"Latency field without 'ms' suffix found: {latency!r}")
        try:
            numeric_latency = int(latency[:-2])
        except ValueError:
            pytest.fail(f"Non-integer latency value found: {latency!r}")

        stats[path].append(numeric_latency)

    # --- Expected truth table -------------------------------------------------
    expected_avgs = {
        "/api/v1/payments": 300.00,
        "/api/v1/orders": 240.00,
        "/api/v1/carts": 160.00,
        "/api/v1/users": 135.00,
        "/api/v1/inventory": 85.00,
    }

    # -------------------------------------------------------------------------
    assert (
        len(stats) == 5
    ), f"Expected exactly 5 unique endpoints for 2023-09-21, found {len(stats)}: {list(stats)}"

    computed_avgs = {}
    for endpoint, latencies in stats.items():
        avg = sum(latencies) / len(latencies)
        # Two-decimal rounding as the final report will do
        avg = round(avg, 2)
        computed_avgs[endpoint] = avg

    # Check that every expected endpoint is present with the correct average.
    for endpoint, expected_avg in expected_avgs.items():
        assert (
            endpoint in computed_avgs
        ), f"Endpoint {endpoint} expected in log but not found."
        assert (
            computed_avgs[endpoint] == expected_avg
        ), f"Average latency mismatch for {endpoint}: expected {expected_avg}, got {computed_avgs[endpoint]}"

    # Finally, ensure ordering by average latency would match the required rank.
    sorted_endpoints = sorted(
        computed_avgs.items(), key=lambda kv: kv[1], reverse=True
    )
    ranking = [ep for ep, _ in sorted_endpoints]
    expected_ranking = [
        "/api/v1/payments",
        "/api/v1/orders",
        "/api/v1/carts",
        "/api/v1/users",
        "/api/v1/inventory",
    ]
    assert (
        ranking == expected_ranking
    ), f"Expected descending order {expected_ranking}, got {ranking}"