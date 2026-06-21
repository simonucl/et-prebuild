# test_initial_state.py
#
# This test-suite verifies the *initial* operating-system / filesystem
# state before the student performs any actions for “incident 42”.
#
# It checks that:
#   1. The configuration directory and file exist.
#   2. The configuration file has the exact, unmodified contents
#      expected at the start of the exercise.
#   3. The incident_fixes directory exists and is completely empty
#      (no patch, log, or any other files yet).
#
# NOTE:  In accordance with the grading-infrastructure guidelines, this
#        suite does *not* look for the eventual output artifacts
#        (patch file, log file, etc.); it only validates the starting
#        conditions.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
CONF_DIR = HOME / "app" / "conf"
CONF_FILE = CONF_DIR / "app.conf"
FIXES_DIR = HOME / "incident_fixes"

EXPECTED_CONF_CONTENT = (
    "# Application configuration\n"
    "TIMEOUT=30\n"
    "LOG_LEVEL=WARN\n"
    "ENABLE_CACHE=true\n"
)


@pytest.mark.describe("Initial configuration directory structure")
def test_conf_directory_exists_and_permissions():
    assert CONF_DIR.is_dir(), (
        f"Expected directory {CONF_DIR} to exist, but it does not."
    )
    # Optional: ensure directory is accessible (0755) – no hard failure on exact mode.
    mode = CONF_DIR.stat().st_mode & 0o777
    assert mode & 0o400, f"Directory {CONF_DIR} is not readable (mode {oct(mode)})"


@pytest.mark.describe("Initial configuration file presence and contents")
def test_app_conf_exists_and_exact_content():
    assert CONF_FILE.is_file(), (
        f"Expected file {CONF_FILE} to exist, but it does not."
    )

    with CONF_FILE.open("r", encoding="utf-8", newline="") as fp:
        actual = fp.read()

    assert actual == EXPECTED_CONF_CONTENT, (
        f"The contents of {CONF_FILE} are not in the expected initial state.\n"
        f"Expected:\n{EXPECTED_CONF_CONTENT!r}\n"
        f"Actual:\n{actual!r}"
    )


@pytest.mark.describe("Incident fixes work area")
def test_incident_fixes_directory_exists_and_is_empty():
    assert FIXES_DIR.is_dir(), (
        f"Expected directory {FIXES_DIR} to exist, but it does not."
    )

    extraneous_items = list(FIXES_DIR.iterdir())
    assert (
        not extraneous_items
    ), (
        f"{FIXES_DIR} is expected to be empty at the start of the exercise, "
        f"but it contains: {', '.join(map(str, extraneous_items))}"
    )