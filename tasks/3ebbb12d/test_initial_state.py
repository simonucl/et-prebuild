# test_initial_state.py
#
# This pytest suite validates *the initial state* of the operating-system /
# filesystem before the student performs any action for the “daily backup”
# exercise.
#
# The tests assert that:
#   • The source directory /home/user/projects/configs exists with exactly
#     four specific *.conf files and nothing else.
#   • Each *.conf file contains the expected (verbatim) text.
#   • The destination directory /home/user/backups exists.
#   • No backup archive matching the pattern  YYYYMMDD_configs_backup.tar.gz
#     is present yet (the student will create it).
#   • The backups directory is otherwise empty except for an optional
#     backup_manifest.log.
#
# If any assertion fails the student’s environment is not in the expected
# “clean” starting condition and subsequent evaluation would be unreliable.

import re
import stat
from pathlib import Path

import pytest

CONFIGS_DIR = Path("/home/user/projects/configs")
BACKUPS_DIR = Path("/home/user/backups")
ARCHIVE_REGEX = re.compile(r"^\d{8}_configs_backup\.tar\.gz$")

EXPECTED_CONFIG_FILES = {
    "httpd.conf": (
        "# Apache HTTPD configuration\n"
        "ServerName localhost\n"
        "Listen 80\n"
    ),
    "sshd.conf": (
        "# OpenSSH daemon configuration\n"
        "Port 22\n"
        "PermitRootLogin no\n"
    ),
    "database.conf": (
        "# Example DB configuration\n"
        "host=127.0.0.1\n"
        "port=5432\n"
    ),
    "app.conf": (
        "# Application configuration\n"
        "debug=true\n"
        "workers=4\n"
    ),
}


def test_configs_directory_exists_and_mode():
    """
    /home/user/projects/configs must exist, be a directory and have mode 0755.
    """
    assert CONFIGS_DIR.is_dir(), (
        f"Expected directory '{CONFIGS_DIR}' to exist."
    )
    mode = stat.S_IMODE(CONFIGS_DIR.stat().st_mode)
    assert mode == 0o755, (
        f"Directory '{CONFIGS_DIR}' should have mode 0755 "
        f"but has {oct(mode)}."
    )


def test_configs_directory_contents():
    """
    The configs directory must contain *exactly* the four expected files (no
    more, no less).
    """
    entries = sorted(p.name for p in CONFIGS_DIR.iterdir())
    expected = sorted(EXPECTED_CONFIG_FILES.keys())
    assert entries == expected, (
        f"'{CONFIGS_DIR}' should contain exactly {expected} but contains {entries}."
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_CONFIG_FILES.items())
def test_each_conf_file_content(filename, expected_content):
    """
    Each conf file must have the exact expected content (including newline
    ordering).
    """
    file_path = CONFIGS_DIR / filename
    assert file_path.is_file(), f"Expected file '{file_path}' to exist."
    with file_path.open("r", encoding="utf-8") as fh:
        data = fh.read()
    assert data == expected_content, (
        f"Content of '{file_path}' does not match the expected reference text."
    )


def test_backups_directory_exists_and_mode():
    """
    /home/user/backups must exist, be a directory and have mode 0755.
    """
    assert BACKUPS_DIR.is_dir(), (
        f"Expected directory '{BACKUPS_DIR}' to exist."
    )
    mode = stat.S_IMODE(BACKUPS_DIR.stat().st_mode)
    assert mode == 0o755, (
        f"Directory '{BACKUPS_DIR}' should have mode 0755 "
        f"but has {oct(mode)}."
    )


def test_backups_directory_clean():
    """
    The backups directory must **not** yet contain any daily backup archives.
    It may contain an existing backup_manifest.log. No other files are allowed.
    """
    unexpected_archives = []
    unexpected_other_files = []

    for entry in BACKUPS_DIR.iterdir():
        # backup_manifest.log is allowed
        if entry.name == "backup_manifest.log":
            continue
        if ARCHIVE_REGEX.match(entry.name):
            unexpected_archives.append(entry.name)
        else:
            unexpected_other_files.append(entry.name)

    assert not unexpected_archives, (
        f"Found pre-existing backup archive(s) in '{BACKUPS_DIR}': "
        f"{unexpected_archives}. The directory must be clean before the task."
    )
    assert not unexpected_other_files, (
        f"Found unexpected file(s) in '{BACKUPS_DIR}': {unexpected_other_files}. "
        "Only an optional 'backup_manifest.log' may exist before the task starts."
    )