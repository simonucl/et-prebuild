# test_initial_state.py
#
# This test-suite verifies that the starting file-system state is exactly
# what the exercise description promises *before* the student performs any
# action.  If any of these tests fail, it means the environment was not
# prepared correctly and the follow-up grading would be unreliable.
#
# The suite checks:
#   • Directory layout (/home/user/cloud_migration/…)
#   • Presence (and absence) of files/directories
#   • Byte-for-byte contents of the four *.log files
#   • That the reports/ directory (and its artefacts) do **not** exist yet
#
# Only stdlib and pytest are used, in compliance with the guidelines.

from pathlib import Path
import pytest

BASE_DIR = Path("/home/user/cloud_migration")
LOG_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"

# --------------------------------------------------------------------------- #
# Expected log contents (byte-for-byte, including the final trailing newline)
# --------------------------------------------------------------------------- #
expected_logs = {
    LOG_DIR / "auth-service_20231015.log": (
        "[2023-10-15 10:00:01] auth-service mig-001 SUCCESS 450\n"
        "[2023-10-15 10:05:22] auth-service mig-002 FAILED 300\n"
        "[2023-10-15 10:15:10] auth-service mig-003 SUCCESS 500\n"
    ).encode(),
    LOG_DIR / "payment-service_20231015.log": (
        "[2023-10-15 10:01:30] payment-service mig-010 SUCCESS 800\n"
        "[2023-10-15 10:07:45] payment-service mig-011 SUCCESS 750\n"
        "[2023-10-15 10:11:05] payment-service mig-012 FAILED 900\n"
        "[2023-10-15 10:12:55] payment-service mig-013 FAILED 880\n"
    ).encode(),
    LOG_DIR / "auth-service_20231016.log": (
        "[2023-10-16 11:00:11] auth-service mig-004 SUCCESS 460\n"
        "[2023-10-16 11:05:55] auth-service mig-005 FAILED 350\n"
    ).encode(),
    LOG_DIR / "payment-service_20231016.log": (
        "[2023-10-16 11:02:01] payment-service mig-014 SUCCESS 780\n"
    ).encode(),
}


# --------------------------------------------------------------------------- #
# Helper assertions
# --------------------------------------------------------------------------- #
def _assert_path_is_dir(path: Path):
    assert path.exists(), f"Expected directory {path} to exist, but it is missing."
    assert path.is_dir(), f"Expected {path} to be a directory, but it is not."


def _assert_path_is_file(path: Path):
    assert path.exists(), f"Expected file {path} to exist, but it is missing."
    assert path.is_file(), f"Expected {path} to be a regular file, but it is not."


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_directory_structure():
    """Verify base and log directories exist; reports/ must not exist yet."""
    _assert_path_is_dir(BASE_DIR)
    _assert_path_is_dir(LOG_DIR)

    # The reports directory should *not* exist yet.
    assert not REPORTS_DIR.exists(), (
        f"{REPORTS_DIR} should not exist before the student runs their solution."
    )


def test_log_files_presence_and_exclusivity():
    """The logs/ directory must contain exactly the four expected files."""
    for logfile in expected_logs:
        _assert_path_is_file(logfile)

    # Ensure there are no unexpected files inside logs/
    unexpected = [p for p in LOG_DIR.iterdir() if p.is_file() and p not in expected_logs]
    assert (
        not unexpected
    ), f"Found unexpected file(s) in {LOG_DIR}: {', '.join(map(str, unexpected))}"


@pytest.mark.parametrize("log_path, expected_bytes", list(expected_logs.items()))
def test_log_file_contents(log_path: Path, expected_bytes: bytes):
    """Each log file must match the byte-for-byte reference content."""
    actual_bytes = log_path.read_bytes()
    assert (
        actual_bytes == expected_bytes
    ), f"Contents of {log_path} do not match what the exercise specifies."


def test_no_pre_existing_report_files():
    """Ensure that no report artefacts are already present."""
    forbidden_paths = [
        REPORTS_DIR / "migration_summary.csv",
        REPORTS_DIR / "failed_migrations.log",
        REPORTS_DIR / "analysis.log",
    ]
    pre_existing = [p for p in forbidden_paths if p.exists()]
    assert (
        not pre_existing
    ), "The following report artefact(s) already exist but should not: " + ", ".join(
        map(str, pre_existing)
    )