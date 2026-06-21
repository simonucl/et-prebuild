# test_initial_state.py
#
# This pytest suite verifies that the starting filesystem/OS state is exactly
# what the exercise specification promises *before* the student’s solution is
# run.  If any of these tests fail, it means the exercise is not in a clean
# initial state and the student cannot be fairly evaluated.

import os
import re
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
CI_DATA_DIR = HOME / "ci_data" / "commit_authors"
EXPECTED_LOG_FILES = {
    "service-a.log",
    "service-b.log",
    "service-c.log",
}

REPORTS_DIR = HOME / "ci_reports"
REPORT_FILE = REPORTS_DIR / "commit_author_frequency.tsv"

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def test_commit_authors_directory_exists_and_is_directory():
    """The /home/user/ci_data/commit_authors directory must exist and be a directory."""
    assert CI_DATA_DIR.exists(), (
        f"Required directory {CI_DATA_DIR} is missing. "
        "The exercise cannot proceed without the raw author logs."
    )
    assert CI_DATA_DIR.is_dir(), f"{CI_DATA_DIR} exists but is not a directory."


def test_expected_log_files_present_and_no_extraneous_files():
    """
    Exactly the expected *.log files must be present.  This ensures the student
    solution will discover all logs via a glob pattern and will not be tripped
    up by unexpected extra files.
    """
    present_files = {p.name for p in CI_DATA_DIR.iterdir() if p.is_file()}
    missing = EXPECTED_LOG_FILES - present_files
    extra = present_files - EXPECTED_LOG_FILES

    assert not missing, (
        "The following required .log file(s) are missing from "
        f"{CI_DATA_DIR}: {', '.join(sorted(missing))}"
    )
    assert not extra, (
        "Unexpected file(s) found in "
        f"{CI_DATA_DIR}: {', '.join(sorted(extra))}. "
        "The initial state must contain only the provided log files."
    )


@pytest.mark.parametrize("log_file", sorted(EXPECTED_LOG_FILES))
def test_each_log_file_non_empty_and_email_per_line(log_file):
    """
    Every line of each log file must contain exactly one e-mail address, and
    there must be no blank lines.  This mirrors the contract given in the
    problem statement.
    """
    file_path = CI_DATA_DIR / log_file
    lines = file_path.read_text(encoding="utf-8").splitlines(keepends=False)

    assert lines, f"{file_path} is empty; it must contain author e-mail addresses."

    for idx, line in enumerate(lines, start=1):
        assert line.strip() == line, (
            f"{file_path}: line {idx} has leading/trailing whitespace. "
            "Lines must contain only the e-mail address."
        )
        assert line, f"{file_path}: line {idx} is blank; no blank lines are allowed."
        assert EMAIL_RE.fullmatch(line), (
            f"{file_path}: line {idx} does not look like a valid e-mail address: {line!r}"
        )


def test_report_file_does_not_yet_exist():
    """
    The commit_author_frequency.tsv report should NOT exist at the initial
    checkpoint.  The student's solution is expected to create it.
    """
    assert not REPORT_FILE.exists(), (
        f"The report file {REPORT_FILE} already exists at test start. "
        "The initial state should not contain any generated reports."
    )