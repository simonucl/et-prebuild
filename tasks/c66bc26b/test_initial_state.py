# test_initial_state.py
#
# This test suite validates the *initial* state of the OS / filesystem
# before the student begins their work.  It confirms that the source log
# file exists and contains the exact five lines that the subsequent task
# description relies upon.
#
# IMPORTANT:  Per the grading-framework rules we **do not** check for
# any of the output artefacts (e.g. /home/user/filtered or
# /home/user/filtered/modified_only.log).  Only the pre-existing
# conditions are verified here.

import pathlib
import pytest

CONFIG_LOG = pathlib.Path("/home/user/config_changes.log")

_EXPECTED_LINES = [
    "2024-01-15 10:12:03 CONFIG: /etc/ssh/sshd_config status=UNCHANGED "
    "checksum=b1946ac92492d2347c6235b4d2611184\n",
    "2024-01-15 10:12:04 CONFIG: /etc/ssh/sshd_config status=MODIFIED "
    "checksum=87acec17cd9dcd20a716cc2cf67417b71c8a7016\n",
    "2024-01-15 10:12:05 CONFIG: /etc/nginx/nginx.conf status=MODIFIED "
    "checksum=3b5d5c3712955042212316173ccf37be\n",
    "2024-01-15 10:12:06 CONFIG: /etc/passwd status=CREATED "
    "checksum=764efa883dda1e11db47671c4a3bbd9e\n",
    "2024-01-15 10:12:07 CONFIG: /etc/nginx/nginx.conf status=UNCHANGED "
    "checksum=cb837b763cf375a3530d9cf68bbee585\n",
]

@pytest.mark.describe("Initial OS state validation")
def test_config_changes_log_exists_and_is_correct():
    # 1. File exists and is a regular file
    assert CONFIG_LOG.exists(), (
        f"Required log file missing: {CONFIG_LOG}. "
        "The starting environment must provide this file."
    )
    assert CONFIG_LOG.is_file(), (
        f"Expected {CONFIG_LOG} to be a regular file, "
        "but it is not."
    )

    # 2. File contents are exactly as specified
    actual_lines = CONFIG_LOG.read_text(encoding="utf-8").splitlines(keepends=True)

    # Helpful diff in assertion message if mismatch occurs
    assert actual_lines == _EXPECTED_LINES, (
        "The contents of /home/user/config_changes.log do not match the "
        "expected initial state.\n"
        "Expected:\n"
        + "".join(_EXPECTED_LINES)
        + "\nActual:\n"
        + "".join(actual_lines)
    )