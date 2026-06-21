# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem
# starts from a clean slate *before* the student performs any action
# for the “nightly preprocessing” exercise.
#
# What we assert about the initial state:
#   1.  /home/user/ml-data/logs/  MUST NOT exist yet.
#   2.  /home/user/ml-data/preprocess.sh  MUST NOT exist yet.
#   3.  The user’s crontab MUST NOT already contain the required cron line.
#
# If any of these conditions are violated, the tests fail with a clear,
# actionable message.  Only Python’s standard library and pytest are used.

import subprocess
from pathlib import Path
import pytest


LOGS_DIR = Path("/home/user/ml-data/logs")
SCRIPT_PATH = Path("/home/user/ml-data/preprocess.sh")
EXPECTED_CRON_LINE = (
    "30 2 * * * /home/user/ml-data/preprocess.sh "
    ">> /home/user/ml-data/logs/preprocess.log 2>&1"
)


def _current_crontab() -> str:
    """
    Return the current user's crontab as text.
    If no crontab exists, return an empty string.
    """
    proc = subprocess.run(
        ["crontab", "-l"],
        text=True,
        capture_output=True,
    )
    # According to `crontab -l` semantics, exit status 0 means the
    # crontab was printed; any non-zero (usually 1) means “no crontab for user”.
    return proc.stdout if proc.returncode == 0 else ""


def test_logs_directory_absent():
    assert not LOGS_DIR.exists(), (
        f"Directory {LOGS_DIR} already exists, but it should NOT be present "
        "before the student starts the task."
    )


def test_preprocess_script_absent():
    assert not SCRIPT_PATH.exists(), (
        f"File {SCRIPT_PATH} already exists, but it should NOT be present "
        "before the student creates it."
    )


def test_crontab_clean():
    crontab_txt = _current_crontab()
    assert EXPECTED_CRON_LINE not in crontab_txt, (
        "The user's crontab already contains the required cron entry:\n"
        f"    {EXPECTED_CRON_LINE}\n"
        "The initial state should *not* include this line."
    )

    # Also be kind and tell the student if *any* crontab lines exist,
    # as that could interfere with later checks.
    if crontab_txt.strip():
        pytest.skip(
            "The user already has other cron jobs configured. "
            "While not strictly forbidden, be aware that only the required "
            "entry should remain after the task is completed."
        )