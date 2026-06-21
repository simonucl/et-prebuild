# test_initial_state.py
#
# This pytest suite validates the **initial** state of the system *before*
# the student has carried out any of the required steps for the task
# “Prepare the staging server for the next rollout with version v1.2.3”.
#
# It checks that none of the artefacts that are expected *after* the task
# has been completed are already present in their final form.  If any of
# them already exist exactly as the grader will later require, the tests
# will fail and clearly report what must be cleaned up first.
#
# Only the Python standard library and pytest are used, and absolute paths
# are referenced throughout, as required.

import os
import pytest
from pathlib import Path

# Constants --------------------------------------------------------------

HOME = Path("/home/user")
RELEASE_VERSION = "v1.2.3"
RELEASE_DIR = HOME / "releases" / RELEASE_VERSION
CURRENT_SYMLINK = HOME / "releases" / "current"
ENV_FILE = HOME / "deploy.env"
LOG_FILE = HOME / "deployment_setup.log"

ENV_EXPECTED_CONTENT = "RELEASE_VERSION=v1.2.3\nDEPLOY_STATUS=ready\n"
LOG_EXPECTED_CONTENT = (
    f"DIR_CREATED:{RELEASE_DIR}\n"
    f"SYMLINK_SET:{CURRENT_SYMLINK}->/home/user/releases/{RELEASE_VERSION}\n"
    f"ENV_FILE_OK:{ENV_FILE}\n"
)

# Helper -----------------------------------------------------------------


def file_content(path: Path) -> str:
    """Read file content as text, return empty string if file is unreadable."""
    try:
        with path.open("r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return ""


# Tests ------------------------------------------------------------------


def test_release_directory_does_not_exist():
    """
    The release directory for v1.2.3 must **not** pre-exist.
    It will be created by the student during the task.
    """
    assert not RELEASE_DIR.exists(), (
        f"The directory {RELEASE_DIR} already exists but should not. "
        "Please remove it so the student can create it afresh."
    )


def test_current_symlink_not_already_pointing_to_new_release():
    """
    /home/user/releases/current may or may not exist at this point, but if it
    exists *as a symlink* it must NOT yet point to the new release directory.
    """
    if CURRENT_SYMLINK.is_symlink():
        target = os.readlink(CURRENT_SYMLINK)
        unacceptable_targets = {str(RELEASE_DIR), RELEASE_VERSION}
        assert target not in unacceptable_targets, (
            f"{CURRENT_SYMLINK} already points to the new release "
            f"({target!r}). It should point elsewhere or not exist yet."
        )
    # Anything that is not a symlink (regular file/dir/non-existent) is fine.


def test_deploy_env_not_in_final_state():
    """
    /home/user/deploy.env must either be absent or, if it exists, must NOT yet
    contain the exact final two-line configuration block.
    """
    if ENV_FILE.exists():
        content = file_content(ENV_FILE)
        assert content != ENV_EXPECTED_CONTENT, (
            f"{ENV_FILE} already has the final required content—"
            "the student should generate this file during the task."
        )
    else:
        assert True  # Explicit for readability: absence is acceptable.


def test_log_file_not_in_final_state():
    """
    /home/user/deployment_setup.log must either be absent or, if it exists,
    must NOT yet contain exactly the three final log lines.
    """
    if LOG_FILE.exists():
        content = file_content(LOG_FILE)
        assert content != LOG_EXPECTED_CONTENT, (
            f"{LOG_FILE} already contains the final log entry block—"
            "the student must produce this after completing the task."
        )
    else:
        assert True  # Absence is the expected initial state.