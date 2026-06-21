# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem/OS state
# before the student performs any actions for the "performance-summary"
# task.  It checks only the pre-existing items that must already be on
# disk and explicitly avoids touching any of the files that the student
# is expected to create.

import os
import stat
from pathlib import Path

import pytest


ANALYTICS_DIR = Path("/home/user/analytics")
PERF_FILE = ANALYTICS_DIR / "query_perf_2023.csv"

# The file content we expect to find *exactly* (including the final \n).
EXPECTED_CSV_CONTENT = (
    "query_id,sql_text,execution_time_ms,rows_examined,rows_returned\n"
    "Q1001,SELECT * FROM users,45,1200,100\n"
    "Q1002,DELETE FROM sessions WHERE expired=1,30,8000,0\n"
    "Q1003,UPDATE orders SET status='shipped' WHERE id=24,52,1,0\n"
    "Q1004,SELECT COUNT(*) FROM logs,120,1500000,1\n"
    "Q1005,INSERT INTO products(name,price) VALUES('Widget',9.99),10,0,1\n"
)


def _octal_permissions(path: Path) -> str:
    """Return the permission bits in octal string form, e.g. '755'."""
    return oct(path.stat().st_mode & 0o777)[2:]


def test_analytics_directory_exists_and_has_correct_permissions():
    assert ANALYTICS_DIR.exists(), (
        f"Required directory '{ANALYTICS_DIR}' is missing.\n"
        "Create it before proceeding."
    )
    assert ANALYTICS_DIR.is_dir(), f"'{ANALYTICS_DIR}' exists but is not a directory."
    expected_perm = "755"
    actual_perm = _octal_permissions(ANALYTICS_DIR)
    assert actual_perm == expected_perm, (
        f"Directory '{ANALYTICS_DIR}' should have permissions {expected_perm}, "
        f"but has {actual_perm}."
    )


def test_perf_csv_exists_is_regular_file_and_permissions_correct():
    assert PERF_FILE.exists(), (
        f"Input file '{PERF_FILE}' is missing. It must be present before you start."
    )
    assert PERF_FILE.is_file(), f"'{PERF_FILE}' exists but is not a regular file."
    expected_perm = "644"
    actual_perm = _octal_permissions(PERF_FILE)
    assert actual_perm == expected_perm, (
        f"File '{PERF_FILE}' should have permissions {expected_perm}, "
        f"but has {actual_perm}."
    )


def test_perf_csv_content_matches_expected_exactly():
    # Read the entire file as text with universal newlines disabled so we
    # inspect bytes as stored (assumes LF line endings as per spec).
    content = PERF_FILE.read_text(encoding="utf-8")
    assert content == EXPECTED_CSV_CONTENT, (
        f"Contents of '{PERF_FILE}' do not match the expected initial data.\n"
        "Please ensure the file is unmodified and contains exactly the 6 lines "
        "specified in the task description (including the trailing newline)."
    )
    # Extra safety: ensure the file ends with exactly one newline.
    assert content.endswith("\n"), (
        f"'{PERF_FILE}' must end with a single newline character."
    )
    # And ensure there are exactly 6 lines (header + 5 data lines).
    lines = content.splitlines()
    assert len(lines) == 6, (
        f"'{PERF_FILE}' should have exactly 6 lines, but has {len(lines)}."
    )