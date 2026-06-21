# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem **before**
# the student performs any actions.  It verifies that the Kubernetes manifest
# files required for the exercise are present and contain the exact expected
# contents.  It deliberately avoids checking for any artefacts that the student
# is supposed to create (e.g. /home/user/docs, README.md, lint.log).

import pathlib
import pytest

# Base paths
HOME = pathlib.Path("/home/user")
MANIFEST_DIR = HOME / "manifests"

# Expected file paths
DEPLOYMENT_YAML = MANIFEST_DIR / "deployment.yaml"
SERVICE_YAML = MANIFEST_DIR / "service.yaml"

# Expected file contents (including final newline)
EXPECTED_DEPLOYMENT_CONTENT = (
    "apiVersion: apps/v1\n"
    "kind: Deployment\n"
    "metadata:\n"
    "  name: demo-deployment\n"
    "  namespace: demo\n"
)

EXPECTED_SERVICE_CONTENT = (
    "apiVersion: v1\n"
    "kind: Service\n"
    "metadata:\n"
    "  name: demo-service\n"
    "  namespace: demo\n"
)


def _read_text(path: pathlib.Path) -> str:
    """Helper that reads a text file, raising a clear assertion if it fails."""
    assert path.exists(), f"Required file not found: {path}"
    assert path.is_file(), f"Expected a file but found something else: {path}"
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read file {path}: {exc}")  # pragma: no cover


def test_manifest_directory_exists():
    assert MANIFEST_DIR.exists(), f"Missing directory: {MANIFEST_DIR}"
    assert MANIFEST_DIR.is_dir(), f"Expected {MANIFEST_DIR} to be a directory"


@pytest.mark.parametrize(
    ("path", "expected_content"),
    [
        (DEPLOYMENT_YAML, EXPECTED_DEPLOYMENT_CONTENT),
        (SERVICE_YAML, EXPECTED_SERVICE_CONTENT),
    ],
)
def test_manifest_files_exist_with_correct_content(path: pathlib.Path, expected_content: str):
    """
    Ensure that each manifest file exists and matches the exact expected content,
    including the final newline.  A mismatch indicates that the starting
    environment is not in the correct state for the exercise.
    """
    actual_content = _read_text(path)
    assert (
        actual_content == expected_content
    ), (
        f"Content mismatch in {path}.\n"
        "---- Expected ----\n"
        f"{expected_content!r}\n"
        "---- Actual ----\n"
        f"{actual_content!r}\n"
        "Ensure the initial manifest content matches the specification."
    )