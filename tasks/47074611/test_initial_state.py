# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present **before** the student starts solving the task.  It checks:
#   1. The existence of /home/user/qa_logs and the two original *.log files.
#   2. That the contents of those logs exactly match the specification
#      (including trailing new-line characters).
#   3. That no output artefacts created by the student are present yet.
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import pytest

QA_DIR = Path("/home/user/qa_logs")

# ---------------------------------------------------------------------------
# Expected exact file contents (each line *must* end with '\n').
# ---------------------------------------------------------------------------

EXPECTED_SUITE1 = (
    "[2023-08-12 10:12:01] TEST test_login ..... PASS\n"
    "[2023-08-12 10:12:02] TEST test_logout ..... FAIL\n"
    "[2023-08-12 10:12:03] TEST test_signup ..... SKIP\n"
    "[2023-08-12 10:12:04] TEST test_profile_update ..... PASS\n"
    "[2023-08-12 10:12:05] TEST test_password_reset ..... PASS\n"
)

EXPECTED_SUITE2 = (
    "[2023-08-12 11:15:11] TEST api_fetch_user ..... PASS\n"
    "[2023-08-12 11:15:12] TEST api_create_user ..... FAIL\n"
    "[2023-08-12 11:15:13] TEST api_delete_user ..... FAIL\n"
    "[2023-08-12 11:15:14] TEST api_update_user ..... PASS\n"
)

# Mapping of file names to their expected contents for parametrised testing.
SOURCE_LOGS = {
    "suite1.log": EXPECTED_SUITE1,
    "suite2.log": EXPECTED_SUITE2,
}

# Output artefacts that must *NOT* exist yet.
OUTPUT_FILES = [
    QA_DIR / "suite1_clean.log",
    QA_DIR / "suite2_clean.log",
    QA_DIR / "summary_report.csv",
]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_qa_directory_exists():
    """The /home/user/qa_logs directory must exist before starting."""
    assert QA_DIR.is_dir(), (
        f"Required directory {QA_DIR} is missing.\n"
        "Create it and place the initial log files inside."
    )


@pytest.mark.parametrize("filename,expected_content", SOURCE_LOGS.items())
def test_source_log_exists_and_content_is_correct(filename, expected_content):
    """
    Each original suite*.log file must exist and contain the exact expected
    lines (including trailing LF characters).
    """
    file_path = QA_DIR / filename
    assert file_path.is_file(), f"Missing required file: {file_path}"

    actual = file_path.read_text(encoding="utf-8")
    assert actual == expected_content, (
        f"Contents of {file_path} do not match the specification.\n"
        "Expected:\n"
        f"{expected_content!r}\n"
        "Got:\n"
        f"{actual!r}"
    )


@pytest.mark.parametrize("path", OUTPUT_FILES)
def test_output_files_do_not_exist_yet(path):
    """
    Generated artefacts must NOT exist before the student runs their solution.
    These files will be produced later by the student's shell commands.
    """
    assert not path.exists(), (
        f"File {path} is present prematurely.\n"
        "The initial state must *not* include any clean logs or CSV report."
    )