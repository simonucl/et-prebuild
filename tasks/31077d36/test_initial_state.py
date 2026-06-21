# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that
# must exist **before** the learner creates the required symbolic link
# and verification file described in the exercise.
#
# It purposely FAILS if the post–exercise artefacts are already
# present, because that would indicate the environment is not in the
# expected starting state.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "helpdesk" / "logs"
AUDIT_FILE = LOG_DIR / "2023-Sept-Audit.log"
SYMLINK_PATH = LOG_DIR / "latest.log"
STATUS_FILE = LOG_DIR / "symlink_status.txt"


def test_logs_directory_exists():
    """The /home/user/helpdesk/logs directory must exist."""
    assert LOG_DIR.exists(), (
        "Required directory {!r} is missing.".format(str(LOG_DIR))
    )
    assert LOG_DIR.is_dir(), (
        "{!r} exists but is not a directory.".format(str(LOG_DIR))
    )


def test_audit_log_file_exists_with_expected_content():
    """The audit log file must exist and contain the two expected lines."""
    assert AUDIT_FILE.exists(), (
        "Required audit log file {!r} is missing.".format(str(AUDIT_FILE))
    )
    assert AUDIT_FILE.is_file(), (
        "{!r} exists but is not a regular file.".format(str(AUDIT_FILE))
    )

    expected_lines = [
        "2023-09-01 00:00:01 Start of audit\n",
        "2023-09-01 00:05:47 Audit completed\n",
    ]
    with AUDIT_FILE.open("r", encoding="utf-8") as fh:
        content = fh.readlines()

    assert content == expected_lines, (
        f"File {AUDIT_FILE} does not contain the expected content.\n"
        f"Expected:\n{''.join(expected_lines)}\n"
        f"Actual:\n{''.join(content)}"
    )


def test_latest_log_symlink_is_absent_or_incorrect():
    """
    The symbolic link 'latest.log' should NOT exist yet, or at least
    should not already be a correct symlink to the audit log.

    If the correct symlink is already present, the pre-exercise state is
    wrong and the test must fail.
    """
    if not SYMLINK_PATH.exists() and not SYMLINK_PATH.is_symlink():
        # Ideal: link truly absent.
        return

    # If it *does* exist, ensure it's *not* already the desired link.
    if SYMLINK_PATH.is_symlink():
        resolved = Path(os.path.realpath(SYMLINK_PATH))
        if resolved == AUDIT_FILE:
            pytest.fail(
                f"Pre-exercise symlink {SYMLINK_PATH} already points to "
                f"{resolved}; it should be missing before the learner starts."
            )
    # Any existing path here is considered incorrect for the initial state.
    # Simply assert True so the test passes if it's an incorrect leftover.
    assert True


def test_status_file_does_not_exist():
    """The verification file must not exist before the exercise."""
    assert not STATUS_FILE.exists(), (
        f"Pre-exercise file {STATUS_FILE} already exists; "
        "it must be created by the learner."
    )