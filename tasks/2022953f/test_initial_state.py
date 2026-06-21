# test_initial_state.py
#
# Pytest suite that validates the starting environment *before* the student
# performs any actions for the benchmark task.  It checks only the immutable
# resources that must already be present.  Nothing related to the output
# artefacts created by the student is verified here.

import os
import stat
import pytest

HOME = "/home/user"

MANIFEST_DIR = os.path.join(HOME, "k8s_manifests")
APPLY_SH = os.path.join(HOME, "k8s_operator", "apply.sh")

# Full, absolute paths to the manifest files that must exist.
MANIFEST_FILES = [
    os.path.join(MANIFEST_DIR, "01-namespace.yaml"),
    os.path.join(MANIFEST_DIR, "02-configmap.yaml"),
    os.path.join(MANIFEST_DIR, "03-secret.yaml"),
    os.path.join(MANIFEST_DIR, "04-deployment.yaml"),
    os.path.join(MANIFEST_DIR, "05-service.yaml"),
    os.path.join(MANIFEST_DIR, "06-crd.yaml"),
]


def _human(path):
    """Return a human-readable description of a path for error messages."""
    return f"‘{path}’"


def test_manifest_directory_exists_and_is_dir():
    assert os.path.exists(
        MANIFEST_DIR
    ), f"Required directory {_human(MANIFEST_DIR)} is missing."
    assert os.path.isdir(
        MANIFEST_DIR
    ), f"{_human(MANIFEST_DIR)} exists but is not a directory."


@pytest.mark.parametrize("file_path", MANIFEST_FILES)
def test_each_manifest_file_exists(file_path):
    assert os.path.exists(
        file_path
    ), f"Required manifest file {_human(file_path)} is missing."
    assert os.path.isfile(
        file_path
    ), f"{_human(file_path)} exists but is not a regular file."
    # An empty manifest would be suspicious; catch obvious corruption.
    assert (
        os.path.getsize(file_path) > 0
    ), f"{_human(file_path)} is unexpectedly empty."


def test_apply_sh_exists_and_is_executable():
    assert os.path.exists(
        APPLY_SH
    ), f"Helper script {_human(APPLY_SH)} is missing."
    assert os.path.isfile(
        APPLY_SH
    ), f"{_human(APPLY_SH)} exists but is not a regular file."

    # Check the executable bit for the current user.
    is_executable = os.access(APPLY_SH, os.X_OK)
    if not is_executable:
        permissions = oct(os.stat(APPLY_SH).st_mode & 0o777)
        pytest.fail(
            f"{_human(APPLY_SH)} is not executable (mode {permissions}). "
            "It must have the executable bit set."
        )

    # Optional sanity check: ensure the first line is a shebang for bash.
    with open(APPLY_SH, "r", encoding="utf-8", errors="ignore") as fh:
        first_line = fh.readline()
    assert first_line.startswith(
        "#!"
    ), f"{_human(APPLY_SH)} must start with a shebang (#!)."