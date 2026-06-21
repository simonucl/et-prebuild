# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system
# before the student carries out the assignment.  If any test in this file
# fails, the environment is not in the expected pristine state and the rest
# of the grading rubric will be unreliable.

import os
import pytest


AUDIT_DIR = "/home/user/audit"
AUDIT_FILE = "/home/user/audit/timezone_locale.log"
TIMEZONE_FILE = "/etc/timezone"
EXPECTED_TIMEZONE_CONTENT = "Etc/UTC"
EXPECTED_LANG = "C.UTF-8"


def test_timezone_file_exists_and_matches_expected():
    """
    The canonical /etc/timezone file must exist and contain the expected
    time-zone string *before* the student begins.  If this test fails the
    grading environment itself is out of spec.
    """
    assert os.path.isfile(TIMEZONE_FILE), (
        f"Required file {TIMEZONE_FILE} is missing. "
        "The grading environment is mis-configured."
    )

    with open(TIMEZONE_FILE, "rt", encoding="utf-8") as fh:
        tz_content = fh.read().rstrip("\n")

    assert tz_content == EXPECTED_TIMEZONE_CONTENT, (
        f"{TIMEZONE_FILE} content mismatch.\n"
        f"Expected: {EXPECTED_TIMEZONE_CONTENT!r}\n"
        f"Found:    {tz_content!r}\n"
        "The grading environment is mis-configured."
    )


def test_lang_environment_variable_matches_expected():
    """
    The LANG environment variable *at test time* must match the documented
    value so that the student can rely on it when producing the output file.
    """
    assert "LANG" in os.environ, (
        "Environment variable LANG is not set; the grading environment is "
        "mis-configured."
    )

    lang_value = os.environ["LANG"]
    assert lang_value == EXPECTED_LANG, (
        f"LANG environment variable mismatch.\n"
        f"Expected: {EXPECTED_LANG!r}\n"
        f"Found:    {lang_value!r}\n"
        "The grading environment is mis-configured."
    )


def test_audit_directory_absent_initially():
    """
    The /home/user/audit directory should NOT exist before the student
    performs the task.  Its presence would indicate that the workspace is
    contaminated by previous runs or manual intervention.
    """
    assert not os.path.exists(AUDIT_DIR), (
        f"Directory {AUDIT_DIR} already exists. "
        "The workspace is not clean; please reset the environment."
    )


def test_audit_file_absent_initially():
    """
    The target output file must not exist before the student creates it.
    """
    assert not os.path.exists(AUDIT_FILE), (
        f"File {AUDIT_FILE} already exists. "
        "The workspace is not clean; please reset the environment."
    )