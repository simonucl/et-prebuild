# test_initial_state.py
#
# This test-suite validates the *initial* state of the workstation
# BEFORE the student performs the actions described in the assignment.
#
# It checks that:
#   1. /home/user/sample_artifact.txt exists and looks correct
#   2. The experiment-tracking directories and files do NOT exist yet
#
# Only stdlib and pytest are used.

import os
import pytest

SRC_ARTIFACT = "/home/user/sample_artifact.txt"
EXP_ROOT = "/home/user/experiments"
EXP01_DIR = os.path.join(EXP_ROOT, "exp01")
ARTIFACTS_DIR = os.path.join(EXP01_DIR, "artifacts")
DEST_ARTIFACT = os.path.join(ARTIFACTS_DIR, "sample_artifact.txt")
CSV_PATH = os.path.join(EXP01_DIR, "exp01_artifacts.csv")


def _read_file_bytes(path: str) -> bytes:
    """Utility: read the whole file as bytes."""
    with open(path, "rb") as fh:
        return fh.read()


@pytest.mark.describe("Initial sample artifact must exist in its original location")
def test_source_artifact_exists_and_has_expected_content():
    assert os.path.isfile(
        SRC_ARTIFACT
    ), (
        f"Required source file {SRC_ARTIFACT} is missing.\n"
        "It must be present *before* the student starts the exercise."
    )

    data = _read_file_bytes(SRC_ARTIFACT)

    # Basic sanity checks on the file content so we know we have the right file
    assert data, f"{SRC_ARTIFACT} is empty; it should contain sample text."
    expected_phrase = b"sample artifact file"
    assert (
        expected_phrase in data
    ), (
        f"{SRC_ARTIFACT} does not contain the expected text fragment "
        f"{expected_phrase!r}. It looks like the wrong file."
    )


@pytest.mark.describe("Destination experiment directory tree must NOT pre-exist")
def test_experiment_directories_do_not_yet_exist():
    assert not os.path.exists(
        EXP01_DIR
    ), (
        f"The directory {EXP01_DIR} already exists, but it should NOT be present "
        "before the student runs their solution."
    )

    assert not os.path.exists(
        ARTIFACTS_DIR
    ), (
        f"The directory {ARTIFACTS_DIR} already exists. "
        "The student is expected to create it."
    )


@pytest.mark.describe("Destination artifact and CSV inventory must NOT pre-exist")
def test_destination_files_do_not_yet_exist():
    assert not os.path.exists(
        DEST_ARTIFACT
    ), (
        f"{DEST_ARTIFACT} already exists, but it should only appear AFTER the "
        "student moves the source artifact."
    )

    assert not os.path.exists(
        CSV_PATH
    ), (
        f"{CSV_PATH} already exists, but it should only be created by the student "
        "as part of the exercise."
    )