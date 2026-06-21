# test_initial_state.py
#
# This pytest suite validates that, **before the student executes any command**,
# the operating-system state already satisfies the assumptions required by the
# assignment.  In particular, we confirm that the init process is running as
# PID 1.  We deliberately do **not** test for the presence of
# /home/user/audit/… because those paths constitute the *output* that the
# student is expected to create.
#
# Only stdlib and pytest are used.

import os
import pytest
from pathlib import Path


def test_proc_1_directory_exists():
    """
    /proc/1 must exist because the init process always runs as PID 1 in Linux.
    """
    proc_1 = Path("/proc/1")
    assert proc_1.exists(), (
        "Expected the directory /proc/1 for the init process, but it is missing."
    )
    assert proc_1.is_dir(), (
        f"/proc/1 exists but is not a directory; found type: {proc_1}"
    )


def test_proc_1_status_reports_pid_1():
    """
    The file /proc/1/status must contain a line starting with 'Pid:\t1'.
    This proves that the kernel recognises PID 1 as an existing task.
    """
    status_path = Path("/proc/1/status")
    assert status_path.is_file(), (
        "Expected /proc/1/status to exist, but it is missing."
    )

    with status_path.open() as fp:
        for line in fp:
            if line.startswith("Pid:"):
                pid_value = line.split(":", 1)[1].strip()
                assert pid_value == "1", (
                    f"Init process should report PID 1, "
                    f"but /proc/1/status shows Pid:\t{pid_value!r}"
                )
                break
        else:
            pytest.fail(
                "Could not find a 'Pid:' line in /proc/1/status; "
                "cannot confirm the init process PID."
            )


def test_proc_1_comm_is_nonempty():
    """
    /proc/1/comm should contain the name of the init process (e.g., 'systemd',
    'init', 'tini', etc.).  The exact name is not enforced—only that the field
    is non-empty.
    """
    comm_path = Path("/proc/1/comm")
    assert comm_path.is_file(), (
        "Expected /proc/1/comm to exist, but it is missing."
    )

    comm = comm_path.read_text().strip()
    assert comm, (
        "The init process name in /proc/1/comm is empty; "
        "expected a non-empty command name."
    )