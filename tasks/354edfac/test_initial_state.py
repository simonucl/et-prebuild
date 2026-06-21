# test_initial_state.py
#
# This test-suite validates the **initial** state of the grading VM
# before the learner carries out any instructions.  It purposefully
# avoids touching or even mentioning any of the paths that the learner
# is expected to create later on (see project rules).
#
# Only stdlib and pytest are used.

import os
import pytest


TIMEZONE_FILE = "/etc/timezone"
EXPECTED_TZ_STRING = "Etc/UTC"


@pytest.mark.describe("Pre-flight check: /etc/timezone")
def test_timezone_file_exists_and_contains_etc_utc():
    """
    1. Verify that /etc/timezone is a regular, readable file.
    2. Verify that its *first* non-empty line (with trailing newline stripped)
       is exactly 'Etc/UTC'.  The trailing newline is tolerated; any other
       content fails the test.
    """
    # 1. File existence & readability -------------------------------------------------
    assert os.path.isfile(
        TIMEZONE_FILE
    ), f"Required file '{TIMEZONE_FILE}' is missing or not a regular file."

    assert os.access(
        TIMEZONE_FILE, os.R_OK
    ), f"Cannot read '{TIMEZONE_FILE}'; check file permissions."

    # 2. Content check ----------------------------------------------------------------
    with open(TIMEZONE_FILE, "r", encoding="utf-8", errors="replace") as fh:
        # Read all lines, strip only newline characters.
        lines = [line.rstrip("\n\r") for line in fh]

    # Filter out any leading blank lines that could exist in rare, mis-configured
    # systems (keeping the check robust while still strict about *content*).
    non_empty_lines = [l for l in lines if l.strip() != ""]

    assert (
        non_empty_lines
    ), f"'{TIMEZONE_FILE}' appears to be empty; expected the string '{EXPECTED_TZ_STRING}'."

    tz_string = non_empty_lines[0]

    assert (
        tz_string == EXPECTED_TZ_STRING
    ), (
        f"Unexpected time-zone string in '{TIMEZONE_FILE}': "
        f"got '{tz_string}', expected '{EXPECTED_TZ_STRING}'.  "
        "Do not modify the system's default time-zone."
    )