# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state **before**
# the learner starts working on the task.  It checks only the resources
# that must already be present and purposefully avoids touching any of
# the files or directories that the learner is expected to create.
#
# Requirements verified here:
#   1. /home/user/api_configs/ exists and is a directory.
#   2. That directory contains **exactly** three regular files:
#        - dev.json
#        - staging.json
#        - prod.json
#   3. Each of those three entries is a regular file (not a symlink,
#      not a directory, etc.).
#
# NOTE:  We intentionally do **not** test for /home/user/app,
#        /home/user/app/config.json, /home/user/api_configs/active,
#        or /home/user/symlink_audit.log because those are the artefacts
#        the learner is supposed to create.

import os
import stat
import pytest

API_CONFIG_DIR = "/home/user/api_configs"
EXPECTED_FILES = {"dev.json", "staging.json", "prod.json"}


def _mode(path: str) -> int:
    """Return the permission bits for *path* in octal (e.g. 0o755)."""
    return os.stat(path, follow_symlinks=False).st_mode & 0o777


@pytest.fixture(scope="module")
def api_config_entries():
    """
    Returns a set with all entries (files/directories) located directly
    inside /home/user/api_configs/.

    The fixture will fail early if the directory itself is missing or
    is not a directory.
    """
    # 1. The directory itself must exist.
    assert os.path.exists(API_CONFIG_DIR), (
        f"Expected directory {API_CONFIG_DIR!r} to exist, but it does not."
    )
    assert os.path.isdir(API_CONFIG_DIR), (
        f"Expected {API_CONFIG_DIR!r} to be a directory, "
        f"but it is not (type: {'symlink' if os.path.islink(API_CONFIG_DIR) else 'file'})."
    )

    # Collect directory entries.
    return set(os.listdir(API_CONFIG_DIR))


def test_api_config_directory_permissions():
    """Ensure /home/user/api_configs/ has the expected permission bits (0755)."""
    # Follow‐links is False—should not matter here, but is explicit.
    mode = _mode(API_CONFIG_DIR)
    assert mode == 0o755, (
        f"Directory {API_CONFIG_DIR!r} should have permissions 0755 "
        f"but has {oct(mode)} instead."
    )


def test_api_config_contains_only_expected_files(api_config_entries):
    """Verify that the directory contains exactly the expected three JSON files."""
    unexpected = api_config_entries - EXPECTED_FILES
    missing = EXPECTED_FILES - api_config_entries

    assert not missing, (
        f"Directory {API_CONFIG_DIR!r} is missing the following expected file(s): "
        f"{', '.join(sorted(missing))}"
    )
    assert not unexpected, (
        f"Directory {API_CONFIG_DIR!r} contains unexpected additional entries: "
        f"{', '.join(sorted(unexpected))}"
    )


@pytest.mark.parametrize("filename", sorted(EXPECTED_FILES))
def test_each_expected_file_is_regular_and_has_0644_permissions(filename):
    """Each expected JSON file must be a regular file (not a symlink) with 0644 permissions."""
    full_path = os.path.join(API_CONFIG_DIR, filename)

    # Existence checks
    assert os.path.exists(full_path), (
        f"Expected file {full_path!r} to exist, but it does not."
    )
    assert os.path.isfile(full_path), (
        f"Expected {full_path!r} to be a regular file, "
        f"but it is {'a symlink' if os.path.islink(full_path) else 'not a file'}."
    )

    # File should NOT be a symlink.
    assert not os.path.islink(full_path), (
        f"Expected {full_path!r} to be a regular file, not a symbolic link."
    )

    # Permission checks
    mode = _mode(full_path)
    assert mode == 0o644, (
        f"File {full_path!r} should have permissions 0644 "
        f"but has {oct(mode)} instead."
    )