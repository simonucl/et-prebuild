# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state *before* the
# student attempts the exercise.  It checks only the pre-existing resources
# and explicitly avoids testing for any files that are supposed to be created
# by the student (e.g., /home/user/docs/index.json).

import os
import pwd
import pytest

DOCS_DIR = "/home/user/docs"
CSV_PATH = os.path.join(DOCS_DIR, "index.csv")


def test_docs_directory_exists_and_writable():
    """
    The directory /home/user/docs must exist and be writable by the current user.
    """
    assert os.path.isdir(DOCS_DIR), (
        f"Required directory {DOCS_DIR!r} is missing."
    )

    # Current effective UID
    euid = os.geteuid()
    # os.access with W_OK checks writability for the current process
    assert os.access(DOCS_DIR, os.W_OK), (
        f"Directory {DOCS_DIR!r} is not writable by user "
        f"{pwd.getpwuid(euid).pw_name!r} (uid={euid})."
    )


def test_index_csv_exists_with_expected_contents():
    """
    The file /home/user/docs/index.csv must exist and contain exactly the
    expected CSV data (including line order and spelling).
    """
    assert os.path.isfile(CSV_PATH), (
        f"Required file {CSV_PATH!r} is missing."
    )

    expected_content = (
        "id,title,section\n"
        "1,Introduction,Getting Started\n"
        "2,Installation,Getting Started\n"
        "3,Configuration,Advanced Topics\n"
        "4,FAQ,Appendix\n"
    )

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        actual_content = f.read()

    # A helpful diff-style assertion message if contents differ
    assert actual_content == expected_content, (
        "The file /home/user/docs/index.csv does not contain the expected "
        "data.\n\nExpected:\n"
        f"{expected_content!r}\n\nActual:\n{actual_content!r}"
    )