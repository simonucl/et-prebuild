# test_initial_state.py
#
# This pytest suite validates the initial state of the execution environment
# *before* the student attempts the task of producing /home/user/uk-time.log.
#
# Expectations for the pristine state:
#   1. The home directory /home/user must exist.
#   2. The target file /home/user/uk-time.log must NOT exist yet.
#   3. The Python standard-library time-zone database must be able to load
#      Europe/London and yield either “BST” or “GMT” as its abbreviation.
#
# Only stdlib + pytest are used, in accordance with the specification.

import os
import datetime

import pytest


HOME_DIR = "/home/user"
LOG_FILE = os.path.join(HOME_DIR, "uk-time.log")
TZ_NAME = "Europe/London"


def test_home_directory_exists():
    """
    The base home directory must already be present.  If this fails, something
    is fundamentally wrong with the test runner's file-system layout.
    """
    assert os.path.isdir(HOME_DIR), (
        f"Expected home directory '{HOME_DIR}' to exist, "
        "but it is missing."
    )


def test_uk_time_log_absent_initially():
    """
    The student has not yet run their command, so the log file should not exist.
    """
    assert not os.path.exists(LOG_FILE), (
        f"The file '{LOG_FILE}' already exists. "
        "It should be created only by the student's one-liner."
    )


def test_europe_london_timezone_available():
    """
    Confirm that Python's stdlib time-zone support can load Europe/London and
    that its current abbreviation is one of the two accepted values (BST/GMT).
    """
    # zoneinfo is available from Python 3.9 onward.
    try:
        from zoneinfo import ZoneInfo
    except ImportError:
        pytest.skip(
            "The 'zoneinfo' module is not available in this Python version; "
            "skipping the Europe/London time-zone availability check."
        )

    try:
        tz = ZoneInfo(TZ_NAME)
    except Exception as exc:
        pytest.fail(
            f"Python could not load the time-zone '{TZ_NAME}' via zoneinfo: {exc}"
        )

    now = datetime.datetime.now(tz)
    abbreviation = now.tzname()
    assert abbreviation in {"BST", "GMT"}, (
        f"Timezone '{TZ_NAME}' loaded, but its current abbreviation is "
        f"'{abbreviation}', not 'BST' or 'GMT'."
    )