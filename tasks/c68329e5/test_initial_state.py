# test_initial_state.py
"""
Pytest suite that validates the *initial* filesystem state
before the student generates any reports or logs.

Only standard‐library modules and pytest are used.
"""

import os
import stat
import pytest

HOME = "/home/user"
AUDIT_DIR = os.path.join(HOME, "audit_data")
PASSWD_FILE = os.path.join(AUDIT_DIR, "mock_passwd")


@pytest.fixture(scope="module")
def passwd_lines():
    """Read the mock_passwd file and yield its stripped, non-empty lines."""
    if not os.path.isfile(PASSWD_FILE):
        pytest.skip(f"{PASSWD_FILE} is missing; cannot perform further tests.")
    with open(PASSWD_FILE, "r", encoding="utf-8") as fp:
        return [ln.rstrip("\n") for ln in fp]


def test_audit_directory_exists():
    """The /home/user/audit_data directory must exist and be a directory."""
    assert os.path.isdir(AUDIT_DIR), (
        f"Required directory {AUDIT_DIR!r} is missing or is not a directory."
    )

    # Optional: check directory permissions (should be 0755)
    mode = stat.S_IMODE(os.stat(AUDIT_DIR).st_mode)
    expected_mode = 0o755
    assert mode == expected_mode, (
        f"{AUDIT_DIR} has mode {oct(mode)}, expected {oct(expected_mode)}."
    )


def test_mock_passwd_exists_and_permissions():
    """The mock_passwd file must exist with the correct permissions."""
    assert os.path.isfile(PASSWD_FILE), (
        f"Required file {PASSWD_FILE!r} not found."
    )

    mode = stat.S_IMODE(os.stat(PASSWD_FILE).st_mode)
    expected_mode = 0o644
    assert mode == expected_mode, (
        f"{PASSWD_FILE} has mode {oct(mode)}, expected {oct(expected_mode)}."
    )


def test_mock_passwd_has_expected_format(passwd_lines):
    """
    Every line in mock_passwd must follow the traditional 7-field
    passwd(5) layout (colon-separated).
    """
    assert passwd_lines, f"{PASSWD_FILE} appears to be empty."

    for idx, line in enumerate(passwd_lines, start=1):
        fields = line.split(":")
        assert len(fields) == 7, (
            f"Line {idx} in {PASSWD_FILE} has {len(fields)} fields "
            f"(expected 7): {line!r}"
        )


def test_mock_passwd_contains_required_shells(passwd_lines):
    """
    The mock_passwd file must contain at least one account
    with each of the following login shells, so the student
    can demonstrate filtering:
        • /usr/sbin/nologin
        • /bin/false
    """
    shells = [line.split(":")[-1] for line in passwd_lines]

    assert "/usr/sbin/nologin" in shells, (
        f"{PASSWD_FILE} lacks an account with shell '/usr/sbin/nologin'."
    )
    assert "/bin/false" in shells, (
        f"{PASSWD_FILE} lacks an account with shell '/bin/false'."
    )