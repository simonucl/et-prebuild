# test_initial_state.py
#
# This test-suite validates the *initial* state of the operating system
# *before* the student attempts the task “Schedule Periodic Connectivity-Check
# with a User Cron Job”.
#
# What we verify:
#   • The user crontab (crontab -l) must NOT yet contain the line
#       * * * * * ping -c1 -W 2 8.8.8.8 >> /home/user/connectivity.log 2>&1
#   • We make no assertions about /home/user/connectivity.log or any other
#     output artefacts, in accordance with the grading-infra rules.
#
# If this test fails, it means the environment is not in the pristine state
# expected by the exercise (e.g. somebody already installed the cron job).

import subprocess
import shlex

import pytest

EXPECTED_CRON_LINE = (
    "* * * * * ping -c1 -W 2 8.8.8.8 >> /home/user/connectivity.log 2>&1"
)


def _get_user_crontab_lines():
    """
    Return a list of *uncommented* lines currently present in the user's crontab.
    If the user has no crontab yet, an empty list is returned.
    """
    result = subprocess.run(
        ["crontab", "-l"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Exit status 0: crontab exists.
    # Exit status 1 with "no crontab for": no crontab — treat as empty.
    if result.returncode not in (0, 1):
        pytest.fail(
            f"Unexpected error while reading crontab: {result.stderr or result.stdout}"
        )

    raw_output = result.stdout if result.returncode == 0 else ""
    lines = [
        line.strip()
        for line in raw_output.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    return lines


def test_crontab_does_not_contain_target_line():
    """
    Ensure the target cron entry is NOT present before the student begins.
    """
    lines = _get_user_crontab_lines()
    assert (
        EXPECTED_CRON_LINE not in lines
    ), (
        "The user crontab already contains the target line:\n"
        f"{EXPECTED_CRON_LINE!r}\n"
        "The environment must start without this entry so the student can add it."
    )