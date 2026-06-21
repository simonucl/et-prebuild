# test_initial_state.py
"""
Pytest suite that validates the initial state of the operating system / filesystem
for the *API audit* exercise.

It checks:
1. The working directory  /home/user/api_audit   exists.
2. The server implementation file
   /home/user/api_audit/restricted_server.py   exists, is a regular file, and can
   be parsed by Python (i.e. has no import-time syntax errors).
3. The permissions report
   /home/user/api_audit/permissions_report.log
   exists and matches the required six-line, fixed-width specification exactly,
   including newlines and the absence of trailing blank lines.

Only the standard library and pytest are used.
"""

import ast
import os
from pathlib import Path

import pytest

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
API_AUDIT_DIR = Path("/home/user/api_audit")
SERVER_FILE = API_AUDIT_DIR / "restricted_server.py"
LOG_FILE = API_AUDIT_DIR / "permissions_report.log"

EXPECTED_LOG_CONTENT = (
    "GET /public 200\n"
    "GET /admin 403\n"
    "GET /missing 404\n"
    "HEAD /public 200\n"
    "HEAD /admin 403\n"
    "SUMMARY total_tested=5 pass_count=5\n"
)

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
def read_text_exact(path: Path) -> str:
    """
    Read a text file exactly as-is (no newline translation) and return a str.
    """
    with path.open("r", encoding="utf-8", newline="") as fp:
        return fp.read()


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_api_audit_directory_exists():
    assert API_AUDIT_DIR.is_dir(), (
        f"Expected working directory '{API_AUDIT_DIR}' to exist as a directory."
    )


def test_restricted_server_file_exists_and_is_valid_python():
    assert SERVER_FILE.is_file(), (
        f"Expected server implementation '{SERVER_FILE}' to exist as a regular file."
    )
    # Attempt to parse the file to ensure it contains syntactically valid Python.
    try:
        source = SERVER_FILE.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read '{SERVER_FILE}': {exc}")

    try:
        ast.parse(source, filename=str(SERVER_FILE))
    except SyntaxError as exc:  # pragma: no cover
        pytest.fail(
            f"'{SERVER_FILE}' exists but contains Python syntax errors:\n{exc}"
        )


def test_permissions_report_log_exists_and_content_is_correct():
    assert LOG_FILE.is_file(), (
        f"Expected permissions report '{LOG_FILE}' to exist as a regular file."
    )

    actual = read_text_exact(LOG_FILE)

    # 1) Content must match expected string exactly.
    assert actual == EXPECTED_LOG_CONTENT, (
        "The contents of permissions_report.log do not match the required six-line "
        "specification.\n\n"
        "Expected:\n"
        f"{EXPECTED_LOG_CONTENT!r}\n\n"
        "Actual:\n"
        f"{actual!r}"
    )

    # 2) Ensure *exactly* six non-empty lines are present (safeguard against hidden chars).
    lines = actual.splitlines(keepends=False)
    assert len(lines) == 6, (
        "permissions_report.log must contain exactly six non-blank lines "
        f"(found {len(lines)})."
    )
    for idx, line in enumerate(lines[:5], start=1):
        parts = line.split(" ")
        assert len(parts) == 3, (
            f"Line {idx} of permissions_report.log should have three space-separated "
            "fields (<METHOD> <PATH> <STATUS_CODE>). "
            f"Found: {line!r}"
        )

    # 3) Confirm the final newline is present (required by spec) and no extra blank lines.
    assert actual.endswith("\n"), (
        "permissions_report.log must terminate with a single trailing newline."
    )


# -----------------------------------------------------------------------------
# The tests above are definitive; no additional tests are necessary or desired.
# -----------------------------------------------------------------------------