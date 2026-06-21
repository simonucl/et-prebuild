# test_initial_state.py
#
# This pytest suite validates that the machine starts in the **expected clean
# state** _before_ the student runs any of their implementation scripts.
#
# What we assert:
# 1. Base working directory "/home/user/db_backup" is present.
# 2. The configuration file "/home/user/db_backup/db_backup.ini" is present,
#    is a regular file, and its **contents match exactly** the canonical truth
#    supplied in the task description.
#
# IMPORTANT:  We intentionally **do not** check for the presence or absence of
# any of the output artefacts the student is supposed to create later
# (backup_plan.txt, validation.log, archives directory, etc.), in compliance
# with the testing rules.


import textwrap
from pathlib import Path

import pytest

BASE_DIR = Path("/home/user/db_backup")
INI_PATH = BASE_DIR / "db_backup.ini"


def test_base_directory_exists():
    """The main working directory must already exist."""
    assert BASE_DIR.exists(), (
        f"Expected base directory {BASE_DIR} to exist, but it is missing."
    )
    assert BASE_DIR.is_dir(), (
        f"{BASE_DIR} exists but is not a directory."
    )


def test_ini_file_exists_and_is_file():
    """The configuration INI file must already be present as a regular file."""
    assert INI_PATH.exists(), (
        f"Expected configuration file {INI_PATH} to exist, but it is missing."
    )
    assert INI_PATH.is_file(), (
        f"{INI_PATH} exists but is not a regular file."
    )


def test_ini_file_contents_match_expected():
    """
    The INI file must match the exact baseline contents provided in the task
    description. A final trailing newline is tolerated.
    """
    expected_content = textwrap.dedent(
        """\
        [database]
        host = localhost
        port = 5432
        name = prod_db
        user = backup_user

        [backup]
        backup_dir = /home/user/db_backup/archives
        compression = true
        method = pg_dump

        [retention]
        retention_days = 30
        """
    )

    actual_content = INI_PATH.read_text()

    # Accept a single trailing newline difference.
    assert actual_content.rstrip("\n") == expected_content.rstrip("\n"), (
        "The contents of db_backup.ini do not match the expected baseline.\n\n"
        "Expected:\n"
        "----------\n"
        f"{expected_content}\n"
        "----------\n"
        "Actual:\n"
        "----------\n"
        f"{actual_content}\n"
        "----------"
    )