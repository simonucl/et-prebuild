# test_initial_state.py
#
# Pytest suite that validates the operating-system / file-system
# BEFORE the student performs any action for the “pipeline.yml
# patch” exercise.
#
# The checks assert that only the *initial* artefacts exist and
# have the expected contents.  They also ensure that files the
# student is supposed to create (diff + log) are NOT present yet.
#
# Author: automated-checker
# ---------------------------------------------------------------------

import os
from pathlib import Path

# Base paths used throughout the tests
HOME = Path("/home/user")
ETL_DIR = HOME / "etl"
CONFIG_DIR = ETL_DIR / "config"
LOGS_DIR = ETL_DIR / "logs"

PIPELINE_FILE = CONFIG_DIR / "pipeline.yml"
DIFF_FILE = LOGS_DIR / "pipeline_update.diff"
UPDATE_LOG = LOGS_DIR / "update.log"


def test_directory_structure_exists():
    """
    Make sure the basic directory scaffold provided to the
    student is present.
    """
    assert ETL_DIR.is_dir(), f"Missing directory: {ETL_DIR}"
    assert CONFIG_DIR.is_dir(), f"Missing directory: {CONFIG_DIR}"
    assert LOGS_DIR.is_dir(), f"Missing directory: {LOGS_DIR}"


def test_pipeline_file_initial_contents():
    """
    Verify that the pipeline.yml file exists and still contains
    the *old* configuration (version 1, raw-data, no validate step).
    """
    assert PIPELINE_FILE.is_file(), f"Missing configuration file: {PIPELINE_FILE}"

    text = PIPELINE_FILE.read_text(encoding="utf-8").splitlines()

    # Expected exact initial file body
    expected_lines = [
        'version: 1',
        'steps:',
        '  extract:',
        '    source: "s3://raw-data"',
        '  transform:',
        '    script: "transform.py"',
        '  load:',
        '    destination: "warehouse"',
    ]

    assert text == expected_lines, (
        f"{PIPELINE_FILE} does not contain the expected initial contents.\n"
        "If you have already modified the file, please roll back so tests "
        "can validate the original state."
    )

    # Extra sanity: ensure "version: 2" or new keys are NOT present
    forbidden_markers = ['version: 2', 'validate:', 's3://processed-data']
    offenders = [m for m in forbidden_markers if any(m in line for line in text)]
    assert not offenders, (
        f"{PIPELINE_FILE} already contains post-patch markers {offenders}. "
        "It should still hold the original configuration."
    )


def test_diff_file_does_not_exist_yet():
    """
    The un-applied diff file must not be present before the task starts.
    """
    assert not DIFF_FILE.exists(), (
        f"{DIFF_FILE} already exists but should be created by the student only."
    )


def test_update_log_does_not_exist_yet():
    """
    The update.log file must not be present before the task starts.
    """
    assert not UPDATE_LOG.exists(), (
        f"{UPDATE_LOG} already exists but should be created by the student only."
    )