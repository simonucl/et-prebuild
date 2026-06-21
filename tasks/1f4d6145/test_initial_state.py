# test_initial_state.py
#
# Pytest suite that verifies the *initial* state of the operating-system /
# filesystem *before* the student makes any changes required by the task
# description.  If **any** of these tests fail it means the environment is
# already (fully or partially) in the “final / compliant” state, which would
# invalidate the premise of the exercise.

import os
from pathlib import Path

HOME = Path("/home/user")
BASHRC = HOME / ".bashrc"
AUDIT_DIR = HOME / "compliance_audit"
AUDIT_LOG = AUDIT_DIR / "timezone_locale_compliance.log"


def _last_two_active_lines(path: Path):
    """
    Return the last two non-blank, non-comment lines of *path* as a list.
    If the file has fewer than two such lines, the list will be shorter.
    """
    active = []
    try:
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                stripped = line.rstrip("\n")
                if stripped and not stripped.lstrip().startswith("#"):
                    active.append(stripped)
    except FileNotFoundError:
        return []
    return active[-2:]


def test_bashrc_does_not_already_end_with_export_lines():
    """
    The student's ~/.bashrc must *not* yet end with the two mandated export
    lines.  Having them already present would mean the exercise is pointless.
    """
    expected = [
        'export TZ="Etc/UTC"',
        'export LANG="en_US.UTF-8"',
    ]
    ending = _last_two_active_lines(BASHRC)

    assert ending != expected, (
        f"{BASHRC} already ends with the required two export lines, "
        "but the environment is supposed to be in its *initial* (non-compliant) "
        "state before the student works on the task."
    )


def test_environment_variables_not_pre_set():
    """
    Neither TZ nor LANG should already have the target values in the current
    (pre-task) shell session.
    """
    tz = os.environ.get("TZ")
    lang = os.environ.get("LANG")

    assert tz != "Etc/UTC", (
        "Environment variable TZ is already set to 'Etc/UTC' — it should only "
        "become that value *after* the student edits ~/.bashrc."
    )
    assert lang != "en_US.UTF-8", (
        "Environment variable LANG is already set to 'en_US.UTF-8' — it should "
        "only become that value *after* the student edits ~/.bashrc."
    )


def test_compliance_directory_absent():
    """
    The compliance_audit directory must not exist yet.
    """
    assert not AUDIT_DIR.exists(), (
        f"{AUDIT_DIR} already exists but should be created by the student as "
        "part of the task."
    )


def test_compliance_log_absent():
    """
    The compliance log file must not exist yet.
    """
    assert not AUDIT_LOG.exists(), (
        f"{AUDIT_LOG} already exists but should be created by the student as "
        "part of the task."
    )