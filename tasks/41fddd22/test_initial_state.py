# test_initial_state.py
#
# This test-suite validates the original filesystem state **before**
# the student runs any commands.  It purposefully does NOT check for the
# presence (or absence) of the artefacts that the student is supposed to
# create later.

import re
from pathlib import Path

import pytest

# --- Constants ----------------------------------------------------------------

HOME = Path("/home/user")
BACKUP_DIR = HOME / "backup"
LOGS_DIR = BACKUP_DIR / "logs"
REPORTS_DIR = BACKUP_DIR / "reports"
LOG_FILE = LOGS_DIR / "backup_2023-09-15.log"

# Ground-truth of the pre-existing log file (lines include the trailing '\n').
EXPECTED_LOG_LINES = [
    "2023-09-15 02:10:34 [INFO] Backup started\n",
    "2023-09-15 02:12:11 [OK] file: /var/data/db1.sql (checksum=ae34bc...)\n",
    "2023-09-15 02:12:15 [ERROR] FILE_MISSING /var/data/config.yml\n",
    "2023-09-15 02:12:16 [OK] file: /var/data/report.pdf (checksum=5b9a7d...)\n",
    "2023-09-15 02:12:20 [WARNING] CHECKSUM_MISMATCH /var/data/image.png\n",
    "2023-09-15 02:12:25 [OK] file: /var/data/archive.tar.gz (checksum=9d4e8f...)\n",
    "2023-09-15 02:12:35 [ERROR] FILE_MISSING /var/data/old_backup.tar.gz\n",
    "2023-09-15 02:13:10 [INFO] Backup finished: duration=2m36s\n",
]

# The lines that the student will be asked to extract later.
PROBLEM_LINES = [
    EXPECTED_LOG_LINES[2],
    EXPECTED_LOG_LINES[4],
    EXPECTED_LOG_LINES[6],
]

# --- Helper -------------------------------------------------------------------


def read_logfile_lines(path: Path):
    """Return the logfile lines *including* trailing newlines."""
    # Binary read keeps exact newline chars untouched.
    raw_bytes = path.read_bytes()
    # splitlines(True) keeps the trailing newline in each element.
    return raw_bytes.splitlines(keepends=True)


def find_problem_lines(lines):
    """Return lines that should be considered problematic."""
    pattern = re.compile(r"\[(ERROR|WARNING)]\s+(FILE_MISSING|CHECKSUM_MISMATCH)\b")
    return [ln for ln in lines if pattern.search(ln)]


# --- Tests --------------------------------------------------------------------


def test_required_directories_exist():
    assert BACKUP_DIR.is_dir(), f"Missing directory: {BACKUP_DIR}"
    assert LOGS_DIR.is_dir(), f"Missing directory: {LOGS_DIR}"
    assert REPORTS_DIR.is_dir(), (
        "The reports directory should exist before the student starts: "
        f"expected directory {REPORTS_DIR!s}"
    )


def test_log_file_exists_and_is_regular_file():
    assert LOG_FILE.exists(), f"Missing logfile: {LOG_FILE}"
    assert LOG_FILE.is_file(), f"Expected {LOG_FILE} to be a regular file, not a directory."


def test_log_file_exact_contents():
    actual_lines_bytes = read_logfile_lines(LOG_FILE)
    # Convert bytes -> str (utf-8); strict so that decoding errors surface.
    actual_lines = [ln.decode("utf-8") for ln in actual_lines_bytes]

    # Helpful diff on failure.
    assert (
        actual_lines == EXPECTED_LOG_LINES
    ), "Log file contents differ from the expected pre-exercise state."


def test_problem_line_detection_logic_matches_ground_truth():
    """Sanity check that the problem-line regex finds exactly the expected lines."""
    lines = read_logfile_lines(LOG_FILE)
    # Decode to str once for regex search
    lines = [ln.decode("utf-8") for ln in lines]
    detected = find_problem_lines(lines)

    assert detected == PROBLEM_LINES, (
        "The set of lines that qualify as 'problematic' in the initial state "
        "does not match the exercise description.\n"
        f"Expected ({len(PROBLEM_LINES)}):\n{''.join(PROBLEM_LINES)}\n"
        f"Found ({len(detected)}):\n{''.join(detected)}"
    )