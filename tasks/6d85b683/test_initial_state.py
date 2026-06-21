# test_initial_state.py
#
# Pytest suite that validates the machine *before* the student
# performs the configuration-management task described in the prompt.
#
# These tests assert that none of the required artifacts created by a
# successful run (virtual-environment directory, tracking directory,
# and the package-inventory log file) exist yet.  If any of them are
# already present, the initial state is incorrect and the suite will
# fail with a clear, actionable message.

import os
import stat
import pytest

HOME = "/home/user"
PROJECTS_DIR = os.path.join(HOME, "projects")
CM_VENV_DIR = os.path.join(PROJECTS_DIR, "cm_venv")
CONFIG_TRACK_DIR = os.path.join(PROJECTS_DIR, "config_track")
ENV_LOG = os.path.join(CONFIG_TRACK_DIR, "env_packages.log")


def _path_exists(path: str) -> bool:
    """Helper: True if path exists (file, dir, or other)."""
    return os.path.exists(path)


@pytest.mark.describe("Initial filesystem state validation")
class TestInitialState:
    def test_cm_venv_does_not_exist(self):
        assert not _path_exists(
            CM_VENV_DIR
        ), (
            f"Pre-condition failure: {CM_VENV_DIR} already exists. "
            "The virtual environment must NOT be present before the student "
            "creates it."
        )

    def test_config_track_dir_does_not_exist(self):
        assert not _path_exists(
            CONFIG_TRACK_DIR
        ), (
            f"Pre-condition failure: {CONFIG_TRACK_DIR} already exists. "
            "The tracking directory must NOT be present before the student "
            "creates it."
        )

    def test_env_packages_log_does_not_exist(self):
        assert not _path_exists(
            ENV_LOG
        ), (
            f"Pre-condition failure: {ENV_LOG} already exists. "
            "The package inventory log must NOT be present before the "
            "student generates it."
        )

    def test_projects_dir_is_clean_of_task_artifacts(self):
        """
        The /home/user/projects directory itself may or may not already
        exist for unrelated reasons.  If it does exist, it must not
        contain any of the task-specific artifacts.
        """
        if not _path_exists(PROJECTS_DIR):
            pytest.skip(f"{PROJECTS_DIR} does not exist yet — this is acceptable.")

        bad_entries = {
            entry
            for entry in os.listdir(PROJECTS_DIR)
            if entry in {"cm_venv", "config_track"}
        }
        assert not bad_entries, (
            f"Pre-condition failure: {PROJECTS_DIR} already contains: "
            f"{', '.join(sorted(bad_entries))}. These items must be created "
            "by the student, not be present beforehand."
        )