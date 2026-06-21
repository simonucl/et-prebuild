# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state _before_ the
# student executes any command for the “Kubernetes manifests backup” task.
#
# The tests assert the presence (and absence) of specific directories,
# files, and file contents exactly as laid out in the task description.
#
# Only the Python standard library and pytest are used.

import os
import stat
import textwrap
import pytest

HOME = "/home/user"
MANIFESTS_DIR = os.path.join(HOME, "manifests")
BACKUPS_DIR = os.path.join(HOME, "backups")
ARCHIVE_PATH = os.path.join(BACKUPS_DIR, "manifests_2025-01-01.tbz2")

_expected_manifest_contents = {
    "deployment.yaml": textwrap.dedent(
        """\
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: webapp
        spec:
          replicas: 2
          selector:
            matchLabels:
              app: webapp
          template:
            metadata:
              labels:
                app: webapp
            spec:
              containers:
              - name: nginx
                image: nginx:1.25
                ports:
                - containerPort: 80
        """
    ).rstrip("\n"),
    "service.yaml": textwrap.dedent(
        """\
        apiVersion: v1
        kind: Service
        metadata:
          name: webapp-svc
        spec:
          selector:
            app: webapp
          ports:
          - protocol: TCP
            port: 80
            targetPort: 80
          type: ClusterIP
        """
    ).rstrip("\n"),
    "ingress.yaml": textwrap.dedent(
        """\
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          name: webapp-ingress
        spec:
          rules:
          - host: webapp.local
            http:
              paths:
              - path: /
                pathType: Prefix
                backend:
                  service:
                    name: webapp-svc
                    port:
                      number: 80
        """
    ).rstrip("\n"),
}

@pytest.fixture(scope="session")
def manifest_files_present():
    """Return list of .yaml files actually present in the manifests directory."""
    assert os.path.isdir(MANIFESTS_DIR), (
        f"Required directory {MANIFESTS_DIR!r} is missing."
    )
    files = [f for f in os.listdir(MANIFESTS_DIR) if f.endswith(".yaml")]
    return files

def test_manifests_directory_exists_and_writable():
    assert os.path.isdir(MANIFESTS_DIR), (
        f"Directory {MANIFESTS_DIR!r} must exist."
    )
    assert os.access(MANIFESTS_DIR, os.W_OK), (
        f"Directory {MANIFESTS_DIR!r} must be writable."
    )

def test_backups_directory_exists_and_writable_and_empty():
    assert os.path.isdir(BACKUPS_DIR), (
        f"Directory {BACKUPS_DIR!r} must exist."
    )
    assert os.access(BACKUPS_DIR, os.W_OK), (
        f"Directory {BACKUPS_DIR!r} must be writable."
    )
    # Directory must be empty before the student runs the task
    leftover = [f for f in os.listdir(BACKUPS_DIR) if not f.startswith(".")]
    assert leftover == [], (
        f"Directory {BACKUPS_DIR!r} should be empty at the beginning, "
        f"found: {leftover}"
    )

def test_archive_does_not_yet_exist():
    assert not os.path.exists(ARCHIVE_PATH), (
        f"The archive {ARCHIVE_PATH!r} must NOT exist yet—"
        "it will be created by the student's command."
    )

def test_expected_yaml_files_exist(manifest_files_present):
    expected_files = sorted(_expected_manifest_contents)
    assert sorted(manifest_files_present) == expected_files, (
        "The manifests directory must contain ONLY these .yaml files: "
        f"{expected_files}. Found: {sorted(manifest_files_present)}"
    )
    for fname in expected_files:
        fpath = os.path.join(MANIFESTS_DIR, fname)
        assert os.path.isfile(fpath), f"Expected file {fpath!r} is missing."
        assert os.access(fpath, os.R_OK), f"File {fpath!r} is not readable."

def _normalize_newlines(text: str) -> str:
    """Return text with all CRLF converted to LF and without trailing newline."""
    return text.replace("\r\n", "\n").rstrip("\n")

def test_yaml_file_contents_match_expected():
    for fname, expected_content in _expected_manifest_contents.items():
        fpath = os.path.join(MANIFESTS_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as fh:
            actual = fh.read()
        assert _normalize_newlines(actual) == expected_content, (
            f"Contents of {fpath!r} do not match the expected specification."
        )