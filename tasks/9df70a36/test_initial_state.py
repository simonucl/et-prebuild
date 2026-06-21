# test_initial_state.py
#
# Pytest suite to verify the clean starting state of the VM
# BEFORE the student carries out any actions for the
# “simpleservice” restoration task.
#
# These tests assert that none of the artefacts the student is
# expected to create already exist.  A failure here indicates the
# machine is not in the required pristine state.

import os
from pathlib import Path
import stat
import re
import pytest


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _assert_absent(path: Path):
    """
    Assert that `path` (file or directory) does NOT exist in the filesystem.
    """
    assert not path.exists(), (
        f"Pre-condition failure: {path} already exists.\n"
        "The starting VM must not contain any simpleservice artefacts."
    )


# ---------------------------------------------------------------------------
# Tests for absence of expected artefacts
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "path_str",
    [
        "/home/user/simpleservice",                       # whole tree should be absent
        "/home/user/simpleservice/logs",                  # logs dir should be absent
        "/home/user/etc/simpleservice.conf",              # config file should be absent
        "/home/user/bin/restart-simpleservice.sh",        # helper script should be absent
        "/home/user/task_outcome.log",                    # evidence file should be absent
    ],
)
def test_expected_artefacts_absent(path_str):
    """
    Ensure that none of the artefacts the student must create
    are present before the task is attempted.
    """
    _assert_absent(Path(path_str))


# ---------------------------------------------------------------------------
# Sanity-check: if a stray file exists with a similar name, fail loudly
# ---------------------------------------------------------------------------

def test_no_stray_simpleservice_items_under_home():
    """
    Make sure there are no stray files or directories whose names start
    with 'simpleservice' anywhere directly under /home/user.
    (This helps catch partial or mis-named leftovers.)
    """
    home = Path("/home/user")
    pattern = re.compile(r"^simpleservice", re.IGNORECASE)
    offending = [
        p for p in home.iterdir()
        if pattern.match(p.name)
    ]
    assert not offending, (
        "Pre-condition failure: found unexpected items under /home/user:\n"
        + "\n".join(str(p) for p in offending)
    )


# ---------------------------------------------------------------------------
# Permissions sanity check
# ---------------------------------------------------------------------------

def test_no_executable_restart_script_present():
    """
    If the restart script does exist for some reason, ensure it is NOT
    already executable.  We expect complete absence; having it and being
    executable would be an even stronger violation.
    """
    script = Path("/home/user/bin/restart-simpleservice.sh")
    if script.exists():
        mode = script.stat().st_mode
        is_exec_owner = bool(mode & stat.S_IXUSR)
        assert not is_exec_owner, (
            "Pre-condition failure: restart-simpleservice.sh is already "
            "present and marked executable.  The starting state must be clean."
        )