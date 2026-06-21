# test_initial_state.py
#
# This pytest suite validates that the operating-system state is correct
# *before* the student runs any commands for the “backup manifest → CSV”
# exercise.  It checks only the pre-existing directory and .txt manifest;
# it deliberately avoids looking for the .csv file that the student will
# create later.

import os
from pathlib import Path

BACKUP_DIR = Path("/home/user/backups/2023-05-10")
TXT_MANIFEST = BACKUP_DIR / "backup_manifest_20230510.txt"

EXPECTED_LINES = [
    "# Backup Manifest generated 2023-05-10",
    "/etc/passwd:2048",
    "/etc/group:1024",
    "/var/log/syslog:512000",
    "/home/user/data.txt:4096",
    "/usr/local/bin/script.sh:8192",
]


def test_backup_dir_exists_and_writable():
    assert BACKUP_DIR.exists(), f"Required directory {BACKUP_DIR} does not exist."
    assert BACKUP_DIR.is_dir(), f"{BACKUP_DIR} exists but is not a directory."
    assert os.access(BACKUP_DIR, os.W_OK), f"Directory {BACKUP_DIR} is not writable by the current user."


def test_manifest_file_exists():
    assert TXT_MANIFEST.exists(), f"Required file {TXT_MANIFEST} does not exist."
    assert TXT_MANIFEST.is_file(), f"{TXT_MANIFEST} exists but is not a regular file."


def test_manifest_file_contents():
    with TXT_MANIFEST.open("rb") as fh:
        raw = fh.read()

    # Split keeping newline characters to verify each line ends with '\n'.
    lines = raw.splitlines(keepends=True)

    assert len(lines) == 6, (
        f"{TXT_MANIFEST} should contain exactly 6 lines, found {len(lines)}."
    )

    for idx, (expected_plain, actual_raw) in enumerate(zip(EXPECTED_LINES, lines), start=1):
        actual_text = actual_raw.decode(errors="replace")
        assert actual_raw.endswith(b"\n"), (
            f"Line {idx} of {TXT_MANIFEST} must end with a single newline."
        )
        # Strip the newline for comparison with the expected plain text.
        actual_plain = actual_text.rstrip("\n")
        assert actual_plain == expected_plain, (
            f"Line {idx} mismatch in {TXT_MANIFEST}.\n"
            f"Expected: {expected_plain!r}\n"
            f"Found   : {actual_plain!r}"
        )