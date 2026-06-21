# test_initial_state.py
#
# This pytest suite validates **the initial state of the operating system**
# BEFORE the student performs any actions for the “fixed time-zone and locale”
# exercise.  It deliberately **fails** if any part of the _final_ expected
# solution is already present.
#
# Checked conditions:
#   1. The project directory /home/user/project must NOT yet exist.
#   2. The verification log file /home/user/project/time_locale_config.log
#      must NOT yet exist.
#   3. /home/user/.bashrc must exist, and its last two non-blank lines must
#      NOT already be the required export statements.
#
# Only stdlib and pytest are used.

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user").expanduser()
PROJECT_DIR = HOME / "project"
LOG_FILE = PROJECT_DIR / "time_locale_config.log"
BASHRC = HOME / ".bashrc"

EXPECTED_EXPORT_LINES = [
    'export TZ="America/New_York"',
    'export LC_ALL="en_US.UTF-8"',
]


def _last_non_blank_lines(path: pathlib.Path, count: int):
    """
    Return the last <count> non-blank lines of the file at *path*.
    Lines are stripped of the trailing newline and any surrounding
    whitespace on either end.
    """
    with path.open("r", encoding="utf-8", errors="ignore") as fh:
        # Read small chunks from the end would be nice, but file sizes are tiny.
        lines = [ln.rstrip("\n").strip() for ln in fh.readlines()]
        non_blank = [ln for ln in lines if ln]
        return non_blank[-count:] if len(non_blank) >= count else non_blank


@pytest.mark.describe("Initial filesystem state – project directory and log file")
def test_project_directory_and_log_file_absent():
    # Directory must not yet exist
    assert not PROJECT_DIR.exists(), (
        f"Directory {PROJECT_DIR} already exists, but it should be created "
        "by the student as part of the task."
    )

    # Log file must not yet exist
    assert not LOG_FILE.exists(), (
        f"Verification log {LOG_FILE} already exists. "
        "The student should create it only after finishing the configuration."
    )


@pytest.mark.describe("Initial filesystem state – bashrc not yet configured")
def test_bashrc_not_already_configured():
    # Ensure ~/.bashrc exists (a standard Ubuntu user should have one).
    assert BASHRC.exists(), (
        f"Expected to find {BASHRC}, but it does not exist. "
        "A default bashrc should be present before the task starts."
    )

    # Fetch the last two non-blank lines of .bashrc
    last_two = _last_non_blank_lines(BASHRC, 2)

    # They must not already be the required export statements
    assert last_two != EXPECTED_EXPORT_LINES, (
        ".bashrc already ends with the required export statements:\n"
        f"  {last_two[0] if last_two else '<none>'}\n"
        f"  {last_two[1] if len(last_two) > 1 else '<none>'}\n"
        "This should not be the case before the student performs the task."
    )