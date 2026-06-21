# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state
# before the student performs any actions.  It checks that:
#   1. /home/user/app/logs exists and is a directory.
#   2. That directory contains exactly three log files:
#        - app.log
#        - db.log
#        - access.log
#   3. app.log and db.log each contain at least one line with
#      the literal string "ERROR" and, more specifically, the
#      expected counts (3 and 2 respectively).
#   4. access.log contains zero lines with "ERROR".
#   5. The incidents directory (/home/user/incidents or any
#      sub-directory such as /home/user/incidents/2023-07-30)
#      does NOT yet exist.
#
# Only stdlib + pytest are used.

from pathlib import Path

LOG_DIR = Path("/home/user/app/logs")
INCIDENTS_DIR = Path("/home/user/incidents")
INCIDENTS_DAY_DIR = INCIDENTS_DIR / "2023-07-30"

EXPECTED_LOG_FILES = {"app.log", "db.log", "access.log"}
EXPECTED_ERROR_COUNTS = {
    "app.log": 3,
    "db.log": 2,
    "access.log": 0,
}


def _count_error_lines(file_path: Path) -> int:
    """Return the number of lines containing the literal string 'ERROR'."""
    with file_path.open(encoding="utf-8") as f:
        return sum(1 for line in f if "ERROR" in line)


def test_logs_directory_exists():
    assert LOG_DIR.exists(), f"Expected directory {LOG_DIR} to exist."
    assert LOG_DIR.is_dir(), f"Expected {LOG_DIR} to be a directory."


def test_logs_directory_contents():
    files_present = {p.name for p in LOG_DIR.iterdir() if p.is_file()}
    missing = EXPECTED_LOG_FILES - files_present
    extra = files_present - EXPECTED_LOG_FILES

    assert not missing, (
        "Missing expected log file(s): "
        + ", ".join(sorted(missing))
    )
    assert not extra, (
        "Found unexpected file(s) in log directory: "
        + ", ".join(sorted(extra))
    )


def test_error_counts_in_each_log():
    for filename, expected_count in EXPECTED_ERROR_COUNTS.items():
        file_path = LOG_DIR / filename
        assert file_path.exists(), f"Expected log file {file_path} to exist."
        assert file_path.is_file(), f"{file_path} should be a regular file."

        actual_count = _count_error_lines(file_path)
        assert (
            actual_count == expected_count
        ), (
            f"{file_path} should contain {expected_count} lines with "
            f'\"ERROR\", but found {actual_count}.'
        )


def test_incidents_directory_not_yet_present():
    assert not INCIDENTS_DIR.exists(), (
        f"{INCIDENTS_DIR} should NOT exist before the student runs the solution."
    )
    assert not INCIDENTS_DAY_DIR.exists(), (
        f"{INCIDENTS_DAY_DIR} should NOT exist before the student runs the solution."
    )