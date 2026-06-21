# test_initial_state.py
#
# This test-suite validates that the initial workspace already contains the
# expected experiment data *before* the student starts working.
#
# IMPORTANT:  We intentionally DO NOT test for the presence (or absence) of
# any files/directories that the student is supposed to create (e.g.
# /home/user/mlops/reports or experiment_summary.log).  We only check the
# pre-existing input data under /home/user/mlops/experiments.

import os
import pytest

BASE_DIR = "/home/user/mlops/experiments"

# --------------------------------------------------------------------------- #
# Expected directory / file structure and *exact* file contents (including
# trailing newlines).  The grader will compare byte-for-byte, so the strings
# below must match exactly what should be on disk.
# --------------------------------------------------------------------------- #
EXPECTED_CONTENT = {
    # EXP001
    os.path.join(BASE_DIR, "EXP001", "metrics.txt"):
        "Accuracy: 0.9321\n"
        "Loss: 0.1278\n",
    os.path.join(BASE_DIR, "EXP001", "params.yaml"):
        "model: ResNet50\n"
        "lr: 0.001\n"
        "batch_size: 32\n",
    os.path.join(BASE_DIR, "EXP001", "artifact_list.txt"):
        "2023-08-21\n"
        "checkpoint.pt\n"
        "tensorboard/\n",

    # EXP002
    os.path.join(BASE_DIR, "EXP002", "metrics.txt"):
        "Accuracy: 0.8876\n"
        "Loss: 0.2345\n",
    os.path.join(BASE_DIR, "EXP002", "params.yaml"):
        "model: EfficientNetB0\n"
        "lr: 0.0005\n"
        "batch_size: 64\n"
        "augment: true\n",
    os.path.join(BASE_DIR, "EXP002", "artifact_list.txt"):
        "2023-08-22\n"
        "checkpoint.pt\n"
        "tensorboard/\n",

    # EXP003
    os.path.join(BASE_DIR, "EXP003", "metrics.txt"):
        "Accuracy: 0.9458\n"
        "Loss: 0.0987\n",
    os.path.join(BASE_DIR, "EXP003", "params.yaml"):
        "model: ViT-B16\n"
        "lr: 0.0001\n"
        "batch_size: 16\n"
        "patch_size: 16\n"
        "epochs: 30\n",
    os.path.join(BASE_DIR, "EXP003", "artifact_list.txt"):
        "2023-08-25\n"
        "checkpoint.pt\n"
        "tensorboard/\n",
}

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_base_directory_exists():
    """The top-level experiments directory must exist."""
    assert os.path.isdir(BASE_DIR), (
        f"Expected base directory {BASE_DIR} to exist, but it does not."
    )


@pytest.mark.parametrize("file_path,expected_content", EXPECTED_CONTENT.items())
def test_file_presence_and_content(file_path, expected_content):
    """
    Verify that each required file is present and contains the exact bytes
    specified in EXPECTED_CONTENT.
    """
    assert os.path.isfile(file_path), (
        f"Required file missing: {file_path}"
    )

    # Read the file in text mode to validate exact string content, including
    # trailing newline.  Using newline='' prevents universal-newline conversion
    # so '\r\n' vs '\n' differences are caught.
    with open(file_path, "r", newline="") as f:
        actual_content = f.read()

    assert actual_content == expected_content, (
        f"File content mismatch in {file_path}.\n"
        f"--- Expected (len {len(expected_content)}):\n{expected_content!r}\n"
        f"---   Actual (len {len(actual_content)}):\n{actual_content!r}"
    )