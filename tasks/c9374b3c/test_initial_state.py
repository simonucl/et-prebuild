# test_initial_state.py
#
# This pytest suite verifies the *initial* filesystem state before
# the student carries out the configuration steps described in the
# assignment.  It purposefully checks that none of the “after”-task
# artefacts exist yet and that the provided artefacts are still in
# their pristine form.

import os
from pathlib import Path

HOME = Path("/home/user")
ARTIE_DIR = HOME / "artie-manager"
CONFIG_DIR = ARTIE_DIR / "config"
CONF_FILE = CONFIG_DIR / "artie.conf"
REPOS_DIR = ARTIE_DIR / "repos"
RELEASES_DIR = REPOS_DIR / "releases"
SNAPSHOTS_DIR = REPOS_DIR / "snapshots"
SETUP_LOG = ARTIE_DIR / "setup.log"


def _assert_path_is_dir(path: Path):
    assert path.exists(), f"Expected directory {path} to exist."
    assert path.is_dir(), f"Expected {path} to be a directory, not a file."


def _assert_path_is_file(path: Path):
    assert path.exists(), f"Expected file {path} to exist."
    assert path.is_file(), f"Expected {path} to be a regular file, not a directory or symlink."


def test_artie_base_layout():
    """
    The minimal skeleton installed by the lab should be present:

        /home/user/artie-manager/
            └── config/
                └── artie.conf   (empty file)

    Nothing else should exist yet.
    """
    _assert_path_is_dir(ARTIE_DIR)
    _assert_path_is_dir(CONFIG_DIR)
    _assert_path_is_file(CONF_FILE)

    # artie.conf must be completely empty to start with.
    size = CONF_FILE.stat().st_size
    assert size == 0, (
        f"{CONF_FILE} is expected to be empty at the start of the exercise "
        f"(size 0 bytes) but is currently {size} bytes long."
    )


def test_repositories_not_yet_created():
    """
    The repository directory tree must *not* be present before the student’s work.
    """
    assert not REPOS_DIR.exists(), (
        f"Repository root {REPOS_DIR} already exists. "
        "It should be created by the student as part of the task."
    )
    # For completeness, also ensure the sub-paths don’t exist independently.
    for subdir in (RELEASES_DIR, SNAPSHOTS_DIR):
        assert not subdir.exists(), (
            f"Directory {subdir} already exists. "
            "It must be created only after the student performs the task."
        )


def test_setup_log_absent():
    """
    No verification log should be present yet.
    """
    assert not SETUP_LOG.exists(), (
        f"Found unexpected file {SETUP_LOG}. "
        "The student should create it during the setup procedure."
    )