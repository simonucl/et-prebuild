# test_initial_state.py
#
# Pytest suite that validates the operating-system state **before**
# the student tackles the task.  It checks that the prerequisite
# artefacts exist and contain exactly the data described in the
# challenge text.  No assertions are made about any output the
# student is expected to create later.

import pathlib
import re

import pytest

HOME = pathlib.Path("/home/user")
SUSPICIOUS_PATH = HOME / "suspicious_ips.txt"
LOG_PATH = HOME / "logs" / "auth.log"

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def read_lines(path):
    """
    Read a file and return a list of lines with trailing newlines stripped.
    """
    with path.open("r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh]


def extract_failed_ips(log_lines):
    """
    From auth.log lines, extract IP addresses that appear in
    lines containing the substring 'Failed password'.

    Returns a list of the matched IP strings.
    """
    pat = re.compile(r"Failed password .* from (?P<ip>\d{1,3}(?:\.\d{1,3}){3}) ")
    ips = []
    for ln in log_lines:
        if "Failed password" not in ln:
            continue
        m = pat.search(ln)
        if m:
            ips.append(m.group("ip"))
    return ips


# ---------------------------------------------------------------------------
# Expected ground-truth data as per the task description
# ---------------------------------------------------------------------------

EXPECTED_IPS_LIST = [
    "203.0.113.45",
    "198.51.100.77",
    "192.0.2.13",
]

EXPECTED_FAILED_COUNTS = {
    "203.0.113.45": 4,
    "198.51.100.77": 2,
    "192.0.2.13": 0,
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_artifact_paths_exist():
    """Validate that all required files/directories exist."""
    assert SUSPICIOUS_PATH.exists(), (
        f"Missing file: {SUSPICIOUS_PATH}. "
        "The list of suspicious IPs must be present before the exercise starts."
    )
    assert SUSPICIOUS_PATH.is_file(), f"{SUSPICIOUS_PATH} exists but is not a regular file."

    assert LOG_PATH.parent.exists(), (
        f"Missing directory: {LOG_PATH.parent}. "
        "The 'logs' directory must exist and contain auth.log."
    )
    assert LOG_PATH.exists(), (
        f"Missing file: {LOG_PATH}. "
        "The authentication log must be present before the exercise starts."
    )
    assert LOG_PATH.is_file(), f"{LOG_PATH} exists but is not a regular file."


def test_suspicious_ips_contents_exact_and_ordered():
    """
    /home/user/suspicious_ips.txt must contain exactly the three IPs stated in
    the instructions, each on its own line, in the given order.
    """
    lines = read_lines(SUSPICIOUS_PATH)

    # The file may have a trailing blank line, so drop empties at the end only.
    while lines and lines[-1] == "":
        lines.pop()

    assert lines == EXPECTED_IPS_LIST, (
        f"{SUSPICIOUS_PATH} contents mismatch.\n"
        f"Expected (order matters):\n  {EXPECTED_IPS_LIST}\n"
        f"Found:\n  {lines}"
    )


def test_auth_log_failed_password_counts_match_description():
    """
    auth.log must contain the exact number of 'Failed password' events for each
    suspicious IP as specified in the task description.
    """
    log_lines = read_lines(LOG_PATH)
    found_ips = extract_failed_ips(log_lines)

    # Count occurrences
    from collections import Counter

    counts = Counter(found_ips)

    # Build a human-readable diff if something is off.
    mismatches = []
    for ip, expected_cnt in EXPECTED_FAILED_COUNTS.items():
        actual_cnt = counts.get(ip, 0)
        if actual_cnt != expected_cnt:
            mismatches.append(f"{ip}: expected {expected_cnt}, found {actual_cnt}")

    assert not mismatches, (
        "auth.log does not contain the expected number of failed-SSH events "
        "for the listed suspicious IPs:\n  " + "\n  ".join(mismatches)
    )


def test_auth_log_does_not_contain_unlisted_failed_ips():
    """
    Ensure that auth.log does not introduce additional suspicious IPs not
    present in suspicious_ips.txt when considering 'Failed password' lines.
    """
    log_lines = read_lines(LOG_PATH)
    failed_ips = set(extract_failed_ips(log_lines))
    unexpected = failed_ips - set(EXPECTED_IPS_LIST)
    assert not unexpected, (
        "auth.log includes 'Failed password' events from IPs that are NOT in "
        f"{SUSPICIOUS_PATH}: {', '.join(sorted(unexpected))}"
    )