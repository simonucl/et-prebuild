# test_initial_state.py
#
# Pytest suite that validates the initial state of the filesystem
# before the learner runs any commands for the “backup administrator” task.
#
# The checks confirm ONLY the pre-existing resources that the task description
# guarantees.  No assertions are made about any output directories or files
# that the learner will create later.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
REPORTS_DIR = HOME / "reports"

@pytest.fixture(scope="module")
def reports_dir():
    """Return the Path object for /home/user/reports and ensure it exists."""
    if not REPORTS_DIR.exists():
        pytest.fail(f"Required directory {REPORTS_DIR} is missing.")
    if not REPORTS_DIR.is_dir():
        pytest.fail(f"{REPORTS_DIR} exists but is not a directory.")
    return REPORTS_DIR


def test_reports_directory_structure(reports_dir):
    """
    Verify the required directory hierarchy under /home/user/reports.

    Expected tree:
        /home/user/reports/
            report1.txt
            report2.txt
            summary/
                quarter3.txt
    """
    # Paths to check
    report1 = reports_dir / "report1.txt"
    report2 = reports_dir / "report2.txt"
    summary_dir = reports_dir / "summary"
    quarter3 = summary_dir / "quarter3.txt"

    # Directory existence
    assert summary_dir.exists() and summary_dir.is_dir(), (
        f"Missing subdirectory: {summary_dir}"
    )

    # File existence
    for path in (report1, report2, quarter3):
        assert path.exists() and path.is_file(), f"Missing file: {path}"


@pytest.mark.parametrize(
    "relative_path, expected_content",
    [
        ("report1.txt", "Q1 financial summary\n"),
        ("report2.txt", "Q2 financial summary\n"),
        ("summary/quarter3.txt", "Q3 details\n"),
    ],
)
def test_file_contents(reports_dir, relative_path, expected_content):
    """
    Confirm that each pre-populated report file contains the exact
    expected text (including the terminating newline).
    """
    file_path = reports_dir / relative_path
    try:
        contents = file_path.read_text()
    except FileNotFoundError:
        pytest.fail(f"Required file {file_path} is missing.")

    assert (
        contents == expected_content
    ), f"File {file_path} has unexpected contents: {contents!r}"