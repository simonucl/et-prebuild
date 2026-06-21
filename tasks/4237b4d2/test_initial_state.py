# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the filesystem
# before the student performs any credential-rotation actions.

import os
import stat
import textwrap
import pytest

HOME = "/home/user"
APP_CFG_DIR = os.path.join(HOME, "app", "config")

SETTINGS_YML = os.path.join(APP_CFG_DIR, "settings.yml")
CREDENTIALS_TOML = os.path.join(APP_CFG_DIR, "credentials.toml")
ROTATION_LOG = os.path.join(HOME, "rotation.log")

EXPECTED_SETTINGS_CONTENT = textwrap.dedent(
    """\
    database:
      user: admin
      password: OldPass123
    aws:
      access_key: OLDACCESSKEY
      secret_key: OLDSECRETKEY
      region: us-east-1
    """
)

EXPECTED_CREDENTIALS_CONTENT = textwrap.dedent(
    """\
    [default]
    username = "admin"
    password = "OldPass123"
    token    = "OLDTOKEN987"
    """
)


def _assert_file_mode(path: str, expected_mode: int) -> None:
    """
    Assert that `path` has mode `expected_mode` (e.g., 0o644).

    Parameters
    ----------
    path : str
        Absolute path to file being checked.
    expected_mode : int
        Octal representation of the expected mode (e.g., 0o644).
    """
    mode = stat.S_IMODE(os.stat(path).st_mode)
    assert (
        mode == expected_mode
    ), f"{path} should have mode {oct(expected_mode)}, found {oct(mode)}"


@pytest.mark.parametrize(
    "path,expected_content",
    [
        (SETTINGS_YML, EXPECTED_SETTINGS_CONTENT),
        (CREDENTIALS_TOML, EXPECTED_CREDENTIALS_CONTENT),
    ],
)
def test_files_exist_with_correct_content_and_mode(path, expected_content):
    """
    Verify that the required configuration files exist, have the correct
    permissions (0644), and contain exactly the expected initial text.
    """
    assert os.path.isfile(path), f"Expected file {path} is missing"

    # Check file permissions (0644)
    _assert_file_mode(path, 0o644)

    with open(path, "r", encoding="utf-8") as fh:
        actual = fh.read()

    # Ignore a single trailing newline difference by using rstrip("\n")
    assert (
        actual.rstrip("\n") == expected_content.rstrip("\n")
    ), f"Contents of {path} do not match the expected initial state."


def test_rotation_log_does_not_exist_initially():
    """
    The rotation log should NOT exist before the student runs their solution.
    """
    assert not os.path.exists(
        ROTATION_LOG
    ), f"{ROTATION_LOG} should not exist before credential rotation."