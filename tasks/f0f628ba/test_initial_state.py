# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# BEFORE the student starts working on the “Kubernetes status reports” task.
#
# Expectations for the clean slate:
# 1. Directory /home/user/status_columns/ exists and contains four single-column
#    text files with the exact, known contents listed in the task description.
# 2. Directory /home/user/reports/ does NOT exist yet (nothing has been created).
#
# Any deviation from this baseline should surface as a clear test failure,
# letting the student know what is missing or unexpectedly present.
#
# Only Python stdlib + pytest are used, in compliance with the grading rules.

from pathlib import Path
import pytest

STATUS_DIR = Path("/home/user/status_columns")
REPORTS_DIR = Path("/home/user/reports")

# Mapping: filename -> expected 3 data rows (order matters)
EXPECTED_COLUMNS = {
    "status_column_1.txt": ["deploy-httpd", "deploy-nginx", "deploy-redis"],
    "status_column_2.txt": ["running", "running", "pending"],
    "status_column_3.txt": ["3/3", "2/2", "0/1"],
    "status_column_4.txt": ["10m", "5m", "12m"],
}


def test_status_columns_directory_exists():
    """The source directory with the four column files must be present."""
    assert STATUS_DIR.is_dir(), (
        f"Required directory {STATUS_DIR} is missing. "
        "The four status_column_*.txt files must live here."
    )


@pytest.mark.parametrize("filename", EXPECTED_COLUMNS.keys())
def test_each_status_file_exists(filename):
    """Every required status_column_*.txt file must exist."""
    path = STATUS_DIR / filename
    assert path.is_file(), f"Expected file {path} is missing."


@pytest.mark.parametrize("filename,expected_rows", EXPECTED_COLUMNS.items())
def test_status_file_contents_are_exact(filename, expected_rows):
    """
    Each status_column_*.txt file must contain exactly three non-blank lines
    with a trailing newline at EOF. The lines and their order are prescribed
    by the task description.
    """
    path = STATUS_DIR / filename
    text = path.read_text(encoding="utf-8")

    # 1. File must end with a single trailing newline
    assert text.endswith("\n"), f"File {path} must end with a single trailing newline (\\n)."

    # 2. Split into lines (strip the final empty item if splitlines(keepends=False) encountered)
    lines = text.strip("\n").split("\n")

    # 3. Exactly three non-blank lines are required
    assert len(lines) == 3, (
        f"File {path} must contain exactly 3 non-blank lines, found {len(lines)}."
    )

    # 4. Verify content and order
    assert lines == expected_rows, (
        f"Content mismatch in {path}.\n"
        f"Expected rows: {expected_rows}\n"
        f"Actual rows:   {lines}"
    )


def test_reports_directory_absent():
    """
    The reports directory should NOT exist before the student runs any commands.
    Its presence would indicate that the workspace is not pristine.
    """
    assert not REPORTS_DIR.exists(), (
        f"Directory {REPORTS_DIR} is already present, but the task instructions "
        "state that it must be created by the student."
    )