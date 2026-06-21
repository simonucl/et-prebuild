# test_initial_state.py
#
# This pytest file verifies that the system is still in its initial
# state **before** the student creates the required artefacts.
#
# It deliberately FAILS if any of the files that the assignment
# asks the student to create already exist.  That way we know the
# starting point is clean.

import os
import stat
import pytest

SCRIPT_PATH = "/home/user/firewall_rules.sh"
AUDIT_DIR = "/home/user/audit"
LOG_PATH = f"{AUDIT_DIR}/firewall_change.log"


def _file_details(path: str) -> str:
    """Return a human-readable description of a file if it exists."""
    try:
        st = os.stat(path)
    except FileNotFoundError:
        return "does not exist"
    else:
        perms = stat.filemode(st.st_mode)
        return f"exists with permissions {perms!r} and size {st.st_size} bytes"


@pytest.mark.order(1)
def test_firewall_script_absent():
    """
    /home/user/firewall_rules.sh must NOT exist yet.
    If it does, the student started the task prematurely.
    """
    assert not os.path.exists(
        SCRIPT_PATH
    ), (
        f"Expected no script at {SCRIPT_PATH!r}, but it {_file_details(SCRIPT_PATH)}.\n"
        "Remove the file before starting the assignment."
    )


@pytest.mark.order(2)
def test_audit_log_absent():
    """
    /home/user/audit/firewall_change.log must NOT exist yet.
    The audit directory itself may or may not exist; we only check the log file.
    """
    assert not os.path.exists(
        LOG_PATH
    ), (
        f"Expected no log file at {LOG_PATH!r}, but it {_file_details(LOG_PATH)}.\n"
        "Remove the log file before starting the assignment."
    )