# test_initial_state.py
#
# Pytest suite that validates the initial (pre-task) state of the
# operating-system environment for the “Berlin time-zone / German locale”
# exercise.  The student has NOT yet modified any files, so
# 1.  /home/user/.bashrc must NOT already end with the two required
#     export statements in the exact spelling and order given.
# 2.  /home/user/output/time_check.txt must NOT yet exist with the final
#     byte-for-byte correct content.
#
# If either of the above is already true, the tests will FAIL with a clear
# explanation so the template image can be fixed before being handed to
# students.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
BASHRC = HOME / ".bashrc"
OUTPUT_FILE = HOME / "output" / "time_check.txt"

# Exact text that must *eventually* be present, but must NOT be there yet.
EXPECTED_BASHRC_TAIL = (
    'export TZ="Europe/Berlin"\n'
    'export LC_TIME="de_DE.UTF-8"\n'
)
EXPECTED_TIME_CHECK_CONTENT = (
    "2023-08-05 14:30:00 | 2023-08-05 16:30:00 CEST\n"
    "2023-12-25 09:15:00 | 2023-12-25 10:15:00 CET\n"
)


def test_bashrc_not_already_patched():
    """
    The two export lines must NOT yet be present as an exact, final,
    consecutive tail of /home/user/.bashrc.
    """
    if not BASHRC.exists():
        # File absent → perfectly fine for the initial state.
        return

    content = BASHRC.read_bytes()
    if content.endswith(EXPECTED_BASHRC_TAIL.encode()):
        pytest.fail(
            f"{BASHRC} already ends with the two required export lines; "
            "the starting image must *not* contain the final solution."
        )


def test_helper_file_not_already_present():
    """
    The helper file must NOT already exist with the exact expected
    content.  It may be absent or have different content; both are valid
    initial states.
    """
    if not OUTPUT_FILE.exists():
        # Not created yet → correct initial state.
        return

    # It exists; ensure it is *not* already correct.
    actual_content = OUTPUT_FILE.read_text(encoding="utf-8", errors="replace")
    if actual_content == EXPECTED_TIME_CHECK_CONTENT:
        pytest.fail(
            f"{OUTPUT_FILE} already exists with the final expected content; "
            "the starting image must *not* contain the final solution file."
        )