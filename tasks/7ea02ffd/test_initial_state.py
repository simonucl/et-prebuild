# test_initial_state.py
#
# This test-suite validates the *initial* filesystem / OS state before the
# student performs any action.  It asserts the existence, permissions and
# exact contents of the legacy SQL utility scripts located under
#     /home/user/query_scripts
#
# DO NOT modify this file.  If any of the assertions below fail it means that
# the starting environment is not in the expected pristine state and the
# real assignment cannot be graded reliably.
#
# IMPORTANT:  The tests deliberately *avoid* touching or asserting anything
# about files that are supposed to be **generated** by the student (e.g.
# `refactor.log`).  Only the pre-existing artefacts are verified here.

import os
import stat
import glob
import textwrap

import pytest


BASE_DIR = "/home/user/query_scripts"

EXPECTED_FILES = {
    "get_users.sql": textwrap.dedent(
        """\
        SELECT * FROM users WHERE active = 1;
        -- some comment
        """
    ),
    "get_orders.sql": textwrap.dedent(
        """\
        SELECT id, total FROM orders;
        """
    ),
    "update_users.sql": textwrap.dedent(
        """\
        UPDATE users SET active = 0 WHERE last_login < '2023-01-01';
        """
    ),
    "archive_customers.sql": textwrap.dedent(
        """\
        SELECT * FROM customers WHERE archived = 0;
        """
    ),
    "delete_tmp.sql": textwrap.dedent(
        """\
        SELECT * FROM tmp_data;
        """
    ),
}

FILES_WITH_SELECT_STAR = {
    "get_users.sql",
    "archive_customers.sql",
    "delete_tmp.sql",
}

DIR_PERMS = 0o755
FILE_PERMS = 0o644


def _oct_permissions(path: str) -> int:
    """
    Return the permission bits (e.g. 0o755) for a file or directory.
    """
    return stat.S_IMODE(os.stat(path).st_mode)


def test_directory_exists_and_permissions():
    assert os.path.isdir(BASE_DIR), (
        f"Directory {BASE_DIR} is missing.  The initial SQL script directory "
        f"must exist before the exercise starts."
    )
    perms = _oct_permissions(BASE_DIR)
    assert perms == DIR_PERMS, (
        f"Directory {BASE_DIR} must have permissions {oct(DIR_PERMS)}, "
        f"but has {oct(perms)}."
    )


def test_expected_files_present_with_correct_permissions():
    present_files = {os.path.basename(p) for p in glob.glob(os.path.join(BASE_DIR, "*.sql"))}
    expected_files = set(EXPECTED_FILES.keys())

    # 1. Exactly the expected set of .sql files must be present
    assert present_files == expected_files, (
        "Unexpected set of .sql files in the directory.\n"
        f"Expected: {sorted(expected_files)}\n"
        f"Found   : {sorted(present_files)}"
    )

    # 2. Every file must have the correct permissions
    for fname in expected_files:
        fpath = os.path.join(BASE_DIR, fname)
        perms = _oct_permissions(fpath)
        assert perms == FILE_PERMS, (
            f"File {fpath} must have permissions {oct(FILE_PERMS)}, "
            f"but has {oct(perms)}."
        )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_FILES.items())
def test_file_contents_match_expected_template(filename, expected_content):
    """
    The initial contents of every SQL file must exactly match the specification
    (ignoring a single trailing newline that editors sometimes add).
    """
    fpath = os.path.join(BASE_DIR, filename)
    with open(fpath, "r", encoding="utf-8") as fp:
        actual = fp.read()

    # Normalise trailing newlines for comparison
    actual_stripped = actual.rstrip("\n")
    expected_stripped = expected_content.rstrip("\n")

    assert actual_stripped == expected_stripped, (
        f"Contents of {fpath} differ from the expected initial state.\n\n"
        f"Expected:\n{expected_stripped!r}\n\nActual:\n{actual_stripped!r}"
    )


def test_select_star_occurs_only_in_expected_files():
    """
    Initially the non-performant pattern 'SELECT *' should be present in exactly
    three specific files and in *no* others.
    """
    offending_files = []

    for fpath in glob.glob(os.path.join(BASE_DIR, "*.sql")):
        with open(fpath, "r", encoding="utf-8") as fp:
            content = fp.read()
        if "SELECT *" in content:
            offending_files.append(os.path.basename(fpath))

    offending_set = set(offending_files)
    assert offending_set == FILES_WITH_SELECT_STAR, (
        "The pattern 'SELECT *' must exist in exactly the following files "
        f"before the refactor: {sorted(FILES_WITH_SELECT_STAR)}.\n"
        f"Currently found in: {sorted(offending_set)}"
    )


def test_no_refactor_log_preexisting():
    """
    The refactor.log file is produced *after* the student runs their command,
    therefore it must not exist in the pristine environment.
    """
    log_path = os.path.join(BASE_DIR, "refactor.log")
    assert not os.path.exists(log_path), (
        f"{log_path} already exists, but it should be created only after the "
        "student executes the required commands."
    )