# test_initial_state.py
#
# This pytest file validates the *initial* state of the execution
# environment **before** the student runs any commands for the
# “security audit” task.  Nothing related to the expected final
# artefacts (directory or log file) should exist yet, and at least one
# suitable command-line web client must be available.

import os
import shutil
import stat
import pytest


HOME_DIR = "/home/user"
AUDIT_DIR = "/home/user/security_audit"
LOG_FILE = "/home/user/security_audit/website_report.log"
REQUIRED_TOOLS = ("curl", "wget", "links")


def test_home_directory_present():
    """
    Sanity check: the base home directory must exist; otherwise the
    remainder of the task cannot succeed.
    """
    assert os.path.isdir(HOME_DIR), f"Expected home directory {HOME_DIR} to exist."


def test_audit_directory_does_not_exist_yet():
    """
    The security_audit directory must NOT exist before the student
    performs any action.  Its presence would indicate that previous
    runs polluted the workspace.
    """
    assert not os.path.exists(
        AUDIT_DIR
    ), (
        f"Found pre-existing path {AUDIT_DIR}. "
        "The workspace should be clean before the task begins."
    )


def test_log_file_does_not_exist_yet():
    """
    The log file expected *after* completion must not exist at the
    beginning of the exercise.
    """
    assert not os.path.exists(
        LOG_FILE
    ), (
        f"Found pre-existing file {LOG_FILE}. "
        "The workspace should be clean before the task begins."
    )


@pytest.mark.parametrize("tool", REQUIRED_TOOLS)
def test_at_least_one_web_client_available(tool):
    """
    At least one of the minimal headless web clients (curl, wget or
    links -dump) must be available in $PATH so that the student’s
    commands can succeed.  We parametrize the test to show *which*
    tool(s) are absent; the test will pass as soon as one is present.
    """
    if shutil.which(tool):
        pytest.skip(f"Found suitable web client: {tool!r}")
    # If we get here, the current tool is absent; we mark the test as xfail.
    pytest.xfail(f"Web client {tool!r} not found.")


def test_at_least_one_tool_final_assertion():
    """
    The previous parametrized test marks missing tools as xfail, not
    fail.  Here we perform a final assertion that *none* of the tools
    were found, turning the situation into a hard failure.
    """
    for tool in REQUIRED_TOOLS:
        if shutil.which(tool):
            return  # All good: at least one tool exists.
    pytest.fail(
        "None of the required web clients (curl, wget, links) are available in $PATH."
    )