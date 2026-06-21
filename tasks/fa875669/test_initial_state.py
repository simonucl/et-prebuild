# test_initial_state.py
#
# This test-suite is executed *before* the student performs any work.
# It verifies that the workspace is completely clean so that the
# assignment can be carried out from scratch.

import os
import stat
import pytest

HOME = "/home/user"

# Final objects that the student will eventually create.
DIRS = [
    f"{HOME}/app",
    f"{HOME}/app/releases",
    f"{HOME}/app/releases/2023-09-01",
    f"{HOME}/app/releases/2023-10-15",
    f"{HOME}/app/releases/2023-11-30",
    f"{HOME}/app/shared",
    f"{HOME}/app/shared/logs",
]

FILES = [
    f"{HOME}/app/releases/2023-09-01/VERSION",
    f"{HOME}/app/releases/2023-10-15/VERSION",
    f"{HOME}/app/releases/2023-11-30/VERSION",
]

SYMLINKS = [
    f"{HOME}/app/current",
    f"{HOME}/app/previous",
    f"{HOME}/app/releases/2023-09-01/logs",
    f"{HOME}/app/releases/2023-10-15/logs",
    f"{HOME}/app/releases/2023-11-30/logs",
]

AUDIT_FILE = f"{HOME}/deployment_symlink_audit.log"


def _exists(path: str) -> bool:
    """
    os.path.lexists returns True for broken symlinks as well.
    That is exactly what we need for the pre-state check.
    """
    return os.path.lexists(path)


@pytest.mark.parametrize("path", DIRS)
def test_directories_do_not_exist_yet(path):
    assert not _exists(path), (
        f"Directory {path!r} already exists; the workspace is supposed to be "
        f"completely empty before the student starts."
    )


@pytest.mark.parametrize("path", FILES)
def test_version_files_do_not_exist_yet(path):
    assert not _exists(path), (
        f"File {path!r} already exists; the student must create it as part of "
        f"the assignment."
    )


@pytest.mark.parametrize("path", SYMLINKS)
def test_symlinks_do_not_exist_yet(path):
    assert not _exists(path), (
        f"Symlink {path!r} already exists; the student must create it as part "
        f"of the assignment."
    )


def test_audit_file_does_not_exist_yet():
    assert not _exists(AUDIT_FILE), (
        f"The audit file {AUDIT_FILE!r} is present, but it must be produced "
        f"by the student after all symlinks have been created."
    )


def test_nothing_under_home_user_app_exists():
    """
    Optional holistic check: if /home/user/app exists at all, it must be
    completely empty (no files, dirs, or entries).  This protects against
    partial leftover work.
    """
    app_path = f"{HOME}/app"
    if not os.path.exists(app_path):
        pytest.skip("/home/user/app does not exist – this is the expected and clean state.")

    # If the directory exists, ensure it is empty.
    with os.scandir(app_path) as it:
        entries = [entry.name for entry in it]
    assert entries == [], (
        "/home/user/app already exists and is not empty:\n"
        + "\n".join(f"  {name}" for name in entries)
        + "\nPlease start from a clean slate."
    )