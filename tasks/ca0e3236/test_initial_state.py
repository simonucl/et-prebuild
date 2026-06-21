# test_initial_state.py
#
# This pytest suite verifies that the workspace is in the expected
# *initial* state for the “dotenv + env capture” exercise.
#
# Nothing related to the final solution should exist yet.  In
# particular, the target directory /home/user/db_backup must not
# already contain the two files that the student is later asked to
# create (.env and env_capture.log).  If either file is present (or
# has the final expected contents), the exercise would be rendered
# meaningless, so we fail fast with a clear explanation.

import os
from pathlib import Path

import pytest

BASE_DIR = Path("/home/user/db_backup")
ENV_FILE = BASE_DIR / ".env"
CAPTURE_FILE = BASE_DIR / "env_capture.log"

@pytest.mark.parametrize(
    "path_obj, description",
    [
        (ENV_FILE, ".env file"),
        (CAPTURE_FILE, "env_capture.log file"),
    ],
)
def test_required_files_do_not_exist_yet(path_obj: Path, description: str) -> None:
    """
    Assert that the key artefacts (.env and env_capture.log) are *absent*
    before the student starts the exercise.
    """
    assert not path_obj.exists(), (
        f"The {description} already exists at {path_obj}. "
        "The workspace must start in a clean state so the student can "
        "demonstrate creating it from scratch."
    )