# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating
# system / filesystem **before** the student runs any command for
# the “workflow.service” exercise.
#
# If any of these tests fail it means the environment is *not* clean
# and the student would start from an unexpected state.  Each failure
# message tells exactly what must **not** be present yet.

import os
from pathlib import Path

HOME = Path("/home/user")
SERVICES_DIR = HOME / "services"
WORKFLOW_SERVICE = SERVICES_DIR / "workflow.service"
CREATION_LOG = SERVICES_DIR / "creation.log"


def _pretty(p: Path) -> str:  # helper for nicer error messages
    return str(p.resolve())


def test_services_directory_absent_or_clean():
    """
    The directory /home/user/services should *either* not exist at all
    or, if it does exist, it must NOT yet contain the two target files.
    """
    if not SERVICES_DIR.exists():
        # Ideal: directory absent
        assert True
        return

    # Directory exists – make sure it does not already contain the files
    offending = []
    if WORKFLOW_SERVICE.exists():
        offending.append(_pretty(WORKFLOW_SERVICE))
    if CREATION_LOG.exists():
        offending.append(_pretty(CREATION_LOG))

    assert not offending, (
        "The following file(s) already exist, but they must be created "
        "by the student’s single-command solution, so they must NOT be "
        "present beforehand:\n"
        f"- " + "\n- ".join(offending)
    )


def test_workflow_service_file_absent():
    """workflow.service must not exist yet."""
    assert not WORKFLOW_SERVICE.exists(), (
        f"{_pretty(WORKFLOW_SERVICE)} already exists. "
        "Remove it so the student can create it with their command."
    )


def test_creation_log_file_absent():
    """creation.log must not exist yet."""
    assert not CREATION_LOG.exists(), (
        f"{_pretty(CREATION_LOG)} already exists. "
        "The student’s command should create it."
    )