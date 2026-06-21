# test_initial_state.py
"""
Pytest suite that validates the expected starting-point of the filesystem
*before* the student begins the assignment.

Rules respected:
1. Only the initial, pre-task state is inspected.
2. No assertions are made about any output files or directories
   (`/home/user/query_tuning` is deliberately **not** referenced).
3. Failures provide clear, actionable messages.
4. Only Python stdlib + pytest are used.
"""

import os
import stat
import textwrap
import pytest

# Constants for reuse
DB_CONFIG_DIR = "/home/user/db_configs"
INI_PATH = os.path.join(DB_CONFIG_DIR, "db_service.ini")

EXPECTED_INI_CONTENT = textwrap.dedent("""\
    [database]
    host=localhost
    port=5432
    dbname=inventory
    user=inventory_admin

    [optimizations]
    max_connections=200
    work_mem=4MB
    shared_buffers=128MB
    effective_cache_size=512MB
    """)  # A single trailing newline is already included by textwrap.dedent


def _mode(path):
    """Return Unix permission bits in octal (e.g., 0o755)."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_db_config_directory_exists_and_has_correct_mode():
    assert os.path.isdir(DB_CONFIG_DIR), (
        f"Required directory {DB_CONFIG_DIR!r} is missing."
    )
    expected_mode = 0o755
    actual_mode = _mode(DB_CONFIG_DIR)
    assert actual_mode == expected_mode, (
        f"Directory {DB_CONFIG_DIR!r} has permissions {oct(actual_mode)}, "
        f"expected {oct(expected_mode)}."
    )


def test_ini_file_exists_and_has_correct_mode():
    assert os.path.isfile(INI_PATH), (
        f"Required INI file {INI_PATH!r} is missing."
    )
    expected_mode = 0o644
    actual_mode = _mode(INI_PATH)
    assert actual_mode == expected_mode, (
        f"INI file {INI_PATH!r} has permissions {oct(actual_mode)}, "
        f"expected {oct(expected_mode)}."
    )


def test_ini_file_has_exact_expected_contents():
    with open(INI_PATH, "r", encoding="utf-8") as fh:
        contents = fh.read()
    assert (
        contents == EXPECTED_INI_CONTENT
    ), "INI file contents do not match the expected initial template."