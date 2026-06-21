# test_initial_state.py
"""
Pytest suite to verify that the operating-system state *before* the
student starts the exercise is clean.

We deliberately do **not** check for any of the output files or
directories required by the assignment (e.g. “/home/user/network_logs”),
because they are supposed to be created later by the student.  The only
thing we validate is that the user’s crontab does **not** already
contain the exact cron job the student will be asked to add.
"""

import re
import subprocess
from typing import List

import pytest

# Exact cron line the student is expected to add later
CRON_REGEX = re.compile(
    r"^\*/2 \* \* \* \* ping -c 1 127\.0\.0\.1 >> "
    r"/home/user/network_logs/ping\.log 2>&1$"
)


def _get_crontab_lines() -> List[str]:
    """
    Return the current user’s crontab as a list of lines.

    If the user has no crontab, `crontab -l` exits with status 1.
    In that case we treat the crontab as empty.
    """
    result = subprocess.run(
        ["crontab", "-l"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    # `crontab -l` returns exit code 1 and prints a message to stderr
    # when no crontab is installed.  That is not an error for our purposes.
    if result.returncode != 0:
        return []
    return [line.rstrip("\n") for line in result.stdout.splitlines()]


def test_crontab_does_not_already_contain_ping_job():
    """
    Ensure the student’s crontab is free of the specific ping job that
    the exercise instructs them to create.  A pre-existing entry would
    invalidate the starting conditions.
    """
    cron_lines = _get_crontab_lines()
    offending_lines = [ln for ln in cron_lines if CRON_REGEX.match(ln)]

    assert not offending_lines, (
        "The crontab already contains the line the student is supposed "
        "to add: "
        f"{offending_lines[0]!r}.  Please remove it so the exercise starts "
        "from a clean slate."
    )