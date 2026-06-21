# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must be
# present **before** the student writes any solution code.
#
# It intentionally DOES NOT test for the presence of the output file
# (/home/user/experiments/experiment_summary.csv); that file will be
# produced by the student later.

import configparser
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected, immutable initial state.
# ---------------------------------------------------------------------------

EXP_DIR = Path("/home/user/experiments").resolve()

# Ground-truth metadata for every experiment that must already exist.
EXPECTED_EXPERIMENTS = {
    "exp001": {
        "metadata": {
            "experiment_id": "exp001",
            "owner": "alice",
        },
        "dataset": {
            "name": "imagenet",
            "version": "1.2",
        },
        "model": {
            "architecture": "resnet50",
            "param_count": "25557032",
        },
    },
    "exp002": {
        "metadata": {
            "experiment_id": "exp002",
            "owner": "bob",
        },
        "dataset": {
            "name": "cifar10",
            "version": "3.0",
        },
        "model": {
            "architecture": "mobilenet_v2",
            "param_count": "3504875",
        },
    },
    "exp003": {
        "metadata": {
            "experiment_id": "exp003",
            "owner": "carol",
        },
        "dataset": {
            "name": "mnist",
            "version": "1.0",
        },
        "model": {
            "architecture": "lenet",
            "param_count": "60000",
        },
    },
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _read_config(path: Path) -> configparser.ConfigParser:
    """Parse an INI file and return the ConfigParser object."""
    parser = configparser.ConfigParser()
    with path.open("r", encoding="utf-8") as fp:
        parser.read_file(fp)
    return parser


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_experiments_directory_exists_and_is_dir():
    assert EXP_DIR.exists(), (
        f"Expected directory {EXP_DIR} does not exist. "
        "The experiments root directory must be present before the task starts."
    )
    assert EXP_DIR.is_dir(), f"{EXP_DIR} exists but is not a directory."


@pytest.mark.parametrize("exp_id", sorted(EXPECTED_EXPERIMENTS.keys()))
def test_experiment_subdirectory_exists(exp_id):
    exp_path = EXP_DIR / exp_id
    assert exp_path.exists(), (
        f"Missing experiment directory: {exp_path}. "
        "All listed experiments must already be available."
    )
    assert exp_path.is_dir(), f"{exp_path} exists but is not a directory."


@pytest.mark.parametrize("exp_id,exp_meta", EXPECTED_EXPERIMENTS.items())
def test_config_ini_presence_and_content(exp_id, exp_meta):
    cfg_path = EXP_DIR / exp_id / "config.ini"
    assert cfg_path.exists(), (
        f"Expected INI file {cfg_path} is missing."
    )
    assert cfg_path.is_file(), f"{cfg_path} exists but is not a regular file."

    parser = _read_config(cfg_path)

    # Validate required sections and keys
    for section, key_vals in exp_meta.items():
        assert parser.has_section(section), (
            f"{cfg_path}: missing required section [{section}]."
        )
        for key, expected_val in key_vals.items():
            assert parser.has_option(section, key), (
                f"{cfg_path}: missing key '{key}' in section [{section}]."
            )
            actual_val = parser.get(section, key, fallback=None)
            assert actual_val == expected_val, (
                f"{cfg_path}: key '{key}' in section [{section}] has value "
                f"'{actual_val}', expected '{expected_val}'."
            )