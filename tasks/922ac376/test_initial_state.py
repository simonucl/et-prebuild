# test_initial_state.py
#
# This pytest suite validates the *initial* state of the machine
# before the learner performs the required synchronisation task.
#
# It checks that:
#   1. /home/user/remote_repo/ exists and is a directory.
#   2. That directory contains *exactly* two regular files with the
#      expected names.
#   3. The contents of those files match the reference manifests
#      (byte-for-byte, aside from an optional trailing newline).
#   4. The target directory (/home/user/k8s-manifests/) does NOT yet
#      exist.
#   5. The sync log (/home/user/sync.log) does NOT yet exist.
#
# If any of these assertions fail, the failure message pin-points the
# missing or unexpected element.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
REMOTE_REPO = HOME / "remote_repo"
TARGET_DIR = HOME / "k8s-manifests"
SYNC_LOG = HOME / "sync.log"

EXPECTED_FILENAMES = {"nginx-deployment.yaml", "nginx-service.yaml"}

EXPECTED_CONTENT = {
    "nginx-deployment.yaml": """apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
""",
    "nginx-service.yaml": """apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
""",
}


def _normalise_newlines(text: str) -> str:
    """
    Return text with trailing whitespace removed and ensure it ends
    with a single '\n'.  This makes comparison resilient to the
    presence/absence of a final newline character.
    """
    return text.rstrip() + "\n"


def test_remote_repo_directory_exists_and_is_directory():
    assert REMOTE_REPO.exists(), (
        f"Expected directory '{REMOTE_REPO}' does not exist. "
        "The starting repository is missing."
    )
    assert REMOTE_REPO.is_dir(), (
        f"Path '{REMOTE_REPO}' exists but is not a directory. "
        "It must be a directory containing the manifests."
    )


def test_remote_repo_contains_exact_expected_files():
    files_in_repo = {p.name for p in REMOTE_REPO.iterdir() if p.is_file()}
    assert files_in_repo == EXPECTED_FILENAMES, (
        "The remote repository should contain *exactly* the following "
        f"regular files: {sorted(EXPECTED_FILENAMES)}. "
        f"Found: {sorted(files_in_repo)}"
    )


@pytest.mark.parametrize("filename", sorted(EXPECTED_FILENAMES))
def test_remote_repo_file_contents_match_reference(filename):
    file_path = REMOTE_REPO / filename
    assert file_path.is_file(), f"Expected file '{file_path}' is missing."

    with file_path.open("r", encoding="utf-8") as fh:
        actual = _normalise_newlines(fh.read())

    expected = _normalise_newlines(EXPECTED_CONTENT[filename])

    assert (
        actual == expected
    ), f"Contents of '{file_path}' do not match the expected reference manifest."


def test_target_directory_does_not_yet_exist():
    assert not TARGET_DIR.exists(), (
        f"Directory '{TARGET_DIR}' already exists. "
        "It should be created by the learner, not present at the start."
    )


def test_sync_log_does_not_yet_exist():
    assert not SYNC_LOG.exists(), (
        f"File '{SYNC_LOG}' already exists. "
        "It should be created by the learner during synchronisation."
    )