# test_initial_state.py
#
# This test-suite validates the state of the operating system *before*
# the student carries out the task described in the assignment.
#
# What we assert here must already be true when the tests are collected:
#
# 1. The directory /home/user/site exists and is writable by the current user.
# 2. The file /home/user/site/accounts.tsv exists,
#    is world-readable (permission mode 0644),
#    and contains exactly the four TAB-separated lines specified in the
#    task description (with Unix LF line endings only).
# 3. There is NO file named /home/user/site/user_email.csv yet.
#
# Only Python’s standard library and pytest are used.

import os
import stat
import pwd
import pytest

SITE_DIR = "/home/user/site"
ACCOUNTS_FILE = os.path.join(SITE_DIR, "accounts.tsv")
OUTPUT_FILE = os.path.join(SITE_DIR, "user_email.csv")

EXPECTED_LINES = [
    "101\talice\talice@example.com\tadmin\n",
    "102\tbob\tbob@domain.com\teditor\n",
    "103\tcarol\tcarol@mail.net\tviewer\n",
    "104\tdave\tdave@site.org\teditor\n",
]


def _mode_str(mode: int) -> str:
    "Return a rwxrwxrwx string representation of a mode."
    return stat.filemode(mode)


def _perm_bits(path: str) -> int:
    "Return the permission bits (lowest 9 bits) of a file."
    return stat.S_IMODE(os.stat(path).st_mode)


def test_site_directory_exists_and_writable():
    assert os.path.isdir(SITE_DIR), (
        f"Required directory {SITE_DIR} does not exist."
    )

    # Check write access for the current real UID.
    assert os.access(SITE_DIR, os.W_OK), (
        f"Directory {SITE_DIR} is not writable by the current user "
        f"({pwd.getpwuid(os.getuid()).pw_name})."
    )


def test_accounts_file_basic_properties():
    assert os.path.isfile(ACCOUNTS_FILE), (
        f"Required file {ACCOUNTS_FILE} does not exist."
    )

    # Check permission bits are exactly 0644.
    perm = _perm_bits(ACCOUNTS_FILE)
    expected_perm = 0o644
    assert perm == expected_perm, (
        f"{ACCOUNTS_FILE} must have mode 0644 "
        f"(rw-r--r--), but has {_mode_str(perm)} instead."
    )


def test_accounts_file_contents():
    with open(ACCOUNTS_FILE, "rb") as f:
        content = f.read()

    # Ensure only LF line endings.
    assert b"\r" not in content, (
        f"{ACCOUNTS_FILE} must use Unix LF line endings only (\\n). "
        "Found CR characters (\\r)."
    )

    lines = content.decode("utf-8").splitlines(keepends=True)

    assert len(lines) == 4, (
        f"{ACCOUNTS_FILE} must contain exactly 4 lines, found {len(lines)}."
    )

    assert lines == EXPECTED_LINES, (
        f"{ACCOUNTS_FILE} contents differ from what is expected.\n"
        "Expected lines:\n"
        + "".join(EXPECTED_LINES)
        + "\nActual lines:\n"
        + "".join(lines)
    )

    # Validate each line has 4 TAB-separated columns, first is numeric.
    for idx, line in enumerate(lines, start=1):
        parts = line.rstrip("\n").split("\t")
        assert len(parts) == 4, (
            f"Line {idx} of {ACCOUNTS_FILE} should have exactly 4 TAB-"
            f"separated columns, found {len(parts)}."
        )
        assert parts[0].isdigit(), (
            f"First column of line {idx} should be numeric user_id, "
            f"got {parts[0]!r}."
        )


def test_output_file_does_not_exist_yet():
    assert not os.path.exists(OUTPUT_FILE), (
        f"The output file {OUTPUT_FILE} should NOT exist before the task "
        "is performed, but it is already present."
    )