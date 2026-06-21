# test_initial_state.py
#
# This test-suite asserts that the brand-new Linux host is still in its
# pristine state *before* the student creates the provisioning skeleton.
#
# Expected pre-task truth:
#   • No /home/user/provisioning tree (or any of its children) exists.
#   • Consequently, no skeleton files (README.md, providers.tf, hosts.ini,
#     bootstrap.log) exist either.
#
# If any of these paths already exist the test will fail, explaining exactly
# which artefact is pre-existing.

import os
import pytest
from pathlib import Path

HOME = Path("/home/user")

# All directories/files that must *NOT* exist yet.
DIRS_SHOULD_NOT_EXIST = [
    HOME / "provisioning",
    HOME / "provisioning" / "terraform",
    HOME / "provisioning" / "ansible",
    HOME / "provisioning" / "logs",
]

FILES_SHOULD_NOT_EXIST = [
    HOME / "provisioning" / "README.md",
    HOME / "provisioning" / "terraform" / "providers.tf",
    HOME / "provisioning" / "ansible" / "hosts.ini",
    HOME / "provisioning" / "logs" / "bootstrap.log",
]


@pytest.mark.parametrize("path", DIRS_SHOULD_NOT_EXIST)
def test_directories_do_not_exist_yet(path: Path):
    assert not path.exists(), (
        f"Pre-task check failed: directory {path} already exists.\n"
        "The task instructions require you to create it yourself, "
        "so the container must start without it."
    )


@pytest.mark.parametrize("path", FILES_SHOULD_NOT_EXIST)
def test_files_do_not_exist_yet(path: Path):
    assert not path.exists(), (
        f"Pre-task check failed: file {path} already exists.\n"
        "The task instructions require you to create it yourself, "
        "so the container must start without it."
    )


def test_no_provisioning_tree_fragment_exists():
    """
    Sanity guard: ensure nothing under /home/user/provisioning/* exists at all.
    If something slipped through the explicit lists above, this generic test
    will still catch it.
    """
    provisioning_root = HOME / "provisioning"
    if provisioning_root.exists():
        # Collect any artefacts that already exist to report them clearly.
        existing_items = [
            str(p) for p in provisioning_root.rglob("*") if p.exists()
        ]
        pytest.fail(
            "Pre-task check failed: /home/user/provisioning already exists with "
            f"the following unexpected contents:\n- " + "\n- ".join(existing_items)
        )