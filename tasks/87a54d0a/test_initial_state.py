# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem are in the
# pristine “pre-task” state.  In other words, the artefact the student is
# supposed to create during the exercise MUST NOT exist yet.
#
# If any of these tests fail it means the exercise environment was already
# modified (or incorrectly provisioned) before the student started.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
AUDIT_LOG = HOME / "network_disk_audit.log"


def _human(path: Path) -> str:
    """Return a readable representation of a Path for assertion messages."""
    return str(path.expanduser())


def test_home_directory_exists():
    """
    The base home directory for the learner must exist; otherwise nothing else
    can be created there.
    """
    assert HOME.exists(), (
        f"Expected the home directory {_human(HOME)} to exist, "
        "but it is missing."
    )
    assert HOME.is_dir(), (
        f"Expected {_human(HOME)} to be a directory, "
        "but something else is occupying that path."
    )


def test_audit_log_not_present_initially():
    """
    The file ‘network_disk_audit.log’ should NOT exist before the student runs
    any commands.  Its presence would indicate a polluted starting state.
    """
    assert not AUDIT_LOG.exists(), (
        f"Found unexpected file {_human(AUDIT_LOG)} — the workspace should be "
        "clean before the student carries out the exercise."
    )