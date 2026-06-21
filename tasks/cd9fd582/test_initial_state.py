# test_initial_state.py
"""
Pytest suite to validate the initial operating-system / filesystem
state BEFORE the student performs any action.

This file checks that:
1. /home/user/backups exists and has permission 0755.
2. /home/user/backups/backup_filelist.txt exists, is mode 0644,
   and contains the exact expected eight-line catalogue.
3. The “to-be-created” restore directory and preview file do NOT
   yet exist — guaranteeing a clean slate for the student.
"""

import os
import stat
import pytest

BACKUP_DIR = "/home/user/backups"
BACKUP_FILE = "/home/user/backups/backup_filelist.txt"
RESTORE_DIR = "/home/user/restores"
PREVIEW_FILE = "/home/user/restores/preview_to_restore.lst"

EXPECTED_CATALOGUE = (
    "/etc/nginx/nginx.conf\n"
    "/etc/ssh/sshd_config\n"
    "/var/www/html/index.html\n"
    "/etc/mysql/my.cnf\n"
    "/home/user/.bashrc\n"
    "/etc/supervisor/supervisord.conf\n"
    "/var/log/syslog\n"
    "/etc/httpd/conf/httpd.conf\n"
)


def _mode(path):
    """Return only the permission bits (e.g. 0o755) of a path."""
    return stat.S_IMODE(os.lstat(path).st_mode)


def test_backup_directory_exists_and_permissions():
    assert os.path.exists(BACKUP_DIR), (
        f"Required directory {BACKUP_DIR} is missing."
    )
    assert os.path.isdir(BACKUP_DIR), (
        f"{BACKUP_DIR} exists but is not a directory."
    )
    expected_mode = 0o755
    actual_mode = _mode(BACKUP_DIR)
    assert actual_mode == expected_mode, (
        f"{BACKUP_DIR} permissions are {oct(actual_mode)}, "
        f"expected {oct(expected_mode)}."
    )


def test_backup_file_exists_permissions_and_content():
    assert os.path.exists(BACKUP_FILE), (
        f"Required catalogue file {BACKUP_FILE} is missing."
    )
    assert os.path.isfile(BACKUP_FILE), (
        f"{BACKUP_FILE} exists but is not a regular file."
    )

    expected_mode = 0o644
    actual_mode = _mode(BACKUP_FILE)
    assert actual_mode == expected_mode, (
        f"{BACKUP_FILE} permissions are {oct(actual_mode)}, "
        f"expected {oct(expected_mode)}."
    )

    with open(BACKUP_FILE, "r", encoding="utf-8") as fh:
        contents = fh.read()

    assert contents == EXPECTED_CATALOGUE, (
        f"{BACKUP_FILE} contents do not match the expected catalogue.\n"
        "Expected:\n"
        f"{EXPECTED_CATALOGUE!r}\n"
        "Got:\n"
        f"{contents!r}"
    )


@pytest.mark.parametrize("path_description, path", [
    ("restore directory", RESTORE_DIR),
    ("preview file", PREVIEW_FILE),
])
def test_restore_objects_do_not_yet_exist(path_description, path):
    assert not os.path.exists(path), (
        f"The {path_description} {path} already exists, but it should "
        f"be created by the student’s solution, not pre-existing."
    )