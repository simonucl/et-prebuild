# test_initial_state.py
#
# Pytest suite to validate the operating-system / filesystem *before*
# the student performs the “Configure shell environment variable for
# incident response” task.
#
# Expectations for a clean starting state:
#
# 1. /home/user/.bashrc MUST exist, but it must *not* already contain the
#    exact export line `export INCIDENT_RESPONDER="active"` as its final
#    (non-empty) line.  The student’s job is to append that line.
#
# 2. /home/user/ir_run.log MUST NOT exist yet.  The student will create
#    this confirmation file later.
#
# Any failure message emitted by these tests should clearly explain what
# pre-existing artefact would incorrectly give the student credit before
# they have done the work.

from pathlib import Path
import pytest

HOME = Path("/home/user")
BASHRC_PATH = HOME / ".bashrc"
LOG_PATH = HOME / "ir_run.log"

EXPECTED_EXPORT_LINE = 'export INCIDENT_RESPONDER="active"'
EXPECTED_LOG_LINE = "INCIDENT_RESPONDER variable configured successfully\n"


def _last_non_empty_line(text: str) -> str:
    """
    Return the last non-empty line in the provided text (stripped of its
    trailing newline).  If every line is empty, return an empty string.
    """
    for line in reversed(text.splitlines()):
        stripped = line.rstrip("\n")
        if stripped:
            return stripped
    return ""


def test_bashrc_exists():
    """
    The responder’s personal Bash start-up file must already be present.
    """
    assert BASHRC_PATH.exists(), (
        f"Expected {BASHRC_PATH} to exist so the student can append to it, "
        "but the file is missing."
    )
    assert BASHRC_PATH.is_file(), f"{BASHRC_PATH} exists but is not a regular file."


def test_bashrc_does_not_already_contain_export():
    """
    The exact export line must *not* yet be the last non-empty line of
    ~/.bashrc.  This ensures the student still needs to perform the task.
    """
    content = BASHRC_PATH.read_text(encoding="utf-8", errors="ignore")
    last_line = _last_non_empty_line(content)
    assert (
        last_line != EXPECTED_EXPORT_LINE
    ), (
        f"{BASHRC_PATH} already ends with the required line:\n"
        f"    {EXPECTED_EXPORT_LINE}\n"
        "The starting state must *not* contain this line so that the "
        "student’s work can be properly evaluated."
    )


def test_ir_run_log_not_present():
    """
    The confirmation log must not exist before the student runs their
    one-liner command.
    """
    assert not LOG_PATH.exists(), (
        f"The confirmation log {LOG_PATH} already exists.  The student is "
        "supposed to create this file; it must be absent in the initial "
        "environment."
    )