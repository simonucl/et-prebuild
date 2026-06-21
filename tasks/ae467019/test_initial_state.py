# test_initial_state.py
#
# This test-suite validates the *initial* state of the workspace **before**
# the student makes any changes.  It ensures that the two configuration
# drafts contain the expected placeholders and that the optional log file
# (if present) is in an acceptable state.
#
# DO NOT MODIFY THIS FILE.

from pathlib import Path
import re
import pytest

# Root of the workspace
ROOT = Path("/home/user/etl_pipeline")
CONFIG_YAML = ROOT / "config" / "config.yaml"
PIPELINE_TOML = ROOT / "config" / "pipeline.toml"
UPDATE_LOG = ROOT / "logs" / "update_config.log"


@pytest.fixture(scope="module")
def yaml_expected() -> str:
    """
    Exact byte-for-byte content that the draft config.yaml must contain
    before the student starts editing.
    """
    return (
        "source:\n"
        "  type: #TODO\n"
        "  host: #TODO\n"
        "  port: #TODO\n"
        "  database: #TODO\n"
        "  user: #TODO\n"
        "  password: #TODO\n"
        "\n"
        "transformations: []\n"
        "\n"
        "destination:\n"
        "  type: #TODO\n"
        "  path: #TODO\n"
    )


@pytest.fixture(scope="module")
def toml_expected() -> str:
    """
    Exact byte-for-byte content that the draft pipeline.toml must contain
    before the student starts editing.
    """
    return (
        "[default]\n"
        "timezone = \"UTC\"\n"
        "retry = 3\n"
    )


def test_directories_exist():
    """Basic sanity-check that required directories are present."""
    assert ROOT.is_dir(), f"Workspace root {ROOT} is missing."
    config_dir = ROOT / "config"
    logs_dir = ROOT / "logs"
    assert config_dir.is_dir(), f"Expected directory {config_dir} is missing."
    assert logs_dir.is_dir(), f"Expected directory {logs_dir} is missing."


def test_config_yaml_initial_content(yaml_expected):
    """
    The draft YAML file must exist and contain the exact placeholder content
    provided in the task description.
    """
    assert CONFIG_YAML.is_file(), f"Missing file: {CONFIG_YAML}"
    actual = CONFIG_YAML.read_text(encoding="utf-8")
    # We compare after stripping a single trailing newline to be tolerant of
    # editors that automatically add one.
    assert actual.rstrip("\n") == yaml_expected.rstrip(
        "\n"
    ), (
        f"{CONFIG_YAML} does not match the expected initial placeholder "
        "content.  Make sure the student starts from the correct draft."
    )


def test_pipeline_toml_initial_content(toml_expected):
    """
    The draft TOML file must exist and contain only the [default] table
    exactly as specified (no extra tables, no extra keys).
    """
    assert PIPELINE_TOML.is_file(), f"Missing file: {PIPELINE_TOML}"
    actual = PIPELINE_TOML.read_text(encoding="utf-8")
    assert actual.rstrip("\n") == toml_expected.rstrip(
        "\n"
    ), (
        f"{PIPELINE_TOML} must contain only the original [default] table "
        "with timezone and retry placeholders."
    )


def test_update_log_optional_state():
    """
    The update_config.log file may or may not pre-exist.
    If it exists, its last line must end with the literal text
    'configs updated' (existing historical entries are allowed).
    """
    if not UPDATE_LOG.exists():
        pytest.skip(f"{UPDATE_LOG} does not exist yet (this is acceptable).")

    assert UPDATE_LOG.is_file(), f"{UPDATE_LOG} exists but is not a file."

    last_line = UPDATE_LOG.read_text(encoding="utf-8").splitlines()[-1]
    assert last_line.strip().endswith(
        "configs updated"
    ), (
        f"The last line of {UPDATE_LOG} must end with "
        "'configs updated' if the file is present."
    )


def test_no_unexpected_files():
    """
    Guard-rail test: ensure no extra files or directories are present in
    /home/user/etl_pipeline besides the ones that should exist at this stage.
    """
    expected_paths = {
        ROOT / "config",
        ROOT / "logs",
        CONFIG_YAML,
        PIPELINE_TOML,
    }
    # The log file is optional.
    if UPDATE_LOG.exists():
        expected_paths.add(UPDATE_LOG)

    unexpected = [p for p in ROOT.rglob("*") if p.is_file() and p not in expected_paths]

    assert (
        not unexpected
    ), f"Unexpected files present before the exercise starts: {unexpected}"