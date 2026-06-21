# test_initial_state.py
#
# This pytest suite verifies that the starting filesystem / OS state
# matches the specification *before* the student performs any work.
#
# It checks:
#   1. Presence and permissions of /home/user/db_logs
#   2. Presence, permissions and **exact** contents of
#      /home/user/db_logs/slow_query.log
#   3. Absence of any output files that the student is expected to
#      create later.

import os
import stat
import textwrap
import pytest

BASE_DIR = "/home/user/db_logs"
SLOW_LOG = os.path.join(BASE_DIR, "slow_query.log")
METRICS_OUT = os.path.join(BASE_DIR, "query_metrics.log")
LONG_SQL_OUT = os.path.join(BASE_DIR, "high_latency_queries.sql")


@pytest.fixture(scope="module")
def expected_slow_log_content() -> str:
    """Return the exact content the slow log file must contain."""
    # Note: textwrap.dedent is used solely to keep the triple-quoted
    # string readable in the source code; it introduces **no** leading
    # whitespace.  A final newline is intentionally included.
    return textwrap.dedent(
        """\
        # Time: 2023-10-11T10:15:23
        # User@Host: root[root] @ localhost []
        # Query_time: 3.125 Lock_time: 0.000 Rows_sent: 12 Rows_examined: 100
        SET timestamp=1697024123;
        SELECT * FROM users WHERE id = 42;
        # Time: 2023-10-11T10:16:00
        # User@Host: app[app] @ 192.168.1.10 []
        # Query_time: 0.256 Lock_time: 0.001 Rows_sent: 1 Rows_examined: 5
        SET timestamp=1697024160;
        SELECT name FROM products WHERE price > 1000;
        # Time: 2023-10-11T10:17:35
        # User@Host: analytics[anl] @ 192.168.1.20 []
        # Query_time: 7.890 Lock_time: 0.002 Rows_sent: 25000 Rows_examined: 500000
        SET timestamp=1697024255;
        SELECT email, created_at FROM audit_logs WHERE created_at < '2023-01-01';
        # Time: 2023-10-11T10:18:12
        # User@Host: root[root] @ localhost []
        # Query_time: 1.050 Lock_time: 0.000 Rows_sent: 0 Rows_examined: 0
        SET timestamp=1697024292;
        DELETE FROM sessions WHERE last_activity < NOW() - INTERVAL 30 DAY;
        # Time: 2023-10-11T10:20:44
        # User@Host: api[api] @ 192.168.1.30 []
        # Query_time: 12.500 Lock_time: 0.010 Rows_sent: 5 Rows_examined: 1500000
        SET timestamp=1697024444;
        UPDATE orders SET status='FAILED' WHERE payment_state='error';
        # Time: 2023-10-11T10:22:05
        # User@Host: app[app] @ 192.168.1.10 []
        # Query_time: 0.600 Lock_time: 0.001 Rows_sent: 1 Rows_examined: 10
        SET timestamp=1697024525;
        SELECT name FROM customers WHERE customer_id = 123;
        """
    )


def _mode(path: str) -> int:
    """Helper that returns the permission bits (e.g. 0o755)."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_db_logs_directory_exists_and_perms():
    assert os.path.isdir(BASE_DIR), (
        f"Expected directory {BASE_DIR} to exist, "
        "but it is missing or not a directory."
    )
    expected_mode = 0o755
    actual_mode = _mode(BASE_DIR)
    assert actual_mode == expected_mode, (
        f"{BASE_DIR} permissions are {oct(actual_mode)}, "
        f"expected {oct(expected_mode)} (drwxr-xr-x)."
    )


def test_slow_query_log_exists_and_perms():
    assert os.path.isfile(SLOW_LOG), (
        f"Expected slow log file {SLOW_LOG} to exist, but it is missing."
    )
    expected_mode = 0o644
    actual_mode = _mode(SLOW_LOG)
    assert actual_mode == expected_mode, (
        f"{SLOW_LOG} permissions are {oct(actual_mode)}, "
        f"expected {oct(expected_mode)} (-rw-r--r--)."
    )


def test_slow_query_log_contents(expected_slow_log_content):
    with open(SLOW_LOG, "r", encoding="utf-8") as fp:
        actual = fp.read()
    assert (
        actual == expected_slow_log_content
    ), "The contents of slow_query.log do not match the expected initial state."


@pytest.mark.parametrize("path", [METRICS_OUT, LONG_SQL_OUT])
def test_result_files_do_not_exist_yet(path):
    assert not os.path.exists(
        path
    ), f"The file {path} should NOT exist before the student runs their solution."