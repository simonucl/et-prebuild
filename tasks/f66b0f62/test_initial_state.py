# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state for the
# “backup-failures report” exercise **before** the student’s solution
# code is run.
#
# The checks performed here intentionally mirror the specification found
# in the task description and the hidden “truth” section.  If any of
# these tests fail, it means the exercise’s starting environment is not
# what the grader expects, and the learner would be unfairly penalised.

import os
import textwrap
import pytest

HOME = "/home/user"
LOG_DIR = os.path.join(HOME, "db_backups", "logs")
REPORT_DIR = os.path.join(HOME, "db_backups", "reports")
REPORT_CSV = os.path.join(REPORT_DIR, "backup_failures_report.csv")

# ---------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------


def read_file(path):
    """Return file contents with universal newline support."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read().replace("\r\n", "\n")


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------


def test_required_directories_exist_and_are_dirs():
    """Validate that both the logs and reports directories exist."""
    assert os.path.isdir(LOG_DIR), (
        f"Required log directory missing: {LOG_DIR}"
    )
    assert os.path.isdir(REPORT_DIR), (
        f"Required reports directory missing: {REPORT_DIR}"
    )


@pytest.mark.parametrize(
    "filename,expected_contents",
    [
        (
            "backup_2023-07-08.log",
            textwrap.dedent(
                """\
                [2023-07-08 03:03:12] INFO  db=customers  status=SUCCESS  duration=43s
                [2023-07-08 03:04:01] ERROR db=customers  code=BKUP-013  msg="Could not open backup file"
                [2023-07-08 03:05:09] INFO  db=customers  status=END   duration=44s
                """
            ),
        ),
        (
            "backup_2023-07-10.log",
            textwrap.dedent(
                """\
                [2023-07-10 01:00:12] INFO  db=orders  status=START
                [2023-07-10 01:01:55] ERROR db=orders  code=BKUP-001  msg="Tablespace read error"
                [2023-07-10 01:02:40] INFO  db=orders  status=END duration=99s
                """
            ),
        ),
        (
            "backup_2023-07-12.log",
            textwrap.dedent(
                """\
                [2023-07-12 04:17:07] INFO  db=inventory  status=START
                [2023-07-12 04:18:00] WARN  db=inventory  message="Slow I/O detected"
                [2023-07-12 04:19:22] ERROR db=inventory  code=BKUP-047  msg="Checksum mismatch"
                [2023-07-12 04:20:00] INFO  db=inventory  status=END duration=173s
                """
            ),
        ),
        (
            "backup_2023-07-14.log",
            textwrap.dedent(
                """\
                [2023-07-14 02:55:02] INFO  db=analytics  status=START
                [2023-07-14 02:56:34] ERROR db=analytics  code=BKUP-001  msg="Tablespace read error"
                [2023-07-14 03:01:10] ERROR db=analytics  code=BKUP-099  msg="Destination full"
                [2023-07-14 03:02:00] INFO  db=analytics  status=END duration=355s
                """
            ),
        ),
    ],
)
def test_log_files_present_with_expected_contents(filename, expected_contents):
    """
    Ensure each expected .log file exists and contains exactly the lines
    provided in the seed data (ignoring trailing newline differences).
    """
    full_path = os.path.join(LOG_DIR, filename)
    assert os.path.isfile(full_path), f"Expected log file not found: {full_path}"

    actual = read_file(full_path).strip()
    expected = expected_contents.strip()
    assert (
        actual == expected
    ), (
        f"Contents of {full_path} do not match the expected seed data.\n"
        f"--- EXPECTED ---\n{expected}\n--- ACTUAL ---\n{actual}\n"
    )


def test_report_file_does_not_exist_yet():
    """
    Prior to the learner’s script running, the report CSV must *not*
    exist.  Its presence would imply the environment is dirty.
    """
    assert not os.path.exists(
        REPORT_CSV
    ), f"Report file {REPORT_CSV} should not exist before the student runs their solution."