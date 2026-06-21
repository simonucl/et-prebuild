# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem
# BEFORE the student begins working on the “Batch-handling log files
# with find + xargs” exercise.
#
# These tests deliberately verify ONLY the initial conditions that
# must already be in place.  They do NOT look for any artefacts the
# student is expected to create (archive directory, tarball, summary
# file, etc.).  If any of these tests fail, the laboratory setup is
# wrong and the student will be starting from a broken baseline.

import os
import stat
import pytest

HOME = "/home/user"
LOG_ROOT = os.path.join(HOME, "logs")
APP1_DIR = os.path.join(LOG_ROOT, "app1")
APP2_DIR = os.path.join(LOG_ROOT, "app2")

# ----------------------------------------------------------------------
# 1.  Directories that must already exist
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "path",
    [
        LOG_ROOT,
        APP1_DIR,
        APP2_DIR,
    ],
)
def test_preexisting_directories_exist(path):
    assert os.path.isdir(path), f"Required directory {path} is missing."
    # Should be user-writable
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IWUSR), f"Directory {path} is not user-writable."


# ----------------------------------------------------------------------
# 2.  Log files that must already exist with *exact* expected content
# ----------------------------------------------------------------------
EXPECTED_LOG_CONTENT = {
    os.path.join(APP1_DIR, "app1-2023-09-01.log"): [
        "[2023-09-01 12:00:00] INFO  Application started",
        "[2023-09-01 12:05:10] ERROR (E101) Failed to connect to DB",
        "[2023-09-01 12:06:00] INFO  Application stopped",
    ],
    os.path.join(APP1_DIR, "app1-2023-09-15.log"): [
        "[2023-09-15 09:00:00] INFO  Application started",
        "[2023-09-15 09:15:27] ERROR (E202) Timeout while processing",
        "[2023-09-15 10:00:00] ERROR (E101) Failed to connect to DB",
        "[2023-09-15 11:00:00] INFO  Application stopped",
    ],
    os.path.join(APP2_DIR, "app2-2023-09-10.log"): [
        "[2023-09-10 08:00:00] INFO  Start",
        "[2023-09-10 08:05:00] ERROR (E303) Disk full",
        "[2023-09-10 08:06:00] INFO  End",
    ],
    os.path.join(APP2_DIR, "app2-2023-09-18.log"): [
        "[2023-09-18 07:00:00] INFO  Start",
        "[2023-09-18 07:30:00] ERROR (E202) Timeout while processing",
        "[2023-09-18 08:00:00] INFO  End",
    ],
}

@pytest.mark.parametrize("log_path,expected_lines", EXPECTED_LOG_CONTENT.items())
def test_log_files_present_and_correct(log_path, expected_lines):
    assert os.path.isfile(log_path), f"Expected log file {log_path} is missing."

    with open(log_path, encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh.readlines()]

    assert lines == expected_lines, (
        f"Content mismatch in {log_path}.\n"
        f"Expected:\n{expected_lines}\n\nActual:\n{lines}"
    )


# ----------------------------------------------------------------------
# 3.  Things that must *not* exist yet (student will create them)
# ----------------------------------------------------------------------
def test_archive_directory_not_yet_present():
    archive_dir = os.path.join(HOME, "archive")
    assert not os.path.exists(archive_dir), (
        f"{archive_dir} should NOT exist at the start of the exercise."
    )

def test_tarball_not_yet_present():
    tarball = os.path.join(HOME, "archive", "old-logs.tar.gz")
    assert not os.path.exists(tarball), (
        f"Tarball {tarball} should NOT exist before the exercise begins."
    )

def test_summary_file_not_yet_present():
    summary_file = os.path.join(LOG_ROOT, "error_summary_20230920.txt")
    assert not os.path.exists(summary_file), (
        f"Summary file {summary_file} must not exist before the exercise."
    )