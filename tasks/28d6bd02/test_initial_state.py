# test_initial_state.py
#
# This test-suite verifies that the workspace is **clean** before the
# student starts the exercise.  In particular, we make sure that none of
# the deliverables that the student is supposed to create already exist.
#
# Expected initial state:
#   • /home/user/projects/doc_site/docs.db           does NOT exist
#     – If it does exist, it must NOT already contain a table called
#       `doc_pages`.
#   • /home/user/projects/doc_site/reports/draft_pages.log
#     does NOT exist.
#
# These checks guarantee that the student begins with a blank slate and
# that any artefacts found after execution were indeed created by them.
#
# Only stdlib and pytest are used, as required.

import os
import sqlite3
import stat
import pytest

BASE_DIR = "/home/user/projects/doc_site"
DB_PATH = os.path.join(BASE_DIR, "docs.db")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
REPORT_FILE = os.path.join(REPORT_DIR, "draft_pages.log")


def _is_world_readable(path: str) -> bool:
    """Return True if 'path' is world-readable (unix mode 0o4 for 'others')."""
    try:
        return bool(os.stat(path).st_mode & stat.S_IROTH)
    except FileNotFoundError:
        return False


def test_database_absent_or_clean():
    """
    The SQLite database file must not exist yet.  If it does for some
    reason, it must not already contain a table named `doc_pages`, as
    that is exactly what the student will create.
    """
    if not os.path.exists(DB_PATH):
        # Ideal clean state: file is not present.
        assert True
        return

    # The file exists; inspect its contents for safety.
    msg_prefix = (
        f"Unexpected pre-existing database at {DB_PATH!r}. "
        "The exercise requires the student to create this file, "
        "so it must be absent OR at least not already contain the "
        "`doc_pages` table."
    )
    try:
        conn = sqlite3.connect(DB_PATH)
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"{msg_prefix}  Additionally, opening the DB failed: {exc}")

    cur = conn.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name='doc_pages';"
    )
    table_row = cur.fetchone()
    conn.close()

    assert (
        table_row is None
    ), f"{msg_prefix}  Table 'doc_pages' is already present—environment is not clean."


def test_report_file_absent():
    """
    The final report should not exist before the student runs any
    commands; its presence would indicate that the environment is dirty.
    """
    assert not os.path.exists(
        REPORT_FILE
    ), (
        f"Found unexpected file {REPORT_FILE!r}. "
        "The student is supposed to generate this report; "
        "please start them with a clean slate."
    )


def test_reports_directory_permissions_if_present():
    """
    If the reports directory already exists (it normally shouldn't),
    verify that it is accessible by the current non-root user.  This
    ensures the student can write the required file.
    """
    if not os.path.isdir(REPORT_DIR):
        pytest.skip("Reports directory does not yet exist — that is OK for a clean state.")

    # Directory exists; check that it is world-readable/executable so the
    # student can access it.  (Mode 0o755 or similar.)
    mode = os.stat(REPORT_DIR).st_mode
    assert mode & stat.S_IROTH, (
        f"Directory {REPORT_DIR!r} exists but is not world-readable. "
        "Please ensure it has at least 0o755 permissions so the student "
        "can create files inside it."
    )
    assert mode & stat.S_IXOTH, (
        f"Directory {REPORT_DIR!r} exists but is not world-executable. "
        "Without the execute bit, the student cannot traverse the path."
    )