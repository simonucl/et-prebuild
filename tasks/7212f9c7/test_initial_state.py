# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state before the student’s solution is run.
#
# The tests assert that:
#   • The experiments tree exists exactly as described.
#   • Each config.ini contains the expected key/value pairs.
#   • No report files or symlinks created by the yet-to-be-written solution
#     are present.

import os
import stat
import configparser
from pathlib import Path

import pytest

HOME = Path("/home/user")
EXPERIMENTS_DIR = HOME / "experiments"
REPORTS_DIR = HOME / "experiment_reports"
SUMMARY_LOG = REPORTS_DIR / "experiments_summary.log"
BEST_ACCURACY_LOG = REPORTS_DIR / "best_accuracy.log"
SYMLINK_PATH = HOME / "best_experiment"

# Expected per-experiment configuration
_EXPECTED = {
    "exp_alpha": {
        ("metadata", "experiment_name"): "exp_alpha",
        ("metadata", "timestamp"): "2023-08-23T15:34:12Z",
        ("training", "learning_rate"): "0.001",
        ("training", "batch_size"): "32",
        ("results", "accuracy"): "0.88",
    },
    "exp_beta": {
        ("metadata", "experiment_name"): "exp_beta",
        ("metadata", "timestamp"): "2023-08-24T09:18:45Z",
        ("training", "learning_rate"): "0.0005",
        ("training", "batch_size"): "64",
        ("results", "accuracy"): "0.93",
    },
    "exp_gamma": {
        ("metadata", "experiment_name"): "exp_gamma",
        ("metadata", "timestamp"): "2023-08-24T17:02:01Z",
        ("training", "learning_rate"): "0.002",
        ("training", "batch_size"): "32",
        ("results", "accuracy"): "0.89",
    },
}


def _read_config(path: Path) -> configparser.ConfigParser:
    """Utility to read an INI file with configparser (keeps string values)."""
    cp = configparser.ConfigParser()
    # Preserve case and avoid interpolation side effects
    cp.optionxform = str
    with path.open("r", encoding="utf-8") as f:
        cp.read_file(f)
    return cp


@pytest.mark.parametrize("exp_name", list(_EXPECTED.keys()))
def test_each_experiment_directory_and_config(exp_name: str):
    """
    For every expected experiment:
    • The directory exists.
    • A config.ini file exists.
    • All required keys are present and have the exact expected value.
    """

    exp_path = EXPERIMENTS_DIR / exp_name
    cfg_path = exp_path / "config.ini"

    assert exp_path.is_dir(), (
        f"Missing experiment directory: {exp_path!s}. "
        "Expected directories: exp_alpha, exp_beta, exp_gamma."
    )

    assert cfg_path.is_file(), f"Missing config.ini in {exp_path!s}."

    cp = _read_config(cfg_path)

    for (section, option), expected_val in _EXPECTED[exp_name].items():
        assert cp.has_option(section, option), (
            f"config.ini for {exp_name} is missing [{section}] {option}."
        )
        actual_val = cp.get(section, option)
        assert actual_val == expected_val, (
            f"{cfg_path!s}: expected [{section}] {option} = {expected_val!r}, "
            f"found {actual_val!r}."
        )


def test_no_unexpected_experiments_summary_or_symlinks():
    """
    Before the student runs their solution, no artefacts of the task should
    already exist: no experiment_reports/, no summary log, no best_accuracy log,
    and no best_experiment symlink.
    """

    # Report directory should not exist at all yet
    assert not REPORTS_DIR.exists(), (
        f"Directory {REPORTS_DIR!s} unexpectedly exists before the task starts."
    )

    # These must NOT exist regardless of whether REPORTS_DIR exists
    assert not SUMMARY_LOG.exists(), (
        f"File {SUMMARY_LOG!s} should not exist before the task starts."
    )
    assert not BEST_ACCURACY_LOG.exists(), (
        f"File {BEST_ACCURACY_LOG!s} should not exist before the task starts."
    )

    # Symlink must be absent
    assert not SYMLINK_PATH.exists(), (
        f"Symlink or file {SYMLINK_PATH!s} should not exist before the task starts."
    )