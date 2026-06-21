# test_initial_state.py
#
# This Pytest suite verifies that the workspace is still *clean* before
# the student performs any action for the “artifact-manager” task.
# Nothing related to the assignment must exist yet.
#
# The tests purposefully FAIL if any of the required end-state artefacts
# (directory, database, or report files) are already present.

from pathlib import Path
import pytest

HOME = Path("/home/user")
ARTIFACTS_DIR = HOME / "artifacts"

DB_FILE = ARTIFACTS_DIR / "repository.db"
REPORT_FILE = ARTIFACTS_DIR / "binary_tag_report.txt"
SCHEMA_DUMP = ARTIFACTS_DIR / "repository_schema.sql"


@pytest.mark.parametrize(
    "path, kind",
    [
        (ARTIFACTS_DIR, "directory"),
        (DB_FILE, "file"),
        (REPORT_FILE, "file"),
        (SCHEMA_DUMP, "file"),
    ],
)
def test_assignment_paths_do_not_exist_yet(path: Path, kind: str) -> None:
    """
    BEFORE the student starts, none of the assignment artefacts should exist.

    The test fails early with a helpful error message if it finds any of the
    paths already present, guaranteeing that the workspace starts from a
    pristine state.
    """
    assert not path.exists(), (
        f"⚠️  The {kind} '{path}' already exists, but the workspace is expected "
        f"to be clean at the beginning of the task.  Remove it before starting."
    )