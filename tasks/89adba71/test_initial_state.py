# test_initial_state.py
#
# This test-suite validates that the environment is still in its
# *pre-task* (clean-slate) state.  None of the directories or files that
# the subsequent exercise asks the student to create should exist yet.
#
# If **any** of the artefacts defined in the task description are
# already present, the tests will fail with a descriptive message –
# preventing accidental contamination of the starting environment.
#
# NOTE:
#     • These checks run *before* the student begins work.
#     • Only the Python stdlib and `pytest` are used.

import os
from pathlib import Path

# Base directory constants
HOME_DIR = Path("/home/user").resolve()
CLOUD_DIR = HOME_DIR / "cloud_migration"
FIREWALL_DIR = CLOUD_DIR / "firewall"

# Expected artefacts (absolute paths)
EXPECTED_PATHS = {
    "dirs": [
        CLOUD_DIR,
        FIREWALL_DIR,
    ],
    "files": [
        FIREWALL_DIR / "inbound_policy_v1.rules",
        FIREWALL_DIR / "inbound_policy_v2.rules",
        FIREWALL_DIR / "apply_firewall.sh",
        FIREWALL_DIR / "implementation.log",
    ],
}


def _fmt(path: Path) -> str:
    """Return the POSIX‐style absolute path for nice error messages."""
    return str(path.as_posix())


def test_home_directory_exists():
    """Sanity-check that the /home/user directory itself exists."""
    assert HOME_DIR.exists(), (
        "The base home directory /home/user is missing. "
        "The container/user setup is not correct."
    )
    assert HOME_DIR.is_dir(), "/home/user exists but is not a directory."


def test_cloud_and_firewall_dirs_absent():
    """
    Ensure that the cloud_migration and firewall directories do NOT
    exist before the student starts the exercise.
    """
    for directory in EXPECTED_PATHS["dirs"]:
        assert not directory.exists(), (
            f"Pre-existing directory found at {_fmt(directory)}.\n"
            "The environment must start clean so the student can create it."
        )


def test_expected_files_absent():
    """
    None of the required files should be present yet.
    """
    for file_path in EXPECTED_PATHS["files"]:
        assert not file_path.exists(), (
            f"Unexpected file already exists: {_fmt(file_path)}.\n"
            "Remove it so the student can generate the correct artefact."
        )