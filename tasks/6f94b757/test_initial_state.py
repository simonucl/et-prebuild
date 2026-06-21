# test_initial_state.py
"""
pytest suite that validates the PRE-EXISTING DIRECTORY TREE *before* the student
performs any actions.

This file checks only the initial conditions—**it does NOT test for any output
artefacts such as backups, logs, or post-update state files.**
"""

from pathlib import Path
import pytest
import os

# Base paths
HOME = Path("/home/user")
NETCONFIGS = HOME / "netconfigs"
OLD_DIR = NETCONFIGS / "old"
NEW_DIR = NETCONFIGS / "new"
ETC_DIR = HOME / "etc"

# Mapping of expected files and their exact contents (byte-for-byte).
EXPECTED_FILES = {
    OLD_DIR / "router.conf": b"hostname router-old\nip route 0.0.0.0/0 via 192.168.0.1\n",
    NEW_DIR / "router.conf": b"hostname router-new\nip route 0.0.0.0/0 via 10.0.0.1\n",
    OLD_DIR / "switch.conf": b"hostname switch-old\nvlan 10\n",
    NEW_DIR / "switch.conf": b"hostname switch-new\nvlan 20\n",
}

# Expected symbolic links (link_path -> expected_target)
EXPECTED_SYMLINKS = {
    ETC_DIR / "router.conf": OLD_DIR / "router.conf",
    ETC_DIR / "switch.conf": OLD_DIR / "switch.conf",
}

###############################################################################
# Directory existence                                                          #
###############################################################################
@pytest.mark.parametrize(
    "path",
    [
        NETCONFIGS,
        OLD_DIR,
        NEW_DIR,
        ETC_DIR,
    ],
)
def test_directories_exist(path):
    assert path.is_dir(), f"Required directory {path} is missing or not a directory."


###############################################################################
# File existence and contents                                                  #
###############################################################################
@pytest.mark.parametrize("file_path, expected_bytes", EXPECTED_FILES.items())
def test_config_files_exist_with_correct_contents(file_path, expected_bytes):
    assert file_path.is_file(), f"Required file {file_path} is missing."
    actual_bytes = file_path.read_bytes()
    assert (
        actual_bytes == expected_bytes
    ), f"Contents of {file_path} do not match expected.\nExpected:\n{expected_bytes.decode()}\nActual:\n{actual_bytes.decode()}"


###############################################################################
# Symbolic links                                                               #
###############################################################################
@pytest.mark.parametrize("link_path, expected_target", EXPECTED_SYMLINKS.items())
def test_symlinks_point_to_old_config(link_path, expected_target):
    assert link_path.exists(), f"Symlink {link_path} is missing."
    assert link_path.is_symlink(), f"{link_path} exists but is not a symbolic link."
    # Resolve the symlink target without following additional links.
    target = Path(os.readlink(link_path))
    # Convert to absolute path in case a relative link was used.
    if not target.is_absolute():
        target = (link_path.parent / target).resolve()
    assert (
        target == expected_target
    ), f"Symlink {link_path} points to {target}, expected {expected_target}."


###############################################################################
# Ensure no premature artefacts                                                #
###############################################################################
def test_no_output_artefacts_yet():
    """Backup directory, log, and state dump must NOT exist before the student runs their solution."""
    disallowed_paths = [
        NETCONFIGS / "backup",
        HOME / "symlink_update.log",
        HOME / "post_update_state.txt",
    ]
    for p in disallowed_paths:
        assert not p.exists(), (
            f"Found {p} but this should not exist before the student performs "
            "the required actions."
        )