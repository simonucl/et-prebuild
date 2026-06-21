# test_initial_state.py
"""
Pytest suite that validates the operating-system / file-system state
*before* the student performs any actions.

This file checks only the pre-existing artefacts that the grader
guarantees to be present for the assignment “SSH failed-login analysis”.

Rules honoured:
• Uses only stdlib + pytest.
• Verifies *input* logs, not the yet-to-be-created output directory/files.
• All paths are absolute under /home/user.
"""
import re
from pathlib import Path

import pytest

# ---------- CONSTANTS --------------------------------------------------------

SYSLOG_DIR = Path("/home/user/syslogs")
LOG_21 = SYSLOG_DIR / "auth.log.2023-07-21"
LOG_22 = SYSLOG_DIR / "auth.log.2023-07-22"

FAILED_PHRASE = "Failed password"
IP_REGEX = re.compile(r"from\s+(\d{1,3}(?:\.\d{1,3}){3})\s+port")

# Ground-truth expectations derived from the task description
EXPECTED_TOTALS = {
    LOG_21.name: 5,
    LOG_22.name: 6,
}

EXPECTED_UNIQUE_IPS = {
    LOG_21.name: 2,
    LOG_22.name: 3,
}

EXPECTED_SUSPICIOUS_IPS = {"10.0.0.5", "192.168.1.10"}  # appear ≥5 times across both logs


# ---------- HELPER FUNCTIONS -------------------------------------------------


def _failed_lines_and_ips(log_path: Path):
    """
    Yield tuples (line, ip) for every line in *log_path*
    that contains the exact phrase 'Failed password'.
    """
    for idx, line in enumerate(log_path.read_text(encoding="utf-8").splitlines(), 1):
        if FAILED_PHRASE in line:
            match = IP_REGEX.search(line)
            if not match:
                pytest.fail(
                    f"Line {idx} in {log_path} contains '{FAILED_PHRASE}' "
                    f"but no valid IPv4 address could be parsed:\n{line}"
                )
            yield line, match.group(1)


# ---------- TESTS ------------------------------------------------------------


def test_syslog_directory_exists():
    assert SYSLOG_DIR.is_dir(), (
        "Directory '/home/user/syslogs' is missing. "
        "All input log files must reside in this directory."
    )


@pytest.mark.parametrize("log_path", [LOG_21, LOG_22])
def test_log_files_exist(log_path):
    assert log_path.is_file(), (
        f"Expected log file '{log_path}' is missing. "
        "Ensure the correct filename and location."
    )


@pytest.mark.parametrize(
    ("log_path", "expected_total"), [(LOG_21, 5), (LOG_22, 6)]
)
def test_failed_password_line_counts(log_path, expected_total):
    failed_lines = list(_failed_lines_and_ips(log_path))
    assert len(failed_lines) == expected_total, (
        f"{log_path.name} should contain {expected_total} lines with the exact "
        f"phrase '{FAILED_PHRASE}', but {len(failed_lines)} were found."
    )


@pytest.mark.parametrize(
    ("log_path", "expected_unique"), [(LOG_21, 2), (LOG_22, 3)]
)
def test_unique_ip_counts_per_log(log_path, expected_unique):
    ips = {ip for _, ip in _failed_lines_and_ips(log_path)}
    assert len(ips) == expected_unique, (
        f"{log_path.name} should contain {expected_unique} distinct IP "
        f"addresses among the '{FAILED_PHRASE}' lines, but {len(ips)} were found."
    )


def test_suspicious_ips_across_all_logs():
    ip_counter = {}
    for log_path in (LOG_21, LOG_22):
        for _, ip in _failed_lines_and_ips(log_path):
            ip_counter[ip] = ip_counter.get(ip, 0) + 1

    suspicious = {ip for ip, count in ip_counter.items() if count >= 5}

    assert suspicious == EXPECTED_SUSPICIOUS_IPS, (
        "Calculated set of IPs responsible for five (5) or more failed log-in "
        f"attempts does not match expectation.\n"
        f"Expected: {sorted(EXPECTED_SUSPICIOUS_IPS)}\n"
        f"Found:    {sorted(suspicious)}"
    )