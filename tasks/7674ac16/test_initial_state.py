# test_initial_state.py
#
# Pytest suite that validates the operating-system state **before** the student
# performs any action for the “Active Users Report” exercise.
#
# It checks only the pre-existing material that must already be on disk,
# never the artefacts the student is supposed to create later.

import pathlib

import pytest

HOME = pathlib.Path("/home/user")
ADMIN_DATA_DIR = HOME / "admin_data"
ACCOUNTS_INI = ADMIN_DATA_DIR / "accounts.ini"


@pytest.fixture(scope="module")
def expected_accounts_ini_contents():
    """
    The exact contents that must already be present in /home/user/admin_data/accounts.ini.

    A final newline is mandatory; the string below includes it implicitly via the
    trailing \n on the very last line.
    """
    return (
        "[alice]\n"
        "status = active\n"
        "role   = editor\n"
        "\n"
        "[bob]\n"
        "status = disabled\n"
        "role   = admin\n"
        "\n"
        "[carol]\n"
        "status = active\n"
        "role   = viewer\n"
        "\n"
        "[dave]\n"
        "status = pending\n"
        "role   = contributor\n"
        "\n"
        "[eve]\n"
        "status = active\n"
        "role   = admin\n"
    )


def test_admin_data_directory_exists():
    """
    The source directory with the configuration file must already be present.
    """
    assert ADMIN_DATA_DIR.is_dir(), (
        f"Required directory missing: {ADMIN_DATA_DIR}. "
        "It must exist before the student script runs."
    )


def test_accounts_ini_file_exists():
    """
    The INI file containing the account information must already be present.
    """
    assert ACCOUNTS_INI.is_file(), (
        f"Required file missing: {ACCOUNTS_INI}. "
        "It must exist before the student script runs."
    )


def test_accounts_ini_contents_exact(expected_accounts_ini_contents):
    """
    The INI file must contain the exact expected text, character-for-character,
    including blank lines, spacing, and the final newline.
    """
    actual = ACCOUNTS_INI.read_text(encoding="utf-8")
    expected = expected_accounts_ini_contents
    assert (
        actual == expected
    ), (
        f"The contents of {ACCOUNTS_INI} do not match the expected template.\n\n"
        f"--- Expected ---\n{expected!r}\n\n--- Found ---\n{actual!r}\n"
        "Ensure the file is present exactly as specified (including blank lines "
        "and the trailing newline)."
    )