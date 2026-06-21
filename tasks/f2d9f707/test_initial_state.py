# test_initial_state.py
#
# This pytest suite validates that the **initial** operating-system state
# matches the specification **before** the student performs any actions.
#
# Rules enforced:
#   * Only standard library + pytest are used.
#   * No checks touch or rely on any of the output files / directories
#     that will be created by the student (/home/user/rotation/*).
#
# What we verify:
#   1. The home directory /home/user exists and is a directory.
#   2. The environment variable TZ is set to “Europe/Berlin”.
#   3. The environment variable LANG is set to “de_DE.UTF-8”.
#
# If any of these conditions are not met, the tests will fail with a clear,
# human-readable explanation so that the learner immediately knows what is
# missing or misconfigured.

import os
import pathlib
import pytest


HOME_PATH = pathlib.Path("/home/user")


def test_home_directory_exists():
    """
    Ensure that the expected home directory is present before any task actions.
    """
    assert HOME_PATH.exists(), (
        f"Expected home directory '{HOME_PATH}' does not exist. "
        "The exercise assumes this directory is present."
    )
    assert HOME_PATH.is_dir(), (
        f"Expected '{HOME_PATH}' to be a directory, but it is not."
    )


@pytest.mark.parametrize(
    ("var_name", "expected_value"),
    [
        ("TZ", "Europe/Berlin"),
        ("LANG", "de_DE.UTF-8"),
    ],
)
def test_initial_environment_variables(var_name, expected_value):
    """
    Verify that the initial shell environment variables match the exercise spec.
    """
    assert var_name in os.environ, (
        f"Environment variable '{var_name}' is not set. "
        f"Expected initial value: '{expected_value}'."
    )

    actual_value = os.environ[var_name]
    assert actual_value == expected_value, (
        f"Environment variable '{var_name}' has value '{actual_value}', "
        f"but the exercise expects the initial value to be '{expected_value}'."
    )