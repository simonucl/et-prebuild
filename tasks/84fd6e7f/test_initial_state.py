# test_initial_state.py
#
# This pytest suite validates that the workstation is in a **clean**
# state before the learner begins the exercise.  It checks that:
#
# 1. The dotenv file `/home/user/.env.train` does **not** yet exist.
# 2. The log directory `/home/user/data_prep/` and the log file
#    `/home/user/data_prep/preparation.log` do **not** yet exist.
# 3. The three required environment variables are **not** pre-set
#    in the current environment.
#
# If any of these checks fail, the accompanying assertion message
# tells the learner exactly what is out of place.

import os
from pathlib import Path
import pytest


DOTENV_PATH = Path("/home/user/.env.train")
LOG_DIR = Path("/home/user/data_prep")
LOG_FILE = LOG_DIR / "preparation.log"

REQUIRED_VARS = (
    "DATASET_NAME",
    "RAW_DATA_DIR",
    "PROCESSED_DATA_DIR",
)


def test_dotenv_file_does_not_exist():
    """
    The dotenv file must *not* exist before the student creates it.
    """
    assert not DOTENV_PATH.exists(), (
        f"Found unexpected dotenv file at {DOTENV_PATH}. "
        "Please start from a clean state (remove or rename the file) "
        "before proceeding with the exercise."
    )


def test_log_file_does_not_exist():
    """
    Neither the log file nor its parent directory should exist yet.
    """
    assert not LOG_FILE.exists(), (
        f"Found unexpected log file at {LOG_FILE}. "
        "Please remove it so the exercise can create it afresh."
    )

    # The directory may or may not exist, but if it does,
    # ensure it is empty so the learner starts clean.
    if LOG_DIR.exists():
        assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."
        contents = list(LOG_DIR.iterdir())
        assert not contents, (
            f"The directory {LOG_DIR} should be empty before the exercise "
            f"begins, but it contains: {', '.join(map(str, contents))}"
        )


@pytest.mark.parametrize("var_name", REQUIRED_VARS)
def test_environment_variables_not_pre_set(var_name):
    """
    The required variables should not be globally set yet; the learner
    will load them from the dotenv file during the task.
    """
    assert var_name not in os.environ, (
        f"Environment variable '{var_name}' is already set. "
        "Unset it (or start a fresh shell) so the exercise can confirm "
        "that the learner's commands load it correctly."
    )