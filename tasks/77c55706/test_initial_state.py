# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# starts in a clean state *before* the student begins the assignment
# described in the instructions.  Nothing related to the task should
# exist or be running yet.

import os
import subprocess
from pathlib import Path

POLICY_DIR = Path("/home/user/policydemo")
WATCHDOG_SH = POLICY_DIR / "watchdog.sh"
AUDIT_LOG = POLICY_DIR / "watchdog_audit.log"
VERIFICATION_TXT = POLICY_DIR / "verification.txt"


def _ps_output() -> str:
    """
    Returns the full text output of `ps -eo pid,cmd` as a single string.
    """
    return subprocess.check_output(["ps", "-eo", "pid,cmd"], text=True)


def _watchdog_pids():
    """
    Yields any (pid, cmd) pair whose command ends with 'watchdog.sh'.
    """
    for line in _ps_output().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            pid, cmd = line.split(maxsplit=1)
        except ValueError:
            # Line did not split into two parts; ignore.
            continue
        if cmd.endswith("watchdog.sh"):
            yield int(pid), cmd


def test_policy_directory_clean_state():
    """
    The /home/user/policydemo directory should not yet exist, OR, if it
    does exist (for example the student precreated only an empty dir),
    it must *not* contain any of the required task artefacts.
    """
    if not POLICY_DIR.exists():
        # Best case: directory absent – nothing to check further.
        return

    existing_items = {p.name for p in POLICY_DIR.iterdir()}
    unexpected = {"watchdog.sh", "watchdog_audit.log", "verification.txt"} & existing_items
    assert not unexpected, (
        "The directory {} already contains files that should only appear "
        "after you complete the exercise: {}.  Start from a clean state "
        "or remove these items before proceeding.".format(POLICY_DIR, ", ".join(sorted(unexpected)))
    )


def test_watchdog_script_absent():
    """
    watchdog.sh must not be present before the student creates it.
    """
    assert not WATCHDOG_SH.exists(), (
        f"The file {WATCHDOG_SH} already exists, but it should be created "
        "by the student as part of the assignment.  Remove it to start from "
        "a clean state."
    )


def test_audit_log_absent():
    """
    watchdog_audit.log must not be present yet.
    """
    assert not AUDIT_LOG.exists(), (
        f"The file {AUDIT_LOG} already exists, but it should not be present "
        "before the student runs their solution."
    )


def test_verification_file_absent():
    """
    verification.txt must not be present yet.
    """
    assert not VERIFICATION_TXT.exists(), (
        f"The file {VERIFICATION_TXT} already exists, but it should not be "
        "present before the student finishes the assignment."
    )


def test_no_watchdog_process_running():
    """
    There must be no running process whose command ends with 'watchdog.sh'.
    """
    pids_found = list(_watchdog_pids())
    assert not pids_found, (
        "Found a running watchdog.sh process(es) even before the exercise "
        "started: {}.  Terminate these process(es) before beginning.".format(
            ", ".join(str(pid) for pid, _ in pids_found)
        )
    )