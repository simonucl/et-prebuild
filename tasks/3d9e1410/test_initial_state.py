# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student performs any actions for the “update_report.csv” task.
#
# What is verified:
#   1. Presence and *exact* contents of the two requirement files.
#   2. Absence of the target report file and its containing directory.
#
# Only stdlib and pytest are used.

from pathlib import Path
import pytest

HOME = Path("/home/user")
APP_DIR = HOME / "app"
OLD_REQ = APP_DIR / "requirements_old.txt"
NEW_REQ = APP_DIR / "requirements_new.txt"
LOG_DIR = HOME / "update_logs"
REPORT_CSV = LOG_DIR / "update_report.csv"


EXPECTED_OLD_CONTENT = (
    "requests==2.25.0\n"
    "numpy==1.18.0\n"
    "pandas==1.1.0\n"
)

EXPECTED_NEW_CONTENT = (
    "requests==2.31.0\n"
    "numpy==1.24.0\n"
    "pandas==2.0.3\n"
)


def _read_file(path: Path) -> str:
    """Return file content or raise a clear assertion error if missing."""
    assert path.exists(), f"Expected file {path} to exist but it does not."
    assert path.is_file(), f"Expected {path} to be a regular file."
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")


def test_requirement_files_exist_with_correct_content():
    """
    The two requirement files must exist with the exact lines specified
    in the task description, including terminating newlines.
    """
    old_content = _read_file(OLD_REQ)
    new_content = _read_file(NEW_REQ)

    assert (
        old_content == EXPECTED_OLD_CONTENT
    ), (
        f"{OLD_REQ} does not contain the expected contents.\n"
        "Expected:\n"
        f"{EXPECTED_OLD_CONTENT!r}\n"
        "Found:\n"
        f"{old_content!r}"
    )

    assert (
        new_content == EXPECTED_NEW_CONTENT
    ), (
        f"{NEW_REQ} does not contain the expected contents.\n"
        "Expected:\n"
        f"{EXPECTED_NEW_CONTENT!r}\n"
        "Found:\n"
        f"{new_content!r}"
    )


def test_update_logs_directory_absent_initially():
    """
    The directory /home/user/update_logs should *not* exist before
    the student runs their solution; it will be created by them.
    """
    assert not LOG_DIR.exists(), (
        f"Directory {LOG_DIR} already exists, but it should be absent "
        "before the student performs the task."
    )


def test_update_report_csv_absent_initially():
    """
    The report CSV must *not* be present at the start; it is created
    by the student's script.
    """
    assert not REPORT_CSV.exists(), (
        f"File {REPORT_CSV} already exists, but it should be absent "
        "before the student performs the task."
    )