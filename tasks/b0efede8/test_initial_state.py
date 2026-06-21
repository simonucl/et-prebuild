# test_initial_state.py
#
# This test-suite validates the *initial* operating-system state **before**
# the learner creates the required “/home/user/dev_env_ready.txt” flag file.
#
# Expectations for the *initial* state:
#   1. The home directory `/home/user` must already exist.
#   2. The file `/home/user/dev_env_ready.txt` must NOT exist yet.
#   3. No other files that start with the prefix `dev_env_ready.` may exist
#      in `/home/user` (e.g. `dev_env_ready.txt.bak`, `dev_env_ready.log`, …).
#
# If any of the assertions below fail, it means the playground has been
# tampered with or a previous attempt has left behind artefacts that must be
# removed before the learner starts the current exercise.

import os
import glob
import pytest

HOME_DIR = "/home/user"
FLAG_FILE = os.path.join(HOME_DIR, "dev_env_ready.txt")
FLAG_PREFIX_GLOB = os.path.join(HOME_DIR, "dev_env_ready.*")


def _human_readable_list(paths):
    """Return a human-readable, comma-separated list of paths."""
    return ", ".join(sorted(paths)) if paths else "(none)"


def test_home_directory_exists():
    assert os.path.isdir(
        HOME_DIR
    ), (
        f"The expected home directory '{HOME_DIR}' is missing.\n"
        "The exercise requires this directory to be present."
    )


def test_flag_file_absent_initially():
    assert not os.path.exists(
        FLAG_FILE
    ), (
        f"The file '{FLAG_FILE}' already exists, but the learner is "
        "supposed to create it.  Please remove it so the exercise starts "
        "from a clean slate."
    )


def test_no_other_dev_env_ready_files_exist():
    # Look for *any* files that begin with 'dev_env_ready.' (including .txt)
    matches = [p for p in glob.glob(FLAG_PREFIX_GLOB) if os.path.isfile(p)]
    assert not matches, (
        "Unexpected file(s) found that would interfere with the exercise:\n"
        f"  {_human_readable_list(matches)}\n"
        "Remove these file(s) before starting."
    )