# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state
# BEFORE the student performs any backup rotation actions.
#
# It deliberately *fails* if anything has already been altered.
#
# Assumptions documented in the task description:
#   • /home/user/configs exists and contains exactly
#       httpd.conf, nginx.conf, ssh.conf
#   • /home/user/config_backup does NOT yet exist
#   • /home/user/backup_report.txt does NOT yet exist
#
# Only stdlib + pytest are used.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
CONFIGS_DIR = HOME / "configs"
BACKUP_DIR = HOME / "config_backup"
REPORT_FILE = HOME / "backup_report.txt"

EXPECTED_CONTENTS = {
    "httpd.conf": "ServerRoot /etc/httpd\nListen 80\n",
    "nginx.conf": "worker_processes  1;\nerror_log  /var/log/nginx/error.log;\n",
    "ssh.conf": "Port 22\nPermitRootLogin no\n",
}


def test_configs_directory_exists():
    assert CONFIGS_DIR.exists(), f"Expected directory {CONFIGS_DIR} to exist."
    assert CONFIGS_DIR.is_dir(), f"{CONFIGS_DIR} exists but is not a directory."


def test_configs_directory_contents_exact():
    # List only regular files (ignore '.', '..', potential stray dirs)
    files = sorted(p.name for p in CONFIGS_DIR.iterdir() if p.is_file())
    expected_files = sorted(EXPECTED_CONTENTS.keys())
    assert files == expected_files, (
        f"{CONFIGS_DIR} should contain exactly {expected_files}, "
        f"but currently contains {files}."
    )


@pytest.mark.parametrize("fname,expected_content", EXPECTED_CONTENTS.items())
def test_individual_conf_file_contents(fname, expected_content):
    file_path = CONFIGS_DIR / fname
    assert file_path.exists(), f"Missing expected file: {file_path}"
    with file_path.open("r", encoding="utf-8") as fh:
        content = fh.read()
    assert (
        content == expected_content
    ), f"File {file_path} has unexpected content:\n{content!r}"


def test_backup_directory_absent_initially():
    assert not BACKUP_DIR.exists(), (
        f"Backup directory {BACKUP_DIR} should NOT exist before the task starts."
    )


def test_conf_files_not_yet_in_backup():
    # Even if someone pre-created the directory, ensure no .conf files reside there.
    if BACKUP_DIR.exists():
        conf_files = [p.name for p in BACKUP_DIR.iterdir() if p.is_file() and p.suffix == ".conf"]
        assert (
            len(conf_files) == 0
        ), f"{BACKUP_DIR} should contain no .conf files initially, found: {conf_files}"


def test_backup_report_absent_initially():
    assert not REPORT_FILE.exists(), (
        f"Report file {REPORT_FILE} should not exist before running the backup."
    )