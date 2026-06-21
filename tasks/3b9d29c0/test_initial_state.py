# test_initial_state.py
#
# This test-suite is executed *before* the student starts working on the
# “DNS status log” task.  It verifies that the expected output artefacts
# are **absent** so that the task starts from a clean slate.
#
# If any of the checks below fail it means the environment is already
# “dirty” (for example, remnants from a previous run are present).  The
# failure messages are intentionally explicit so that the student—or the
# course infrastructure—can remove the offending paths before continuing.
#
# Tested prerequisites:
#   1.  The directory  /home/user/alerts            must NOT exist.
#   2.  The file       /home/user/alerts/dns_status.log  must NOT exist.
#
# No third-party libraries are used; only stdlib + pytest.

import os
import stat
import pytest

HOME_DIR = "/home/user"
ALERTS_DIR = os.path.join(HOME_DIR, "alerts")
DNS_LOG   = os.path.join(ALERTS_DIR, "dns_status.log")


@pytest.mark.order(1)
def test_alerts_directory_absent():
    """
    The 'alerts' directory must NOT exist before the student starts.
    We check both for directory and for any other filesystem object
    occupying that path (file, symlink, socket, etc.).
    """
    if not os.path.exists(ALERTS_DIR):
        # All good: nothing at that path.
        return

    st = os.lstat(ALERTS_DIR)
    kind = "directory" if stat.S_ISDIR(st.st_mode) else "file/object"
    pytest.fail(
        f"Pre-existing {kind} detected at '{ALERTS_DIR}'.\n"
        "Please remove it so the exercise can start with a clean state."
    )


@pytest.mark.order(2)
def test_dns_status_log_absent():
    """
    The 'dns_status.log' file must NOT exist before the student starts.
    If the parent directory itself is already wrongly present, the first
    test will have failed; we still separately ensure the file is absent.
    """
    if not os.path.exists(DNS_LOG):
        # Desired: no file yet.
        return

    st = os.lstat(DNS_LOG)
    kind = "directory" if stat.S_ISDIR(st.st_mode) else "file/object"
    pytest.fail(
        f"Pre-existing {kind} detected at '{DNS_LOG}'.\n"
        "Remove it to guarantee the student produces a fresh file."
    )