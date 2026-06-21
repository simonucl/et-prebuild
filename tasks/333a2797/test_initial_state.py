# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state BEFORE the student starts working on the assignment.
#
# This suite intentionally **fails fast** with clear, instructive error
# messages if anything in the starting conditions is missing or altered.
#
# It checks:
#   1. Presence of the required log directory and file.
#   2. Exact byte-for-byte contents (including newlines) of the log file.
#   3. Absence of the output directory and its three target artefact files.
#
# Only modules from the Python standard library are imported, in addition
# to pytest.

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

ROOT              = Path("/home/user/api_test")
LOG_DIR           = ROOT / "logs"
OUTPUT_DIR        = ROOT / "output"
ACCESS_LOG        = LOG_DIR / "access.log"

CRITICAL_POSTS    = OUTPUT_DIR / "critical_posts.log"
ENDPOINT_SUMMARY  = OUTPUT_DIR / "endpoint_summary.csv"
SANITIZED_LOG     = OUTPUT_DIR / "access_sanitized.log"

EXPECTED_ACCESS_LOG_LINES = [
    "2024-04-01T10:00:01Z 192.168.1.10 GET /v1/users 200 123",
    "2024-04-01T10:00:02Z 192.168.1.11 POST /v1/login 201 87",
    "2024-04-01T10:00:03Z 192.168.1.12 POST /v1/orders 503 232",
    "2024-04-01T10:00:04Z 192.168.1.13 GET /v1/products 200 145",
    "2024-04-01T10:00:05Z 192.168.1.14 POST /v1/orders 500 310",
    "2024-04-01T10:00:06Z 192.168.1.15 GET /v1/users 404 99",
    "2024-04-01T10:00:07Z 192.168.1.16 POST /v1/login 502 120",
    "2024-04-01T10:00:08Z 192.168.1.17 GET /v1/products 200 98",
]

# ---------------------------------------------------------------------------


def read_text_exact(path: Path) -> str:
    """
    Helper: Read text file as UTF-8 and return its contents exactly as stored.
    Any UnicodeDecodeError is propagated to give immediate feedback.
    """
    with path.open("r", encoding="utf-8") as fp:
        return fp.read()


@pytest.mark.dependency(name="directory_structure")
def test_required_directories_exist():
    # logs directory must exist
    assert LOG_DIR.is_dir(), (
        f"Missing required directory: {LOG_DIR}. "
        "The initial repo should already contain /logs with the access.log."
    )

    # output directory must NOT exist at the start
    assert not OUTPUT_DIR.exists(), (
        f"The output directory {OUTPUT_DIR} already exists, "
        "but the instructions state it should be created by the student."
    )


@pytest.mark.dependency(name="access_log_present", depends=["directory_structure"])
def test_access_log_file_exists_and_is_regular():
    assert ACCESS_LOG.is_file(), (
        f"Missing required file: {ACCESS_LOG}. "
        "Ensure the starting dataset is untouched and available."
    )


@pytest.mark.dependency(depends=["access_log_present"])
def test_access_log_contents_are_exact():
    """
    Verify that the access.log file matches the exact expected 8 lines,
    ensuring:  
    • UTF-8 encoding  
    • Each line ends with a single newline ('\\n')  
    • No extra blank lines / trailing whitespace
    """
    text = read_text_exact(ACCESS_LOG)

    # Ensure the file ends with a newline exactly once.
    assert text.endswith("\n"), (
        f"{ACCESS_LOG} must be newline-terminated. "
        "Expected a trailing '\\n' at the end of the file."
    )

    # Split lines while keeping behaviour consistent with newline termination.
    lines = text.rstrip("\n").split("\n")
    assert lines == EXPECTED_ACCESS_LOG_LINES, (
        f"{ACCESS_LOG} contents differ from the expected initial data.\n"
        "Differences detected (expected vs actual):\n"
        f"EXPECTED:\n{os.linesep.join(EXPECTED_ACCESS_LOG_LINES)}\n\n"
        f"ACTUAL:\n{os.linesep.join(lines)}"
    )


@pytest.mark.dependency(depends=["directory_structure"])
def test_no_output_files_yet():
    """
    None of the artefact files should exist before the student runs their
    solution.
    """
    for path in (CRITICAL_POSTS, ENDPOINT_SUMMARY, SANITIZED_LOG):
        assert not path.exists(), (
            f"Found unexpected file at start of exercise: {path}\n"
            "The student is supposed to create this file during the task; "
            "it should NOT be present initially."
        )