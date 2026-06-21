# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system /
# filesystem before the student starts working on the task described in the
# prompt.  If any of these assertions fail, the environment is not clean and
# the exercise should not proceed.
#
# Only stdlib and pytest are used, as required.

import os
import pytest

PROJECT_DIR = "/home/user/project"
DB_PATH = os.path.join(PROJECT_DIR, "project_files.db")
CSV_PATH = os.path.join(PROJECT_DIR, "file_inventory.csv")


def _human_path(p: str) -> str:
    """Small helper to make assertion messages read nicely."""
    return f"“{p}”"


def test_project_directory_clean_state():
    """
    The project directory should either not exist at all or, if it does exist,
    it must *not* already contain the artefacts that the student is expected to
    create (database or CSV).  This ensures the student begins with a clean
    slate and cannot accidentally pass the exercise due to pre-existing files.
    """
    # 1. project_files.db must NOT exist yet
    assert not os.path.exists(
        DB_PATH
    ), (
        f"The SQLite database {_human_path(DB_PATH)} already exists. "
        "The student must create it themselves; please remove it from the "
        "starter repository."
    )

    # 2. file_inventory.csv must NOT exist yet
    assert not os.path.exists(
        CSV_PATH
    ), (
        f"The CSV export file {_human_path(CSV_PATH)} already exists. "
        "The student must create it; please remove it from the starter "
        "repository."
    )

    # 3. If the containing directory exists, it must not already contain
    #    any file that the student is supposed to create.
    if os.path.isdir(PROJECT_DIR):
        # Gather any unexpected contents for a helpful failure message.
        offending = [
            name
            for name in os.listdir(PROJECT_DIR)
            if name in {"project_files.db", "file_inventory.csv"}
        ]
        assert not offending, (
            f"The directory {_human_path(PROJECT_DIR)} already contains "
            f"unexpected files: {', '.join(offending)}."
        )
    else:
        # Directory absence is perfectly fine (the student will create it).
        assert not os.path.exists(PROJECT_DIR), (
            f"Expected either no directory at {_human_path(PROJECT_DIR)} "
            "or a clean one; found something else."
        )