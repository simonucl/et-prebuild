# test_initial_state.py
#
# Pytest suite to validate the *initial* state of the OS / filesystem
# before the student runs any command for the “initial connectivity
# finding” exercise.
#
# Nothing related to the task (directories or files) should exist yet.
# If any of the artefacts are already present, the test suite must fail
# with an explicit, human-readable message.
#
# Allowed imports: only stdlib and pytest.

import os
from pathlib import Path

import pytest

# Constants for full, absolute paths
HOME = Path("/home/user")
NETWORK_DIR = HOME / "network"
AUDIT_DIR = NETWORK_DIR / "audit"
STATUS_FILE = AUDIT_DIR / "connectivity_status.log"


def _format_path(p: Path) -> str:
    """Return the absolute path as a str for clearer error reporting."""
    return str(p.resolve())


def _exists(p: Path) -> bool:
    """Wrapper around .exists() to keep the code DRY and explicit."""
    return p.exists()


@pytest.mark.describe("Sanity-check that the task artefacts are NOT present yet")
class TestInitialState:
    def test_audit_directory_absent(self):
        """
        The directory /home/user/network/audit must NOT exist *before*
        the student performs the task. Its presence would indicate that
        the environment is already pre-seeded or the student’s command
        has been executed prematurely.
        """
        assert not _exists(
            AUDIT_DIR
        ), (
            f"The directory {_format_path(AUDIT_DIR)} already exists, "
            "but it should not be present at the start of the exercise. "
            "Remove it so the student can create it as part of the task."
        )

    def test_status_file_absent(self):
        """
        The file /home/user/network/audit/connectivity_status.log must NOT
        exist yet. The student is responsible for creating it with the
        correct contents in a single shell command.
        """
        assert not _exists(
            STATUS_FILE
        ), (
            f"The file {_format_path(STATUS_FILE)} already exists, "
            "but it should not be present at the start of the exercise. "
            "Remove it so the student can create it fresh with the "
            "required content."
        )

    def test_parent_network_directory_may_exist_but_empty_of_audit_dir(self):
        """
        It is permissible for /home/user/network to exist for unrelated
        reasons, but if it does, it must *not* already contain the 'audit'
        subdirectory. This test ensures a clean slate without being overly
        restrictive about other potential contents.
        """
        if NETWORK_DIR.exists():
            assert (
                not AUDIT_DIR.exists()
            ), (
                f"The parent directory {_format_path(NETWORK_DIR)} exists and "
                f"already contains {_format_path(AUDIT_DIR)}. "
                "The 'audit' subdirectory should not be present yet."
            )