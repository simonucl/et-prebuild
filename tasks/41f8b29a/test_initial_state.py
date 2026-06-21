# test_initial_state.py
#
# Pytest suite that validates the OS / filesystem *before* the student does any work.
# It makes sure the starting files, directories, and their exact contents match
# the specification, and that output/backup artefacts do **not** exist yet.
#
# No third-party libraries are used; only the standard library + pytest.

import pathlib
import pytest
import textwrap

HOME = pathlib.Path("/home/user")

# --------------------------------------------------------------------------- #
# Helper constants with the exact, byte-for-byte contents we expect to find
# (including final trailing newlines).
# --------------------------------------------------------------------------- #
EXPECTED_LOG_CONTENT = textwrap.dedent("""\
    [2023-06-18 09:00:01] QUERY_ID=1001 duration=250ms select * from accounts where id=1;
    [2023-06-18 09:00:05] QUERY_ID=1002 duration=1200ms select * from transactions where amount > 1000;
    [2023-06-18 09:00:10] QUERY_ID=1003 duration=810ms update accounts set balance=balance+100 where id=2;
    [2023-06-18 09:00:20] QUERY_ID=1004 duration=1350ms delete from sessions where expired=1;
    [2023-06-18 09:00:25] QUERY_ID=1005 duration=90ms select * from accounts;
    """)  # noqa: E501

EXPECTED_CONFIG_CONTENT = textwrap.dedent("""\
    # Database configuration
    work_mem = 4MB
    enable_seqscan = off
    shared_buffers = 128MB
    """)

# --------------------------------------------------------------------------- #
# 1. Basic directory existence
# --------------------------------------------------------------------------- #
def test_required_directories_exist():
    logs_dir = HOME / "db_logs"
    cfg_dir = HOME / "db_config"

    assert logs_dir.is_dir(), (
        f"Required directory {logs_dir} does not exist. "
        "The starting log directory must be present."
    )
    assert cfg_dir.is_dir(), (
        f"Required directory {cfg_dir} does not exist. "
        "The starting config directory must be present."
    )


# --------------------------------------------------------------------------- #
# 2. Verify initial log file exists and is 100 % correct
# --------------------------------------------------------------------------- #
def test_query_performance_log_contents():
    log_file = HOME / "db_logs" / "query_performance.log"
    assert log_file.is_file(), (
        f"Log file {log_file} is missing. "
        "It must be present before any student action."
    )

    actual = log_file.read_text(encoding="utf-8")
    assert actual == EXPECTED_LOG_CONTENT, (
        "The contents of query_performance.log do not match the expected "
        "initial state. Ensure the file is an exact, byte-for-byte match."
    )


# --------------------------------------------------------------------------- #
# 3. Verify initial PostgreSQL configuration file exists and is unmodified
# --------------------------------------------------------------------------- #
def test_postgres_conf_contents():
    cfg_file = HOME / "db_config" / "postgres.conf"
    assert cfg_file.is_file(), (
        f"Configuration file {cfg_file} is missing. "
        "It must be present before any student action."
    )

    actual = cfg_file.read_text(encoding="utf-8")
    assert actual == EXPECTED_CONFIG_CONTENT, (
        "postgres.conf has unexpected content. "
        "It must start with work_mem = 4MB and enable_seqscan = off, "
        "exactly as specified."
    )


# --------------------------------------------------------------------------- #
# 4. Ensure reports directory & artefacts do NOT exist yet
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "path_description, path_obj",
    [
        ("Report directory", HOME / "db_reports"),
        ("CSV report", HOME / "db_reports" / "slow_queries_report.csv"),
        ("Summary log", HOME / "db_reports" / "slow_queries_summary.log"),
    ],
)
def test_reports_not_yet_created(path_description, path_obj):
    assert not path_obj.exists(), (
        f"{path_description} ({path_obj}) already exists, but it should NOT be "
        "present before the student runs their solution."
    )


# --------------------------------------------------------------------------- #
# 5. Ensure backup of postgres.conf does NOT exist yet
# --------------------------------------------------------------------------- #
def test_no_backup_yet():
    backup = HOME / "db_config" / "postgres.conf.bak"
    assert not backup.exists(), (
        f"Backup file {backup} already exists. "
        "It should be created only by the student's script."
    )