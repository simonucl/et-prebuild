# test_initial_state.py
#
# This test-suite validates that the *starting* file-system state for the
# “production hand-off” task is correct.  It **must** be run BEFORE the
# student’s solution is executed.  If any of these tests fail it means the
# playground image itself is broken or has been modified unexpectedly.
#
# What we check:
#   1. The expected experiment directory exists.
#   2. Exactly four raw artifact files are present and readable.
#   3. Their basic contents / formats look sane.
#   4. No derived output artefacts (archive or checksum log) are present yet.
#
# NOTE:  We purposefully do *not* test anything that should be produced by the
#        student (e.g. the .tar.gz archive or the checksum manifest).  Those
#        belong to a *post-execution* test-suite.
#
# Only stdlib + pytest are used.

import json
import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants                                                                   #
# --------------------------------------------------------------------------- #

HOME = Path("/home/user")
EXP_BASE = HOME / "experiments"
RUN_DIR = EXP_BASE / "run_2024_03_18"
ARCHIVES_DIR = EXP_BASE / "archives"
ARCHIVE_FILE = ARCHIVES_DIR / "run_2024_03_18_artifacts.tar.gz"
MANIFEST_FILE = RUN_DIR / "artifact_checksums.log"

RAW_FILES = {
    "accuracy.txt": {
        "path": RUN_DIR / "accuracy.txt",
        "validator": "validate_accuracy",
    },
    "loss.txt": {
        "path": RUN_DIR / "loss.txt",
        "validator": "validate_loss",
    },
    "params.json": {
        "path": RUN_DIR / "params.json",
        "validator": "validate_params_json",
    },
    "model.bin": {
        "path": RUN_DIR / "model.bin",
        "validator": "validate_model_bin",
    },
}


# --------------------------------------------------------------------------- #
# Helper validation functions                                                 #
# --------------------------------------------------------------------------- #

def validate_accuracy(path: Path):
    """
    Expected content: single line in the form 'accuracy:<float>\\n'
    """
    data = path.read_text(encoding="utf-8")
    lines = data.splitlines()
    assert len(lines) == 1, f"{path} should contain exactly one line, found {len(lines)} lines."
    line = lines[0]
    assert line.startswith("accuracy:"), f"{path} first line must start with 'accuracy:', got '{line}'."
    try:
        float(line.split("accuracy:")[1])
    except ValueError:
        pytest.fail(f"Could not parse float value from {path}: '{line}'.")


def validate_loss(path: Path):
    """
    Expected content: single line in the form 'loss:<float>\\n'
    """
    data = path.read_text(encoding="utf-8")
    lines = data.splitlines()
    assert len(lines) == 1, f"{path} should contain exactly one line, found {len(lines)} lines."
    line = lines[0]
    assert line.startswith("loss:"), f"{path} first line must start with 'loss:', got '{line}'."
    try:
        float(line.split("loss:")[1])
    except ValueError:
        pytest.fail(f"Could not parse float value from {path}: '{line}'.")


def validate_params_json(path: Path):
    """
    Expected content: valid JSON with at least the keys
    'learning_rate', 'batch_size', 'epochs'.
    """
    text = path.read_text(encoding="utf-8")
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{path} is not valid JSON: {exc}")

    required = {"learning_rate", "batch_size", "epochs"}
    missing = required.difference(obj.keys())
    assert not missing, f"{path} is missing expected keys: {missing}"


def validate_model_bin(path: Path):
    """
    Binary snapshot must be non-empty (≈ 1 KB).  We only verify it is > 100 bytes.
    """
    size = path.stat().st_size
    assert size > 100, f"{path} is unexpectedly small ({size} bytes)."


# Mapping name -> function object
_VALIDATORS = {
    "validate_accuracy": validate_accuracy,
    "validate_loss": validate_loss,
    "validate_params_json": validate_params_json,
    "validate_model_bin": validate_model_bin,
}


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_experiment_directory_exists():
    assert RUN_DIR.is_dir(), f"Required directory {RUN_DIR} is missing."


def test_raw_artifact_files_present_and_valid():
    # Check presence & run individual validators
    for fname, meta in RAW_FILES.items():
        path = meta["path"]
        assert path.is_file(), f"Expected file {path} is missing."
        assert os.access(path, os.R_OK), f"File {path} is not readable."

        validator_name = meta["validator"]
        _VALIDATORS[validator_name](path)

    # Sanity: ensure *exactly* these four files exist and no unexpected extras
    observed_files = {p.name for p in RUN_DIR.iterdir() if p.is_file()}
    expected_files = set(RAW_FILES.keys())
    unexpected = observed_files - expected_files
    assert not unexpected, (
        f"Unexpected extra file(s) present in {RUN_DIR}: {sorted(unexpected)}"
    )


def test_no_derived_outputs_present_yet():
    if ARCHIVE_FILE.exists():
        pytest.fail(
            f"Derived archive {ARCHIVE_FILE} already exists BEFORE the student "
            f"has run their solution. The playground image is corrupted."
        )

    if MANIFEST_FILE.exists():
        pytest.fail(
            f"Checksum manifest {MANIFEST_FILE} already exists BEFORE the student "
            f"has run their solution. The playground image is corrupted."
        )