# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem and the
# scan-log inputs *before* the student performs any actions required by the
# assignment.
#
# It asserts that:
#   * The expected /home/user/scan_logs directory exists.
#   * Exactly three *.log files are present: scan1.log, scan2.log, scan3.log.
#   * Each log file contains the correct host line, the correct ordered list of
#     open TCP ports, and the correct “#METRIC real” timing line.
#   * Neither the /home/user/benchmark directory nor the final CSV file yet
#     exist (they must be created by the student solution).
#
# Only the Python stdlib and pytest are used.

import os
import re
from pathlib import Path

import pytest

HOME = Path("/home/user")
SCAN_DIR = HOME / "scan_logs"
BENCHMARK_DIR = HOME / "benchmark"
CSV_FILE = BENCHMARK_DIR / "2023-05-24-scan-performance.csv"

# Ground-truth expectations for each log file
LOG_EXPECTATIONS = {
    "scan1.log": {
        "host": "10.0.0.5",
        "open_ports": ["22", "80", "443"],
        "metric_real": "0m0.362s",
    },
    "scan2.log": {
        "host": "10.0.0.12",
        "open_ports": ["21", "25"],
        "metric_real": "0m0.428s",
    },
    "scan3.log": {
        "host": "10.0.0.20",
        "open_ports": ["22", "25", "993", "995"],
        "metric_real": "0m0.672s",
    },
}


def read_file_lines(path: Path):
    """
    Read *binary* then decode using utf-8 with universal newlines to cope with
    any line-ending variants. Returns a list of stripped lines.
    """
    content = path.read_bytes().decode("utf-8", errors="replace")
    return [ln.rstrip("\r\n") for ln in content.splitlines()]


@pytest.mark.order(1)
def test_scan_logs_directory_exists():
    assert SCAN_DIR.is_dir(), (
        f"Required directory {SCAN_DIR} is missing. "
        "It must contain the raw nmap scan files."
    )


@pytest.mark.order(2)
def test_expected_scan_log_files_present_and_only_them():
    log_files = sorted(f.name for f in SCAN_DIR.glob("*.log"))
    expected_files = sorted(LOG_EXPECTATIONS.keys())

    assert log_files, f"No *.log files found in {SCAN_DIR}"
    assert log_files == expected_files, (
        f"Expected log files {expected_files} in {SCAN_DIR}, "
        f"but found {log_files}."
    )


@pytest.mark.order(3)
@pytest.mark.parametrize("filename,expect", LOG_EXPECTATIONS.items())
def test_each_log_file_content(filename, expect):
    file_path = SCAN_DIR / filename
    lines = read_file_lines(file_path)

    # 1. Host line
    host_line_pattern = re.compile(rf"^Nmap scan report for {re.escape(expect['host'])}$")
    assert any(host_line_pattern.match(ln) for ln in lines), (
        f"{filename}: Host line with IP {expect['host']} is missing or malformed."
    )

    # 2. Open TCP ports – collect them in the order they appear
    open_port_pattern = re.compile(r"^(\d+)/tcp\s+open\b", re.IGNORECASE)
    found_ports = [m.group(1) for ln in lines if (m := open_port_pattern.match(ln))]

    assert found_ports, f"{filename}: No open TCP ports were detected."
    assert found_ports == expect["open_ports"], (
        f"{filename}: Expected open ports {expect['open_ports']} in order, "
        f"but found {found_ports}."
    )

    # 3. #METRIC real line
    metric_pattern = re.compile(rf"^#METRIC real {re.escape(expect['metric_real'])}\b")
    assert any(metric_pattern.match(ln) for ln in lines), (
        f"{filename}: '#METRIC real {expect['metric_real']}' line is missing or incorrect."
    )


@pytest.mark.order(4)
def test_benchmark_directory_and_csv_do_not_yet_exist():
    assert not BENCHMARK_DIR.exists(), (
        f"Directory {BENCHMARK_DIR} already exists but should be created by the "
        "student's solution script."
    )
    assert not CSV_FILE.exists(), (
        f"CSV file {CSV_FILE} already exists. The student script should create it; "
        "it must not be present beforehand."
    )