# test_initial_state.py
#
# This pytest suite validates the **initial** state of the operating system /
# filesystem _before_ the student performs any actions for the “site-01” uptime
# log task.  It confirms that only the expected pre-existing assets are present
# and that no output artifacts have been created yet.
#
# Requirements verified:
# 1. The log directory (/home/user/logs) exists.
# 2. The log file (/home/user/logs/site-01-2023-10-05.log) exists and its
#    contents match the exact seven lines supplied in the spec (including
#    trailing UNIX newline characters).
# 3. The output directory (/home/user/output) does **not** yet exist.
# 4. The two output files that will be generated later are **not** present.

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants reflecting the authoritative “ground truth” for the initial state
# ---------------------------------------------------------------------------

LOG_DIR = Path("/home/user/logs")
LOG_FILE = LOG_DIR / "site-01-2023-10-05.log"

OUTPUT_DIR = Path("/home/user/output")
ALERTS_FILE = OUTPUT_DIR / "site-01_alerts.log"
INCIDENT_REPORT_FILE = OUTPUT_DIR / "incident_report_2023-10-05.txt"

EXPECTED_LOG_LINES = [
    "2023-10-05T13:00:00Z site-01 OK response_time=120ms\n",
    "2023-10-05T13:05:00Z site-01 ERROR connection_timeout\n",
    "2023-10-05T13:10:00Z site-01 OK response_time=118ms\n",
    "2023-10-05T13:15:00Z site-01 WARNING high_latency response_time=350ms\n",
    "2023-10-05T13:20:00Z site-01 OK response_time=119ms\n",
    "2023-10-05T13:25:00Z site-01 CRITICAL host_unreachable\n",
    "2023-10-05T13:30:00Z site-01 OK response_time=117ms\n",
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _read_file_lines(path: Path):
    """
    Read a text file and return a list of lines **including** the newline
    character.  The file is opened in binary mode first to ensure that Windows
    CRLFs are not present; then decoded as UTF-8.
    """
    with path.open("rb") as fh:
        data = fh.read()
    # Ensure only UNIX LF line endings are present
    assert b"\r" not in data, (
        f"File {path} contains Windows CRLF line endings; "
        "expected UNIX LF ('\\n')."
    )
    text = data.decode("utf-8")
    return [line + "\n" for line in text.rstrip("\n").split("\n")] if text else []


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_log_directory_exists():
    """Verify that the log directory is present and is a directory."""
    assert LOG_DIR.exists(), f"Required log directory missing: {LOG_DIR}"
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory"


def test_log_file_exists_and_contents_are_exact():
    """Verify that the log file exists and match its exact expected contents."""
    assert LOG_FILE.exists(), f"Required log file missing: {LOG_FILE}"
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file"

    actual_lines = _read_file_lines(LOG_FILE)

    # 1. Exact number of lines
    assert len(actual_lines) == len(EXPECTED_LOG_LINES), (
        f"{LOG_FILE} should contain {len(EXPECTED_LOG_LINES)} lines, "
        f"found {len(actual_lines)}"
    )

    # 2. Exact content line-by-line
    for idx, (expected, actual) in enumerate(zip(EXPECTED_LOG_LINES, actual_lines), 1):
        assert expected == actual, (
            f"Line {idx} in {LOG_FILE!s} does not match expected content:\n"
            f"  Expected: {expected!r}\n"
            f"  Found:    {actual!r}"
        )


def test_output_directory_absent():
    """
    The tasks have not yet been executed, therefore the output directory
    MUST NOT exist at this point.
    """
    assert not OUTPUT_DIR.exists(), (
        f"Output directory {OUTPUT_DIR} already exists; the environment is "
        "not in the expected initial state."
    )


@pytest.mark.parametrize(
    "path",
    [ALERTS_FILE, INCIDENT_REPORT_FILE],
    ids=["alerts file", "incident report file"],
)
def test_output_files_absent(path):
    """Neither of the expected output files should exist yet."""
    assert not path.exists(), (
        f"Output file {path} already exists; the environment is not in the "
        "expected initial state."
    )