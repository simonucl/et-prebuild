# test_initial_state.py
#
# This pytest suite verifies that the operating-system state is correct
# *before* the student performs any action.  It checks only the supplied
# artefacts and intentionally ignores the files that the student is
# expected to create later on.

import os
from pathlib import Path

AUDIT_DIR = Path("/home/user/audit")
SOURCE_CSV = AUDIT_DIR / "source_permissions.csv"

# The CSV file must contain **exactly** this content, including the
# single trailing newline at the very end.
EXPECTED_CSV_CONTENT = (
    "path,user,group,perms\n"
    "/etc/passwd,root,root,644\n"
    "/etc/shadow,root,root,640\n"
    "/var/log/syslog,syslog,adm,640\n"
    "/home/user/.bashrc,user,user,600\n"
    "/usr/bin/sudo,root,root,4755\n"
    "/tmp/shared.txt,guest,guest,666\n"
    "/var/www/html/index.html,www-data,www-data,644\n"
)


def test_audit_directory_exists():
    """
    The /home/user/audit directory must exist and be a directory.
    """
    assert AUDIT_DIR.exists(), (
        f"Required directory {AUDIT_DIR} does not exist."
    )
    assert AUDIT_DIR.is_dir(), (
        f"{AUDIT_DIR} exists but is not a directory."
    )


def test_source_permissions_csv_exists():
    """
    The source_permissions.csv file must exist inside /home/user/audit.
    """
    assert SOURCE_CSV.exists(), (
        f"Required file {SOURCE_CSV} is missing."
    )
    assert SOURCE_CSV.is_file(), (
        f"{SOURCE_CSV} exists but is not a regular file."
    )


def test_source_permissions_csv_contents():
    """
    The source_permissions.csv file must match the exact expected content,
    including the final newline.
    """
    actual_content = SOURCE_CSV.read_text(encoding="utf-8")
    assert actual_content == EXPECTED_CSV_CONTENT, (
        "The contents of "
        f"{SOURCE_CSV} do not match the expected initial state.\n\n"
        "Expected:\n"
        f"{EXPECTED_CSV_CONTENT!r}\n\n"
        "Actual:\n"
        f"{actual_content!r}"
    )