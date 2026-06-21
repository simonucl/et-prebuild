# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state that
# must be present _before_ the student runs any commands.
#
# It checks that:
#   • The directory /home/user/experiments/run_03/ exists.
#   • Exactly four expected artifact files exist inside it.
#   • Each file’s byte-for-byte content and size match the truth table.
#   • The report file /home/user/experiments/run_03/artifact_report.csv
#     does NOT exist yet.
#
# Any discrepancy will raise a clear, actionable assertion failure.

import os
from pathlib import Path

import pytest

ROOT_DIR = Path("/home/user/experiments/run_03")

# Mapping: filename -> expected exact content (including the trailing '\n')
EXPECTED_FILES = {
    "model.pt": "DUMMY_MODEL_CONTENT\n",
    "metrics.json": '{"accuracy": 0.92, "loss": 0.15}\n',
    "config.yaml": "batch_size: 32\nlearning_rate: 0.001\n",
    "training.log": (
        "Epoch,Loss,Accuracy\n"
        "1,0.45,0.78\n"
        "2,0.32,0.84\n"
        "3,0.21,0.88\n"
    ),
}

REPORT_FILE = ROOT_DIR / "artifact_report.csv"


def test_experiment_directory_exists():
    assert ROOT_DIR.is_dir(), (
        f"Required directory {ROOT_DIR} is missing. "
        "The experiment artifacts must reside here."
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_FILES.items())
def test_artifact_file_content_and_size(filename, expected_content):
    file_path = ROOT_DIR / filename
    assert file_path.is_file(), f"Expected file {file_path} is missing."

    # Read bytes to be 100 % sure about length and content.
    data = file_path.read_bytes()
    expected_bytes = expected_content.encode()

    assert data == expected_bytes, (
        f"Contents of {file_path} do not match the expected truth value.\n"
        f"Expected bytes: {expected_bytes!r}\n"
        f"Found bytes:    {data!r}"
    )

    assert len(data) == len(expected_bytes), (
        f"Size mismatch for {file_path}. "
        f"Expected {len(expected_bytes)} bytes, found {len(data)} bytes."
    )


def test_no_extra_or_missing_files():
    """
    Ensure *only* the expected files are present (no surprise files that could
    interfere with the exercise).
    """
    present_files = {p.name for p in ROOT_DIR.iterdir() if p.is_file()}
    expected_files = set(EXPECTED_FILES)
    missing = expected_files - present_files
    extra = present_files - expected_files - {"artifact_report.csv"}  # report not yet created
    assert not missing, f"Missing expected files: {', '.join(sorted(missing))}"
    assert not extra, f"Unexpected extra files present: {', '.join(sorted(extra))}"


def test_report_file_is_absent_initially():
    assert not REPORT_FILE.exists(), (
        f"The summary report {REPORT_FILE} should NOT exist before the "
        "student runs their one-liner command."
    )