# test_initial_state.py
#
# This pytest suite verifies the **initial** filesystem state that must be
# present *before* the student begins solving the exercise.  It intentionally
# avoids checking for any output artifacts that the student is expected to
# create later (e.g. /home/user/observability/reports/ or the final log file).

import os
import textwrap
import pytest

HOME = "/home/user"
BASE_DIR = os.path.join(HOME, "observability")
RAW_DIR = os.path.join(BASE_DIR, "raw_metrics")

# --------------------------------------------------------------------------- #
# Helper data:  the exact, canonical contents of each raw metric CSV file.
# Trailing newlines are stripped so that minor OS-newline differences
# (e.g. final \n) do not trip up the comparison.
# --------------------------------------------------------------------------- #

EXPECTED_CONTENTS = {
    os.path.join(RAW_DIR, "cpu_metrics.csv"): textwrap.dedent(
        """\
        timestamp,cpu_usage_percent
        2024-06-01T10:00:00Z,45.3
        2024-06-01T11:00:00Z,55.1
        2024-06-01T12:00:00Z,49.8"""
    ).strip(),
    os.path.join(RAW_DIR, "memory_metrics.csv"): textwrap.dedent(
        """\
        timestamp,mem_used_mb
        2024-06-01T10:00:00Z,7832
        2024-06-01T11:00:00Z,8124
        2024-06-01T12:00:00Z,7998"""
    ).strip(),
    os.path.join(RAW_DIR, "http_requests.csv"): textwrap.dedent(
        """\
        timestamp,method,status_code,latency_ms
        2024-06-01T10:00:00Z,GET,200,123
        2024-06-01T10:01:00Z,POST,200,256
        2024-06-01T10:02:00Z,GET,500,789
        2024-06-01T11:15:00Z,GET,200,101
        2024-06-01T12:22:00Z,POST,404,303"""
    ).strip(),
}

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_raw_metrics_directory_exists():
    """The raw_metrics directory must exist before work begins."""
    assert os.path.isdir(
        RAW_DIR
    ), f"Required directory missing: {RAW_DIR}"


@pytest.mark.parametrize("file_path", list(EXPECTED_CONTENTS.keys()))
def test_raw_metric_file_exists(file_path):
    """Each expected CSV file must exist."""
    assert os.path.isfile(
        file_path
    ), f"Required file missing: {file_path}"


@pytest.mark.parametrize("file_path,expected", EXPECTED_CONTENTS.items())
def test_raw_metric_file_contents_exact(file_path, expected):
    """
    The contents of each CSV must match the canonical version *exactly*
    (ignoring a final trailing newline, which some editors may omit or add).
    """
    with open(file_path, "r", encoding="utf-8") as fp:
        actual = fp.read().strip()
    assert (
        actual == expected
    ), (
        f"Contents of {file_path} do not match the expected initial data.\n"
        "---- Expected ----\n"
        f"{expected}\n"
        "---- Actual ----\n"
        f"{actual}\n"
    )