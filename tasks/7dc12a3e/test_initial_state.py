# test_initial_state.py
#
# This pytest suite validates the *starting* filesystem state that should
# exist **before** the learner carries out any of the required commands.
#
# Rules verified here:
# 1. /home/user/pt_reports exists.
# 2. /home/user/pt_reports/scan_results_critical.txt exists and contains
#    exactly the expected three-line payload.
# 3. /home/user/archives must NOT yet exist.
# 4. No files called pt_reports_backup.tar.gz or
#    pt_reports_backup_MANIFEST.txt are anywhere under /home/user.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
PT_DIR = HOME / "pt_reports"
SCAN_FILE = PT_DIR / "scan_results_critical.txt"

ARCHIVES_DIR = HOME / "archives"
BACKUP_TARBALL = ARCHIVES_DIR / "pt_reports_backup.tar.gz"
MANIFEST_FILE = ARCHIVES_DIR / "pt_reports_backup_MANIFEST.txt"


def test_pt_reports_directory_exists():
    assert PT_DIR.is_dir(), (
        f"Expected directory {PT_DIR} is missing. "
        "It should be present before any action is taken."
    )


def test_scan_results_file_exists_and_has_expected_contents():
    assert SCAN_FILE.is_file(), (
        f"Expected file {SCAN_FILE} is missing. "
        "The raw scan results must exist before taking a backup."
    )

    expected_contents = (
        "CVE-2023-1234: OpenSSH user enumeration vulnerability\n"
        "CVE-2022-3456: Apache Struts remote code execution\n"
        "CVE-2021-0001: Sample vulnerability\n"
    )

    with SCAN_FILE.open(encoding="utf-8") as fh:
        actual_contents = fh.read()

    assert actual_contents == expected_contents, (
        f"The contents of {SCAN_FILE} do not match the expected baseline. "
        "Ensure no file corruption or modification has occurred."
    )


def test_archives_directory_does_not_yet_exist():
    assert not ARCHIVES_DIR.exists(), (
        f"Directory {ARCHIVES_DIR} should NOT exist yet. "
        "Creating it is part of the exercise for the learner."
    )


@pytest.mark.parametrize(
    "path_obj",
    [BACKUP_TARBALL, MANIFEST_FILE],
    ids=["tarball", "manifest"],
)
def test_backup_files_do_not_yet_exist(path_obj: Path):
    assert not path_obj.exists(), (
        f"File {path_obj} should NOT exist before the learner runs their commands."
    )


def test_no_stray_backup_files_anywhere_under_home():
    """
    Guarantee that no file named pt_reports_backup.tar.gz or
    pt_reports_backup_MANIFEST.txt is lurking anywhere under /home/user.
    """
    disallowed_names = {"pt_reports_backup.tar.gz", "pt_reports_backup_MANIFEST.txt"}
    for root, _, files in os.walk(HOME):
        for fname in files:
            if fname in disallowed_names:
                pytest.fail(
                    f"Found unexpected pre-existing file: {Path(root) / fname}. "
                    "The backup should not exist yet."
                )