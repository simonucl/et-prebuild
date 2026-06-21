# test_initial_state.py
#
# This pytest file validates the **initial** filesystem / operating-system
# state that must be present *before* the student begins the incident
# triage task.  If any of these tests fail, the exercise environment is
# not correctly provisioned.
#
# Only the Python standard library and pytest are used.

import gzip
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
LOG_DIR = HOME / "logs"
ARCHIVE_DIR = LOG_DIR / "archive"

SYS01 = LOG_DIR / "sys01-2023-10-15.log"
SYS02 = LOG_DIR / "sys02-2023-10-15.log"
SYS03_GZ = ARCHIVE_DIR / "sys03-2023-10-15.log.gz"

INCIDENT_DIR = HOME / "incident_reports"
SUMMARY_CSV = INCIDENT_DIR / "2023-10-15_error_summary.csv"
RUN_LOG = INCIDENT_DIR / "2023-10-15_run.log"

# Expected contents for each file (order preserved for readability;
# we only assert that each expected line is *present* somewhere in the file).
EXPECTED_SYS01_LINES = [
    "2023-10-15T13:59:59Z [service:billing] ERROR E1024 Card declined for user 000",
    "2023-10-15T14:05:12Z [service:billing] ERROR E1024 Card declined for user 123",
    "2023-10-15T14:07:30Z [service:billing] ERROR E1024 Card declined for user 456",
    "2023-10-15T14:15:50Z [service:checkout] ERROR E2048 Inventory mismatch for product 789",
    "2023-10-15T15:10:00Z [service:checkout] ERROR E2048 Inventory mismatch for product 654",
    "2023-10-15T15:20:17Z [service:search]  ERROR E3001 Search backend timeout",
    "2023-10-15T16:10:00Z [service:billing] ERROR E1024 Card declined for user 321",
]

EXPECTED_SYS02_LINES = [
    "2023-10-15T14:45:00Z [service:billing] ERROR E1024 Card declined for user 789",
    "2023-10-15T14:50:22Z [service:user]    ERROR E5000 Unable to fetch profile",
    "2023-10-15T15:05:36Z [service:user]    ERROR E5000 Unable to fetch profile",
    "2023-10-15T15:22:01Z [service:search]  ERROR E3001 Search backend timeout",
    "2023-10-15T15:45:59Z [service:checkout] ERROR E2048 Inventory mismatch for product 321",
]

EXPECTED_SYS03_LINES = [
    "2023-10-15T14:30:00Z [service:billing] ERROR E1024 Card declined for user 999",
    "2023-10-15T15:12:12Z [service:search]  ERROR E3001 Search backend timeout",
]


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def _read_text_lines(path: Path) -> list[str]:
    """
    Read *all* lines from a text file, stripping the trailing newline.
    """
    return [line.rstrip("\n") for line in path.read_text(encoding="utf-8").splitlines()]


def _read_gzip_text_lines(path: Path) -> list[str]:
    """
    Read *all* lines from a single-member gzip archive containing UTF-8 text.
    """
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh.readlines()]


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------

def test_log_files_exist():
    """Verify that all expected log files are present with correct types."""
    assert SYS01.is_file(), f"Missing log file: {SYS01}"
    assert SYS02.is_file(), f"Missing log file: {SYS02}"
    assert SYS03_GZ.is_file(), f"Missing gzip log file: {SYS03_GZ}"

    # The archive directory must be a directory.
    assert ARCHIVE_DIR.is_dir(), f"Expected directory missing: {ARCHIVE_DIR}"


@pytest.mark.parametrize(
    ("log_path", "expected_lines", "reader"),
    [
        (SYS01, EXPECTED_SYS01_LINES, _read_text_lines),
        (SYS02, EXPECTED_SYS02_LINES, _read_text_lines),
        (SYS03_GZ, EXPECTED_SYS03_LINES, _read_gzip_text_lines),
    ],
)
def test_log_contents(log_path: Path, expected_lines: list[str], reader):
    """
    Ensure that every expected log line is present in its respective file.
    We do not enforce ordering; presence is sufficient.
    """
    content_lines = reader(log_path)

    for expected in expected_lines:
        assert (
            expected in content_lines
        ), f"Expected line not found in {log_path}: `{expected}`"


def test_incident_reports_directory_does_not_exist_yet():
    """
    The incident_reports directory (and its artefacts) should NOT exist prior
    to the student's solution; the student is responsible for creating them.
    """
    assert not INCIDENT_DIR.exists(), (
        "The directory /home/user/incident_reports/ should NOT exist "
        "before the student starts.  It will be created by the student's "
        "solution script."
    )
    # Defensive: if the directory *does* exist, ensure that the artefact files
    # are not already present (prevents the environment from 'accidentally'
    # meeting success criteria before the student acts).
    if INCIDENT_DIR.exists():
        assert not SUMMARY_CSV.exists(), (
            f"Unexpected pre-existing summary CSV: {SUMMARY_CSV}"
        )
        assert not RUN_LOG.exists(), f"Unexpected pre-existing run log: {RUN_LOG}"