# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem **before**
# the student’s action is graded.  It checks that the DBA environment
# preparation was carried out exactly as specified in the task description.
#
# Only the Python standard library + pytest are used.

import os
import stat
import pytest

HOME = "/home/user"
ENV_FILE = os.path.join(HOME, ".env_dba")
BASHRC   = os.path.join(HOME, ".bashrc")
TUNING_DIR = os.path.join(HOME, "db_tuning")
LOG_FILE   = os.path.join(TUNING_DIR, "optimize_queries.log")

# ---------------------------------------------------------------------------
# Expected, byte-perfect file contents (including the mandatory trailing \n)
# ---------------------------------------------------------------------------

EXPECTED_ENV_CONTENT = (
    'export PGDATABASE="salesdb"\n'
    'export PGUSER="analyst"\n'
    'export PGTZ="UTC"\n'
    'export PGOPTIONS="-c work_mem=64MB -c shared_buffers=256MB"\n'
)

EXPECTED_BASH_SNIPPET = (
    "# >>> DBA ENV START >>>\n"
    "if [ -f ~/.env_dba ]; then\n"
    "    . ~/.env_dba\n"
    "fi\n"
    "# <<< DBA ENV END <<<\n"
)

EXPECTED_LOG_CONTENT = (
    "========== BEFORE ==========\n"
    "Seq Scan on sales (cost=0.00..431.00 rows=24000 width=12)\n"
    "\n"
    "========== TUNING_STEPS ==========\n"
    "1. Created index: CREATE INDEX idx_sales_date ON sales(order_date);\n"
    "2. Adjusted work_mem to 64MB.\n"
    "3. Enabled indexscan with: SET enable_seqscan = off;\n"
    "\n"
    "========== AFTER ==========\n"
    "Index Scan using idx_sales_date on sales (cost=0.43..123.00 rows=24000 width=12)\n"
)

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _assert_permissions(path: str, mode_oct: int):
    """Assert that the filesystem permissions on *path* equal *mode_oct* (octal)."""
    st_mode = os.stat(path).st_mode
    actual  = stat.S_IMODE(st_mode)
    assert actual == mode_oct, (
        f"{path!r} has permissions {oct(actual)}, expected {oct(mode_oct)}"
    )

def _read_file(path: str):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read()

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_env_file_exists_and_content_and_permissions():
    assert os.path.isfile(ENV_FILE), f"Required file {ENV_FILE} does not exist."
    _assert_permissions(ENV_FILE, 0o644)

    content = _read_file(ENV_FILE)
    assert content == EXPECTED_ENV_CONTENT, (
        f"{ENV_FILE} content is not exactly as specified.\n"
        "Expected:\n"
        "----------------\n"
        f"{EXPECTED_ENV_CONTENT}"
        "----------------\n"
        "Actual:\n"
        "----------------\n"
        f"{content}"
        "----------------"
    )

def test_bashrc_contains_snippet_at_very_end():
    assert os.path.isfile(BASHRC), f"Required file {BASHRC} does not exist."

    bashrc_content = _read_file(BASHRC)

    # Bash requires files to end with a newline; enforce that first.
    assert bashrc_content.endswith("\n"), f"{BASHRC} must end with a newline."

    # Verify that the very end of the file is exactly the expected snippet
    tail = bashrc_content[-len(EXPECTED_BASH_SNIPPET):]
    assert tail == EXPECTED_BASH_SNIPPET, (
        f"The last lines of {BASHRC} do not match the required snippet.\n"
        "Expected tail:\n"
        "----------------\n"
        f"{EXPECTED_BASH_SNIPPET}"
        "----------------\n"
        "Actual tail:\n"
        "----------------\n"
        f"{tail}"
        "----------------"
    )

def test_tuning_directory_exists_with_correct_permissions():
    assert os.path.isdir(TUNING_DIR), f"Required directory {TUNING_DIR} does not exist."
    _assert_permissions(TUNING_DIR, 0o755)

def test_log_file_exists_content_and_permissions():
    assert os.path.isfile(LOG_FILE), f"Required file {LOG_FILE} does not exist."
    _assert_permissions(LOG_FILE, 0o644)

    content = _read_file(LOG_FILE)
    assert content == EXPECTED_LOG_CONTENT, (
        f"{LOG_FILE} content is not exactly as specified.\n"
        "Expected:\n"
        "----------------\n"
        f"{EXPECTED_LOG_CONTENT}"
        "----------------\n"
        "Actual:\n"
        "----------------\n"
        f"{content}"
        "----------------"
    )