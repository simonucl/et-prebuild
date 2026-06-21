# test_initial_state.py
#
# This pytest suite validates the **initial** state of the filesystem
# before the student implements the disk-usage report.  It guarantees that
# the Kubernetes manifest files are present with the exact, immutable byte
# sizes expected by the downstream checker **and** that the target output
# file has **not** been created yet.
#
# Requirements verified
# ---------------------
# 1. /home/user/k8s/manifests/ exists and is a directory.
# 2. The five manifest files exist, each with the exact size (bytes).
# 3. No extra files are present inside /home/user/k8s/manifests/.
# 4. The report directory /home/user/k8s-reports/ either does not exist
#    or, if it does, the report file manifest_disk_usage.log is **absent**.
#
# NOTE: Do *not* add or remove files in /home/user/k8s/manifests/;
#       their presence and exact sizes are relied upon by the autograder.

import os
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Constants describing the canonical initial state
# ---------------------------------------------------------------------------

MANIFEST_DIR = Path("/home/user/k8s/manifests")
EXPECTED_MANIFESTS = {
    "configmap_env.yaml": 500,
    "deploy_backend.yaml": 2310,
    "deploy_frontend.yaml": 1560,
    "service_backend.yaml": 830,
    "service_frontend.yaml": 780,
}

REPORT_DIR = Path("/home/user/k8s-reports")
REPORT_FILE = REPORT_DIR / "manifest_disk_usage.log"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _full_path(filename: str) -> Path:
    """Return absolute Path object for a manifest filename."""
    return MANIFEST_DIR / filename


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_manifest_directory_exists_and_is_directory():
    assert MANIFEST_DIR.exists(), (
        f"Required directory {MANIFEST_DIR} is missing. The starter image should "
        f"contain the Kubernetes manifests under this path."
    )
    assert MANIFEST_DIR.is_dir(), f"{MANIFEST_DIR} exists but is not a directory."


def test_manifest_files_exist_with_correct_sizes():
    """
    Verify that every expected Kubernetes YAML manifest exists and has the
    immutable byte size specified by the task description.
    """
    for filename, expected_size in EXPECTED_MANIFESTS.items():
        path = _full_path(filename)
        assert path.exists(), (
            f"Missing manifest: {path}.  The autograder relies on this file "
            f"being present."
        )
        assert path.is_file(), f"{path} exists but is not a regular file."
        actual_size = path.stat().st_size
        assert actual_size == expected_size, (
            f"Size mismatch for {path}: expected {expected_size} bytes, "
            f"found {actual_size} bytes."
        )


def test_no_unexpected_files_in_manifest_directory():
    """
    Ensure there are no stray files in the manifest directory; this prevents
    students from being tripped up by unexpected entries during their size
    calculations.
    """
    expected_set = set(EXPECTED_MANIFESTS.keys())
    actual_set = {p.name for p in MANIFEST_DIR.iterdir() if p.is_file()}
    unexpected = actual_set - expected_set
    assert not unexpected, (
        f"Unexpected file(s) in {MANIFEST_DIR}: {', '.join(sorted(unexpected))}. "
        f"Only the following files should be present initially: "
        f"{', '.join(sorted(expected_set))}."
    )


def test_report_file_absent_before_student_action():
    """
    The target log file must NOT exist yet.  Its presence would indicate that
    the task has already been executed, which violates the 'initial state'
    contract for these tests.
    """
    if REPORT_FILE.exists():
        pytest.fail(
            f"The report file {REPORT_FILE} should not exist before the student "
            f"has run their solution script.  Please remove it to restore the "
            f"clean initial state."
        )