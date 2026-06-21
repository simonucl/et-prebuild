# test_initial_state.py
#
# This pytest suite validates the **initial** operating-system / filesystem
# state before the student carries out any steps for the “profiling
# environment variables” exercise.
#
# It deliberately checks that:
#
# 1.  The required output files are **absent**.
# 2.  The required environment variables are **not yet** set to their target
#     values.
#
# If any of these assertions fail, it means the playground is already “dirty”
# and cannot be trusted to test the student’s forthcoming work.

import os
import pytest

# Absolute paths to the artefacts that must *not* exist yet.
ENV_FILE = "/home/user/.config/profiling/.env"
LOG_FILE = "/home/user/profiling_env.log"

@pytest.mark.parametrize("path", [ENV_FILE, LOG_FILE])
def test_output_files_absent(path):
    """
    Neither the dotenv file nor the demonstration log file should exist
    before the student starts the task.
    """
    assert not os.path.exists(path), (
        f"Pre-task sanity check failed: '{path}' already exists. "
        "The workspace must start clean so the student can create it."
    )

def test_environment_variables_not_set():
    """
    APP_MODE and PROFILER_PORT should *not* yet have the final required
    values in the current process environment.
    """
    env = os.environ
    assert env.get("APP_MODE") != "profiling", (
        "Pre-task sanity check failed: environment variable APP_MODE is "
        "already set to 'profiling'. It should be unset or have a "
        "different value at the start of the exercise."
    )
    assert env.get("PROFILER_PORT") != "6060", (
        "Pre-task sanity check failed: environment variable PROFILER_PORT is "
        "already set to '6060'. It should be unset or have a different "
        "value at the start of the exercise."
    )