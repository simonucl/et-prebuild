# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating-system
# filesystem **before** the student performs any work for the “ping-diagnostics”
# task.  It checks that:
#
# • The expected log file exists in the correct location and is readable.
# • The log contains exactly four distinct ping reports.
# • The set of hosts that were completely unreachable can be unambiguously
#   determined from the log and matches the reference truth value
#   {'10.0.0.5', '192.168.2.200'}.
# • The output file that the student will have to create
#   (/home/user/network/reports/unreachable.list) does *not* exist yet, ensuring
#   the environment is clean.
#
# Only the Python standard library and pytest are used.

import re
from pathlib import Path
import pytest

HOME = Path("/home/user")
LOG_FILE = HOME / "network" / "logs" / "diag.log"
REPORTS_DIR = HOME / "network" / "reports"
REPORT_FILE = REPORTS_DIR / "unreachable.list"


@pytest.fixture(scope="module")
def log_contents():
    """Return the full text of the diagnostics log file."""
    if not LOG_FILE.exists():
        pytest.fail(f"Required diagnostics log file is missing: {LOG_FILE}")
    if not LOG_FILE.is_file():
        pytest.fail(f"Path exists but is not a regular file: {LOG_FILE}")
    try:
        text = LOG_FILE.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Cannot read {LOG_FILE}: {exc}")
    return text


def test_log_file_exists_and_is_not_empty(log_contents):
    """The diagnostics log must exist and contain data."""
    assert log_contents.strip(), (
        f"{LOG_FILE} exists but is empty; it must contain ping diagnostics."
    )


def _parse_ping_reports(text):
    """
    Very lightweight parser that walks through the log and yields tuples
    of (target_ip, report_text).

    A new report starts at a line that matches r'^PING\\s+<ip>\\s+\\(' and
    ends right before the next 'PING ' line or the end of the file.
    """
    ping_header = re.compile(r"^PING\s+(\d+\.\d+\.\d+\.\d+)\s+\(")
    reports = []
    current_ip = None
    current_lines = []

    for line in text.splitlines():
        m = ping_header.match(line)
        if m:
            # Save the previous report if there was one
            if current_ip is not None:
                reports.append((current_ip, "\n".join(current_lines)))
            # Start a new report
            current_ip = m.group(1)
            current_lines = [line]
        else:
            if current_ip is not None:
                current_lines.append(line)

    # Capture the final report
    if current_ip is not None:
        reports.append((current_ip, "\n".join(current_lines)))

    return reports


def _is_completely_unreachable(report_text):
    """
    Decide if a ping report indicates total failure.

    Conditions considered:
    • Summary line contains ' 0 received'
    • Any line contains the phrase 'Destination Host Unreachable'
    """
    if "Destination Host Unreachable" in report_text:
        return True
    summary_0_received = re.search(r"\b0\s+received\b", report_text)
    return bool(summary_0_received)


def test_log_contains_expected_reports(log_contents):
    """Ensure exactly four distinct ping targets are present."""
    reports = _parse_ping_reports(log_contents)
    targets = {ip for ip, _ in reports}

    assert len(reports) == 4, (
        f"Expected 4 ping reports in {LOG_FILE}, found {len(reports)}."
    )
    assert len(targets) == 4, (
        f"Expected 4 unique targets, found {len(targets)}: {sorted(targets)}"
    )


def test_unreachable_hosts_match_truth(log_contents):
    """
    The log file must contain two and only two completely unreachable hosts:
    10.0.0.5 and 192.168.2.200.
    """
    reports = _parse_ping_reports(log_contents)
    unreachable = sorted(
        ip for ip, txt in reports if _is_completely_unreachable(txt)
    )

    expected = sorted({"10.0.0.5", "192.168.2.200"})
    assert unreachable == expected, (
        "The set of unreachable hosts parsed from the log does not match the "
        f"expected truth value.\nExpected: {expected}\nFound: {unreachable}"
    )


def test_output_file_absent_initially():
    """
    Prior to the student's work, neither the reports directory nor the
    unreachable.list file should exist.  This guarantees that the solution
    script will have to create them.
    """
    assert not REPORT_FILE.exists(), (
        f"Output file {REPORT_FILE} should **not** exist yet. "
        "The working environment must be clean."
    )