# test_initial_state.py
"""
Pytest suite that validates the *initial* operating-system / filesystem state
BEFORE the student performs any work on the task “tiny local artifact
catalogue in SQLite”.

The checks purposefully assert that none of the artefacts that the student will
eventually have to create are present yet.  If any of them already exist, we
fail fast with a clear error message so that the exercise starts from a clean,
predictable baseline.

Only the Python standard-library and pytest are used, as required.
"""

from pathlib import Path
import pytest


# ---------- Paths that must NOT exist in the initial state -------------------

CATALOG_DIR = Path("/home/user/build_artifacts")
DB_FILE = CATALOG_DIR / "artifacts.db"
CSV_FILE = CATALOG_DIR / "builds_report.csv"
SQL_LOG = CATALOG_DIR / "sql_commands.log"


@pytest.mark.parametrize(
    "path, description",
    [
        (CATALOG_DIR, "directory /home/user/build_artifacts"),
        (DB_FILE, "SQLite database file /home/user/build_artifacts/artifacts.db"),
        (CSV_FILE, "CSV report /home/user/build_artifacts/builds_report.csv"),
        (SQL_LOG, "SQL log /home/user/build_artifacts/sql_commands.log"),
    ],
)
def test_path_does_not_exist_yet(path: Path, description: str):
    """
    Ensure that none of the target artefacts/directories are present at the
    very beginning.  The student is expected to create them during the task.
    """
    assert not path.exists(), (
        f"The {description} already exists at the start of the exercise.\n"
        f"Please remove it so the task can be performed from scratch."
    )