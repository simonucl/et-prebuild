# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem is in the
# expected *initial* state ­before the student performs any actions for the
# “Post-greSQL client settings” task.
#
# The tests deliberately assert the *absence* of the configuration lines in
# /home/user/.bashrc and the non-existence of the log file
# /home/user/db_env_config.log.  If any of these artefacts are already present,
# the environment is not pristine and the tests will fail with a clear message.
#
# Only Python’s standard library and pytest are used, as required.

import os
import pytest

HOME = "/home/user"
BASHRC_PATH = os.path.join(HOME, ".bashrc")
LOG_PATH = os.path.join(HOME, "db_env_config.log")

PGTZ_LINE = "export PGTZ='UTC'"
PGOPTIONS_LINE = (
    "export PGOPTIONS='--client-min-messages=warning -c default_statistics_target=500'"
)


@pytest.fixture(scope="module")
def bashrc_contents():
    """
    Read the current contents of ~/.bashrc, if the file exists.
    Returns an empty string if the file does not exist.
    """
    if os.path.isfile(BASHRC_PATH):
        with open(BASHRC_PATH, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return ""


def test_bashrc_does_not_contain_pgtz_line(bashrc_contents):
    """
    ~/.bashrc must NOT yet contain the export PGTZ line.
    """
    assert PGTZ_LINE not in bashrc_contents, (
        f"The file {BASHRC_PATH} already contains the line:\n"
        f"    {PGTZ_LINE}\n"
        "The environment is not in the required initial state."
    )


def test_bashrc_does_not_contain_pgoptions_line(bashrc_contents):
    """
    ~/.bashrc must NOT yet contain the export PGOPTIONS line.
    """
    assert PGOPTIONS_LINE not in bashrc_contents, (
        f"The file {BASHRC_PATH} already contains the line:\n"
        f"    {PGOPTIONS_LINE}\n"
        "The environment is not in the required initial state."
    )


def test_log_file_does_not_exist_yet():
    """
    The log file /home/user/db_env_config.log must NOT exist at the start.
    """
    assert not os.path.exists(LOG_PATH), (
        f"The log file {LOG_PATH} already exists.\n"
        "It should be absent in the initial state."
    )