# test_initial_state.py
#
# This pytest file validates the **initial** state of the operating system
# before the student performs any actions.  It checks that the access-log
# file required for the task is present and contains exactly the expected
# contents—nothing more, nothing less.

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

ACCESS_LOG = Path("/home/user/server_access.log")

# Expected contents of /home/user/server_access.log
EXPECTED_LINES = [
    "server1",
    "server2",
    "server1",
    "server3",
    "server2",
    "server2",
    "server1",
    "server4",
    "server3",
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def read_file(path: Path) -> str:
    """Read a text file and return its contents as a single string."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Required file not found: {path!s}")
    except Exception as exc:
        pytest.fail(f"Could not read {path!s}: {exc}")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_access_log_exists_and_is_file():
    """Verify that /home/user/server_access.log exists and is a regular file."""
    assert ACCESS_LOG.exists(), (
        f"The required access-log file {ACCESS_LOG} is missing.\n"
        "Create this file before running your solution."
    )
    assert ACCESS_LOG.is_file(), (
        f"{ACCESS_LOG} exists but is not a regular file."
    )


def test_access_log_contents_exact_match():
    """
    Ensure the access-log file contains exactly the nine expected lines,
    each terminated by a single newline, with no extra whitespace.
    """
    text = read_file(ACCESS_LOG)

    # Check for mandatory final newline
    assert text.endswith("\n"), (
        f"{ACCESS_LOG} must end with a newline (\\n) after the last line."
    )

    # Split into lines without retaining the newline characters
    lines = text.splitlines()

    # Verify line count
    assert len(lines) == len(EXPECTED_LINES), (
        f"{ACCESS_LOG} should contain {len(EXPECTED_LINES)} lines, "
        f"but contains {len(lines)}."
    )

    # Verify each line matches expected value and has no leading/trailing spaces
    for idx, (expected, actual) in enumerate(zip(EXPECTED_LINES, lines), start=1):
        assert actual == expected, (
            f"Line {idx} of {ACCESS_LOG} is incorrect.\n"
            f"Expected: {expected!r}\n"
            f"Actual:   {actual!r}"
        )
        assert actual == actual.strip(), (
            f"Line {idx} of {ACCESS_LOG} contains leading or trailing whitespace:\n"
            f"Actual line: {actual!r}"
        )


def test_access_log_no_extra_content():
    """
    Confirm that there is no extra content in the access-log file beyond the
    expected lines (e.g., blank lines, headers, or footers).
    """
    text = read_file(ACCESS_LOG)

    # After splitting and rejoining with '\n', we should get the same text.
    reconstructed = "\n".join(EXPECTED_LINES) + "\n"
    assert text == reconstructed, (
        f"{ACCESS_LOG} contains unexpected content.\n"
        "It must match exactly (including whitespace) the 9 specified lines."
    )