# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state before the
# student runs any backup commands.  These tests make sure the Kubernetes
# manifest source directory exists with the correct files and contents, and
# that the backup root directory is present and writable.
#
# IMPORTANT:
# • We purposefully do NOT test for the presence or absence of any output
#   artefacts (e.g. the timestamp directory, tarball, or updated log) because
#   they are supposed to be created by the student during the exercise.
# • Only stdlib and pytest are used.

import os
import hashlib
import stat
import pytest


HOME = "/home/user"
MANIFEST_DIR = os.path.join(HOME, "k8s", "manifests")
BACKUP_DIR = os.path.join(HOME, "backup")


# --------------------------------------------------------------------------- #
# Helper data                                                                 #
# --------------------------------------------------------------------------- #
EXPECTED_MANIFEST_FILES = {
    "deployment.yaml": """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 2
""",
    "service.yaml": """\
apiVersion: v1
kind: Service
metadata:
  name: nginx
spec:
  type: ClusterIP
""",
    "configmap.yaml": """\
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
data:
  key: value
""",
}


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_manifest_directory_exists():
    assert os.path.isdir(
        MANIFEST_DIR
    ), f"Directory {MANIFEST_DIR} does not exist – the manifests must live here."


def test_manifest_directory_contains_exact_three_files():
    files_in_dir = sorted(
        f for f in os.listdir(MANIFEST_DIR) if os.path.isfile(os.path.join(MANIFEST_DIR, f))
    )
    expected_files_sorted = sorted(EXPECTED_MANIFEST_FILES.keys())
    assert (
        files_in_dir == expected_files_sorted
    ), (
        f"{MANIFEST_DIR} must contain exactly the three manifest files "
        f"{expected_files_sorted}.\nCurrently found: {files_in_dir}"
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_MANIFEST_FILES.items())
def test_each_manifest_file_content_matches_expected(filename, expected_content):
    """Content must match byte-for-byte so later SHA-256 hashes are predictable."""
    file_path = os.path.join(MANIFEST_DIR, filename)
    with open(file_path, "r", encoding="utf-8") as fh:
        actual_content = fh.read()

    assert (
        actual_content == expected_content
    ), f"Content of {file_path} does not match the expected manifest template."

    # As an extra guard, verify deterministic SHA-256 digest
    expected_digest = hashlib.sha256(expected_content.encode()).hexdigest()
    actual_digest = hashlib.sha256(actual_content.encode()).hexdigest()
    assert (
        actual_digest == expected_digest
    ), f"SHA-256 digest mismatch for {file_path} – file may have been modified."


def test_backup_root_directory_exists_and_is_writable():
    assert os.path.isdir(
        BACKUP_DIR
    ), f"Backup root directory {BACKUP_DIR} is missing – create it before running backups."

    # Check writability using os.access and, as a fallback, permission bits.
    writable = os.access(BACKUP_DIR, os.W_OK)
    mode = stat.S_IMODE(os.stat(BACKUP_DIR).st_mode)
    assert writable or mode & stat.S_IWUSR, (
        f"Backup root directory {BACKUP_DIR} exists but is not writable by the current user."
    )