# test_initial_state.py
#
# Pytest suite that validates the machine’s state *before* the student begins
# any work.  It checks that the required input log files exist and contain the
# expected information, and that none of the required output artefacts have
# been created yet.
#
# Only the Python standard library and pytest are used.

import collections
import os
import pathlib
import re

SYSLOG_PATH = pathlib.Path("/home/user/logs/syslog")
ACCESS_LOG_PATH = pathlib.Path("/home/user/logs/access.log")
ANALYSIS_DIR = pathlib.Path("/home/user/analysis")

EXPECTED_SERVICE_COUNTS = {
    "sshd":    {"ERROR": 3, "WARNING": 2},
    "apache2": {"ERROR": 3, "WARNING": 1},
    "cron":    {"ERROR": 0, "WARNING": 1},
}

EXPECTED_TOP_IPS = [
    ("192.168.1.10", 5),
    ("192.168.1.11", 4),
    ("10.0.0.5",     3),
    ("192.168.1.12", 3),
    ("172.16.0.2",   2),
]


def _parse_syslog(path: pathlib.Path):
    """
    Parse the syslog file and return a nested dictionary:
        {service: {"ERROR": n, "WARNING": m}}
    """
    counts = collections.defaultdict(lambda: {"ERROR": 0, "WARNING": 0})
    service_re = re.compile(r'\s(?P<svc>[A-Za-z0-9_\-]+)\[')

    with path.open("r", encoding="utf-8") as fh:
        for line_nr, line in enumerate(fh, 1):
            m = service_re.search(line)
            assert m, f"Unable to extract service token on line {line_nr} of syslog"
            service = m.group("svc")
            if "ERROR" in line:
                counts[service]["ERROR"] += 1
            if "WARNING" in line:
                counts[service]["WARNING"] += 1
    return counts


def _parse_access_log(path: pathlib.Path):
    """
    Parse the access log and return a Counter keyed by IP address.
    """
    ip_counter = collections.Counter()
    with path.open("r", encoding="utf-8") as fh:
        for line_nr, line in enumerate(fh, 1):
            tokens = line.split()
            assert tokens, f"Empty line {line_nr} in access.log"
            ip = tokens[0]
            ip_counter[ip] += 1
    return ip_counter


def test_logs_exist_and_are_files():
    """
    Basic sanity-check: required input log files must be present.
    """
    assert SYSLOG_PATH.is_file(), f"Missing required syslog file at {SYSLOG_PATH}"
    assert ACCESS_LOG_PATH.is_file(), f"Missing required access log at {ACCESS_LOG_PATH}"


def test_syslog_service_error_warning_counts():
    """
    Verify that the syslog contains exactly the expected ERROR/WARNING
    counts per service.
    """
    counts = _parse_syslog(SYSLOG_PATH)

    # First, ensure we saw all expected services.
    for svc in EXPECTED_SERVICE_COUNTS:
        assert svc in counts, f"Service '{svc}' not found in {SYSLOG_PATH}"

    # Now compare numeric counts.
    for svc, expected in EXPECTED_SERVICE_COUNTS.items():
        actual = counts[svc]
        assert actual["ERROR"]   == expected["ERROR"],   (
            f"Service '{svc}' ERROR count mismatch: expected {expected['ERROR']}, got {actual['ERROR']}"
        )
        assert actual["WARNING"] == expected["WARNING"], (
            f"Service '{svc}' WARNING count mismatch: expected {expected['WARNING']}, got {actual['WARNING']}"
        )

    # Finally, ensure there are no *extra* unexpected services.
    unexpected_svcs = set(counts) - set(EXPECTED_SERVICE_COUNTS)
    assert not unexpected_svcs, f"Unexpected services found in syslog: {sorted(unexpected_svcs)}"


def test_access_log_top_five_ips():
    """
    Confirm that the top-five IP addresses and their hit counts match the
    ground-truth data provided by the task.
    """
    ip_counter = _parse_access_log(ACCESS_LOG_PATH)

    # Derive the calculated top-five list.
    top_five = sorted(
        ip_counter.items(),
        key=lambda kv: (-kv[1], kv[0])
    )[:5]

    assert top_five == EXPECTED_TOP_IPS, (
        "Top-five IP list mismatch.\n"
        f"Expected: {EXPECTED_TOP_IPS}\n"
        f"Got:      {top_five}"
    )


def test_no_output_files_present_yet():
    """
    Before the student starts, the /home/user/analysis directory should NOT
    already contain the final output files.  (It may not exist at all.)
    """
    error_csv = ANALYSIS_DIR / "error_warning_summary.csv"
    top_ips   = ANALYSIS_DIR / "top_ips.log"

    if ANALYSIS_DIR.exists():
        assert not error_csv.exists(), f"Output file should not exist yet: {error_csv}"
        assert not top_ips.exists(),   f"Output file should not exist yet: {top_ips}"