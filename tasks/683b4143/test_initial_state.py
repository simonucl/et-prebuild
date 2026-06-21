# test_initial_state.py
#
# This pytest suite validates that the workspace is **clean** before the
# student performs any of the prescribed actions.  None of the artefacts
# that the final grader will later look for should exist at this point.
#
# If any of these tests fail, it means the environment was not in the
# expected pristine state prior to the student’s work.

import os
import pytest
from pathlib import Path

# Base paths that the later tasks will populate
HOME_DIR = Path("/home/user")
QA_DIR = HOME_DIR / "qa_tests"
DB_DIR = QA_DIR / "db"

DB_FILE = DB_DIR / "test_env.db"
SEED_FILE = DB_DIR / "test_env_seed.sql"
LOG_FILE = DB_DIR / "verification.log"

@pytest.mark.parametrize(
    "path",
    [
        pytest.param(DB_DIR, id="workspace directory /home/user/qa_tests/db"),
        pytest.param(DB_FILE, id="SQLite database file test_env.db"),
        pytest.param(SEED_FILE, id="SQL dump file test_env_seed.sql"),
        pytest.param(LOG_FILE, id="verification log file"),
    ],
)
def test_artifacts_absent(path):
    """
    Ensure that none of the directories or files the student is supposed
    to create already exist.  A pre-existing artefact would invalidate
    the clean-room assumption of the exercise.
    """
    assert not path.exists(), (
        f"Unexpected existing artefact found at {path}. "
        "The workspace must start empty so the student can create it."
    )