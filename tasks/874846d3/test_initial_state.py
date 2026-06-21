# test_initial_state.py
#
# This pytest suite validates that the container is in the **clean**
# initial state expected *before* the student/user performs any work
# on the exercise “tz-locale report”.
#
# Truth we assert here:
#   1.  The working directory /home/user/incident must *not* exist yet.
#   2.  Consequently the report file
#          /home/user/incident/tz_locale_report.log
#       must also be absent.
#   3.  The container’s timezone as reported by
#          date -u +%Z
#       must be the literal string “UTC”.
#   4.  The shell-level locale contained in the LANG environment
#       variable must equal “en_US.UTF-8”.
#
# If any of these checks fail the starting point for the learner is
# wrong and the remainder of the exercise cannot be graded
# reliably, so we fail fast with a clear diagnostic.

import os
import subprocess
import sys
import pytest
from pathlib import Path


HOME = Path("/home/user")
INCIDENT_DIR = HOME / "incident"
REPORT_FILE = INCIDENT_DIR / "tz_locale_report.log"


@pytest.mark.describe("Filesystem must be clean before the student begins")
def test_incident_directory_absent():
    """The directory /home/user/incident must NOT exist at start-up."""
    assert not INCIDENT_DIR.exists(), (
        f"The directory {INCIDENT_DIR} already exists, but the exercise "
        f"expects it to be created by the learner."
    )


def test_report_file_absent():
    """The report file must NOT exist before the learner creates it."""
    assert not REPORT_FILE.exists(), (
        f"The file {REPORT_FILE} already exists, but the exercise "
        f"expects it to be created by the learner."
    )


@pytest.mark.describe("Runtime environment must expose a predictable timezone")
def test_timezone_is_utc():
    """`date -u +%Z` must return the literal string 'UTC'"""
    try:
        tz_output = subprocess.check_output(
            ["date", "-u", "+%Z"],
            text=True,
        ).strip()
    except FileNotFoundError:
        pytest.fail(
            "The `date` command is not available in the container. "
            "It is required to verify the timezone."
        )
    assert tz_output == "UTC", (
        "The container’s UTC timezone expectation failed: "
        f"`date -u +%Z` returned {tz_output!r} instead of 'UTC'."
    )


@pytest.mark.describe("Runtime environment must expose a predictable locale")
def test_lang_env_is_en_us_utf8():
    """The LANG environment variable must be exactly 'en_US.UTF-8'."""
    lang = os.environ.get("LANG")
    assert lang == "en_US.UTF-8", (
        "The LANG environment variable must be 'en_US.UTF-8' for the "
        "automated checks to work, but the current value is "
        f"{lang!r}."
    )