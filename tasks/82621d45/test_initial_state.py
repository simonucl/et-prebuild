# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem **before**
# the student performs any action for the “enable PostgreSQL slow-query
# logging” exercise.
#
# The initial (expected) state is:
#   1. A sandbox directory exists at /home/user/pg_sandbox
#   2. A configuration file exists at /home/user/pg_sandbox/postgresql.conf
#      in which the parameters
#          log_min_duration_statement
#          log_line_prefix
#      are currently *commented out* (i.e. start with “#”) and there are
#      no active (uncommented) occurrences of those parameters.
#   3. No confirmation report file
#          /home/user/pg_sandbox/slow_query_config.log
#      exists yet.
#
# These tests fail with clear, actionable messages if any of the above
# pre-conditions are not met.

from pathlib import Path
import re

# Absolute paths as required
SANDBOX_DIR = Path("/home/user/pg_sandbox")
CONF_FILE = SANDBOX_DIR / "postgresql.conf"
CONFIRM_FILE = SANDBOX_DIR / "slow_query_config.log"


def _read_conf_lines():
    """Helper that returns a list of lines in postgresql.conf, preserving EOLs."""
    try:
        return CONF_FILE.read_text(encoding="utf-8", errors="replace").splitlines()
    except FileNotFoundError:  # pragma: no cover
        # Let the calling test raise the assertion; returning empty list here
        # prevents secondary errors when tests chain helper calls.
        return []


def _find_lines(parameter_name, lines):
    """
    Return two lists:
        uncommented_lines – lines whose first non-space char is not '#'
                            and which start with the parameter_name
        commented_lines   – lines starting with '#' (after optional spaces)
                            followed by the parameter_name
    """
    uncommented, commented = [], []

    # Anchored regex to avoid false positives inside comments etc.
    # Example: r'^\s*log_min_duration_statement\b'
    pattern = re.compile(rf"^\s*{re.escape(parameter_name)}\b")
    commented_pattern = re.compile(rf"^\s*#\s*{re.escape(parameter_name)}\b")

    for ln in lines:
        if commented_pattern.match(ln):
            commented.append(ln)
        elif pattern.match(ln):
            uncommented.append(ln)

    return uncommented, commented


def test_pg_sandbox_directory_exists():
    assert SANDBOX_DIR.is_dir(), (
        f"Expected directory {SANDBOX_DIR} to exist before the exercise "
        "begins, but it is missing."
    )


def test_postgresql_conf_exists():
    assert CONF_FILE.is_file(), (
        f"Expected configuration file {CONF_FILE} to exist in the sandbox, "
        "but it is missing."
    )


def test_log_min_duration_statement_is_only_commented():
    lines = _read_conf_lines()
    uncommented, commented = _find_lines("log_min_duration_statement", lines)

    assert not uncommented, (
        "The configuration already contains an *active* "
        "'log_min_duration_statement' line, but the initial state should have "
        "it commented out so that the student can enable it."
    )

    assert commented, (
        "No commented '#log_min_duration_statement' line found. The initial "
        "template should include a commented example for the student to edit."
    )


def test_log_line_prefix_is_only_commented():
    lines = _read_conf_lines()
    uncommented, commented = _find_lines("log_line_prefix", lines)

    assert not uncommented, (
        "The configuration already contains an *active* 'log_line_prefix' "
        "line, but the initial state should have it commented out so that the "
        "student can enable it."
    )

    assert commented, (
        "No commented '#log_line_prefix' line found. The initial template "
        "should include a commented example for the student to edit."
    )


def test_confirmation_log_not_present_yet():
    assert not CONFIRM_FILE.exists(), (
        f"The confirmation file {CONFIRM_FILE} already exists, but the "
        "student has not yet performed the task. It should be created only "
        "after the required edits have been made."
    )