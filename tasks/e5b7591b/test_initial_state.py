# test_initial_state.py
#
# This pytest suite verifies that the workspace is still in its **initial**
# (pre–solution) state.  None of the artefacts that the student is asked to
# create for “operator-test” should exist yet.  If any of the expected files
# or directories are already present, these tests will fail with a clear and
# specific message.

import os
import pytest
from pathlib import Path

HOME = Path("/home/user").expanduser()
BASE_DIR = HOME / "operator-test"

# Paths that must *not* exist before the student starts
PATHS_THAT_MUST_NOT_EXIST = {
    "root directory": BASE_DIR,
    "manifests/": BASE_DIR / "manifests",
    "my-configmap.yaml": BASE_DIR / "manifests" / "my-configmap.yaml",
    "my-deployment.yaml": BASE_DIR / "manifests" / "my-deployment.yaml",
    "mock-api.json": BASE_DIR / "mock-api.json",
    "mock-api-response.json": BASE_DIR / "mock-api-response.json",
    "api-test.log": BASE_DIR / "api-test.log",
}


@pytest.mark.parametrize("human_readable,path_obj", PATHS_THAT_MUST_NOT_EXIST.items())
def test_no_expected_solution_artifacts_exist(human_readable: str, path_obj: Path):
    """
    Ensure that none of the files or directories that belong to the finished
    solution exist yet.  If any of them are found, the environment is already
    “polluted” and the assignment cannot be graded reliably.
    """
    assert not path_obj.exists(), (
        f"The pre-flight check discovered '{path_obj}' already present.  "
        f"The {human_readable!r} should NOT exist before the student starts "
        f"working on the exercise."
    )