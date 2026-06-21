# test_initial_state.py
#
# This test-suite validates that the three micro-service log files required
# for the audit task already exist **before** the student performs any action
# and that they contain exactly the lines specified in the problem
# description.  If anything is missing or different, the tests will fail with
# a clear, actionable error message.
#
# NOTE:  These tests purposely do *not* look for the final output file
# (/home/user/audit/error_audit.log); they only verify the initial state.

import os
import textwrap
import pytest

BASE_PATH = "/home/user/services"
LOG_PATHS = {
    "auth":     "/home/user/services/auth/logs/service.log",
    "orders":   "/home/user/services/orders/logs/service.log",
    "payments": "/home/user/services/payments/logs/service.log",
}

EXPECTED_CONTENT = {
    "auth": textwrap.dedent("""\
        2023-10-30T23:59:59Z INFO Startup complete
        2023-10-31T00:00:02Z ERROR Token validation failed for user id 42
        2023-10-31T06:30:11Z WARN Token near expiry for user id 7
        2023-10-31T22:15:45Z ERROR Unauthorized access attempt detected
    """).splitlines(),
    "orders": textwrap.dedent("""\
        2023-10-31T01:15:22Z INFO Order service started
        2023-10-31T02:47:05Z ERROR Order ID 1001 failed validation
        2023-10-31T14:22:33Z ERROR Payment gateway timeout for order 2033
    """).splitlines(),
    "payments": textwrap.dedent("""\
        2023-10-31T03:10:00Z ERROR Credit card declined transaction 5005
        2023-10-31T12:00:00Z INFO Daily settlement completed
        2023-10-31T20:59:59Z ERROR Fraud detection triggered for transaction 6006
    """).splitlines(),
}


@pytest.mark.parametrize("service_name,log_path", LOG_PATHS.items())
def test_log_file_exists(service_name, log_path):
    """Verify that each service.log file exists and is a regular file."""
    assert os.path.isfile(log_path), (
        f"Expected log file for service '{service_name}' not found at:\n  {log_path}"
    )


@pytest.mark.parametrize("service_name,expected_lines", EXPECTED_CONTENT.items())
def test_log_file_contents_exact_match(service_name, expected_lines):
    """
    Verify that the content of each service.log matches the specification
    exactly—same number of lines and same text (LF endings are ignored by
    splitting into logical lines).
    """
    log_path = LOG_PATHS[service_name]
    with open(log_path, "rt", encoding="utf-8") as fh:
        actual_lines = fh.read().splitlines()

    # Helpful diff-style error message if the content differs.
    if actual_lines != expected_lines:
        diff_lines = [
            f"Content mismatch for {log_path}:",
            "---- expected",
            *[f"    {line}" for line in expected_lines],
            "---- actual",
            *[f"    {line}" for line in actual_lines],
        ]
        pytest.fail("\n".join(diff_lines))

    # Also ensure that there are no blank lines sneaking in.
    assert all(line.strip() for line in actual_lines), (
        f"Blank line detected in {log_path}; every line must contain text."
    )


def test_directory_structure_present():
    """
    Make sure that the overall directory structure /home/user/services/<svc>/logs
    exists for all three services.  This guards against mis-named or missing
    directories that could break the student's solution later on.
    """
    for service in LOG_PATHS:
        logs_dir = os.path.dirname(LOG_PATHS[service])
        service_dir = os.path.dirname(logs_dir)

        assert os.path.isdir(service_dir), (
            f"Missing directory for service '{service}':\n  {service_dir}"
        )
        assert os.path.isdir(logs_dir), (
            f"Missing 'logs' directory for service '{service}':\n  {logs_dir}"
        )