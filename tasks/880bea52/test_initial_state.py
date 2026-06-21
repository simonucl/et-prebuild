# test_initial_state.py
#
# This pytest suite validates that the operating-system state is **clean**
# before the student carries out the provisioning task.  In particular,
# we ensure that nothing related to “/home/user/provisioning” (the target
# directory, the script, or the log-template file) is already present.
#
# A failure here means the environment is **not** in the pristine state
# required for the exercise and may give the student an unfair advantage
# (or mask an implementation error).

import os
from pathlib import Path
import stat
import pytest

HOME = Path("/home/user")
PROVISION_DIR = HOME / "provisioning"
SCRIPT_PATH = PROVISION_DIR / "quick_provision.sh"
LOG_PATH = PROVISION_DIR / "expected_output.log"


@pytest.mark.describe("Pre-exercise sanity checks")
class TestInitialState:
    def test_home_exists_and_is_directory(self):
        """The base home directory must exist; otherwise the whole exercise is mis-configured."""
        assert HOME.exists(), f"Required base directory {HOME} is missing."
        assert HOME.is_dir(), f"{HOME} exists but is not a directory."

    def test_provisioning_directory_absent(self):
        """
        The /home/user/provisioning directory should NOT exist yet.
        Its presence would mean the exercise has already been attempted
        or the image is incorrectly prepared.
        """
        assert not PROVISION_DIR.exists(), (
            f"{PROVISION_DIR} already exists, but it should be created by the student."
        )

    @pytest.mark.parametrize("path,label", [
        (SCRIPT_PATH, "script"),
        (LOG_PATH, "log template"),
    ])
    def test_target_files_absent(self, path: Path, label: str):
        """
        Neither quick_provision.sh nor expected_output.log should exist
        before the student starts working.
        """
        assert not path.exists(), (
            f"The {label} file {path} already exists; "
            "the student is expected to create it from scratch."
        )

    def test_no_parent_directory_artifacts(self):
        """
        Even if /home/user/provisioning does not yet exist, make sure
        there are no stray files with similar names in /home/user that
        could interfere with path comparisons or confuse the student.
        """
        unexpected_items = [
            p for p in HOME.iterdir()
            if p.name.startswith("provisioning") and p != PROVISION_DIR
        ]
        assert not unexpected_items, (
            "Found unexpected items in /home/user related to the exercise: "
            f"{', '.join(map(str, unexpected_items))}"
        )