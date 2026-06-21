# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state expected **before** the student creates their Makefile‐based CI/CD
# solution.  These checks guarantee that the grading environment starts from
# a clean, known baseline.

import subprocess
from pathlib import Path
import pytest

# Absolute paths that the assignment specification hard-codes.
PROJECT_DIR = Path("/home/user/project")
REPORT_FILE = PROJECT_DIR / "ci_report.txt"


def test_project_directory_present():
    """
    The repository directory must already exist so the student can drop their
    Makefile into it.
    """
    assert PROJECT_DIR.exists(), f"Required directory {PROJECT_DIR} is missing."
    assert PROJECT_DIR.is_dir(), f"{PROJECT_DIR} exists but is not a directory."


def test_ci_report_not_preexisting():
    """
    The output artefact generated *after* running `make ci` must not linger
    from an earlier run.  Starting in a clean state avoids false positives.
    """
    assert not REPORT_FILE.exists(), (
        f"Stale file {REPORT_FILE} should not be present before the Makefile "
        "is created and executed."
    )


def test_gnu_make_available():
    """
    The default Debian/Ubuntu minimal image must provide GNU Make.  The student
    relies on it to drive the CI pipeline.
    """
    try:
        completed = subprocess.run(
            ["make", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
    except FileNotFoundError:  # pragma: no cover
        pytest.fail("'make' binary not found on PATH. GNU Make is required.")

    first_line = completed.stdout.strip().splitlines()[0] if completed.stdout else ""
    assert "GNU Make" in first_line, (
        f"'make --version' did not report GNU Make. First line was: {first_line!r}"
    )