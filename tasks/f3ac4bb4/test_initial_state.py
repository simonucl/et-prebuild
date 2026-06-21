# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system state
# before the student attempts the remediation task.
#
# What we assert:
# 1. /home/user/cron.d/evil_job exists and its only non-blank line is the
#    exact, un-commented cron job expected by the brief.
# 2. /home/user/cron.d/evil.sh exists and looks like a shell script.
# 3. Neither /home/user/quarantine nor /home/user/incident_logs exist yet.
#
# If any of these checks fail, the failure messages will point out what is
# missing or incorrect so the student knows that the starting conditions
# are not as prescribed.


import os
import stat
import pytest

HOME = "/home/user"
EVIL_DIR = os.path.join(HOME, "cron.d")
EVIL_JOB = os.path.join(EVIL_DIR, "evil_job")
EVIL_SCRIPT = os.path.join(EVIL_DIR, "evil.sh")
QUAR_DIR = os.path.join(HOME, "quarantine")
LOG_DIR = os.path.join(HOME, "incident_logs")


def _read_non_blank_lines(path):
    """Return a list of non-blank lines with trailing newlines stripped."""
    with open(path, "r", encoding="utf-8") as fp:
        return [ln.rstrip("\n") for ln in fp.readlines() if ln.strip()]


def test_evil_job_exists_and_is_uncommented():
    """The cron job file must exist and contain exactly one active line."""
    assert os.path.isfile(EVIL_JOB), (
        f"Expected cron job file {EVIL_JOB!r} to exist."
    )

    # File permission sanity: readable by owner at least
    st = os.stat(EVIL_JOB)
    assert bool(st.st_mode & stat.S_IRUSR), (
        f"Cron job file {EVIL_JOB!r} is not readable."
    )

    lines = _read_non_blank_lines(EVIL_JOB)
    expected_line = "* * * * * /home/user/cron.d/evil.sh"
    assert lines == [expected_line], (
        "Cron job should contain exactly one non-blank line "
        f"equal to {expected_line!r}. "
        f"Found {len(lines)} line(s): {lines}"
    )


def test_evil_script_exists_and_is_shell_script():
    """The malicious script referenced by the cron job must exist."""
    assert os.path.isfile(EVIL_SCRIPT), (
        f"Expected script {EVIL_SCRIPT!r} to exist."
    )

    st = os.stat(EVIL_SCRIPT)
    # Ensure executable bit for owner is set (0700 in the brief)
    assert bool(st.st_mode & stat.S_IXUSR), (
        f"Script {EVIL_SCRIPT!r} should be executable by the owner."
    )

    # Basic content check – first line should be a shebang for bash
    with open(EVIL_SCRIPT, "r", encoding="utf-8") as fp:
        first_line = fp.readline().rstrip("\n")

    assert first_line == "#!/bin/bash", (
        f"First line of {EVIL_SCRIPT!r} should be '#!/bin/bash', "
        f"but was {first_line!r}"
    )


def test_quarantine_directory_does_not_exist_yet():
    """No quarantine directory should be present before remediation."""
    assert not os.path.exists(QUAR_DIR), (
        f"Directory {QUAR_DIR!r} should NOT exist before the student acts."
    )


def test_incident_logs_directory_does_not_exist_yet():
    """No incident log directory should be present before remediation."""
    assert not os.path.exists(LOG_DIR), (
        f"Directory {LOG_DIR!r} should NOT exist before the student acts."
    )