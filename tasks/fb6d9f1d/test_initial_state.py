# test_initial_state.py
#
# This pytest suite validates the host’s *initial* filesystem state
# before the student performs any restoration actions.  It asserts:
#   1. Snapshot files exist and contain the pristine reference data.
#   2. Live service files exist, contain the drifted data, and *differ*
#      from the pristine snapshots.
#   3. The restore work-directory exists and is empty.
#
# All paths are absolute as required.

import hashlib
from pathlib import Path
import pytest

HOME = Path("/home/user")

SNAPSHOT_DIR = HOME / "backup_snapshot_2023-01-15"
SERVICE_DIR = HOME / "service_config"
WORK_DIR = HOME / "restore_work"

SNAPSHOT_HTTPD = SNAPSHOT_DIR / "httpd.conf"
SNAPSHOT_APPENV = SNAPSHOT_DIR / "app.env"
SERVICE_HTTPD = SERVICE_DIR / "httpd.conf"
SERVICE_APPENV = SERVICE_DIR / "app.env"

# --------------------------------------------------------------------------- #
# Expected file contents (including a trailing newline).
# --------------------------------------------------------------------------- #
EXPECTED_SNAPSHOT_HTTPD = (
    'ServerRoot "/etc/httpd"\n'
    "Listen 80\n"
    "LoadModule dir_module modules/mod_dir.so\n"
    "Include conf/extra/httpd-vhosts.conf\n"
)

EXPECTED_SNAPSHOT_APPENV = (
    "DB_HOST=prod-db.internal\n"
    "DB_PORT=5432\n"
    "DB_USER=app\n"
    "DB_PASS=secret\n"
    "APP_ENV=production\n"
)

EXPECTED_SERVICE_HTTPD = (
    'ServerRoot "/etc/httpd"\n'
    "Listen 8080\n"
    "LoadModule dir_module modules/mod_dir.so\n"
)

EXPECTED_SERVICE_APPENV = (
    "DB_HOST=prod-db.internal\n"
    "DB_PORT=5432\n"
    "DB_USER=app\n"
    "APP_ENV=production\n"
)

# Helper --------------------------------------------------------------------- #


def md5sum(data: bytes) -> str:
    return hashlib.md5(data, usedforsecurity=False).hexdigest()


def assert_file_content(path: Path, expected: str):
    assert path.is_file(), f"Expected file {path} to exist."
    actual = path.read_text(encoding="utf-8")
    assert (
        actual == expected
    ), f"Content mismatch in {path}. Expected:\n{expected!r}\nGot:\n{actual!r}"


# Tests ---------------------------------------------------------------------- #


def test_snapshot_files_exist_and_pristine():
    """
    Snapshot files must exist with the pristine reference contents.
    """
    for path in (SNAPSHOT_HTTPD, SNAPSHOT_APPENV):
        assert path.is_file(), f"Missing snapshot file: {path}"

    assert_file_content(SNAPSHOT_HTTPD, EXPECTED_SNAPSHOT_HTTPD)
    assert_file_content(SNAPSHOT_APPENV, EXPECTED_SNAPSHOT_APPENV)

    # Quick sanity check that the two snapshot files are distinct.
    assert md5sum(SNAPSHOT_HTTPD.read_bytes()) != md5sum(
        SNAPSHOT_APPENV.read_bytes()
    ), "Snapshot files unexpectedly have identical checksums."


def test_service_config_files_exist_and_contain_drift():
    """
    Service config files must exist, embody the drift, and differ from snapshot.
    """
    for path in (SERVICE_HTTPD, SERVICE_APPENV):
        assert path.is_file(), f"Missing service config file: {path}"

    # Validate drifted contents.
    assert_file_content(SERVICE_HTTPD, EXPECTED_SERVICE_HTTPD)
    assert_file_content(SERVICE_APPENV, EXPECTED_SERVICE_APPENV)

    # Ensure they actually differ from pristine versions.
    assert (
        md5sum(SERVICE_HTTPD.read_bytes())
        != md5sum(SNAPSHOT_HTTPD.read_bytes())
    ), "service_config/httpd.conf is already identical to snapshot; expected drift."

    assert (
        md5sum(SERVICE_APPENV.read_bytes())
        != md5sum(SNAPSHOT_APPENV.read_bytes())
    ), "service_config/app.env is already identical to snapshot; expected drift."


def test_restore_work_directory_exists_and_is_empty():
    """
    /home/user/restore_work/ must exist and be empty before any restoration.
    """
    assert WORK_DIR.is_dir(), f"Missing work directory: {WORK_DIR}"
    leftover = list(WORK_DIR.iterdir())
    assert (
        not leftover
    ), f"restore_work directory is expected to be empty but contains: {leftover}"