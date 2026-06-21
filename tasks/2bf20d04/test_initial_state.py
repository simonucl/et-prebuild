# test_initial_state.py
#
# This pytest suite validates the *initial* state of the OS / filesystem
# before the learner performs any actions for the deployment task.
#
# What we CHECK (must already be present):
#   • /home/user/deploy directory exists.
#   • /home/user/deploy/update_app.sh exists and is a regular file.
#   • The helper script has at least one executable bit set.
#
# What we deliberately DO **NOT** CHECK:
#   • Any of the artefacts the learner is supposed to create
#     (/home/user/app_update.cron or the systemd unit files).
#   • We avoid asserting on paths/contents that belong to learner output.

import os
import stat
from pathlib import Path
import pytest

SCRIPT_PATH = Path("/home/user/deploy/update_app.sh")


def test_deploy_directory_exists():
    """The /home/user/deploy directory must already exist."""
    deploy_dir = SCRIPT_PATH.parent
    assert deploy_dir.is_dir(), (
        f"Required directory '{deploy_dir}' is missing. "
        "Create it (and the helper script inside) before running the task."
    )


def test_helper_script_exists():
    """The helper script must be present as a regular file."""
    assert SCRIPT_PATH.is_file(), (
        f"Required helper script '{SCRIPT_PATH}' is missing. "
        "It should be provided before you attempt the scheduling steps."
    )


def test_helper_script_is_executable():
    """The helper script must have at least one executable bit set."""
    mode = SCRIPT_PATH.stat().st_mode
    executable = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert executable, (
        f"Helper script '{SCRIPT_PATH}' is not executable. "
        "Ensure it has executable permissions (e.g., chmod +x)."
    )