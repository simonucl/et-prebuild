# test_initial_state.py
#
# This pytest suite verifies the initial state of the operating system /
# filesystem *before* the student’s solution is executed.
#
# It checks only the pre-existing objects that the task description claims
# must already be present.  Output artefacts such as
# “/home/user/diagnostics/diag_report.txt” are deliberately **not** touched
# here because they do **not** exist yet and are produced by the student’s
# code.

import os
import re
import configparser
import pytest

HOME = "/home/user"
APP_LOGS_DIR = os.path.join(HOME, "app_logs")
APP_LOG_FILE = os.path.join(APP_LOGS_DIR, "app.log")
CONFIG_FILE = os.path.join(APP_LOGS_DIR, "config.ini")

# The 10 lines that must already exist at the *start* of app.log
EXPECTED_FIRST_TEN_LINES = [
    "2023-03-01 10:00:00 INFO Service started\n",
    "2023-03-01 10:05:00 WARN Cache miss\n",
    "2023-03-01 10:10:00 ERROR Connection timeout\n",
    "2023-03-01 10:15:00 INFO Retrying...\n",
    "2023-03-01 10:20:00 INFO Connected\n",
    "2023-03-01 10:25:00 INFO Health check OK\n",
    "2023-03-01 10:30:00 WARN Slow response\n",
    "2023-03-01 10:35:00 INFO Cleanup initiated\n",
    "2023-03-01 10:40:00 INFO Cleanup finished\n",
    "2023-03-01 10:45:00 INFO Service running\n",
]

TIMESTAMP_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2} "          # YYYY-MM-DD
    r"\d{2}:\d{2}:\d{2} "           # HH:MM:SS
    r"(INFO|WARN|ERROR) "           # log level
)

@pytest.fixture(scope="module")
def app_log_lines():
    """Read the entire app.log file and return its lines."""
    if not os.path.isfile(APP_LOG_FILE):
        pytest.fail(f"Required log file missing: {APP_LOG_FILE}")
    with open(APP_LOG_FILE, "r", encoding="utf-8") as f:
        return f.readlines()


def test_app_logs_directory_exists():
    assert os.path.isdir(APP_LOGS_DIR), (
        f"Expected directory {APP_LOGS_DIR} does not exist. "
        "The task states this directory must be present before execution."
    )


def test_app_log_has_minimum_lines(app_log_lines):
    assert len(app_log_lines) >= 10, (
        f"{APP_LOG_FILE} must contain at least 10 lines, "
        f"but only {len(app_log_lines)} lines were found."
    )


def test_app_log_first_ten_lines_exact(app_log_lines):
    # Compare only the first 10 lines against the expected canonical content.
    actual_first_ten = app_log_lines[:10]
    assert actual_first_ten == EXPECTED_FIRST_TEN_LINES, (
        "The first 10 lines of app.log do not match the expected initial "
        "contents.\n\n"
        "Expected:\n"
        + "".join(EXPECTED_FIRST_TEN_LINES)
        + "\nActual:\n"
        + "".join(actual_first_ten)
    )


def test_app_log_line_format(app_log_lines):
    # Quickly sanity-check that every line present follows the timestamp format.
    for lineno, line in enumerate(app_log_lines, 1):
        assert TIMESTAMP_RE.match(line), (
            f"Line {lineno} in {APP_LOG_FILE!r} is not in the expected "
            "timestamped log format:\n"
            f"    {line!r}"
        )


def test_config_ini_exists():
    assert os.path.isfile(CONFIG_FILE), (
        f"Required config file missing: {CONFIG_FILE}"
    )


def test_config_ini_version_value():
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_FILE, encoding="utf-8")

    assert "general" in cfg, (
        f"The section [general] is missing from {CONFIG_FILE}."
    )
    assert "version" in cfg["general"], (
        f"The key 'version' is missing under [general] in {CONFIG_FILE}."
    )
    version_value = cfg["general"]["version"].strip()
    assert version_value == "2.4.7", (
        f"Expected version '2.4.7' in {CONFIG_FILE} "
        f"but found '{version_value}'."
    )