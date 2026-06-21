# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before* the
# student starts working on the task.  It checks that the two source CSV files
# needed for the exercise are present and contain the exact, unmodified data
# the instructions describe.  No assertions are made about any output that the
# student is supposed to create later.

import os
from pathlib import Path
import pytest

INCIDENT_DIR = Path("/home/user/incidents")
FAILED_FILE = INCIDENT_DIR / "failed_attempts.csv"
SUCCESS_FILE = INCIDENT_DIR / "successful_attempts.csv"

# Expected raw file contents (LF terminated, including the final newline)
EXPECTED_FAILED_CONTENT = (
    "SessionID,IP\n"
    "1001,192.0.2.10\n"
    "1002,203.0.113.55\n"
    "1003,198.51.100.30\n"
    "1004,203.0.113.77\n"
    "1005,198.51.100.88\n"
)

EXPECTED_SUCCESS_CONTENT = (
    "SessionID,IP\n"
    "1001,198.51.100.23\n"
    "1002,198.51.100.24\n"
    "1003,203.0.113.60\n"
    "1004,192.0.2.44\n"
    "1005,203.0.113.90\n"
)


def _read_file(path: Path) -> str:
    """
    Helper that reads the entire file as text, preserving newlines exactly.
    Raises a helpful assertion if the file is missing.
    """
    assert path.exists(), f"Expected file {path} is missing."
    assert path.is_file(), f"Expected {path} to be a regular file."
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        pytest.fail(f"Could not read {path}: {exc}")


def test_incident_directory_exists():
    """Verify that /home/user/incidents/ exists and is a directory."""
    assert INCIDENT_DIR.exists(), (
        f"Required directory {INCIDENT_DIR} does not exist. "
        "The starter files should be located there."
    )
    assert INCIDENT_DIR.is_dir(), f"{INCIDENT_DIR} exists but is not a directory."


@pytest.mark.parametrize(
    "file_path, expected_content",
    [
        (FAILED_FILE, EXPECTED_FAILED_CONTENT),
        (SUCCESS_FILE, EXPECTED_SUCCESS_CONTENT),
    ],
)
def test_source_csv_files_have_expected_content(file_path: Path, expected_content: str):
    """
    Ensure that the two starter CSV files exist **and** have not been modified.
    The files must:
      1. Be present and readable.
      2. Contain exactly six LF-terminated lines.
      3. Match the byte-for-byte content specified in the task description.
    """
    content = _read_file(file_path)

    # 1. Exact content match (this implicitly covers line count and ordering).
    assert (
        content == expected_content
    ), (
        f"The contents of {file_path} do not match the expected starter data.\n"
        "If you have already modified the file, restore it to the original "
        "state shown in the instructions."
    )

    # 2. Verify final newline explicitly for clearer error messages.
    assert content.endswith(
        "\n"
    ), f"The file {file_path} must end with a single LF newline character."


def test_source_csv_line_counts():
    """
    Redundant but explicit check that each source CSV has exactly six lines
    (header + 5 data rows).
    """
    for file_path in (FAILED_FILE, SUCCESS_FILE):
        lines = _read_file(file_path).splitlines()
        assert len(lines) == 6, (
            f"{file_path} should contain exactly 6 lines "
            f"(1 header + 5 data rows); found {len(lines)}."
        )


def test_sessionid_alignment_between_files():
    """
    Ensure that the SessionID column in both files aligns exactly.
    This guarantees that the side-by-side comparison the student is asked
    to build will be meaningful.
    """
    failed_lines = _read_file(FAILED_FILE).splitlines()[1:]  # skip header
    success_lines = _read_file(SUCCESS_FILE).splitlines()[1:]  # skip header

    failed_session_ids = [line.split(",", 1)[0] for line in failed_lines]
    success_session_ids = [line.split(",", 1)[0] for line in success_lines]

    assert failed_session_ids == success_session_ids, (
        "SessionID columns do not line up between failed_attempts.csv and "
        "successful_attempts.csv.  Check that both files are intact and have "
        "not been altered."
    )