# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the operating system /
# filesystem that the student is expected to start from.  It deliberately
# avoids checking for any files that the student is supposed to create
# during the exercise (e.g. error_2021-09-15.log or analysis.txt).
#
# The tests will fail with clear, actionable messages if the provided
# environment does not match the specification in the task description.

import os
import stat
import textwrap
import pytest
from pathlib import Path

# Absolute paths that must exist before the student begins.
LOG_DIR = Path("/home/user/logs")
APP_LOG = LOG_DIR / "app.log"


@pytest.fixture(scope="module")
def expected_app_log_content():
    """
    The exact content that /home/user/logs/app.log must contain *before*
    the student performs any commands.
    Every line ends with a single '\n'.
    """
    content = textwrap.dedent(
        """\
        2021-09-14 10:12:01,234 INFO  [module]  - Started
        2021-09-15 11:01:17,890 ERROR [auth]    - Invalid credentials
        2021-09-15 11:02:00,123 WARN  [auth]    - Slow response
        2021-09-15 11:05:43,456 ERROR [auth]    - User locked out
        2021-09-16 09:15:00,001 ERROR [db]      - Connection lost
        2021-09-15 12:00:00,000 INFO  [module]  - Ended
        2021-09-15 13:15:10,678 ERROR [payment] - Payment failed
        2021-09-15 14:20:30,789 DEBUG [payment] - Debug message
        2021-09-14 15:10:50,987 ERROR [module]  - Unexpected error
        """
    )
    # Re-append the trailing newline that textwrap.dedent strips from the end.
    return content.splitlines(keepends=False)


def test_logs_directory_exists_and_permissions():
    """
    The directory /home/user/logs must already exist and be readable/executable.
    """
    assert LOG_DIR.is_dir(), (
        f"Required directory {LOG_DIR} does not exist. "
        "The instructor should provide it."
    )

    mode = stat.S_IMODE(LOG_DIR.stat().st_mode)
    expected_mode = 0o755
    assert mode == expected_mode, (
        f"Directory {LOG_DIR} exists but has mode {oct(mode)}; "
        f"expected {oct(expected_mode)}."
    )


def test_app_log_exists_and_permissions():
    """
    The file /home/user/logs/app.log must already exist and be readable.
    """
    assert APP_LOG.is_file(), (
        f"Required log file {APP_LOG} does not exist. "
        "The instructor should provide it."
    )

    mode = stat.S_IMODE(APP_LOG.stat().st_mode)
    expected_mode = 0o644
    assert mode == expected_mode, (
        f"File {APP_LOG} exists but has mode {oct(mode)}; "
        f"expected {oct(expected_mode)}."
    )


def test_app_log_content(expected_app_log_content):
    """
    The pre-populated app.log must contain exactly the nine lines specified
    in the task description and nothing more or less.
    """
    with APP_LOG.open("r", encoding="utf-8") as fh:
        file_lines = fh.read().splitlines(keepends=False)

    assert (
        file_lines == expected_app_log_content
    ), textwrap.dedent(
        f"""
        File {APP_LOG} does not contain the expected content.

        Expected ({len(expected_app_log_content)} lines):
        --------------------------------------------------
        {chr(10).join(expected_app_log_content)}
        --------------------------------------------------

        Found ({len(file_lines)} lines):
        --------------------------------------------------
        {chr(10).join(file_lines)}
        --------------------------------------------------
        """
    )