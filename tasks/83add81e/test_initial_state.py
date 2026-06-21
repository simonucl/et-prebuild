# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must exist
# BEFORE the student starts writing shell one-liners.  It asserts
# 1) the presence and exact contents of the raw log files and the Grafana
#    template, and
# 2) the *absence* of any produced artefacts that the student is supposed
#    to create later on.
#
# If any of these checks fail, the failure message will clearly indicate
# what is wrong or missing.
#
# Standard library only ‑- no external dependencies apart from pytest.

import os
from pathlib import Path

RAW_DIR = Path("/home/user/metrics/raw")
PROCESSED_DIR = Path("/home/user/metrics/processed")
GRAFANA_DIR = Path("/home/user/grafana/dashboards")

SERVICE_A_FILE = RAW_DIR / "serviceA-2023-10-01.log"
SERVICE_B_FILE = RAW_DIR / "serviceB-2023-10-01.log"

EXPECTED_SERVICE_A_LINES = [
    "2023-10-01T00:00:01Z serviceA 120 200",
    "2023-10-01T00:00:02Z serviceA 250 200",
    "2023-10-01T00:00:03Z serviceA 110 500",
]

EXPECTED_SERVICE_B_LINES = [
    "2023-10-01T00:00:01Z serviceB 95 200",
    "2023-10-01T00:00:02Z serviceB 105 200",
]

TEMPLATE_CONF = GRAFANA_DIR / "sample_dashboard.conf"
EXPECTED_TEMPLATE_LINES = [
    "cpu_threshold=PLACEHOLDER_CPU_THRESHOLD",
    "mem_threshold=PLACEHOLDER_MEM_THRESHOLD",
    "disk_threshold=PLACEHOLDER_DISK_THRESHOLD",
]

# Output artefacts that *must not* exist yet
DATE_STR = "2023-10-01"
EXPECTED_CSV = PROCESSED_DIR / f"{DATE_STR}_metrics_summary.csv"
EXPECTED_UPDATED_CONF = GRAFANA_DIR / "sample_dashboard.conf.updated"


def _read_stripped_lines(path: Path):
    """Helper that returns a list of stripped lines without trailing newlines."""
    with path.open("r", encoding="utf-8") as fh:
        return [ln.rstrip("\n").rstrip("\r") for ln in fh.readlines()]


def test_raw_directory_and_files_exist():
    assert RAW_DIR.is_dir(), (
        f"Required directory {RAW_DIR} is missing."
    )

    missing = [str(p) for p in (SERVICE_A_FILE, SERVICE_B_FILE) if not p.is_file()]
    assert not missing, (
        "The following required log file(s) are missing:\n"
        + "\n".join(missing)
    )


def test_raw_file_contents():
    # Service A
    actual_a = _read_stripped_lines(SERVICE_A_FILE)
    assert actual_a == EXPECTED_SERVICE_A_LINES, (
        f"Contents of {SERVICE_A_FILE} do not match the expected lines.\n"
        f"Expected:\n{EXPECTED_SERVICE_A_LINES}\n\nGot:\n{actual_a}"
    )

    # Service B
    actual_b = _read_stripped_lines(SERVICE_B_FILE)
    assert actual_b == EXPECTED_SERVICE_B_LINES, (
        f"Contents of {SERVICE_B_FILE} do not match the expected lines.\n"
        f"Expected:\n{EXPECTED_SERVICE_B_LINES}\n\nGot:\n{actual_b}"
    )


def test_grafana_template_exists_and_is_correct():
    assert TEMPLATE_CONF.is_file(), (
        f"Template dashboard configuration {TEMPLATE_CONF} is missing."
    )

    actual = _read_stripped_lines(TEMPLATE_CONF)
    assert actual == EXPECTED_TEMPLATE_LINES, (
        f"Contents of {TEMPLATE_CONF} do not match expectation.\n"
        f"Expected:\n{EXPECTED_TEMPLATE_LINES}\n\nGot:\n{actual}"
    )


def test_processed_artefacts_do_not_exist_yet():
    """
    These are the files the student must create; they must *not* exist at the
    initial checkpoint.
    """
    assert not EXPECTED_CSV.exists(), (
        f"File {EXPECTED_CSV} already exists, but it should be created by the student."
    )

    assert not EXPECTED_UPDATED_CONF.exists(), (
        f"File {EXPECTED_UPDATED_CONF} already exists, but it should be created by the student."
    )