# test_initial_state.py
#
# This test-suite validates the *initial* OS / filesystem state that must
# be present **before** the student starts implementing the task.
#
# It checks that:
#   • /home/user/migration_logs exists and contains exactly the three
#     expected log files.
#   • Each log file has the exact, newline-terminated contents that the
#     grading rubric specifies.
#   • The report file that the student is supposed to create does *not*
#     exist yet (to avoid false positives in later grading stages).
#
# Any failure message should clearly tell the student what piece of the
# initial state is missing or incorrect.
#
# NOTE: Only stdlib + pytest are used, per the constraints.

from pathlib import Path
import os
import pytest
import textwrap

LOG_DIR = Path("/home/user/migration_logs")
SUMMARY_DIR = Path("/home/user/migration_summary")
SUMMARY_CSV = SUMMARY_DIR / "service_frequency_20240101.csv"

EXPECTED_LOG_FILES = {
    "day1.log": textwrap.dedent(
        """\
        auth
        billing
        auth
        user
        search
        billing
        auth
        cdn
        """
    ),
    "day2.log": textwrap.dedent(
        """\
        search
        video
        auth
        search
        billing
        user
        video
        video
        cdn
        """
    ),
    "day3.log": textwrap.dedent(
        """\
        auth
        billing
        search
        search
        cdn
        cdn
        billing
        auth
        video
        video
        analytics
        """
    ),
}


def _normalise_newlines(s: str) -> str:
    """
    Ensure we are comparing strings with \n as newline and that each
    line *including the last* is newline-terminated.
    """
    if not s.endswith("\n"):
        s += "\n"
    return s.replace("\r\n", "\n")


def test_log_directory_exists():
    assert LOG_DIR.exists(), f"Required directory '{LOG_DIR}' is missing."
    assert LOG_DIR.is_dir(), f"'{LOG_DIR}' exists but is not a directory."


def test_log_directory_contains_exact_three_logs():
    actual_logs = sorted(p.name for p in LOG_DIR.iterdir() if p.is_file())
    expected_logs = sorted(EXPECTED_LOG_FILES.keys())
    assert actual_logs == expected_logs, (
        "The directory '/home/user/migration_logs' must contain exactly "
        f"these three files: {expected_logs}. Found: {actual_logs}"
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_LOG_FILES.items())
def test_each_log_file_content_exact(filename, expected_content):
    """
    Verify that every log file contains **exactly** the expected lines,
    and that every line (including the last) ends with '\n'.
    """
    file_path = LOG_DIR / filename
    assert file_path.exists(), f"Expected log file '{file_path}' is missing."

    # Read raw bytes to preserve newline information
    raw = file_path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"Log file '{file_path}' is not valid UTF-8: {exc}")

    # Ensure the final byte is a newline
    assert text.endswith(
        "\n"
    ), f"Log file '{file_path}' must end with exactly one trailing newline."

    # Normalise newlines for comparison
    normalised_expected = _normalise_newlines(expected_content)
    assert (
        text == normalised_expected
    ), f"Contents of '{file_path}' do not match the expected specification."


def test_summary_csv_does_not_exist_yet():
    """
    The student has not run their solution yet, therefore the summary CSV
    should NOT exist at this stage.
    """
    assert not SUMMARY_CSV.exists(), (
        f"Report file '{SUMMARY_CSV}' already exists. "
        "The initial state should *not* contain the file to be produced "
        "by the student's solution."
    )