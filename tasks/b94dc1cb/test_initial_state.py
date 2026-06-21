# test_initial_state.py
#
# This pytest suite verifies that the operating-system state is clean
# *before* the student performs the exercise.
#
# IMPORTANT:  We intentionally do **not** test for the presence or absence
#             of any artefacts that the student is expected to create
#             (e.g. /home/user/profiling or env_check.log), in accordance
#             with the grading-system rules.

import os
from pathlib import Path
import pytest


def test_home_directory_exists():
    """
    The baseline expectation is that the canonical home directory for the
    student account is present and is a directory.  If this is missing, all
    subsequent instructions are guaranteed to fail, so we check it first.
    """
    home = Path("/home/user")

    assert home.exists(), (
        "The directory /home/user does not exist. A valid home directory is "
        "required before the exercise can be attempted."
    )
    assert home.is_dir(), (
        "/home/user exists but is not a directory. Please ensure the home "
        "directory is correctly set up."
    )


def test_app_profiling_env_var_not_pre_set():
    """
    The exercise requires the student to *introduce* an APP_PROFILING
    environment variable.  Verify that it is not already set to a truthy
    value; otherwise the task would be a no-op and would mask user errors.
    """
    current_value = os.environ.get("APP_PROFILING")

    assert current_value in (None, "", "0"), (
        "The environment variable APP_PROFILING is already present in the "
        "current session with value {!r}. It must be unset (or set to an "
        "empty string/0) before the student runs their one-line command."
    ).format(current_value)