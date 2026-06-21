# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state
# before the student begins making any changes.  It confirms that
# the repository was cloned to /home/user/projects/deploy with the
# expected baseline configuration files and that no update log has
# been generated yet.
#
# Only the Python standard library and pytest are used.

import difflib
from pathlib import Path

DEPLOY_DIR = Path("/home/user/projects/deploy")
CONFIG_YAML = DEPLOY_DIR / "config.yaml"
SETTINGS_TOML = DEPLOY_DIR / "settings.toml"
UPDATE_LOG = DEPLOY_DIR / "update_log.txt"


def _assert_text_equal(actual: str, expected: str, file_path: Path) -> None:
    """
    Helper: assert that two multi-line strings are identical.
    On failure a unified diff of the mismatch is shown.
    """
    if actual != expected:
        diff = "\n".join(
            difflib.unified_diff(
                expected.splitlines(),
                actual.splitlines(),
                fromfile="expected",
                tofile=str(file_path),
                lineterm="",
            )
        )
        # The diff is included in the assertion message for easier debugging.
        assert False, f"Contents of {file_path} do not match expected baseline:\n{diff}"


def test_deploy_directory_exists():
    """The main repository directory must exist and be a directory."""
    assert DEPLOY_DIR.is_dir(), f"Expected directory {DEPLOY_DIR} to exist."


def test_config_yaml_initial_contents():
    """config.yaml must exist with the exact unmodified baseline contents."""
    assert CONFIG_YAML.is_file(), f"Missing required file {CONFIG_YAML}."

    expected = (
        "app:\n"
        "  name: \"AcmeApp\"\n"
        "  version: \"1.2.3\"\n"
        "  env: \"staging\"\n"
        "\n"
        "services:\n"
        "  auth:\n"
        "    enabled: true\n"
        "    port: 8080\n"
        "  api:\n"
        "    enabled: true\n"
        "    port: 9000\n"
    )  # NOTE: the final '\n' above represents the required trailing newline.

    actual = CONFIG_YAML.read_text(encoding="utf-8")
    _assert_text_equal(actual, expected, CONFIG_YAML)


def test_settings_toml_initial_contents():
    """settings.toml must exist with the exact unmodified baseline contents."""
    assert SETTINGS_TOML.is_file(), f"Missing required file {SETTINGS_TOML}."

    expected = (
        "[general]\n"
        "owner = \"devops team\"\n"
        "timeout = 30\n"
        "\n"
        "[features]\n"
        "logging = true\n"
        "metrics = false\n"
    )  # NOTE: the final '\n' above represents the required trailing newline.

    actual = SETTINGS_TOML.read_text(encoding="utf-8")
    _assert_text_equal(actual, expected, SETTINGS_TOML)


def test_update_log_not_present_yet():
    """
    The verification log must NOT exist yet.  It will be created
    by the student after patching the configuration files.
    """
    assert not UPDATE_LOG.exists(), (
        f"{UPDATE_LOG} should not be present before any modifications. "
        "Found an unexpected update log."
    )