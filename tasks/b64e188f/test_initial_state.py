# test_initial_state.py
#
# This test-suite validates the *initial* state of the host **before**
# the learner performs any action.  It deliberately avoids checking for
# any artefacts that the learner is expected to create (e.g.,
# /home/user/audit_log.json).  Only the pre-existing directory and file
# are examined.

import os
import stat
import pytest


DIR_PATH = "/home/user/audit_demo"
FILE_PATH = "/home/user/audit_demo/credentials.txt"


def _octal_mode(path):
    """
    Return the permission bits of *path* as a three-digit string, e.g. '755'.
    """
    mode = stat.S_IMODE(os.stat(path, follow_symlinks=False).st_mode)
    return f"{mode:03o}"


@pytest.fixture(scope="module")
def demo_dir_stat():
    if not os.path.exists(DIR_PATH):
        pytest.skip(f"{DIR_PATH} is missing on the target system.")
    return os.stat(DIR_PATH, follow_symlinks=False)


@pytest.fixture(scope="module")
def credentials_stat():
    if not os.path.exists(FILE_PATH):
        pytest.skip(f"{FILE_PATH} is missing on the target system.")
    return os.stat(FILE_PATH, follow_symlinks=False)


def test_directory_exists_and_is_directory(demo_dir_stat):
    assert stat.S_ISDIR(demo_dir_stat.st_mode), (
        f"{DIR_PATH} exists but is not a directory."
    )


def test_directory_permissions_are_755_before_change(demo_dir_stat):
    perms = _octal_mode(DIR_PATH)
    assert perms == "755", (
        f"Expected {DIR_PATH} to have mode 755, found {perms}."
    )


def test_credentials_file_exists_and_is_regular(credentials_stat):
    assert stat.S_ISREG(credentials_stat.st_mode), (
        f"{FILE_PATH} exists but is not a regular file."
    )


def test_credentials_permissions_are_644_before_change(credentials_stat):
    perms = _octal_mode(FILE_PATH)
    assert perms == "644", (
        f"Expected {FILE_PATH} to have mode 644, found {perms}."
    )


def test_credentials_file_has_expected_structure():
    """
    Basic sanity check that the credentials file contains three
    newline-separated key=value pairs with the expected keys.
    (We do NOT assert on the secret values themselves.)
    """
    with open(FILE_PATH, "r", encoding="utf-8") as fh:
        lines = [ln.strip() for ln in fh.readlines() if ln.strip()]

    assert len(lines) >= 3, (
        f"{FILE_PATH} should contain at least three non-empty lines."
    )

    expected_prefixes = ["username=", "password=", "token="]
    for idx, prefix in enumerate(expected_prefixes):
        assert lines[idx].startswith(prefix), (
            f"Line {idx+1} of {FILE_PATH} should start with '{prefix}'."
        )