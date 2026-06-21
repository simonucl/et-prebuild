# test_initial_state.py
#
# This pytest suite validates the REQUIRED **initial** filesystem state
# before the student performs any actions for the exercise “archive the
# experiment run_01”.
#
# The checks assert that:
#   • /home/user/experiments/run_01/ exists and contains **exactly** the three
#     expected files (no more, no less).
#   • Each file has the correct type and basic contents/size.
#   • No archive, restore-area, or log file has been pre-created yet.
#
# Only the Python standard library and pytest are used.

import os
import json
import hashlib
from pathlib import Path
import pytest


HOME = Path("/home/user")
EXP_DIR = HOME / "experiments" / "run_01"
ARCHIVE_DIR = HOME / "archive"
ARCHIVE_PATH = ARCHIVE_DIR / "run_01.tar.gz"
LOG_PATH = ARCHIVE_DIR / "compression_log.txt"
RESTORE_DIR = HOME / "restore" / "run_01"

EXPECTED_FILES = {
    "model.bin",
    "metrics.json",
    "config.yaml",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def sha256_of_file(path: Path) -> str:
    """Return the hex SHA-256 digest of a file (lower-case)."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- #
# Tests for the initial state
# --------------------------------------------------------------------------- #
def test_experiment_directory_exists():
    assert EXP_DIR.exists(), (
        f"Expected experiment directory {EXP_DIR} does not exist. "
        "The exercise requires it to be present before any action is taken."
    )
    assert EXP_DIR.is_dir(), f"{EXP_DIR} exists but is not a directory."


def test_experiment_directory_contains_exactly_three_expected_files():
    items = {p.name for p in EXP_DIR.iterdir() if p.is_file()}
    extras = items - EXPECTED_FILES
    missing = EXPECTED_FILES - items

    assert not missing, (
        f"The following required files are missing from {EXP_DIR}: {', '.join(sorted(missing))}"
    )
    assert not extras, (
        f"The directory {EXP_DIR} contains unexpected extra files: {', '.join(sorted(extras))}"
    )


def test_model_bin_contents_and_size():
    model_path = EXP_DIR / "model.bin"
    assert model_path.is_file(), f"Expected file {model_path} is missing."

    expected_size = 95  # 19 bytes * 5 repetitions
    size = model_path.stat().st_size
    assert size == expected_size, (
        f"{model_path} has size {size} bytes but expected {expected_size} bytes."
    )

    # Ensure the repeating string pattern is present.
    expected_fragment = b"MODEL_WEIGHTS_v1.0\n"
    with model_path.open("rb") as f:
        data = f.read()
        assert data.count(expected_fragment) == 5, (
            f"{model_path} does not contain the expected 5 repetitions of "
            "the string 'MODEL_WEIGHTS_v1.0\\n'."
        )


def test_metrics_json_is_valid_and_has_expected_keys():
    metrics_path = EXP_DIR / "metrics.json"
    assert metrics_path.is_file(), f"Expected file {metrics_path} is missing."

    with metrics_path.open("r", encoding="utf-8") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError as exc:
            pytest.fail(f"{metrics_path} is not valid JSON: {exc}")

    required_keys = {"accuracy", "loss"}
    assert required_keys.issubset(metrics), (
        f"{metrics_path} is missing required keys: {required_keys - metrics.keys()}"
    )


def test_config_yaml_contains_expected_lines():
    cfg_path = EXP_DIR / "config.yaml"
    assert cfg_path.is_file(), f"Expected file {cfg_path} is missing."

    with cfg_path.open("r", encoding="utf-8") as f:
        text = f.read()

    expected_lines = {
        "learning_rate: 0.001",
        "epochs: 10",
    }
    missing = {ln for ln in expected_lines if ln not in text}
    assert not missing, (
        f"{cfg_path} is missing expected configuration lines: {', '.join(sorted(missing))}"
    )


def test_no_archive_or_restore_artifacts_preexist():
    # /home/user/archive/ may or may not exist yet, but the *archive file* and
    # *log file* definitely should not exist before the student runs commands.
    assert not ARCHIVE_PATH.exists(), (
        f"{ARCHIVE_PATH} already exists but should not be present before the task is executed."
    )
    assert not LOG_PATH.exists(), (
        f"{LOG_PATH} already exists but should not be present before the task is executed."
    )

    # The restore directory should likewise be absent.
    assert not RESTORE_DIR.exists(), (
        f"{RESTORE_DIR} already exists but should not be present before extraction."
    )