# test_initial_state.py
#
# This test-suite validates the *initial* state of the repository **before**
# the student registers the new experiment.  It asserts that:
#
# 1. /home/user/mlops_project/config.yml contains *only* the first experiment
#    (exp_001) and nothing about exp_002.
# 2. /home/user/mlops_project/pyproject.toml still has version "0.1.0" and
#    does NOT yet have a `last_experiment` line.
# 3. /home/user/experiment_update.log does not exist.
#
# Any failure message should clearly indicate what is missing or out of place.

from pathlib import Path
import pytest

HOME = Path("/home/user")
PROJECT_DIR = HOME / "mlops_project"
CONFIG_YML = PROJECT_DIR / "config.yml"
PYPROJECT_TOML = PROJECT_DIR / "pyproject.toml"
AUDIT_LOG = HOME / "experiment_update.log"


@pytest.fixture(scope="module")
def config_content():
    """Return the list of stripped lines in config.yml."""
    if not CONFIG_YML.exists():
        pytest.fail(f"Expected configuration file is missing: {CONFIG_YML}")
    return CONFIG_YML.read_text().splitlines()


@pytest.fixture(scope="module")
def pyproject_content():
    """Return the list of stripped lines in pyproject.toml."""
    if not PYPROJECT_TOML.exists():
        pytest.fail(f"Expected pyproject file is missing: {PYPROJECT_TOML}")
    return PYPROJECT_TOML.read_text().splitlines()


def test_config_yaml_initial_state(config_content):
    """
    The YAML file must contain exactly the original single experiment block
    for exp_001 and *must not* yet reference exp_002.
    """
    expected_lines = [
        "experiments:",
        "  - id: exp_001",
        "    model: resnet50",
        "    accuracy: 0.85",
        "artifacts_dir: artifacts/",
    ]

    # Ensure line-by-line equality (ignoring final newline behaviour)
    assert config_content == expected_lines, (
        f"{CONFIG_YML} contents differ from expected initial state.\n"
        f"Expected:\n{expected_lines}\n\nActual:\n{config_content}"
    )

    # Extra safety: make sure exp_002 is not mentioned anywhere.
    assert not any("exp_002" in line for line in config_content), (
        f"{CONFIG_YML} should NOT mention 'exp_002' before the update."
    )


def test_pyproject_toml_initial_state(pyproject_content):
    """
    pyproject.toml must still be at version 0.1.0 and must not yet
    include 'last_experiment'.
    """
    expected_lines = [
        "[tool.mymlpipe]",
        'version = "0.1.0"',
        'default_data_dir = "data/"',
    ]

    assert pyproject_content == expected_lines, (
        f"{PYPROJECT_TOML} contents differ from expected initial state.\n"
        f"Expected:\n{expected_lines}\n\nActual:\n{pyproject_content}"
    )

    assert not any("last_experiment" in line for line in pyproject_content), (
        f"{PYPROJECT_TOML} should NOT yet contain a 'last_experiment' key."
    )


def test_audit_log_absent():
    """
    The audit log should not exist before the student runs their commands.
    """
    assert not AUDIT_LOG.exists(), (
        f"Audit log {AUDIT_LOG} should NOT exist in the initial state."
    )