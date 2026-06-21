# test_initial_state.py
# This test-suite validates the initial filesystem state **before**
# the student script is executed.  It checks that all required
# input files and directories exist **and** contain the exact
# expected contents.  Output artefacts are deliberately *not*
# tested here (per instructions).

import json
import csv
from pathlib import Path

# Base paths
SECURITY_AUDIT_DIR = Path("/home/user/security_audit")
INPUT_DIR = SECURITY_AUDIT_DIR / "input"
USERS_CSV = INPUT_DIR / "users.csv"
GROUPS_JSON = INPUT_DIR / "groups.json"


def test_required_directories_exist():
    """Ensure the expected directory hierarchy is present."""
    assert SECURITY_AUDIT_DIR.is_dir(), (
        f"Missing directory: {SECURITY_AUDIT_DIR}"
    )
    assert INPUT_DIR.is_dir(), (
        f"Missing directory: {INPUT_DIR}"
    )


def test_required_files_exist():
    """Ensure the expected input files are present."""
    assert USERS_CSV.is_file(), f"Missing file: {USERS_CSV}"
    assert GROUPS_JSON.is_file(), f"Missing file: {GROUPS_JSON}"


def test_users_csv_contents_are_exact():
    """
    The users.csv file must match the canonical contents exactly
    (apart from universal newline differences).
    """
    expected_rows = [
        ["username", "uid", "gid", "home", "shell", "access_level"],
        ["root", "0", "0", "/root", "/bin/bash", "admin"],
        ["alice", "1001", "1001", "/home/alice", "/bin/bash", "standard"],
        ["bob", "1002", "1002", "/home/bob", "/usr/sbin/nologin", "restricted"],
        ["carol", "1003", "1001", "/home/carol", "/bin/zsh", "standard"],
        ["dave", "999", "999", "/home/dave", "/bin/bash", "standard"],
        ["eve", "1004", "1004", "/home/eve", "/bin/fish", "standard"],
        ["mallory", "1200", "1002", "/home/mallory", "/bin/bash", "restricted"],
    ]

    with USERS_CSV.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        actual_rows = list(reader)

    assert actual_rows == expected_rows, (
        "The contents of users.csv differ from the expected canonical "
        "data.\n\nExpected:\n"
        f"{expected_rows}\n\nActual:\n{actual_rows}"
    )


def test_groups_json_contents_are_exact():
    """Validate that groups.json matches the expected data structure exactly."""
    expected_data = [
        {
            "gid": 0,
            "group_name": "root",
            "allowed_shells": ["/bin/bash"],
        },
        {
            "gid": 1001,
            "group_name": "developers",
            "allowed_shells": ["/bin/bash", "/bin/zsh"],
        },
        {
            "gid": 1002,
            "group_name": "ops",
            "allowed_shells": ["/usr/sbin/nologin"],
        },
        {
            "gid": 1004,
            "group_name": "interns",
            "allowed_shells": ["/bin/bash"],
        },
    ]

    with GROUPS_JSON.open(encoding="utf-8") as fh:
        actual_data = json.load(fh)

    assert actual_data == expected_data, (
        "The contents of groups.json differ from the expected canonical "
        "data.\n\nExpected:\n"
        f"{json.dumps(expected_data, indent=2)}\n\nActual:\n"
        f"{json.dumps(actual_data, indent=2)}"
    )