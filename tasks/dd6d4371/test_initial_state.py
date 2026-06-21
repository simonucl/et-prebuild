# test_initial_state.py
#
# This test-suite validates that the **starting** file-system and log data
# are precisely in the expected state *before* the student runs any command.
#
# It intentionally **fails** if:
#   • the input logs are missing, renamed, unreadable, or altered
#   • additional /home/user/project/logs/*.log files are present
#   • /home/user/project/reports/ already exists (it must be created by the student)
#
# Only the Python standard library and pytest are used.

import pathlib
import pwd
import os

import pytest

HOME = pathlib.Path("/home/user").resolve()
PROJECT_DIR = HOME / "project"
LOG_DIR = PROJECT_DIR / "logs"
REPORT_DIR = PROJECT_DIR / "reports"

# Expected *.log files and the IPv4 (first-token) sequence in each file
EXPECTED_LOG_STRUCTURE = {
    LOG_DIR / "access1.log": [
        "192.168.0.1",
        "192.168.0.2",
        "192.168.0.1",
        "10.0.0.5",
        "192.168.0.1",
        "172.16.0.3",
        "192.168.0.2",
        "192.168.0.2",
        "10.0.0.5",
        "10.0.0.5",
    ],
    LOG_DIR / "access2.log": [
        "172.16.0.3",
        "192.168.0.1",
        "192.168.0.2",
        "192.168.0.2",
        "10.0.0.5",
        "172.16.0.3",
        "172.16.0.3",
        "10.0.0.5",
        "10.0.0.5",
        "10.0.0.5",
    ],
}

# Derived from the specification
EXPECTED_IP_COUNTS = {
    "10.0.0.5": 7,
    "192.168.0.2": 5,
    "172.16.0.3": 4,
    "192.168.0.1": 4,
}


def _get_first_token(line: str) -> str:
    """Return everything up to (but not including) the first ASCII space."""
    return line.split(" ", 1)[0]


@pytest.fixture(scope="module")
def log_files_content():
    """
    Read all expected log files and return a mapping of Path -> list[str] (stripped LF).
    The fixture itself will already assert basic presence and readability.
    """
    # 1. Directory /home/user/project/logs/ exists and is readable
    assert LOG_DIR.is_dir(), (
        f"Expected directory {LOG_DIR} to exist, but it is missing."
    )
    assert os.access(LOG_DIR, os.R_OK | os.X_OK), (
        f"Directory {LOG_DIR} is not readable/searchable by the current user."
    )

    # 2. No unexpected *.log files are present
    actual_logs = {p for p in LOG_DIR.glob("*.log") if p.is_file()}
    expected_logs = set(EXPECTED_LOG_STRUCTURE.keys())
    missing = expected_logs - actual_logs
    extra = actual_logs - expected_logs
    assert not missing, (
        "The following expected log file(s) are missing:\n"
        + "\n".join(str(p) for p in sorted(missing))
    )
    assert not extra, (
        "Found unexpected *.log file(s) in the logs directory:\n"
        + "\n".join(str(p) for p in sorted(extra))
    )

    # 3. Read the content of each file, verifying line counts
    content_map = {}
    for path in sorted(expected_logs):
        with path.open("r", encoding="utf-8") as fh:
            lines = [ln.rstrip("\n") for ln in fh]
        content_map[path] = lines

    return content_map


def test_no_reports_directory_yet():
    """/home/user/project/reports/ must NOT exist before the student acts."""
    assert not REPORT_DIR.exists(), (
        f"Directory {REPORT_DIR} already exists, "
        "but it must be created by the student solution."
    )


def test_log_files_have_expected_number_of_lines(log_files_content):
    """Each log file must contain exactly 10 lines as specified."""
    for path, lines in log_files_content.items():
        assert len(lines) == 10, (
            f"{path} is expected to have 10 lines, but has {len(lines)}."
        )


def test_first_tokens_match_expected_order(log_files_content):
    """
    Every line must begin with the exact IPv4 address specified in the truth value,
    and appear in the same order.
    """
    for path, expected_tokens in EXPECTED_LOG_STRUCTURE.items():
        actual_tokens = [_get_first_token(ln) for ln in log_files_content[path]]
        assert actual_tokens == expected_tokens, (
            f"The first-token IPv4 sequence in {path} deviates from the expected list.\n"
            f"Expected: {expected_tokens}\n"
            f"Actual:   {actual_tokens}"
        )


def test_combined_ip_frequencies_are_correct(log_files_content):
    """
    Across BOTH log files, the hit counts for every IPv4 must match the specification.
    """
    from collections import Counter

    combined_tokens = []
    for lines in log_files_content.values():
        combined_tokens.extend(_get_first_token(ln) for ln in lines)

    counter = Counter(combined_tokens)
    assert counter == EXPECTED_IP_COUNTS, (
        "The aggregated hit counts across all log files are incorrect.\n"
        f"Expected counts: {EXPECTED_IP_COUNTS}\n"
        f"Observed counts: {dict(counter)}"
    )