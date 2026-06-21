# test_initial_state.py
# Pytest suite to verify the operating-system / file-system state
# BEFORE the learner writes any code for the “optimize_slow_queries” task.

import os
import stat
import pytest

HOME = "/home/user"
LOG_PATH = os.path.join(HOME, "db_queries.log")
SCRIPT_PATH = os.path.join(HOME, "optimize_slow_queries.sh")
REPORT_PATH = os.path.join(HOME, "slow_queries_report.txt")


@pytest.fixture(scope="module")
def log_contents():
    """Read the contents of the log file once for all tests."""
    if not os.path.exists(LOG_PATH):
        pytest.fail(
            f"Required log file not found at {LOG_PATH!r}. "
            "It must be present before the task begins."
        )
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as fp:
            text = fp.read()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {LOG_PATH}: {exc}")
    return text


def test_log_file_exists_and_permissions():
    """The initial db_queries.log must exist with mode 0644."""
    assert os.path.isfile(
        LOG_PATH
    ), f"{LOG_PATH!r} should exist as a regular file before the task starts."

    mode = stat.S_IMODE(os.stat(LOG_PATH).st_mode)
    expected_mode = 0o644
    assert (
        mode == expected_mode
    ), f"{LOG_PATH} must have permissions 0644 (got {oct(mode)})"


def test_log_file_has_exact_expected_content(log_contents):
    """Ensure db_queries.log has exactly the five expected lines and a trailing newline."""
    expected_lines = [
        "1,1800,SELECT id, name FROM customers WHERE vip = true;\n",
        "2,3050,UPDATE products SET stock = stock - 1 WHERE id = 987;\n",
        "3,150,DELETE FROM sessions WHERE last_access < NOW() - INTERVAL '30 days';\n",
        "4,4990,SELECT * FROM orders WHERE status = 'PENDING';\n",
        "5,2400,INSERT INTO audit_log (event) VALUES ('user_login');\n",
    ]

    actual_lines = log_contents.splitlines(keepends=True)

    assert (
        actual_lines == expected_lines
    ), (
        "The contents of db_queries.log do not match the expected initial data.\n"
        "Expected lines:\n"
        + "".join(expected_lines)
        + "\nActual lines:\n"
        + "".join(actual_lines)
    )

    # Explicitly ensure the file ends with a single final newline character.
    assert log_contents.endswith(
        "\n"
    ), "db_queries.log must end with a single trailing newline character"


def test_script_does_not_yet_exist():
    """The optimize_slow_queries.sh script should NOT exist prior to the learner’s work."""
    assert not os.path.exists(
        SCRIPT_PATH
    ), f"{SCRIPT_PATH!r} should NOT exist before the learner creates it."


def test_report_file_does_not_yet_exist():
    """The slow_queries_report.txt file should NOT exist prior to running the new script."""
    assert not os.path.exists(
        REPORT_PATH
    ), f"{REPORT_PATH!r} should NOT exist before the learner runs their script."