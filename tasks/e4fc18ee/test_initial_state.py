# test_initial_state.py
#
# Pytest suite that validates the INITIAL state of the operating system /
# filesystem before the student begins the assignment described in the
# prompt.  It deliberately avoids checking for the presence or contents of
# any output artifacts that the student is expected to create or overwrite
# (e.g., chrome_success_summary.json or generate_report.log).

import os
import stat

import pytest

# ---------------------------------------------------------------------------
# Constants describing the required initial filesystem layout and contents
# ---------------------------------------------------------------------------

WEBAPP_DIR = "/home/user/projects/webapp"
DATA_DIR = f"{WEBAPP_DIR}/data"
REPORTS_DIR = f"{WEBAPP_DIR}/reports"
VISITS_CSV = f"{DATA_DIR}/visits.csv"

EXPECTED_CSV_CONTENT = (
    "date,user_id,browser,status\n"
    "2024-05-01,101,Chrome,200\n"
    "2024-05-01,102,Firefox,200\n"
    "2024-05-01,103,Chrome,404\n"
    "2024-05-02,104,Chrome,200\n"
    "2024-05-02,105,Edge,200\n"
    "2024-05-03,106,Chrome,200\n"
)  # NOTE: the final \n is *required* and is included in the string above.


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _is_world_readable(path: str) -> bool:
    """
    Return True if 'path' has world-readable permissions (mode 0o444 or more
    permissive).  Symlinks, if any, are resolved to their target.
    """
    mode = os.stat(path, follow_symlinks=True).st_mode
    return bool(mode & stat.S_IROTH)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_directories_exist_and_are_directories():
    """
    Validate that the required directory hierarchy exists and that each entry
    is indeed a directory (not, e.g., a file or symlink).  The test messages
    are explicit so that students know exactly what is missing or mis-typed.
    """
    for path in [WEBAPP_DIR, DATA_DIR, REPORTS_DIR]:
        assert os.path.exists(path), f"Expected directory '{path}' is missing."
        assert os.path.isdir(
            path
        ), f"'{path}' exists but is not a directory.  It must be a directory."


def test_visits_csv_exists_with_expected_content_and_permissions():
    """
    Check that visits.csv is present, world-readable, and contains exactly the
    lines described in the task (including the trailing newline).
    """
    assert os.path.exists(
        VISITS_CSV
    ), f"Required CSV file '{VISITS_CSV}' is missing from the data directory."
    assert os.path.isfile(
        VISITS_CSV
    ), f"'{VISITS_CSV}' exists but is not a regular file."

    # Verify file permissions (world-readable permissions are required).
    assert _is_world_readable(
        VISITS_CSV
    ), f"'{VISITS_CSV}' must be world-readable (permission mode 644 or more permissive)."

    # Read and compare file content exactly.
    with open(VISITS_CSV, "r", encoding="utf-8") as fp:
        actual_content = fp.read()

    # Exact match check (length + text + final newline).
    assert (
        actual_content == EXPECTED_CSV_CONTENT
    ), (
        f"The contents of '{VISITS_CSV}' do not match the expected initial "
        f"dataset.  The file must contain exactly:\n\n{EXPECTED_CSV_CONTENT!r}"
    )


@pytest.mark.skip(
    reason=(
        "The task requires the student to create/overwrite certain report "
        "files.  The specification explicitly forbids validating the presence "
        "or contents of those output files in the *initial* state."
    )
)
def test_output_files_are_not_validated_in_initial_state():
    """
    Placeholder test (skipped) to document why we intentionally do NOT inspect
    chrome_success_summary.json or generate_report.log before the student's
    solution runs.
    """
    pass