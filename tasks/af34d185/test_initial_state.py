# test_initial_state.py
#
# This suite validates that the *initial* filesystem state required for the
# “artifact summary” task is present and correct.  It deliberately avoids
# checking for any of the *output* paths (/home/user/logs or its contents),
# in compliance with the grading-infrastructure guidelines.

import os
import stat
import pytest

ARTIFACTS_DIR = "/home/user/repos/artifacts"
INVENTORY_CSV = os.path.join(ARTIFACTS_DIR, "inventory.csv")

EXPECTED_PERMS_DIR = 0o755
EXPECTED_PERMS_FILE = 0o644

EXPECTED_CSV_LINES = [
    "filename,size_bytes",
    "core-1.2.3.jar,2048",
    "utils-4.5.6.jar,4096",
    "plugin-0.9.1.zip,1024",
    "readme.txt,512",
    "cli-2.0.0.tar.gz,3072",
]


def _mode(path):
    """
    Convenience helper: returns the filesystem mode bits (e.g. 0o755) of *path*.
    """
    return stat.S_IMODE(os.stat(path).st_mode)


def test_artifacts_directory_exists_and_permissions():
    """
    The directory /home/user/repos/artifacts must exist, be a directory, and
    have exactly the expected permissions (0755).
    """
    assert os.path.exists(ARTIFACTS_DIR), (
        f"Required directory missing: {ARTIFACTS_DIR}"
    )
    assert os.path.isdir(ARTIFACTS_DIR), (
        f"Expected {ARTIFACTS_DIR} to be a directory, but it is not."
    )

    actual_mode = _mode(ARTIFACTS_DIR)
    assert actual_mode == EXPECTED_PERMS_DIR, (
        f"{ARTIFACTS_DIR} permissions are {oct(actual_mode)}, expected "
        f"{oct(EXPECTED_PERMS_DIR)} (rwxr-xr-x)."
    )


def test_inventory_csv_exists_and_permissions():
    """
    The inventory file must exist, be a regular file, and have the correct
    permissions (0644).
    """
    assert os.path.exists(INVENTORY_CSV), (
        f"Required inventory file missing: {INVENTORY_CSV}"
    )
    assert os.path.isfile(INVENTORY_CSV), (
        f"Expected {INVENTORY_CSV} to be a file, but it is not."
    )

    actual_mode = _mode(INVENTORY_CSV)
    assert actual_mode == EXPECTED_PERMS_FILE, (
        f"{INVENTORY_CSV} permissions are {oct(actual_mode)}, expected "
        f"{oct(EXPECTED_PERMS_FILE)} (rw-r--r--)."
    )


def test_inventory_csv_contents_exact():
    """
    The CSV file must contain exactly six lines (one header + five entries)
    and must match the expected data verbatim (apart from the final newline).
    """
    with open(INVENTORY_CSV, encoding="utf-8") as fp:
        contents = fp.read().splitlines()

    assert contents == EXPECTED_CSV_LINES, (
        "Contents of inventory CSV do not match the expected data.\n"
        f"Expected lines:\n{EXPECTED_CSV_LINES}\n"
        f"Actual lines:\n{contents}"
    )