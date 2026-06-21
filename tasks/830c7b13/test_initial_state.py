# test_initial_state.py
#
# This test-suite validates that the system is in a **clean** state *before*
# the student carries out any actions required by the assignment
# “SQLite provisioning demo”.
#
# Specifically, we assert that none of the artefacts the student is expected
# to create already exist on the filesystem.  A pre-existing directory,
# database or report file would invalidate the exercise and could mask
# implementation errors.
#
# NOTE: These checks purposefully do **not** enforce the *absence* of higher-
# level parent directories such as /home/user or /home/user/provisioning
# because those may be present in the base image for perfectly valid reasons.
#
# Only stdlib + pytest are used, in accordance with the authoring guidelines.

import os
import stat
import pytest
from pathlib import Path


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME_DIR          = Path("/home/user")
PROVISION_DIR     = HOME_DIR / "provisioning"
DB_DIR            = PROVISION_DIR / "db"
DB_FILE           = DB_DIR / "infra.db"
REPORT_FILE       = DB_DIR / "servers_report.log"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _pretty_path(path: Path) -> str:
    """Return a POSIX-style string for error reporting."""
    return str(path)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_db_directory_absent():
    """
    The target directory /home/user/provisioning/db/ must NOT exist yet.

    The assignment requires the student to create this directory themselves.
    A pre-existing directory would invalidate the exercise and potentially
    conceal mistakes (e.g. incorrect permissions).
    """
    assert not DB_DIR.exists(), (
        f"The directory {_pretty_path(DB_DIR)} already exists. "
        "The student is expected to create it during provisioning."
    )


@pytest.mark.parametrize("path_description,path", [
    ("SQLite database file", DB_FILE),
    ("status-report file",   REPORT_FILE),
])
def test_files_absent(path_description, path):
    """
    Neither the SQLite database nor the text report should be present yet.
    """
    assert not path.exists(), (
        f"{path_description} {_pretty_path(path)} already exists. "
        "All artefacts must be created fresh by the student's solution."
    )