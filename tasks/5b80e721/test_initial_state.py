# test_initial_state.py
#
# Pytest suite that verifies the **initial** state of the container **before**
# the student performs any configuration steps for time-zone / locale.
#
# What we assert:
#   1. /home/user/.bashrc either does not exist **or**, if it does, it must NOT
#      yet contain the exact lines:
#          export TZ="Europe/Paris"
#          export LC_ALL="fr_FR.UTF-8"
#   2. /home/user/dev_setup/time_locale.log must NOT exist at all.
#
# Rationale: These tests guarantee that the student’s actions are necessary and
# that subsequent “after” tests can unambiguously verify success.

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
BASHRC = HOME / ".bashrc"
DEV_SETUP_DIR = HOME / "dev_setup"
LOG_FILE = DEV_SETUP_DIR / "time_locale.log"

TZ_LINE = 'export TZ="Europe/Paris"'
LC_ALL_LINE = 'export LC_ALL="fr_FR.UTF-8"'

@pytest.mark.describe("Initial state of /home/user/.bashrc")
def test_bashrc_does_not_contain_new_exports():
    """
    The .bashrc file must not yet contain the required export lines.
    If the file does not exist, that is acceptable.
    """
    if not BASHRC.exists():
        pytest.skip(f"{BASHRC} does not exist yet (acceptable for initial state).")

    with BASHRC.open("r", encoding="utf-8", errors="ignore") as fh:
        content = fh.read().splitlines()

    assert TZ_LINE not in content, (
        f'Unexpected line found in {BASHRC}: {TZ_LINE!r}. '
        "The configuration should NOT be present before the student acts."
    )
    assert LC_ALL_LINE not in content, (
        f'Unexpected line found in {BASHRC}: {LC_ALL_LINE!r}. '
        "The configuration should NOT be present before the student acts."
    )

@pytest.mark.describe("Initial state of verification log file")
def test_time_locale_log_absent():
    """
    The verification log file must not exist before the student creates it.
    """
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} already exists. "
        "The student is expected to create this file during the task, "
        "so it must be absent in the initial state."
    )