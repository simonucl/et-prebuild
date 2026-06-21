# test_initial_state.py
#
# Pytest suite that verifies the **initial** filesystem/OS state
# before the student performs any actions for the “configs” assignment.
#
# Rules & scope:
#   • Uses only the Python stdlib + pytest.
#   • Checks for presence / absence of ONLY the items that must exist
#     at the very start.  (It deliberately says nothing about the
#     files/symlinks the student is expected to create later.)
#   • Provides clear, readable assertion messages to help diagnose
#     environment problems quickly.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
PROJECTS_DIR = HOME / "projects"
CONFIGS_DIR = PROJECTS_DIR / "configs"
AVAILABLE_DIR = CONFIGS_DIR / "available"
ENABLED_DIR = CONFIGS_DIR / "enabled"

APP_CONF = AVAILABLE_DIR / "app.conf"
DB_CONF = AVAILABLE_DIR / "db.conf"
OLD_SYMLINK = ENABLED_DIR / "old.conf"


def _assert_is_dir(path: Path):
    assert path.exists(), f"Expected directory '{path}' to exist, but it is missing."
    assert path.is_dir(), f"'{path}' exists but is not a directory."


def _assert_is_regular_file(path: Path):
    assert path.exists(), f"Expected file '{path}' to exist, but it is missing."
    assert path.is_file(), f"'{path}' exists but is not a regular file."
    assert not path.is_symlink(), f"'{path}' should be a regular file, not a symlink."


def _assert_is_dangling_symlink(link_path: Path, target_rel: str):
    assert link_path.exists() or link_path.is_symlink(), (
        f"Expected symlink '{link_path}' to exist, but it is missing."
    )
    assert link_path.is_symlink(), f"'{link_path}' exists but is not a symlink."

    # Verify the link target
    link_target = os.readlink(link_path)
    assert link_target == target_rel, (
        f"Symlink '{link_path}' points to '{link_target}', "
        f"expected '{target_rel}'."
    )

    # Confirm the link is *broken* (dangling)
    resolved_target = (link_path.parent / link_target).resolve()
    assert not resolved_target.exists(), (
        f"Symlink '{link_path}' should be broken, "
        f"but its target '{resolved_target}' unexpectedly exists."
    )


def test_directory_layout_exists():
    """Top-level directory structure must already be present."""
    _assert_is_dir(PROJECTS_DIR)
    _assert_is_dir(CONFIGS_DIR)
    _assert_is_dir(AVAILABLE_DIR)
    _assert_is_dir(ENABLED_DIR)


def test_available_contains_app_and_db_conf():
    """The 'available/' directory must start with two regular configuration files."""
    _assert_is_regular_file(APP_CONF)
    _assert_is_regular_file(DB_CONF)


def test_enabled_contains_exactly_one_broken_symlink():
    """
    The 'enabled/' directory must initially contain only the dangling
    symlink 'old.conf' that points to '../available/old.conf'.
    """
    # Collect non-hidden entries (exclude '.' and '..')
    entries = [p.name for p in ENABLED_DIR.iterdir()]
    assert entries, "The 'enabled/' directory is empty; expected at least 'old.conf'."
    assert entries == ["old.conf"], (
        f"'enabled/' contains unexpected items: {entries}; "
        "it should contain exactly one entry: 'old.conf'."
    )

    # Validate that 'old.conf' is a dangling symlink
    _assert_is_dangling_symlink(OLD_SYMLINK, "../available/old.conf")