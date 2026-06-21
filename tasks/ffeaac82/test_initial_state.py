# test_initial_state.py
#
# This pytest suite asserts that the filesystem is in the **initial**
# state expected *before* the student carries out any actions.
# If any of these tests fail, the environment is already wrong and
# the subsequent exercise cannot be validated reliably.
#
# Only the Python stdlib and pytest are used, per instructions.

import os
from pathlib import Path
import stat
import pytest

HOME = Path("/home/user")
PROJECT_DIR = HOME / "project"
I18N_DIR = PROJECT_DIR / "i18n"
EN_YAML = I18N_DIR / "en.yaml"
CONFIG_TOML = PROJECT_DIR / "config.toml"
UPDATE_LOG = PROJECT_DIR / "update_log.txt"


@pytest.fixture(scope="module")
def expected_files():
    """Return the exact expected contents of the initial files."""
    expected_en_yaml = (
        "# English (United States) translations\n"
        "welcome: \"Welcome\"\n"
        "login: \"Log in\"\n"
        "profile: \"Profile\"\n"
        "settings: \"Settings\"\n"
        "help: \"Help\"\n"
    )

    expected_config_toml = (
        "# Project build configuration\n"
        "[translations]\n"
        "supported = 5           # number of keys in the en.yaml catalogue\n"
        "\n"
        "[meta]\n"
        "last_updated = \"2023-09-01\"\n"
    )

    return {
        "en_yaml": expected_en_yaml,
        "config_toml": expected_config_toml,
    }


def _read_file(path: Path) -> str:
    """Read a text file as UTF-8 and normalise line endings to '\n'."""
    with path.open("r", encoding="utf-8") as fh:
        data = fh.read()
    # convert any CRLF to LF just in case (should not be present)
    return data.replace("\r\n", "\n")


def _assert_mode_0644(path: Path):
    """Assert that a file's mode bits are exactly 0644."""
    mode = stat.S_IMODE(path.stat().st_mode)
    assert (
        mode == 0o644
    ), f"File {path} should have permission 0644, found {oct(mode)} instead."


def test_directory_structure():
    """Check presence of /home/user/project and its sub-directories."""
    assert PROJECT_DIR.is_dir(), f"Missing directory: {PROJECT_DIR}"
    assert I18N_DIR.is_dir(), f"Missing directory: {I18N_DIR}"


def test_en_yaml_exists_and_contents(expected_files):
    """Verify that i18n/en.yaml exists with the exact initial content."""
    assert EN_YAML.is_file(), f"Missing file: {EN_YAML}"
    _assert_mode_0644(EN_YAML)

    content = _read_file(EN_YAML)
    # Strip a single trailing newline so we allow (or not) an EOF newline.
    content_stripped = content[:-1] if content.endswith("\n") else content
    assert (
        content_stripped == expected_files["en_yaml"][:-1]  # expected text without EOF newline
    ), (
        "The contents of en.yaml are not in the expected initial state.\n"
        "If you have already added the 'logout' key or changed other lines, "
        "please revert the file so that it matches the original:\n"
        f"{expected_files['en_yaml']}"
    )

    # Extra defensive check: ensure 'logout:' is **not** yet present.
    assert (
        "logout:" not in content
    ), "The key 'logout:' should NOT be present in the initial en.yaml."


def test_config_toml_exists_and_contents(expected_files):
    """Verify that config.toml exists with the exact initial content."""
    assert CONFIG_TOML.is_file(), f"Missing file: {CONFIG_TOML}"
    _assert_mode_0644(CONFIG_TOML)

    content = _read_file(CONFIG_TOML)
    content_stripped = content[:-1] if content.endswith("\n") else content
    assert (
        content_stripped == expected_files["config_toml"][:-1]
    ), (
        "config.toml does not match the expected initial content.\n"
        "Do not modify this file until instructed. Expected content:\n"
        f"{expected_files['config_toml']}"
    )

    # Defensive checks to ensure unsupported modifications haven't happened.
    assert (
        "supported = 6" not in content
    ), "supported should be 5 in the initial config.toml, not 6."
    assert (
        "\"2023-10-31\"" not in content
    ), "last_updated should be \"2023-09-01\" in the initial config.toml."


def test_update_log_absent():
    """update_log.txt must NOT exist yet."""
    assert (
        not UPDATE_LOG.exists()
    ), f"{UPDATE_LOG} should not exist in the initial state."