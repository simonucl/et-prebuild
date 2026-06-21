# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state expected by the
# assignment “mini-mock API smoke-test”.  All checks are read-only and rely
# solely on Python’s standard library plus pytest.

import os
import re
from pathlib import Path

# --------------------------------------------------------------------------- #
# Constants describing the expected artefacts
# --------------------------------------------------------------------------- #
HOME = Path("/home/user")
MOCKAPI_DIR = HOME / "mockapi"
DATA_DIR = MOCKAPI_DIR / "data"
LOGS_DIR = MOCKAPI_DIR / "logs"

USER_JSON = DATA_DIR / "user.json"
PRODUCT_JSON = DATA_DIR / "product.json"
LOG_FILE = LOGS_DIR / "api_test.log"

# Exact contents (trailing newline is optional and tolerated when comparing)
USER_JSON_CONTENT = (
    '{"id":101,"username":"testuser","email":"tester@example.com"}'
)
PRODUCT_JSON_CONTENT = (
    '{"id":501,"name":"Widget","price":19.99}'
)

# Regular expression for TIMESTAMP line (ISO-8601 UTC, e.g., 2024-03-15T08:22:40Z)
TIMESTAMP_RE = re.compile(r"^TIMESTAMP:\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _read_file_strip_newline(path: Path) -> str:
    """
    Read a small text file and strip **one** trailing newline
    (if present) to allow either representation in comparisons.
    """
    data = path.read_text(encoding="utf-8")
    return data[:-1] if data.endswith("\n") else data


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_directory_structure():
    # Root mockapi directory
    assert MOCKAPI_DIR.is_dir(), (
        f"Missing directory: {MOCKAPI_DIR} — create it with two sub-directories "
        f"'data' and 'logs'."
    )

    # Sub-directories
    assert DATA_DIR.is_dir(), (
        f"Missing directory: {DATA_DIR}. Expected structure:\n"
        f"{MOCKAPI_DIR}/data"
    )
    assert LOGS_DIR.is_dir(), (
        f"Missing directory: {LOGS_DIR}. Expected structure:\n"
        f"{MOCKAPI_DIR}/logs"
    )


def test_json_file_user():
    assert USER_JSON.is_file(), f"Expected JSON file not found: {USER_JSON}"
    content = _read_file_strip_newline(USER_JSON)
    assert content == USER_JSON_CONTENT, (
        f"Content mismatch in {USER_JSON}.\n"
        f"Expected: {USER_JSON_CONTENT!r}\n"
        f"Found:    {content!r}"
    )


def test_json_file_product():
    assert PRODUCT_JSON.is_file(), f"Expected JSON file not found: {PRODUCT_JSON}"
    content = _read_file_strip_newline(PRODUCT_JSON)
    assert content == PRODUCT_JSON_CONTENT, (
        f"Content mismatch in {PRODUCT_JSON}.\n"
        f"Expected: {PRODUCT_JSON_CONTENT!r}\n"
        f"Found:    {content!r}"
    )


def test_log_file_exists_and_format():
    assert LOG_FILE.is_file(), f"Expected log file not found: {LOG_FILE}"

    lines = LOG_FILE.read_text(encoding="utf-8").rstrip("\n").split("\n")
    assert len(lines) == 6, (
        f"{LOG_FILE} must contain exactly 6 lines. Found {len(lines)} line(s)."
    )

    # Line-1: TIMESTAMP
    assert TIMESTAMP_RE.match(lines[0]), (
        "Line 1 of api_test.log must match the ISO-8601 UTC pattern "
        "'TIMESTAMP:YYYY-MM-DDTHH:MM:SSZ'.\n"
        f"Found: {lines[0]!r}"
    )

    # Lines 2-4: numeric status codes must all be 000
    expected_status_lines = [
        "USER_STATUS:000",
        "PRODUCT_STATUS:000",
        "POST_STATUS:000",
    ]
    for idx, expected in enumerate(expected_status_lines, start=1):
        actual = lines[idx]
        assert actual == expected, (
            f"Line {idx+1} of api_test.log expected {expected!r} but found {actual!r}"
        )

    # Line-5: USERNAME
    assert lines[4] == "USERNAME:testuser", (
        f"Line 5 of api_test.log must be 'USERNAME:testuser'. Found: {lines[4]!r}"
    )

    # Line-6: PRODUCT_NAME
    assert lines[5] == "PRODUCT_NAME:Widget", (
        f"Line 6 of api_test.log must be 'PRODUCT_NAME:Widget'. Found: {lines[5]!r}"
    )