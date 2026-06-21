# test_initial_state.py
"""
Pytest suite to validate the initial operating‐system / filesystem state
*before* the student performs any actions for the FinOps cost-summary task.

This suite checks ONLY the pre-existing artefacts.  It deliberately avoids
asserting anything about the expected output file or its directory, as per the
authoring guidelines.
"""

import os
import pytest

COSTS_INI_PATH = "/home/user/cloud/costs.ini"

# Canonical, whitespace-exact contents of the pre-existing INI file.
EXPECTED_COSTS_INI = """[vm1]
status=active
env=dev
cost=12.34

[db1]
status=inactive
env=dev
cost=5.00

[web1]
status=active
env=staging
cost=20.00

[cache1]
status=active
env=prod
cost=15.50

[queue1]
status=inactive
env=prod
cost=3.00
"""


def test_costs_ini_file_exists_and_is_regular():
    """/home/user/cloud/costs.ini must exist and be a regular file."""
    assert os.path.exists(
        COSTS_INI_PATH
    ), f"Expected '{COSTS_INI_PATH}' to exist, but it does not."
    assert os.path.isfile(
        COSTS_INI_PATH
    ), f"Expected '{COSTS_INI_PATH}' to be a regular file, but it is not."


def test_costs_ini_contents_are_exact():
    """
    The INI file must contain the anticipated canonical data.
    We normalise line endings to '\n' and strip a single trailing newline
    so that trivial EOF newline differences don't trigger a failure.
    """
    with open(COSTS_INI_PATH, "r", encoding="utf-8") as f:
        actual = f.read()

    # Normalise possible Windows line endings to UNIX for comparison.
    actual_normalised = actual.replace("\r\n", "\n").rstrip("\n")
    expected_normalised = EXPECTED_COSTS_INI.rstrip("\n")

    assert (
        actual_normalised == expected_normalised
    ), (
        "Contents of '/home/user/cloud/costs.ini' do not match the expected "
        "initial state.  Please ensure the file has NOT been modified before "
        "running the learner's solution.\n\n"
        "Expected:\n"
        f"{EXPECTED_COSTS_INI}\n\n"
        "Actual:\n"
        f"{actual}"
    )