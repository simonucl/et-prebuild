# test_initial_state.py
#
# Pytest suite that validates the INITIAL filesystem / OS state
# before the student’s deployment-automation script is executed.
#
# The tests assert that everything required for starting the
# deployment is present, and equally important, that nothing that
# should only appear *after* a successful deployment is already on
# disk.  Any failure message should guide the student toward the
# exact piece of missing or pre-existing state that would break the
# grading rubric.

import os
import tarfile
from pathlib import Path

# Base paths
HOME = Path("/home/user")
APPS_DIR = HOME / "apps"
APP_V1_1_DIR = APPS_DIR / "app_v1.1"
APP_V1_2_DIR = APPS_DIR / "app_v1.2"          # must NOT exist yet
BACKUP_DIR = APPS_DIR / "backups" / "app_v1.1_backup"  # must NOT exist yet
CURRENT_SYMLINK = APPS_DIR / "current"

UPDATE_PACKAGES_DIR = HOME / "update_packages"
TARBALL = UPDATE_PACKAGES_DIR / "app_v1.2.tar.gz"

DEPLOY_LOG_DIR = HOME / "deployment_logs"
DEPLOY_HISTORY_FILE = DEPLOY_LOG_DIR / "deploy_history.csv"
STEP_LOG_FILE = DEPLOY_LOG_DIR / "update_steps.log"


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def assert_path_is_dir(p: Path, msg: str):
    assert p.exists(), f"Expected directory {p} is missing: {msg}"
    assert p.is_dir(), f"Path {p} exists but is not a directory: {msg}"


def assert_path_not_exists(p: Path, msg: str):
    assert not p.exists(), f"Path {p} should NOT exist yet: {msg}"


def assert_file_contains_exactly(path: Path, expected_bytes: bytes):
    assert path.exists(), f"Required file {path} is missing."
    assert path.is_file(), f"Path {path} exists but is not a regular file."
    data = path.read_bytes()
    assert data == expected_bytes, (
        f"File {path} contains unexpected bytes.\n"
        f"Expected: {expected_bytes!r}\n"
        f"Actual:   {data!r}"
    )


# ---------------------------------------------------------------------------
# Tests verifying the initial state
# ---------------------------------------------------------------------------

def test_base_directories_exist():
    """
    Sanity-check that the top-level directories required for the deployment
    are present.
    """
    assert_path_is_dir(APPS_DIR, "Top-level apps directory required.")
    assert_path_is_dir(APP_V1_1_DIR, "Directory for live v1.1 app required.")
    assert_path_is_dir(UPDATE_PACKAGES_DIR,
                       "Directory holding update packages required.")
    assert_path_is_dir(DEPLOY_LOG_DIR,
                       "Directory for deployment logs must already exist.")


def test_app_v1_1_mandatory_files_exist_and_version_correct():
    """
    Validate that app_v1.1 contains all files the deployment will duplicate.
    """
    required = ["app.py", "config.yml", "README.md", "VERSION"]
    for fname in required:
        fpath = APP_V1_1_DIR / fname
        assert fpath.exists(), f"Required file {fpath} is missing."
        assert fpath.is_file(), f"{fpath} exists but is not a regular file."

    # Ensure VERSION file has the exact expected contents.
    assert_file_contains_exactly(APP_V1_1_DIR / "VERSION", b"v1.1\n")


def test_symlink_current_points_to_v1_1():
    """
    The symbolic link .../current must exist and reference app_v1.1.
    """
    assert CURRENT_SYMLINK.exists(), (
        f"Symlink {CURRENT_SYMLINK} is missing. "
        "The application cannot be discovered without it."
    )
    assert CURRENT_SYMLINK.is_symlink(), (
        f"{CURRENT_SYMLINK} exists but is not a symbolic link."
    )
    target = os.readlink(CURRENT_SYMLINK)
    expected_target = str(APP_V1_1_DIR)
    assert target == expected_target, (
        f"Symlink {CURRENT_SYMLINK} points to {target!r}, "
        f"but it must point to {expected_target!r} in the initial state."
    )


def test_update_tarball_presence_and_basic_contents():
    """
    Ensure the update tarball exists and contains at least the mandatory files
    for version 1.2, including VERSION with the exact 'v1.2\\n' bytes.
    DEPLOYED_BY is NOT expected to be present yet.
    """
    assert TARBALL.exists(), f"Update package {TARBALL} is missing."
    assert TARBALL.is_file(), f"Path {TARBALL} exists but is not a file."

    mandatory_members = {
        "app_v1.2/app.py",
        "app_v1.2/config.yml",
        "app_v1.2/README.md",
        "app_v1.2/VERSION",
    }

    with tarfile.open(TARBALL, "r:gz") as tf:
        names = set(tf.getnames())

        missing = mandatory_members - names
        assert not missing, (
            f"Tarball {TARBALL} is missing required members: {sorted(missing)}"
        )

        # Check VERSION file content inside the tarball.
        version_member = tf.extractfile("app_v1.2/VERSION")
        assert version_member is not None, "VERSION file missing in tarball."
        data = version_member.read()
        assert data == b"v1.2\n", (
            f"VERSION inside tarball must be exactly b'v1.2\\n'; "
            f"got {data!r}"
        )


def test_no_backup_or_new_version_yet():
    """
    Backup directory and the new version directory should NOT exist
    prior to running the deployment automation.
    """
    assert_path_not_exists(BACKUP_DIR,
                           "Backup directory must not exist before deployment.")
    assert_path_not_exists(APP_V1_2_DIR,
                           "New version directory must not exist yet.")


def test_deployment_logs_initially_empty():
    """
    deploy_history.csv and update_steps.log must not pre-exist.  The directory
    itself should be empty.
    """
    assert DEPLOY_LOG_DIR.is_dir(), "Deployment log directory is missing."

    assert_path_not_exists(DEPLOY_HISTORY_FILE,
                           "deploy_history.csv should be created by the script, "
                           "not beforehand.")
    assert_path_not_exists(STEP_LOG_FILE,
                           "update_steps.log should be generated by the script, "
                           "not beforehand.")

    # Optionally ensure directory really is empty so nothing interferes.
    remaining_files = [
        p for p in DEPLOY_LOG_DIR.iterdir()
        if p.is_file() or p.is_symlink() or p.is_dir()
    ]
    assert not remaining_files, (
        f"deployment_logs directory must be empty initially, "
        f"but found: {', '.join(str(p) for p in remaining_files)}"
    )