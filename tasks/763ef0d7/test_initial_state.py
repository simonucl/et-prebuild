# test_initial_state.py
"""
Pytest suite validating that the operating-system/Filesystem is in the
expected *initial* state – i.e. before the student creates the reusable
firewall package.

These checks guarantee that no artefacts from a previous run are present,
so the student starts with a clean slate.

Rules enforced here (mirroring the specification):

1. The directory /home/user/profile_firewall/ must NOT exist yet.
2. Consequently, none of the four required files must be present:
     • /home/user/profile_firewall/rules_ipv4.conf
     • /home/user/profile_firewall/rules_ipv6.conf
     • /home/user/profile_firewall/apply_firewall.sh
     • /home/user/profile_firewall/firewall_validation.log
3. /home/user itself must exist (sanity check).
"""

import os
import stat
import pytest

HOME_DIR = "/home/user"
FIREWALL_DIR = os.path.join(HOME_DIR, "profile_firewall")

FILES_EXPECTED_LATER = [
    os.path.join(FIREWALL_DIR, "rules_ipv4.conf"),
    os.path.join(FIREWALL_DIR, "rules_ipv6.conf"),
    os.path.join(FIREWALL_DIR, "apply_firewall.sh"),
    os.path.join(FIREWALL_DIR, "firewall_validation.log"),
]


def test_home_directory_exists():
    """
    Sanity-check that the user's home directory is present
    and is indeed a directory.
    """
    assert os.path.isdir(HOME_DIR), (
        f"Expected home directory {HOME_DIR} to exist and be a directory, "
        "but it is missing."
    )


def test_firewall_directory_absent():
    """
    The firewall directory should NOT exist before the student runs their
    provisioning script.
    """
    assert not os.path.exists(FIREWALL_DIR), (
        f"Directory {FIREWALL_DIR} already exists. "
        "The environment is not in the required initial state."
    )


@pytest.mark.parametrize("filepath", FILES_EXPECTED_LATER)
def test_no_firewall_files_present(filepath):
    """
    None of the firewall artefact files should exist yet.
    Parametrised over the four files that will exist after successful
    completion of the task.
    """
    assert not os.path.exists(filepath), (
        f"File {filepath} is present, but the initial state requires it to be "
        "absent. Ensure the workspace is clean before beginning the task."
    )