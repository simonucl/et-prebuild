# test_initial_state.py
#
# This pytest file validates the *initial* state of the system
# before the student carries out any instructions.  It asserts that
# no pre-existing capacity-planning artefacts are present so that the
# exercise starts from a clean slate.

import os
import pytest

# Constants used throughout the tests
REPORT_DIR = "/home/user/capacity_planning"
REPORT_FILE = os.path.join(REPORT_DIR, "report.log")


def _is_regular_file(path: str) -> bool:
    """Return True only if *path* exists and is a regular file."""
    try:
        return os.path.isfile(path)
    except Exception:  # pragma: no cover
        # In the unlikely event of permission errors or other OS issues,
        # treat it as "not a regular file" and let the assertion below fail.
        return False


def test_report_directory_may_exist_but_is_not_required():
    """
    The directory /home/user/capacity_planning is expected to be absent,
    but if it *does* exist, that's acceptable.  The key requirement is that
    no report.log file exists yet.
    """
    # Directory is optional; no assertion needed on its existence.
    # This test exists mainly to provide a clear explanation if the report
    # file is already present even though the student has not run anything.
    if os.path.isdir(REPORT_DIR):
        # Directory exists—fine.  Make sure it's not world-writable to avoid
        # accidental tampering before the exercise begins.
        mode = os.stat(REPORT_DIR).st_mode & 0o777
        assert mode & 0o002 == 0, (
            f"The directory {REPORT_DIR} is world-writable (mode {oct(mode)}). "
            "Please secure it or start from a pristine environment."
        )
    else:
        # Directory is absent, which is perfectly normal for the start state.
        assert not os.path.exists(REPORT_DIR), (
            f"{REPORT_DIR} exists but is not a directory—unexpected initial state."
        )


def test_report_log_must_not_exist_initially():
    """
    No pre-existing report.log should be present.  The exercise requires the
    student to create it from scratch, so its prior existence is a failure.
    """
    assert not _is_regular_file(REPORT_FILE), (
        f"The file {REPORT_FILE} already exists. "
        "The exercise must begin with no report present."
    )
    # If a path exists at REPORT_FILE but is NOT a regular file (e.g., a
    # directory or symlink), that is also incorrect for the initial state.
    assert not os.path.exists(REPORT_FILE), (
        f"A filesystem object already exists at {REPORT_FILE}. "
        "Please remove or rename it before starting the task."
    )