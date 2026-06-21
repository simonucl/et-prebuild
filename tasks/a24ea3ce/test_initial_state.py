# test_initial_state.py
#
# This pytest suite verifies that the system starts in the expected
# *initial* state ­— i.e. **before** the student performs any of the
# required actions.  It ensures that only the legacy SQL script is
# present and that no “optimized” artefacts or directories exist yet.
#
# NOTE: If any test in this file fails, the exercise environment is
#       broken *before* the student even begins, so the student must
#       not be penalised; rather, the template image must be fixed.

import os
from pathlib import Path

import pytest

# -----------------------------------------------------------------------------
# Constants describing the required initial state
# -----------------------------------------------------------------------------
ORIGINAL_SQL_PATH = Path("/home/user/projects/sql_work/original.sql")
OPTIMIZED_DIR = Path("/home/user/projects/sql_work/optimized")
OPTIMIZED_SQL_PATH = OPTIMIZED_DIR / "optimized.sql"
CHECKSUMS_PATH = OPTIMIZED_DIR / "checksums.sha256"
REPORT_PATH = OPTIMIZED_DIR / "optimization_report.log"

EXPECTED_ORIGINAL_SQL_CONTENT = (
    "-- original.sql\n"
    "CREATE TABLE employees (\n"
    "    id INT PRIMARY KEY,\n"
    "    name TEXT,\n"
    "    department TEXT\n"
    ");\n"
    "\n"
    "SELECT * FROM employees WHERE department = 'Engineering';\n"
)


# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
def _read_text(path: Path) -> str:
    """Read a text file in UTF-8, raising a helpful error if it cannot be read."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Required file is missing: {path}")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {path}: {exc}")


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_original_sql_exists_with_expected_content():
    """
    The legacy file /home/user/projects/sql_work/original.sql must exist and
    its byte-for-byte content must match what the exercise description states.
    """
    assert ORIGINAL_SQL_PATH.is_file(), (
        "Pre-existing SQL script is missing: "
        f"{ORIGINAL_SQL_PATH}.  The exercise template is corrupted."
    )

    actual = _read_text(ORIGINAL_SQL_PATH)
    assert actual == EXPECTED_ORIGINAL_SQL_CONTENT, (
        "The content of original.sql does not match the expected initial "
        "state.  The template file seems to have been altered."
    )


def test_optimized_directory_is_absent():
    """
    Before the student starts, the directory /home/user/projects/sql_work/optimized
    must NOT exist.  Its presence would indicate that the environment is dirty.
    """
    assert not OPTIMIZED_DIR.exists(), (
        f"Directory {OPTIMIZED_DIR} already exists. "
        "The initial environment must be clean."
    )


@pytest.mark.parametrize(
    "path",
    [
        OPTIMIZED_SQL_PATH,
        CHECKSUMS_PATH,
        REPORT_PATH,
    ],
)
def test_no_optimized_artifacts_exist(path: Path):
    """
    No artefacts from the optimisation task should be present yet.
    """
    assert not path.exists(), (
        f"Found unexpected artefact: {path}. "
        "The environment should not contain any files created by the student yet."
    )