# test_initial_state.py
#
# Pytest test-suite that validates the *initial* filesystem/OS state
# BEFORE the learner carries out any actions.  All checks are performed
# against absolute paths under /home/user.
#
# Requirements verified:
#   1. /home/user/k8s/manifests/ exists as a directory.
#   2. That directory contains *exactly* three YAML files:
#        deployment.yaml, service.yaml, configmap.yaml
#   3. Each YAML file contains the expected contents (ignoring a final
#      trailing newline, if present).
#   4. Neither /home/user/manifests_backup.tar.gz nor
#      /home/user/backup.log exists yet.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path

import pytest


K8S_MANIFESTS_DIR = Path("/home/user/k8s/manifests")
EXPECTED_FILES = {
    "deployment.yaml",
    "service.yaml",
    "configmap.yaml",
}

# Expected file contents (as canonical strings without a trailing newline).
EXPECTED_CONTENTS = {
    "deployment.yaml": (
        "apiVersion: apps/v1\n"
        "kind: Deployment\n"
        "metadata:\n"
        "  name: demo-deployment\n"
        "spec:\n"
        "  replicas: 2\n"
        "  selector:\n"
        "    matchLabels:\n"
        "      app: demo\n"
        "  template:\n"
        "    metadata:\n"
        "      labels:\n"
        "        app: demo\n"
        "    spec:\n"
        "      containers:\n"
        "      - name: demo\n"
        "        image: nginx:1.21"
    ),
    "service.yaml": (
        "apiVersion: v1\n"
        "kind: Service\n"
        "metadata:\n"
        "  name: demo-service\n"
        "spec:\n"
        "  selector:\n"
        "    app: demo\n"
        "  ports:\n"
        "  - protocol: TCP\n"
        "    port: 80\n"
        "    targetPort: 80\n"
        "  type: ClusterIP"
    ),
    "configmap.yaml": (
        "apiVersion: v1\n"
        "kind: ConfigMap\n"
        "metadata:\n"
        "  name: demo-config\n"
        "data:\n"
        "  example.property.1: hello\n"
        "  example.property.2: world"
    ),
}


def _read_file_trimmed(path: Path) -> str:
    """
    Read the file and strip a *single* trailing newline if present.
    This makes the comparison tolerant to POSIX-style files that end
    with '\n' as well as exact-length files without one.
    """
    data = path.read_text(encoding="utf-8")
    if data.endswith("\n"):
        return data[:-1]
    return data


@pytest.fixture(scope="module")
def manifests_dir():
    return K8S_MANIFESTS_DIR


def test_manifests_directory_exists(manifests_dir):
    assert manifests_dir.is_dir(), (
        f"Required directory '{manifests_dir}' does not exist or is "
        "not a directory."
    )


def test_exact_yaml_files_present(manifests_dir):
    present_files = {p.name for p in manifests_dir.iterdir() if p.is_file()}
    missing = EXPECTED_FILES - present_files
    unexpected = present_files - EXPECTED_FILES

    assert not missing, (
        "The following expected YAML file(s) are missing from "
        f"'{manifests_dir}': {', '.join(sorted(missing))}"
    )
    assert not unexpected, (
        "The manifests directory contains unexpected file(s): "
        f"{', '.join(sorted(unexpected))}. It should contain exactly "
        f"{', '.join(sorted(EXPECTED_FILES))}"
    )


@pytest.mark.parametrize("filename", sorted(EXPECTED_FILES))
def test_yaml_file_contents(manifests_dir, filename):
    path = manifests_dir / filename
    assert path.is_file(), f"Expected file '{path}' is missing."

    actual = _read_file_trimmed(path)
    expected = EXPECTED_CONTENTS[filename]
    assert actual == expected, (
        f"Contents of '{path}' do not match the expected specification."
    )


def test_backup_artifacts_do_not_exist_yet():
    backup_tar = Path("/home/user/manifests_backup.tar.gz")
    backup_log = Path("/home/user/backup.log")

    assert not backup_tar.exists(), (
        f"Archive '{backup_tar}' should NOT exist before the task is "
        "performed."
    )
    assert not backup_log.exists(), (
        f"Log file '{backup_log}' should NOT exist before the task is "
        "performed."
    )