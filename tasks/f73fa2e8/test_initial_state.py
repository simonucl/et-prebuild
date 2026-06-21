# test_initial_state.py
#
# Pytest suite that validates the _initial_ state of the operating system
# before the student carries out the deployment task described in the
# assignment.  The required artefacts (database directory, SQLite file and
# log file) **must not exist yet**.  If any of them are already present,
# the environment is considered polluted and the test will fail with a
# clear, actionable message.
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import pytest

# Base paths used throughout the assignment
HOME = Path("/home/user")
DEPLOYMENT_DIR = HOME / "deployment"
DB_DIR = DEPLOYMENT_DIR / "db"
DB_FILE = DB_DIR / "versioning.db"
LOG_FILE = DEPLOYMENT_DIR / "release_check.log"


@pytest.mark.parametrize(
    "path, description",
    [
        (DB_DIR, "directory '/home/user/deployment/db'"),
        (DB_FILE, "SQLite database '/home/user/deployment/db/versioning.db'"),
        (LOG_FILE, "log file '/home/user/deployment/release_check.log'"),
    ],
)
def test_required_artefacts_do_not_exist_yet(path: Path, description: str):
    """
    Ensure that none of the artefacts expected after successful completion
    of the task are present _before_ the student starts working.

    If any of these objects already exist, it means the workspace has been
    pre-populated or left over from a previous run, which would invalidate
    the assessment.
    """
    assert not path.exists(), (
        f"Unexpected {description} already exists at {path}. "
        "The workspace must start empty so the student's work can be "
        "evaluated accurately."
    )