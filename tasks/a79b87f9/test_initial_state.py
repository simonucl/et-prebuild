# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present BEFORE the student performs any actions.  It intentionally avoids
# checking for the presence (or absence) of any files that the student is
# expected to create, as per the instructions.

import os
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

LOGS_DIR = Path("/home/user/ci_cd/logs")
BUILD_LOG = LOGS_DIR / "build.log"

EXPECTED_BUILD_LINES = [
    "2023-07-01 12:00:00 INFO Build started\n",
    "2023-07-01 12:00:01 INFO Running tests...\n",
    "2023-07-01 12:00:02 FAIL TestUserLogin failed with AssertionError\n",
    "2023-07-01 12:00:03 ERROR Deployment aborted\n",
    "2023-07-01 12:00:04 WARNING Disk space low\n",
    (
        "2023-07-01 12:00:05 FAIL "
        "TestPaymentProcessing failed with NullPointerException\n"
    ),
    "2023-07-01 12:00:06 INFO Build finished\n",
]

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def read_text_file(path: Path):
    """Read a text file in binary mode and decode with UTF-8, preserving newlines."""
    with path.open("rb") as fp:
        data = fp.read()
    # We expect pure LF line endings; make sure those are preserved.
    text = data.decode("utf-8")
    return text


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_logs_directory_exists_and_is_writable():
    assert LOGS_DIR.exists(), f"Expected directory {LOGS_DIR} to exist."
    assert LOGS_DIR.is_dir(), f"{LOGS_DIR} exists but is not a directory."
    assert os.access(LOGS_DIR, os.W_OK), f"Directory {LOGS_DIR} is not writable."


def test_build_log_exists_and_is_a_file():
    assert BUILD_LOG.exists(), f"Expected file {BUILD_LOG} to exist."
    assert BUILD_LOG.is_file(), f"{BUILD_LOG} exists but is not a regular file."


def test_build_log_has_expected_content():
    file_text = read_text_file(BUILD_LOG)

    # 1) Verify CRLF does not appear anywhere.
    assert "\r" not in file_text, (
        "build.log contains CRLF (Windows style) line endings; "
        "only LF line endings are expected."
    )

    # 2) Split into lines *keeping* the newline character for an exact match.
    actual_lines = [line for line in file_text.splitlines(keepends=True)]

    assert (
        actual_lines == EXPECTED_BUILD_LINES
    ), "build.log does not contain the exact expected lines."

    # 3) Ensure no line has trailing spaces before the newline.
    for idx, line in enumerate(actual_lines, start=1):
        stripped = line.rstrip("\n")
        assert stripped == stripped.rstrip(" "), (
            f"Line {idx} in build.log has trailing spaces: {repr(line)}"
        )


def test_logs_directory_contains_only_build_log():
    """The logs directory should initially contain exactly one file: build.log."""
    contents = sorted(p.name for p in LOGS_DIR.iterdir() if not p.is_dir())
    assert contents == ["build.log"], (
        f"Expected logs directory to contain only 'build.log', "
        f"but found: {contents}"
    )