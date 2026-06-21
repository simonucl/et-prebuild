# test_initial_state.py
#
# Pytest suite that verifies the PRE-EXISTING state of the sandbox
# before the learner carries out the “Acme-Payments” firewall task.
#
# IMPORTANT:
#   • This file purposefully checks ONLY the resources that are supposed
#     to exist at the very beginning of the exercise.
#   • It must NOT touch or mention any of the files the learner is
#     expected to create later (e.g. “current.rules”, release logs, …).

import os
import stat
import pytest

HOME = "/home/user"
FIREWALL_DIR = os.path.join(HOME, "firewall")
BASE_RULES = os.path.join(FIREWALL_DIR, "base.rules")
RELEASE_LOGS_DIR = os.path.join(HOME, "release_logs")

EXPECTED_BASE_RULES_CONTENT = (
    "*filter\n"
    ":INPUT DROP [0:0]\n"
    ":FORWARD DROP [0:0]\n"
    ":OUTPUT ACCEPT [0:0]\n"
    "-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT\n"
    "-A INPUT -i lo -j ACCEPT\n"
    "COMMIT\n"
)


def _is_world_readable(path: str) -> bool:
    """Return True if 'others' have read permission on the file."""
    st_mode = os.stat(path).st_mode
    return bool(st_mode & stat.S_IROTH)


def _is_writable_by_user(path: str) -> bool:
    """
    Return True if the current real UID can open the path in write
    mode (for directories, create files; for files, write bytes).
    """
    return os.access(path, os.W_OK)


@pytest.mark.resource
def test_firewall_directory_exists_and_writable():
    assert os.path.isdir(
        FIREWALL_DIR
    ), f"Required directory '{FIREWALL_DIR}' is missing."
    assert _is_writable_by_user(
        FIREWALL_DIR
    ), f"Directory '{FIREWALL_DIR}' must be writable by the current user."


@pytest.mark.resource
def test_release_logs_directory_exists_and_writable():
    assert os.path.isdir(
        RELEASE_LOGS_DIR
    ), f"Required directory '{RELEASE_LOGS_DIR}' is missing."
    assert _is_writable_by_user(
        RELEASE_LOGS_DIR
    ), f"Directory '{RELEASE_LOGS_DIR}' must be writable by the current user."


@pytest.mark.resource
def test_base_rules_file_present_and_exact_content(tmp_path):
    # 1. Presence and readability
    assert os.path.isfile(
        BASE_RULES
    ), f"Base rules file '{BASE_RULES}' is missing."
    assert os.access(
        BASE_RULES, os.R_OK
    ), f"Base rules file '{BASE_RULES}' must be readable."

    # 2. Content must match exactly (byte-for-byte)
    with open(BASE_RULES, "r", encoding="utf-8") as fh:
        actual = fh.read()

    assert (
        actual == EXPECTED_BASE_RULES_CONTENT
    ), (
        "The contents of '{0}' are not exactly as expected.\n\n"
        "----- EXPECTED -----\n{1!r}\n"
        "------ ACTUAL ------\n{2!r}\n"
        "--------------------".format(BASE_RULES, EXPECTED_BASE_RULES_CONTENT, actual)
    )

    # 3. File should be at most 0644 (not writable by group/others)
    mode = os.stat(BASE_RULES).st_mode & 0o777
    assert (
        mode & 0o022 == 0
    ), f"File permissions for '{BASE_RULES}' are too permissive: {oct(mode)}; expected 0644 or stricter."

    # 4. File must be world-readable (others have r bit)
    assert _is_world_readable(
        BASE_RULES
    ), f"File '{BASE_RULES}' must be world-readable (others should have read permission)."