# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must be
# present before the student starts working on the exercise described in
# the task instructions.  Nothing related to the *output* artefacts (such
# as /home/user/api_tests/error_report.log) is checked here; those will be
# verified by a separate, post-action test-suite.

import os
from pathlib import Path

import pytest

API_TESTS_DIR = Path("/home/user/api_tests").resolve()

# Expected files (absolute Path objects) and their exact byte contents.
EXPECTED_LOG_FILES = {
    API_TESTS_DIR / "api1.log": (
        "2023-07-01T12:00:00Z ERROR 500 INTERNAL_SERVER_ERROR /v1/users/123\n"
        "2023-07-01T12:00:02Z INFO 204 NO_CONTENT /v1/users/123\n"
    ),
    API_TESTS_DIR / "api2.log": (
        "2023-07-02T15:30:10Z ERROR 504 GATEWAY_TIMEOUT /v1/orders\n"
        "2023-07-02T15:31:10Z INFO 201 CREATED /v1/orders\n"
    ),
    API_TESTS_DIR / "deprecated.log": (
        "2023-06-30T10:00:00Z ERROR 410 GONE /v0/legacy\n"
    ),
}


def test_api_tests_directory_exists_and_is_dir():
    assert API_TESTS_DIR.exists(), (
        f"The directory {API_TESTS_DIR} is missing.  It must exist before "
        "students start the task."
    )
    assert API_TESTS_DIR.is_dir(), f"{API_TESTS_DIR} exists but is not a directory."


@pytest.mark.parametrize("path,expected_content", EXPECTED_LOG_FILES.items())
def test_log_file_exists_with_correct_content(path: Path, expected_content: str):
    # 1. Basic existence.
    assert path.exists(), f"Required log file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."

    # 2. Read and compare exact byte contents (including final newline).
    # Using newline='' prevents universal-newline translation.
    with path.open("r", encoding="utf-8", newline="") as fp:
        content = fp.read()

    assert content == expected_content, (
        f"File {path} content mismatch.\n"
        "EXPECTED:\n"
        f"{expected_content!r}\n"
        "GOT:\n"
        f"{content!r}"
    )


def test_no_unexpected_log_files_present():
    """
    Only the three specified .log files must be present initially in the
    /home/user/api_tests directory (other file types are ignored here).
    """
    expected_names = {p.name for p in EXPECTED_LOG_FILES}
    found_names = {p.name for p in API_TESTS_DIR.glob("*.log")}
    unexpected = found_names - expected_names
    missing = expected_names - found_names

    assert not missing, (
        "The following expected .log files are missing: "
        f"{', '.join(sorted(missing))}"
    )
    assert not unexpected, (
        "Unexpected .log files present in the initial fixture: "
        f"{', '.join(sorted(unexpected))}"
    )