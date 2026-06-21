# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state for the
# “backup log line–count summary” exercise.  It verifies that the input
# directories and log files exist *before* the student runs any commands.
#
# NOTE:  Per the grading-suite rules we **do not** look for the eventual
# output file “/home/user/data/backup_reports/line_counts.csv”.

import os
import stat
import pytest

# ---------------------------------------------------------------------------
# Helper data
# ---------------------------------------------------------------------------

BACKUP_DIR      = "/home/user/data/backups"
REPORTS_DIR     = "/home/user/data/backup_reports"

EXPECTED_DIRS = [
    (BACKUP_DIR,  0o755),
    (REPORTS_DIR, 0o755),
]

EXPECTED_FILES = {
    "/home/user/data/backups/2023-05-01.log": [
        "2023-05-01 00:00:01 Backup job started",
        "2023-05-01 00:15:23 Compressing data",
        "2023-05-01 00:45:50 Uploading archive",
        "2023-05-01 01:10:05 Verification successful",
        "2023-05-01 01:10:06 Backup completed",
    ],
    "/home/user/data/backups/2023-05-02.log": [
        "2023-05-02 00:00:02 Backup job started",
        "2023-05-02 00:54:10 Backup failed: network timeout",
        "2023-05-02 00:54:11 Backup aborted",
    ],
    "/home/user/data/backups/2023-05-03.log": [
        "2023-05-03 00:00:02 Backup job started",
        "2023-05-03 00:25:15 Compressing data",
        "2023-05-03 00:49:40 Uploading archive",
        "2023-05-03 01:05:12 Backup completed",
    ],
}

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("dir_path, expected_mode", EXPECTED_DIRS)
def test_required_directories_exist(dir_path: str, expected_mode: int):
    """All mandatory directories must exist with the correct permissions."""
    assert os.path.isdir(dir_path), (
        f"Required directory missing: {dir_path}"
    )

    mode = stat.S_IMODE(os.stat(dir_path).st_mode)
    assert mode == expected_mode, (
        f"Directory {dir_path} should have permissions {oct(expected_mode)},"
        f" but has {oct(mode)}"
    )


@pytest.mark.parametrize("file_path, expected_lines", EXPECTED_FILES.items())
def test_required_log_files_exist_and_match_content(file_path: str, expected_lines: list[str]):
    """Each .log file must exist, have mode 0644, and match the expected content."""
    assert os.path.isfile(file_path), (
        f"Required file missing: {file_path}"
    )

    mode = stat.S_IMODE(os.stat(file_path).st_mode)
    assert mode == 0o644, (
        f"File {file_path} should have permissions 0644, but has {oct(mode)}"
    )

    with open(file_path, encoding="utf-8") as fh:
        actual_lines = [ln.rstrip("\n") for ln in fh]

    assert actual_lines == expected_lines, (
        f"Content mismatch in {file_path}.\n"
        f"Expected ({len(expected_lines)} lines):\n{expected_lines}\n\n"
        f"Got ({len(actual_lines)} lines):\n{actual_lines}"
    )


def test_expected_line_counts():
    """Verify that the line counts of each file match the specification."""
    for path, expected_lines in EXPECTED_FILES.items():
        with open(path, encoding="utf-8") as fh:
            actual_line_count = sum(1 for _ in fh)
        assert actual_line_count == len(expected_lines), (
            f"Line count mismatch for {path}: "
            f"expected {len(expected_lines)}, got {actual_line_count}"
        )