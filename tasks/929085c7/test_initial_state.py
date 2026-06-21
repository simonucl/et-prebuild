# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present BEFORE the student runs their compound shell-command solution.
#
# It intentionally does **not** look for the final artefact
# (/home/user/dev_utils/perm_report.txt) because that file should not exist yet.
#
# Checked pre-conditions
# ---------------------
# 1. Directory /home/user/dev_utils
#       • exists
#       • is a directory
#       • has permission bits 0755 (rwxr-xr-x) — NO set-gid bit
# 2. Three helper scripts inside that directory
#       • build.sh, test.sh, deploy.sh all exist as regular files
#       • each has mode 0644 (rw-r--r--)
#
# Any deviation from the above will fail the tests with a descriptive message.

import os
import stat
import pwd
import grp
import pytest

DEV_UTILS_DIR = "/home/user/dev_utils"
SCRIPTS = ["build.sh", "test.sh", "deploy.sh"]


def _mode(path):
    """Return the permission bits (including special bits) for *path* as an int."""
    return stat.S_IMODE(os.stat(path, follow_symlinks=False).st_mode)


def _as_octal_str(mode_int):
    """Return mode_int as at least three-digit octal string (e.g. '755', '2750')."""
    octal = oct(mode_int)[2:]  # Strip '0o'
    return octal.rjust(3, "0")


def test_dev_utils_directory_exists_and_is_0755():
    assert os.path.exists(DEV_UTILS_DIR), (
        f"Expected directory {DEV_UTILS_DIR} to exist, but it is missing."
    )
    assert os.path.isdir(DEV_UTILS_DIR), (
        f"Expected {DEV_UTILS_DIR} to be a directory, but it is not."
    )

    mode = _mode(DEV_UTILS_DIR)
    expected = 0o755
    assert mode == expected, (
        f"{DEV_UTILS_DIR} should have permissions 0755 (rwxr-xr-x) before the student "
        f"runs their command, but has {_as_octal_str(mode)} instead."
    )

    # Extra safety: ensure the set-gid bit is not already set.
    assert not (mode & stat.S_ISGID), (
        f"{DEV_UTILS_DIR} unexpectedly already has the set-gid bit. Initial mode must "
        f"be 0755, not {_as_octal_str(mode)}."
    )


@pytest.mark.parametrize("script_name", SCRIPTS)
def test_helper_scripts_exist_and_are_0644(script_name):
    script_path = os.path.join(DEV_UTILS_DIR, script_name)

    assert os.path.exists(script_path), (
        f"Script {script_path} should exist in the initial state, but it is missing."
    )
    assert os.path.isfile(script_path), (
        f"Expected {script_path} to be a regular file, but it is not."
    )

    mode = _mode(script_path)
    expected = 0o644
    assert mode == expected, (
        f"{script_path} should have permissions 0644 (rw-r--r--) before the student "
        f"runs their command, but has {_as_octal_str(mode)} instead."
    )