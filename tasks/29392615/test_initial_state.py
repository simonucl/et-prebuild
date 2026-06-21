# test_initial_state.py
#
# This test suite verifies the _initial_ filesystem state that must be
# present **before** the student performs the task.  It deliberately
# avoids checking for any of the output paths/files that the student is
# supposed to create.

import os
import pytest

REGISTRY_PATH = "/home/user/project/experiments/registry.yaml"
ARTIFACTS_DIR = "/home/user/project/artifacts"

# The registry.yaml file must already contain exactly these 7 text lines
# terminated by a single trailing newline character (i.e. byte-for-byte
# equality with the following string).
EXPECTED_REGISTRY_CONTENT = (
    "experiments:\n"
    "  - id: exp_001\n"
    "    artifact_path: /home/user/project/artifacts/exp_001\n"
    "    commit: a1b2c3d\n"
    "  - id: exp_002\n"
    "    artifact_path: /home/user/project/artifacts/exp_002\n"
    "    commit: d4e5f6g\n"
)


def test_registry_file_exists_and_has_exact_content():
    """
    The registry YAML must exist and contain exactly the expected
    7 lines (including the precise indentation and a final newline).
    """
    assert os.path.isfile(
        REGISTRY_PATH
    ), f"Required registry file not found at: {REGISTRY_PATH}"

    with open(REGISTRY_PATH, "r", encoding="utf-8") as fh:
        actual = fh.read()

    assert (
        actual == EXPECTED_REGISTRY_CONTENT
    ), (
        "registry.yaml content mismatch.\n\n"
        "Expected:\n"
        f"{EXPECTED_REGISTRY_CONTENT!r}\n\n"
        "Found:\n"
        f"{actual!r}"
    )


def test_artifacts_directory_exists():
    """
    The base artifacts directory must already be present so that new
    experiment sub-directories can be added underneath it.
    """
    assert os.path.isdir(
        ARTIFACTS_DIR
    ), f"Directory {ARTIFACTS_DIR} is missing or is not a directory."