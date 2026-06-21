# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem before the
# student starts working on the assignment.  It purposefully makes NO reference
# to any of the artefacts that the student is supposed to create later
# (build_reports/*  etc.).
#
# If any of these tests fail it means the playground is not in the pristine
# state that the assignment description promises.

import os
import re
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
PROJECT_ROOT = HOME / "projects"
CI_LOGS_DIR = PROJECT_ROOT / "ci_logs"
GITIGNORE = PROJECT_ROOT / ".gitignore"


@pytest.fixture(scope="module")
def ci_log_files():
    """
    Return a mapping  {date_str: Path} for the two expected raw log files.
    """
    files = {
        "2023-11-01": CI_LOGS_DIR / "logs_2023-11-01.txt",
        "2023-11-02": CI_LOGS_DIR / "logs_2023-11-02.txt",
    }
    return files


def test_ci_logs_directory_exists():
    assert CI_LOGS_DIR.is_dir(), (
        f"Directory {CI_LOGS_DIR} is expected to exist but is missing."
    )


def _parse_log_line(line):
    """
    Parse one log line and return (date, status).
    Expected format:
        [YYYY-MM-DD HH:MM:SS] BUILD_ID=<id> STATUS=<SUCCESS|FAILURE> DURATION=<n>s
    """
    pattern = (
        r"\[(?P<date>\d{4}-\d{2}-\d{2}) \d{2}:\d{2}:\d{2}\]\s+"
        r"BUILD_ID=[A-Za-z0-9\-]+\s+STATUS=(?P<status>SUCCESS|FAILURE)\s+"
        r"DURATION=\d+s"
    )
    m = re.fullmatch(pattern, line.strip())
    if not m:
        raise ValueError(f"Log line does not match expected format: {line!r}")
    return m.group("date"), m.group("status")


@pytest.mark.parametrize("date_str,total,failures", [
    ("2023-11-01", 10, 2),
    ("2023-11-02", 10, 3),
])
def test_each_log_file_exists_and_has_expected_content(ci_log_files, date_str,
                                                       total, failures):
    log_path = ci_log_files[date_str]
    assert log_path.is_file(), f"Log file {log_path} is missing."

    lines = log_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == total, (
        f"{log_path} should have exactly {total} lines, found {len(lines)}."
    )

    # Parse every line, verifying date and counting statuses.
    failure_count = 0
    for idx, line in enumerate(lines, 1):
        try:
            date, status = _parse_log_line(line)
        except ValueError as e:
            pytest.fail(f"{log_path}: line {idx}: {e}")

        assert date == date_str, (
            f"{log_path}: line {idx}: expected date {date_str}, found {date}."
        )
        if status == "FAILURE":
            failure_count += 1

    assert failure_count == failures, (
        f"{log_path}: expected {failures} FAILURE lines, found {failure_count}."
    )


def test_git_repository_exists():
    git_dir = PROJECT_ROOT / ".git"
    assert git_dir.is_dir(), (
        f"{git_dir} directory is missing. Project should already be a git repo."
    )


def test_gitignore_initial_state():
    assert GITIGNORE.is_file(), f"{GITIGNORE} is missing."

    expected_lines = [
        "# Existing ignore patterns",
        "*.tmp",
    ]
    actual_lines = GITIGNORE.read_text(encoding="utf-8").splitlines()
    assert actual_lines == expected_lines, (
        f"{GITIGNORE} should contain exactly the two default lines:\n"
        f"{expected_lines!r}\nFound:\n{actual_lines!r}"
    )


def test_build_reports_directory_not_present_yet():
    """
    The build_reports directory and any deliverables should NOT exist before
    the student runs their solution.
    """
    build_reports = PROJECT_ROOT / "build_reports"
    assert not build_reports.exists(), (
        f"{build_reports} should not exist in the initial state."
    )