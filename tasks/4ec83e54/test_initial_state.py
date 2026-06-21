# test_initial_state.py
"""
Pytest suite that validates the **initial** (pre-task) state of the operating
system / filesystem for the “k8s manifest sync” exercise.

The suite asserts that:
1. /opt/remote_manifests exists and contains **only** the three expected YAML
   files.
2. Each file’s contents exactly match the reference strings specified in this
   test (byte-for-byte, including newlines).
3. The destination directory (/home/user/work/manifests) and the report file
   (/home/user/sync_report.log) do **not** exist yet.

Only Python’s stdlib and pytest are used.
"""

import hashlib
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants describing the expected initial state
# --------------------------------------------------------------------------- #

SRC_DIR = Path("/opt/remote_manifests")
DST_DIR = Path("/home/user/work/manifests")
REPORT_FILE = Path("/home/user/sync_report.log")

EXPECTED_FILES = (
    "configmap.yaml",
    "deployment.yaml",
    "service.yaml",
)

EXPECTED_CONTENTS = {
    "configmap.yaml": (
        "apiVersion: v1\n"
        "kind: ConfigMap\n"
        "metadata:\n"
        "  name: app-config\n"
        "data:\n"
        '  LOG_LEVEL: "info"\n'
    ),
    "deployment.yaml": (
        "apiVersion: apps/v1\n"
        "kind: Deployment\n"
        "metadata:\n"
        "  name: web\n"
        "spec:\n"
        "  replicas: 3\n"
        "  selector:\n"
        "    matchLabels:\n"
        "      app: web\n"
        "  template:\n"
        "    metadata:\n"
        "      labels:\n"
        "        app: web\n"
        "    spec:\n"
        "      containers:\n"
        "      - name: nginx\n"
        "        image: nginx:1.25\n"
        "        ports:\n"
        "        - containerPort: 80\n"
    ),
    "service.yaml": (
        "apiVersion: v1\n"
        "kind: Service\n"
        "metadata:\n"
        "  name: web\n"
        "spec:\n"
        "  type: ClusterIP\n"
        "  selector:\n"
        "    app: web\n"
        "  ports:\n"
        "  - port: 80\n"
        "    targetPort: 80\n"
    ),
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #


def md5sum_of_bytes(data: bytes) -> str:
    """Return a lowercase hex MD5 digest for the given bytes."""
    return hashlib.md5(data, usedforsecurity=False).hexdigest()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #


def test_source_directory_exists_and_is_directory():
    assert SRC_DIR.exists(), f"Required source directory {SRC_DIR} does not exist."
    assert SRC_DIR.is_dir(), f"{SRC_DIR} exists but is not a directory."


def test_source_contains_exactly_three_expected_files():
    present_files = sorted(f.name for f in SRC_DIR.iterdir() if f.is_file())
    assert (
        present_files == list(EXPECTED_FILES)
    ), (
        f"{SRC_DIR} should contain exactly these files: {EXPECTED_FILES}, "
        f"but found: {present_files}"
    )


@pytest.mark.parametrize("filename", EXPECTED_FILES)
def test_each_source_file_has_expected_content(filename):
    file_path = SRC_DIR / filename
    assert file_path.exists(), f"Expected file {file_path} missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    expected_text = EXPECTED_CONTENTS[filename]
    actual_bytes = file_path.read_bytes()
    expected_bytes = expected_text.encode()

    assert (
        actual_bytes == expected_bytes
    ), (
        f"Content mismatch in {file_path}. "
        f"MD5 expected={md5sum_of_bytes(expected_bytes)}, "
        f"got={md5sum_of_bytes(actual_bytes)}."
    )


def test_destination_directory_does_not_exist_yet():
    assert not DST_DIR.exists(), (
        f"Destination directory {DST_DIR} should NOT exist before the task starts, "
        "but it is present."
    )


def test_report_file_does_not_exist_yet():
    assert not REPORT_FILE.exists(), (
        f"Report file {REPORT_FILE} should NOT exist before the task starts, "
        "but it is present."
    )