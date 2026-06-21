# test_initial_state.py
"""
Pytest suite that validates the initial filesystem state **before** the student
executes any commands.

The tests check only the prerequisites (inputs) and deliberately avoid
examining any artefacts that the student is supposed to create (e.g.
 /home/user/diagnostics or summary.log).

If any of these tests fail, the grading environment itself is broken and the
student should not be penalised.
"""

import os
from pathlib import Path
import textwrap
import pytest

HOME = Path("/home/user")
LOGS_DIR = HOME / "logs"
CONFIG_DIR = HOME / "config"

SYSTEM_LOG = LOGS_DIR / "system.log"
APP_CONF = CONFIG_DIR / "app.conf"


@pytest.fixture(scope="module")
def expected_log_contents() -> str:
    """Return the canonical contents of /home/user/logs/system.log."""
    return textwrap.dedent(
        """\
        2023-05-01 10:15:23 INFO  Startup complete
        2023-05-01 10:15:24 ERROR [E101] Failed to load module alpha
        2023-05-01 10:15:25 WARN  Low memory
        2023-05-01 10:15:26 ERROR [E102] Connection timeout
        2023-05-01 10:15:27 INFO  Health check passed
        2023-05-01 10:15:28 ERROR [E101] Failed to load module alpha
        2023-05-01 10:15:29 ERROR [E103] Disk full
        """
    )


def test_system_log_exists():
    """Verify the log file exists and is a regular file."""
    assert SYSTEM_LOG.is_file(), (
        f"Required log file {SYSTEM_LOG} is missing.\n"
        "The grading environment is not set up correctly."
    )


def test_system_log_contents(expected_log_contents):
    """
    Verify that /home/user/logs/system.log contains exactly the expected
    seven lines (including newlines).
    """
    actual = SYSTEM_LOG.read_text(encoding="utf-8")
    # Normalise line endings to '\n' only, remove a single trailing newline for comparison
    actual_norm = actual.replace("\r\n", "\n").rstrip("\n")
    expected_norm = expected_log_contents.rstrip("\n")

    assert (
        actual_norm == expected_norm
    ), (
        f"Contents of {SYSTEM_LOG} differ from the expected initial state.\n\n"
        "Expected:\n"
        f"{expected_norm}\n\n"
        "Actual:\n"
        f"{actual_norm}\n"
    )


def test_app_conf_exists():
    """Verify the configuration file exists and is a regular file."""
    assert APP_CONF.is_file(), (
        f"Required configuration file {APP_CONF} is missing.\n"
        "The grading environment is not set up correctly."
    )


def test_app_conf_initial_state():
    """
    The student is expected to uncomment and modify the diagnostics line.
    Prior to that, we must ensure:
      * '#diagnostics=false' exists.
      * 'diagnostics=true' does NOT exist.
    """
    contents = APP_CONF.read_text(encoding="utf-8").splitlines()

    # Check for the commented diagnostics line
    assert any(
        line.strip() == "#diagnostics=false" for line in contents
    ), (
        f"{APP_CONF} does not contain the required line '#diagnostics=false'.\n"
        "Initial configuration is incorrect."
    )

    # Ensure that the line has not already been modified
    assert all(
        line.strip() != "diagnostics=true" for line in contents
    ), (
        f"{APP_CONF} already contains an active 'diagnostics=true' setting.\n"
        "This should only be present after the student's solution runs."
    )