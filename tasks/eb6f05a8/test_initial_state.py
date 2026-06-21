# test_initial_state.py
"""
Pytest suite that validates the **initial** operating-system / filesystem state
*before* the student executes any part of the assignment.

We check that:
1. The home directory /home/user exists.
2. Neither of the two deliverable files already exist.
3. If the parent directories for those files exist, that is fine—the
   assignment allows students to re-use them—but the target files
   themselves must be absent so that the student can create them.

Only the Python standard library and pytest are used.
"""

import os
import stat
import pytest

HOME = "/home/user"

FIREWALL_AUDIT_DIR = os.path.join(HOME, "firewall_audit")
FIREWALL_CONFIGS_DIR = os.path.join(HOME, "firewall_configs")

LOG_FILE = os.path.join(
    FIREWALL_AUDIT_DIR, "2024-05-21_firewall_update.log"
)

RULES_FILE = os.path.join(
    FIREWALL_CONFIGS_DIR, "iptables-2024-05-21.rules"
)


def _human_perms(mode: int) -> str:
    """Return a rwxrwxrwx-style string for an st_mode integer."""
    # Only the last nine bits (permission bits)
    perms = ["r", "w", "x"] * 3
    bits = bin(mode & 0o777)[2:].rjust(9, "0")
    return "".join(ch if bit == "1" else "-" for ch, bit in zip(perms, bits))


def test_home_directory_exists():
    assert os.path.isdir(HOME), (
        f"Expected the base directory {HOME} to exist and be a directory."
    )
    st_mode = os.stat(HOME).st_mode
    perms = stat.S_IMODE(st_mode)
    assert perms & stat.S_IRUSR, (
        f"The directory {HOME} must be readable by its owner. "
        f"Current permissions: {_human_perms(perms)}"
    )


@pytest.mark.parametrize("path,description", [
    (LOG_FILE, "firewall audit log file"),
    (RULES_FILE, "iptables rules file"),
])
def test_target_files_do_not_yet_exist(path, description):
    assert not os.path.exists(path), (
        f"The {description} ({path}) already exists. "
        f"The student task is to create this file, so the initial state "
        f"should not contain it."
    )


def test_parent_directories_state():
    """
    The assignment allows the parent directories to pre-exist,
    but they must *not* already contain the deliverable files.
    """
    for directory, child in [
        (FIREWALL_AUDIT_DIR, LOG_FILE),
        (FIREWALL_CONFIGS_DIR, RULES_FILE),
    ]:
        if os.path.exists(directory):
            assert os.path.isdir(directory), (
                f"Expected {directory} to be a directory (if it exists)."
            )
            # Defensive check: make sure the deliverable file is not inside.
            assert not os.path.exists(child), (
                f"Found unexpected pre-existing file {child} inside {directory}. "
                f"It should be absent at the start of the exercise."
            )