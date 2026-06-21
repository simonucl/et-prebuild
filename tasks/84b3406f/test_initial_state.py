# test_initial_state.py
#
# Pytest suite that validates the *starting* operating-system / filesystem
# state for the “FAILED LOGIN” incident-response exercise.
#
# These checks run **before** the student writes any code, shell scripts or
# produces any output artefacts.  If any of the assertions below fail it means
# the practical lab has been provisioned incorrectly and the student should
# not be penalised.

import gzip
import os
import re
from datetime import datetime
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constant paths used throughout the tests
# --------------------------------------------------------------------------- #
HOME                = Path("/home/user")
EVIDENCE_DIR        = HOME / "incidents" / "syslog-backups"
SCRIPT_DIR          = HOME / "scripts"
REPORTS_DIR         = HOME / "incident_reports"
SCRIPT_PATH         = SCRIPT_DIR / "analyze_failed_logins.sh"

# The four evidence files that *must* be present.
EXPECTED_GZ_FILES = {
    "syslog-2023-07-20.gz",
    "syslog-2023-07-21.gz",
    "syslog-2023-07-22.gz",
    "syslog-2023-07-23.gz",
}

# Expected statistics derived from all logs.
EXPECTED_IP_COUNTS = {
    "192.168.0.101": 7,
    "10.0.0.5":      5,
    "172.16.5.22":   2,
}
EXPECTED_TOTAL_EVENTS        = 14
EXPECTED_FIRST_LAST_PER_IP   = {
    "10.0.0.5":      ("2023-07-20T23:51:00Z", "2023-07-23T12:30:00Z"),
    "172.16.5.22":   ("2023-07-20T23:50:00Z", "2023-07-22T00:05:00Z"),
    "192.168.0.101": ("2023-07-21T02:13:45Z", "2023-07-23T12:00:00Z"),
}

IP_REGEX   = re.compile(r"[0-9]{1,3}(?:\.[0-9]{1,3}){3}")
TS_REGEX   = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _iter_failed_login_lines():
    """
    Yield (timestamp_str, ip_str) tuples for every “FAILED LOGIN” line found
    in every .gz file inside the evidence directory.
    """
    for gz_name in sorted(EXPECTED_GZ_FILES):
        gz_path = EVIDENCE_DIR / gz_name
        with gzip.open(gz_path, "rt", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if "FAILED LOGIN" not in line:
                    continue
                # Extract timestamp – first RFC-3339 token on the line.
                ts_match = TS_REGEX.match(line)
                assert ts_match, f"Line lacks RFC-3339 timestamp: {line!r}"
                ts = ts_match.group(0)

                # Extract first IPv4 address on the line.
                ip_match = IP_REGEX.search(line)
                assert ip_match, f"FAILED LOGIN line without IPv4: {line!r}"
                ip = ip_match.group(0)

                yield ts, ip


def _parse_iso8601_z(ts: str) -> datetime:
    """
    Convert an ISO-8601 string ending in “Z” into a timezone-aware datetime
    object using UTC.
    """
    if not ts.endswith("Z"):
        raise ValueError(f"Timestamp lacks trailing 'Z': {ts!r}")
    # Remove the 'Z' and parse as UTC.
    return datetime.fromisoformat(ts[:-1]).replace(tzinfo=None)


# --------------------------------------------------------------------------- #
# Test cases
# --------------------------------------------------------------------------- #
def test_evidence_directory_exists():
    assert EVIDENCE_DIR.is_dir(), (
        f"Expected evidence directory {EVIDENCE_DIR} to exist and be a directory."
    )


def test_expected_gz_files_present_and_readable():
    actual_files = {p.name for p in EVIDENCE_DIR.glob("*.gz")}
    missing = EXPECTED_GZ_FILES - actual_files
    extras  = actual_files - EXPECTED_GZ_FILES
    assert not missing, f"Missing .gz evidence files: {', '.join(sorted(missing))}"
    assert not extras,  f"Unexpected extra .gz files present: {', '.join(sorted(extras))}"

    # Also ensure each .gz file can be opened.
    for gz_name in EXPECTED_GZ_FILES:
        gz_path = EVIDENCE_DIR / gz_name
        try:
            with gzip.open(gz_path, "rb") as fh:
                fh.peek(1)  # Trigger decompression header check.
        except OSError as exc:
            pytest.fail(f"Evidence file {gz_path} is not a valid gzip archive: {exc}")


def test_failed_login_event_statistics_match_expected():
    ip_counts  = {}
    first_seen = {}
    last_seen  = {}

    for ts_str, ip in _iter_failed_login_lines():
        # Count events.
        ip_counts[ip] = ip_counts.get(ip, 0) + 1

        # Track first/last seen timestamps for every IP.
        ts_dt = _parse_iso8601_z(ts_str)
        if ip not in first_seen or ts_dt < first_seen[ip]:
            first_seen[ip] = ts_dt
        if ip not in last_seen or ts_dt > last_seen[ip]:
            last_seen[ip] = ts_dt

    # ----  Validate counts  ----
    assert ip_counts == EXPECTED_IP_COUNTS, (
        "Per-IP FAILED LOGIN counts do not match the expected baseline.\n"
        f"Observed:  {ip_counts}\n"
        f"Expected:  {EXPECTED_IP_COUNTS}"
    )

    observed_total = sum(ip_counts.values())
    assert observed_total == EXPECTED_TOTAL_EVENTS, (
        f"Total number of FAILED LOGIN events is {observed_total}, "
        f"expected {EXPECTED_TOTAL_EVENTS}."
    )

    # ----  Validate first / last seen times  ----
    for ip, (expected_first, expected_last) in EXPECTED_FIRST_LAST_PER_IP.items():
        first_obs = first_seen[ip].isoformat(timespec="seconds") + "Z"
        last_obs  = last_seen[ip].isoformat(timespec="seconds")  + "Z"
        assert first_obs == expected_first, (
            f"First-seen timestamp for {ip} is {first_obs}, expected {expected_first}."
        )
        assert last_obs == expected_last, (
            f"Last-seen timestamp for {ip} is {last_obs}, expected {expected_last}."
        )


def test_script_directory_exists_but_script_not_yet_created():
    assert SCRIPT_DIR.is_dir(), f"Scripts directory {SCRIPT_DIR} should exist."
    assert not SCRIPT_PATH.exists(), (
        f"Analysis script {SCRIPT_PATH} should NOT exist before the student creates it."
    )


def test_reports_directory_absent():
    assert not REPORTS_DIR.exists(), (
        f"Reports directory {REPORTS_DIR} must NOT exist before the student runs any code."
    )